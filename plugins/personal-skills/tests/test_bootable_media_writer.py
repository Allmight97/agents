import importlib.machinery
import importlib.util
import tempfile
import unittest
import os
import fcntl
import bz2
import hashlib
import io
import json
import lzma
import stat
import threading
import zipfile
from unittest import mock
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "skills" / "write-bootable-media" / "scripts" / "bootable-media-writer"
loader = importlib.machinery.SourceFileLoader("media_writer", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
media_writer = importlib.util.module_from_spec(spec)
loader.exec_module(media_writer)


class MediaWriterTests(unittest.TestCase):
    def test_sha256_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.iso"
            path.write_bytes(b"bootable-media")
            self.assertEqual(
                media_writer.sha256_file(path),
                "bf7d0556874cca004017a8c56c31abf2e8c051e1b30a611d1b01cca1c5a82032",
            )

    def test_plan_id_binds_complete_source_and_target(self):
        plan = {
            "schema_version": 1,
            "source": {"path": "/tmp/a.iso", "sha256": "a" * 64, "bytes": 1},
            "target": {"disk": "/dev/disk4", "serial": "abc", "bytes": 2},
        }
        original = media_writer.canonical_plan_id(plan)
        plan["target"]["disk"] = "/dev/disk5"
        self.assertNotEqual(original, media_writer.canonical_plan_id(plan))

    def test_plan_tampering_is_rejected(self):
        plan = {
            "schema_version": 1,
            "source": {"path": "/tmp/a.iso", "sha256": "a" * 64, "bytes": 1},
            "target": {"disk": "/dev/disk4", "serial": "abc", "bytes": 2},
        }
        plan["plan_id"] = media_writer.canonical_plan_id(plan)
        plan["target"]["disk"] = "/dev/disk5"
        with self.assertRaises(media_writer.MediaError):
            media_writer.validate_plan(plan)

    def test_authopen_returns_bounded_descriptor(self):
        with tempfile.NamedTemporaryFile() as target:
            target.write(b"descriptor-test")
            target.flush()
            fd = media_writer.authorized_fd(target.name, writable=False)
            try:
                self.assertEqual(os.read(fd, 15), b"descriptor-test")
            finally:
                os.close(fd)

    def test_authopen_writable_descriptor_is_readwrite_and_seekable(self):
        with tempfile.NamedTemporaryFile() as target:
            fd = media_writer.authorized_fd(target.name, writable=True)
            try:
                self.assertEqual(fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_ACCMODE, os.O_RDWR)
                os.write(fd, b"roundtrip")
                os.fsync(fd)
                os.lseek(fd, 0, os.SEEK_SET)
                self.assertEqual(os.read(fd, 9), b"roundtrip")
            finally:
                os.close(fd)

    def test_run_uses_combined_write_verify_then_eject(self):
        plan_path = Path("/tmp/test-plan.json")
        with mock.patch.object(media_writer, "plan_lock") as lock, mock.patch.object(
            media_writer, "_write_plan_locked"
        ) as write, mock.patch.object(
            media_writer, "_eject_plan_locked"
        ) as eject:
            lock.return_value.__enter__.return_value = plan_path
            media_writer.run_plan(plan_path, "reviewed")
        write.assert_called_once_with(plan_path, "reviewed", verify_after_write=True)
        eject.assert_called_once_with(plan_path)

    def test_plan_lock_allows_only_one_writer_to_reach_device_io(self):
        payload = b"exclusive write"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target_file = root / "raw-device"
            target_file.write_bytes(b"\0" * len(payload))
            source = {
                "artifact_snapshot_path": str(root / "unused.img"),
                "snapshot_path": str(root / "unused.img"),
                "artifact_sha256": hashlib.sha256(payload).hexdigest(),
                "artifact_bytes": len(payload),
                "expanded_sha256": hashlib.sha256(payload).hexdigest(),
                "expanded_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
            }
            target = {"disk": "/dev/disk4", "raw_disk": str(target_file), "bytes": len(payload)}
            plan = {"schema_version": 2, "source": source, "target": target, "state": media_writer.initial_state()}
            plan["plan_id"] = media_writer.canonical_plan_id(plan)
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan))
            entered = threading.Event()
            release = threading.Event()
            errors = []

            def blocking_snapshot(_source):
                entered.set()
                release.wait(timeout=5)
                return io.BytesIO(payload)

            def first_writer():
                try:
                    media_writer.write_plan(plan_path, plan["plan_id"])
                except Exception as exc:
                    errors.append(exc)

            with mock.patch.object(media_writer, "snapshot_source", side_effect=blocking_snapshot), mock.patch.object(
                media_writer, "checked_identity", return_value=target
            ), mock.patch.object(media_writer, "command"), mock.patch.object(
                media_writer, "authorized_fd", side_effect=lambda *_args, **_kwargs: os.open(target_file, os.O_RDWR)
            ) as authorize, mock.patch("sys.stderr", new=io.StringIO()):
                thread = threading.Thread(target=first_writer)
                thread.start()
                self.assertTrue(entered.wait(timeout=5))
                with self.assertRaisesRegex(media_writer.MediaError, "PLAN_BUSY"):
                    media_writer.write_plan(plan_path, plan["plan_id"])
                release.set()
                thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [])
            self.assertEqual(authorize.call_count, 1)
            persisted = json.loads(plan_path.read_text())
            self.assertEqual(persisted["state"]["auth_request_count"], 1)
            self.assertEqual(persisted["state"]["phase"], "written")

    def test_combined_write_and_verify_uses_one_authorized_descriptor(self):
        payload = b"one authorization" * 100
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            snapshot = root / "snapshot.img"
            snapshot.write_bytes(payload)
            target_file = root / "raw-device"
            target_file.write_bytes(b"\0" * len(payload))
            source = {
                "snapshot_path": str(snapshot),
                "artifact_snapshot_path": str(snapshot),
                "expanded_sha256": hashlib.sha256(payload).hexdigest(),
                "expanded_bytes": len(payload),
                "artifact_sha256": hashlib.sha256(payload).hexdigest(),
                "artifact_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
            }
            target = {"disk": "/dev/disk4", "raw_disk": str(target_file), "bytes": len(payload)}
            plan = {"schema_version": 2, "source": source, "target": target, "state": media_writer.initial_state()}
            plan["plan_id"] = media_writer.canonical_plan_id(plan)
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan))
            with mock.patch.object(media_writer, "checked_identity", return_value=target), mock.patch.object(
                media_writer, "command"
            ), mock.patch.object(media_writer, "authorized_fd", wraps=media_writer.authorized_fd) as authorize, mock.patch(
                "sys.stderr", new=io.StringIO()
            ), mock.patch("sys.stdout", new=io.StringIO()):
                result = media_writer.write_plan(plan_path, plan["plan_id"], verify_after_write=True)
            authorize.assert_called_once_with(str(target_file), writable=True)
            self.assertEqual(target_file.read_bytes(), payload)
            self.assertTrue(result["state"]["written"])
            self.assertTrue(result["state"]["verified"])
            self.assertEqual(result["state"]["auth_request_count"], 1)

    def test_forged_verified_boolean_is_not_a_receipt(self):
        plan = {
            "plan_id": "abc",
            "source": {"sha256": "a" * 64, "bytes": 10},
            "state": {"verified": True, "verification_receipt": None},
        }
        self.assertNotEqual(
            plan["state"]["verification_receipt"],
            media_writer.verification_receipt(plan),
        )

    def test_replayed_plan_is_rejected_before_source_or_device_access(self):
        plan = {
            "schema_version": 1,
            "source": {"path": "/tmp/a.iso", "sha256": "a" * 64, "bytes": 1},
            "target": {"disk": "/dev/disk4", "serial": "abc", "bytes": 2},
            "state": media_writer.initial_state(),
        }
        plan["plan_id"] = media_writer.canonical_plan_id(plan)
        plan["state"]["ejected"] = True
        plan["state"]["phase"] = "ejected"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan.json"
            path.write_text(__import__("json").dumps(plan))
            with mock.patch.object(media_writer, "snapshot_source") as snapshot:
                with self.assertRaisesRegex(media_writer.MediaError, "PLAN_ALREADY_USED"):
                    media_writer.write_plan(path, plan["plan_id"])
            snapshot.assert_not_called()

    def test_usb_registry_keeps_serialless_hub_and_child_separate(self):
        fixture = [
            {
                "locationID": 0x00200000,
                "USB Product Name": "USB3 HUB",
                "sessionID": 100,
                "IORegistryEntryID": 0x100000AAA,
                "IORegistryEntryChildren": [
                    {
                        "locationID": 0x01200000,
                        "USB Product Name": "USB DISK 3.0",
                        "kUSBSerialNumberString": "DRIVE-SERIAL",
                        "sessionID": 200,
                        "IORegistryEntryID": 0x100000BBB,
                    }
                ],
            }
        ]
        devices = media_writer.parse_usb_registry(__import__("plistlib").dumps(fixture))
        self.assertNotIn("00200000", devices)
        self.assertEqual(
            devices["01200000"],
            {
                "serial": "DRIVE-SERIAL",
                "product": "USB DISK 3.0",
                "location": "01200000",
                "registry_entry_id": "0x100000bbb",
                "session_id": "200",
            },
        )

    def test_usb_registry_keeps_serialized_hub_and_child_separate(self):
        fixture = [
            {
                "locationID": 0x00200000,
                "USB Product Name": "USB3 HUB",
                "kUSBSerialNumberString": "HUB-SERIAL",
                "sessionID": 100,
                "IORegistryEntryID": 0x100000AAA,
                "IORegistryEntryChildren": [
                    {
                        "locationID": 0x01200000,
                        "USB Product Name": "USB DISK 3.0",
                        "kUSBSerialNumberString": "DRIVE-SERIAL",
                        "sessionID": 200,
                        "IORegistryEntryID": 0x100000BBB,
                    }
                ],
            }
        ]
        devices = media_writer.parse_usb_registry(__import__("plistlib").dumps(fixture))
        self.assertEqual(devices["00200000"]["serial"], "HUB-SERIAL")
        self.assertEqual(devices["01200000"]["serial"], "DRIVE-SERIAL")

    def test_detects_compression_by_magic(self):
        samples = {
            "sample.bogus": b"BZh9payload",
            "sample.other": b"\xfd7zXZ\x00payload",
            "sample.data": b"\x1f\x8bpayload",
            "sample.archive": b"PK\x03\x04payload",
        }
        with tempfile.TemporaryDirectory() as directory:
            for name, content in samples.items():
                path = Path(directory) / name
                path.write_bytes(content)
                self.assertEqual(
                    media_writer.detect_format(path),
                    {"sample.bogus": "bz2", "sample.other": "xz", "sample.data": "gz", "sample.archive": "zip"}[name],
                )

    def test_zip_requires_unambiguous_image_or_explicit_member(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "images.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("first.iso", b"one")
                archive.writestr("second.img", b"two")
            with self.assertRaisesRegex(media_writer.MediaError, "ARCHIVE_AMBIGUOUS"):
                media_writer.create_snapshots(path, None, None)
            details = media_writer.create_snapshots(path, None, "second.img")
            try:
                with media_writer.snapshot_source(details) as expanded:
                    self.assertEqual(expanded.read(), b"two")
                self.assertEqual(details["archive_member"], "second.img")
            finally:
                __import__("shutil").rmtree(Path(details["snapshot_dir"]))

    def test_compressed_source_expands_to_read_only_verified_snapshot(self):
        payload = b"expanded boot image" * 100
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "image.iso.bz2"
            source.write_bytes(bz2.compress(payload))
            details = media_writer.create_snapshots(source, hashlib.sha256(source.read_bytes()).hexdigest(), None)
            try:
                artifact = Path(details["snapshot_path"])
                with media_writer.snapshot_source(details) as expanded:
                    self.assertEqual(expanded.read(), payload)
                self.assertEqual(details["expanded_bytes"], len(payload))
                self.assertEqual(details["expanded_sha256"], hashlib.sha256(payload).hexdigest())
                self.assertEqual(stat.S_IMODE(artifact.stat().st_mode), 0o400)
                self.assertEqual(details["artifact_snapshot_path"], details["snapshot_path"])
            finally:
                __import__("shutil").rmtree(artifact.parent)

    def test_xz_source_is_fully_scanned_before_authorization(self):
        payload = b"xz boot image" * 100
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "image.img.xz"
            source.write_bytes(lzma.compress(payload))
            details = media_writer.create_snapshots(
                source,
                hashlib.sha256(source.read_bytes()).hexdigest(),
                None,
                max_expanded_bytes=len(payload),
            )
            try:
                self.assertEqual(details["expanded_sha256"], hashlib.sha256(payload).hexdigest())
                with media_writer.snapshot_source(details) as expanded:
                    self.assertEqual(expanded.read(), payload)
            finally:
                __import__("shutil").rmtree(Path(details["snapshot_dir"]))

    def test_oversized_raw_source_is_rejected_before_snapshot_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "image.img"
            source.write_bytes(b"12345")
            with mock.patch.object(media_writer, "_private_snapshot_dir") as snapshot_dir:
                with self.assertRaisesRegex(media_writer.MediaError, "INSUFFICIENT_TARGET_CAPACITY"):
                    media_writer.create_snapshots(source, None, None, max_expanded_bytes=4)
            snapshot_dir.assert_not_called()

    def test_create_snapshots_rejects_growth_after_outer_preflight(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "image.img"
            source.write_bytes(b"1234")
            original_snapshot = media_writer._snapshot_file

            def grow_before_copy(path, destination, *, expected_stat):
                path.write_bytes(b"12345")
                return original_snapshot(path, destination, expected_stat=expected_stat)

            with mock.patch.object(media_writer, "_snapshot_file", side_effect=grow_before_copy):
                with self.assertRaisesRegex(media_writer.MediaError, "SOURCE_CHANGED"):
                    media_writer.create_snapshots(
                        source,
                        None,
                        None,
                        snapshot_parent=root,
                        snapshot_prefix="plan.json.media-",
                        max_expanded_bytes=4,
                    )
            self.assertEqual(list(root.glob("plan.json.media-*")), [])

    def test_prepared_stream_overrun_is_stopped_before_target_write(self):
        reviewed = b"1234"
        oversized = b"12345"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target_file = root / "raw-device"
            target_file.write_bytes(b"\0" * len(oversized))
            source = {
                "expanded_sha256": hashlib.sha256(reviewed).hexdigest(),
                "expanded_bytes": len(reviewed),
                "sha256": hashlib.sha256(reviewed).hexdigest(),
                "bytes": len(reviewed),
            }
            target = {"disk": "/dev/disk4", "raw_disk": str(target_file), "bytes": len(oversized)}
            plan = {"schema_version": 2, "source": source, "target": target, "state": media_writer.initial_state()}
            plan["plan_id"] = media_writer.canonical_plan_id(plan)
            plan_path = root / "plan.json"
            plan_path.write_text(json.dumps(plan))
            with mock.patch.object(media_writer, "snapshot_source", return_value=io.BytesIO(oversized)), mock.patch.object(
                media_writer, "checked_identity", return_value=target
            ), mock.patch.object(media_writer, "command"), mock.patch.object(
                media_writer, "authorized_fd", side_effect=lambda *_args, **_kwargs: os.open(target_file, os.O_RDWR)
            ), mock.patch("sys.stderr", new=io.StringIO()):
                with self.assertRaisesRegex(media_writer.MediaError, "SNAPSHOT_CHANGED"):
                    media_writer.write_plan(plan_path, plan["plan_id"])
            self.assertEqual(target_file.read_bytes(), b"\0" * len(oversized))

    def test_primary_url_only_provenance_requires_explicit_opt_in(self):
        target = {"disk": "/dev/disk4", "raw_disk": "/dev/rdisk4", "bytes": 100}
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "image.iso"
            image.write_bytes(b"image")
            plan_path = Path(directory) / "plan.json"
            base = {
                "image": str(image),
                "sha256": None,
                "provenance_url": "https://vendor.invalid/image",
                "archive_member": None,
                "device": "/dev/disk4",
                "plan": str(plan_path),
                "allow_primary_url_only": False,
            }
            with mock.patch.object(media_writer, "disk_info", return_value=target):
                with self.assertRaisesRegex(media_writer.MediaError, "SOURCE_HASH_REQUIRED"):
                    media_writer.cmd_prepare(type("Args", (), base)())
                base["allow_primary_url_only"] = True
                with mock.patch("sys.stdout", new=io.StringIO()):
                    media_writer.cmd_prepare(type("Args", (), base)())
            plan = json.loads(plan_path.read_text())
            self.assertEqual(plan["source"]["trust_tier"], "primary-url-only")

    def test_expanded_capacity_is_checked(self):
        payload = b"x" * 101
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "image.iso.gz"
            import gzip
            source.write_bytes(gzip.compress(payload))
            args = type("Args", (), {
                "image": str(source),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "provenance_url": "https://vendor.invalid/image",
                "allow_primary_url_only": False,
                "archive_member": None,
                "device": "/dev/disk4",
                "plan": str(Path(directory) / "plan.json"),
            })()
            with mock.patch.object(media_writer, "disk_info", return_value={"disk": "/dev/disk4", "bytes": 100}):
                with self.assertRaisesRegex(media_writer.MediaError, "INSUFFICIENT_TARGET_CAPACITY"):
                    media_writer.cmd_prepare(args)
            self.assertEqual(list(Path(directory).glob("plan.json.media-*")), [])

    def test_prepare_uses_plan_owned_snapshot_and_discard_cleans_it(self):
        target = {"disk": "/dev/disk4", "raw_disk": "/dev/rdisk4", "bytes": 100}
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "image.iso"
            source.write_bytes(b"image")
            plan_path = Path(directory) / "plan.json"
            args = type("Args", (), {
                "image": str(source),
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "provenance_url": "https://vendor.invalid/image",
                "allow_primary_url_only": False,
                "archive_member": None,
                "device": "/dev/disk4",
                "plan": str(plan_path),
            })()
            with mock.patch.object(media_writer, "disk_info", return_value=target), mock.patch("sys.stdout", new=io.StringIO()):
                media_writer.cmd_prepare(args)
            plan = json.loads(plan_path.read_text())
            snapshot_dir = Path(plan["source"]["snapshot_dir"])
            self.assertEqual(snapshot_dir.parent, plan_path.parent.resolve())
            self.assertTrue(snapshot_dir.name.startswith("plan.json.media-"))
            self.assertTrue(snapshot_dir.is_dir())
            media_writer.discard_plan(plan_path)
            self.assertFalse(snapshot_dir.exists())
            state = json.loads(plan_path.read_text())["state"]
            self.assertTrue(state["discarded"])
            self.assertTrue(state["snapshot_cleaned"])

    def test_cleanup_refuses_directory_not_owned_by_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            valuable = root / "valuable"
            valuable.mkdir()
            artifact = valuable / "artifact.iso"
            artifact.write_bytes(b"keep")
            plan_path = root / "plan.json"
            plan = {
                "source": {
                    "snapshot_dir": str(valuable),
                    "artifact_snapshot_path": str(artifact),
                    "snapshot_path": str(artifact),
                }
            }
            with self.assertRaisesRegex(media_writer.MediaError, "SNAPSHOT_CLEANUP_REFUSED"):
                media_writer.cleanup_snapshots(plan_path, plan)
            self.assertEqual(artifact.read_bytes(), b"keep")

    def test_empty_raw_image_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "empty.img"
            source.touch()
            with self.assertRaisesRegex(media_writer.MediaError, "IMAGE_UNSUPPORTED"):
                media_writer.create_snapshots(source, None, None)

    def test_status_is_no_auth_and_receipt_is_plan_bound(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "plan.json"
            source = {"sha256": "a" * 64, "bytes": 10, "expanded_sha256": "a" * 64, "expanded_bytes": 10, "artifact_sha256": "a" * 64, "artifact_bytes": 10}
            plan = {"schema_version": 2, "source": source, "target": {"disk": "/dev/disk4"}, "state": media_writer.initial_state()}
            plan["plan_id"] = media_writer.canonical_plan_id(plan)
            plan_path.write_text(json.dumps(plan))
            with mock.patch.object(media_writer, "authorized_fd") as auth, mock.patch("sys.stdout", new=io.StringIO()) as output:
                media_writer.status_plan(plan_path)
            auth.assert_not_called()
            parsed = json.loads(output.getvalue())
            self.assertEqual(parsed["plan_id"], plan["plan_id"])
            self.assertEqual(media_writer.durable_receipt(plan)["expanded_bytes"], 10)

    def test_compare_records_external_verification_and_allows_eject(self):
        payload = b"already flashed image"
        target = {"disk": "/dev/disk4", "raw_disk": "/dev/rdisk4", "bytes": len(payload), "serial": "s", "model": "m", "transport": "USB", "device_tree_path": "p", "port_location": "1", "registry_entry_id": "0x1", "usb_session_id": "2"}
        with tempfile.TemporaryDirectory() as directory:
            snapshot = Path(directory) / "expanded.img"
            snapshot.write_bytes(payload)
            plan = {"schema_version": 2, "source": {"snapshot_path": str(snapshot), "artifact_snapshot_path": str(snapshot), "expanded_sha256": hashlib.sha256(payload).hexdigest(), "expanded_bytes": len(payload), "artifact_sha256": hashlib.sha256(payload).hexdigest(), "artifact_bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "bytes": len(payload)}, "target": target, "state": media_writer.initial_state()}
            plan["plan_id"] = media_writer.canonical_plan_id(plan)
            plan_path = Path(directory) / "plan.json"
            plan_path.write_text(json.dumps(plan))
            fd = os.open(snapshot, os.O_RDONLY)
            with mock.patch.object(media_writer, "disk_info", return_value=target), mock.patch.object(media_writer, "authorized_fd", return_value=fd), mock.patch.object(media_writer, "command") as diskutil:
                result = media_writer.verify_plan(plan_path, external=True)
            diskutil.assert_called_once_with("diskutil", "unmountDisk", "/dev/disk4", capture=False)
            self.assertTrue(result["state"]["verified_external"])
            self.assertEqual(result["state"]["phase"], "verified_external")
            self.assertEqual(result["state"]["auth_request_count"], 1)
            self.assertEqual(result["state"]["receipt"]["verification_mode"], "external")

    def test_staged_verify_unmounts_before_opening_fresh_descriptor(self):
        payload = b"written image"
        target = {"disk": "/dev/disk4", "raw_disk": "/dev/rdisk4", "bytes": len(payload)}
        with tempfile.TemporaryDirectory() as directory:
            media = Path(directory) / "media"
            media.write_bytes(payload)
            source = {
                "artifact_snapshot_path": str(media),
                "snapshot_path": str(media),
                "artifact_sha256": hashlib.sha256(payload).hexdigest(),
                "artifact_bytes": len(payload),
                "expanded_sha256": hashlib.sha256(payload).hexdigest(),
                "expanded_bytes": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
            }
            state = media_writer.initial_state()
            state.update({"phase": "written", "written": True})
            plan = {"schema_version": 2, "source": source, "target": target, "state": state}
            plan["plan_id"] = media_writer.canonical_plan_id(plan)
            plan_path = Path(directory) / "plan.json"
            plan_path.write_text(json.dumps(plan))
            fd = os.open(media, os.O_RDONLY)
            with mock.patch.object(media_writer, "disk_info", return_value=target), mock.patch.object(
                media_writer, "authorized_fd", return_value=fd
            ), mock.patch.object(media_writer, "command") as diskutil, mock.patch("sys.stdout", new=io.StringIO()):
                result = media_writer.verify_plan(plan_path)
            diskutil.assert_called_once_with("diskutil", "unmountDisk", "/dev/disk4", capture=False)
            self.assertEqual(result["state"]["phase"], "verified")

    def test_compare_and_discarded_plans_cannot_be_replayed(self):
        for phase in ("verified_external", "discarded"):
            plan = {
                "schema_version": 2,
                "source": {"sha256": "a" * 64, "bytes": 1},
                "target": {"disk": "/dev/disk4"},
                "state": {**media_writer.initial_state(), "phase": phase},
            }
            plan["plan_id"] = media_writer.canonical_plan_id(plan)
            with tempfile.TemporaryDirectory() as directory:
                plan_path = Path(directory) / "plan.json"
                plan_path.write_text(json.dumps(plan))
                with mock.patch.object(media_writer, "disk_info") as inspect:
                    with self.assertRaisesRegex(media_writer.MediaError, "PLAN_ALREADY_USED"):
                        media_writer.verify_plan(plan_path, external=True)
                inspect.assert_not_called()

    def test_atomic_plan_save_preserves_previous_file_when_replace_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path = Path(directory) / "plan.json"
            plan_path.write_text("previous valid plan\n")
            with mock.patch.object(os, "replace", side_effect=OSError("interrupted")):
                with self.assertRaisesRegex(OSError, "interrupted"):
                    media_writer.save_plan(plan_path, {"new": True})
            self.assertEqual(plan_path.read_text(), "previous valid plan\n")
            self.assertEqual(list(Path(directory).glob(".plan.json.*")), [])


if __name__ == "__main__":
    unittest.main()
