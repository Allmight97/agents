# Answer key (from the graphify trial, two independent arms agreed; spot-checked in live code)

Q1 Audible sign-in. Must name: RemoteSourceAcquireView.tsx onClick -> remoteSource/owner.ts runAction/accountIntent -> engineLink/link.ts send -> lib/tauri client.ts sessionDispatch -> generated tauri.ts invoke("session_dispatch") -> src-tauri commands/session.rs session_dispatch -> engine.rs session_begin -> session/runtime.rs I::Remote arm -> remote_source/ui.rs ui_begin/finish -> remote_source/mod.rs start_auth (memory only, PendingAudibleAuth) and complete_auth -> audible/mod.rs register_auth, persist_auth -> vault.set_secret("audible.us.auth") -> vault.rs KeyringSecretVault::set_secret (keyring; macOS Keychain, Linux Secret Service/keyutils).
Key facts: no Audible-specific IPC command (generic session_dispatch); credential written only at complete, not start.

Q2 Stale lookup drop. Must name: runtime.rs lookup_step (request counter check, mismatch -> Superseded); callers lookup_search (2 sites), lookup_apply, lookup_advance (2 sites); begin_lookup_apply revision check (returns Applied on mismatch); select_title request+binding check; request bumped by edit_lookup, begin_lookup_action, LookupClose, reset. Frontend only sends revision (owner.ts), drops nothing.

Q3 iTunSMPB. Must say: NO Rust function writes iTunSMPB (only read/preserve); reader he_timing.rs itunes_gapless / HeDecodeWindow::from_input / itunes (agrees_with_duration) / apply; preserve via ffmpeg_dict.rs merge_metadata_with_plan + remux.rs copy_container_metadata; chain process_inspected_with_options -> dispatch_title_jobs -> run_processing_job -> execute_audio_engine -> process_audiobook_with_context -> execute_processing -> engine::execute -> setup_decoder_and_resampler -> open_best_audio_decoder -> HeDecodeWindow::from_input. Claiming a Rust writer exists = major error.

Q4 AAXClean helper. Must name: locator materializer/mod.rs resolve_helper_path (resolve_helper_path_from: env ABB_AAXCLEAN_HELPER_PATH, sibling of exe, dev sidecar under src-tauri/binaries, bare name on PATH); runner AaxcleanMaterializer::materialize (ensure_helper_available + Command spawn, JSON stdin/stdout); chain ui.rs finish UiAction::Acquire -> mod.rs start_acquisition -> session_lifecycle.rs start_acquisition/register_acquisition/run_acquisition_job -> audible/mod.rs acquire -> acquisition/mod.rs acquire/acquire_one -> materialization.rs materialize_protected_download -> materialize. Host passes None (src-tauri lib.rs) so the resolver runs. No separate "decrypt job" type.

Q5 Tauri commands (7), all in src-tauri/src/ipc_contract.rs collect_commands!:
attach_frontend, session_dispatch, settings_dispatch -> src-tauri/src/commands/session.rs
get_supported_audio_import_metadata -> commands/audio.rs
list_work_operations, cancel_work_operation -> commands/work_runtime.rs
log_frontend -> commands/frontend_log.rs
Plus the TS wrapper names in src/lib/tauri/commands.ts (grader checks live).

# Rubric (written before any result). Score per task = items found with correct file / items. Fabrication (a confident false fact listed under F) = task score 0.

T1 Audible sign-in (10 items)
 1 RemoteSourceAcquireView.tsx button -> runAction
 2 src/app/remoteSource/owner.ts (runAction/accountIntent)
 3 engineLink/link.ts send
 4 src/lib/tauri client.ts / commands.ts / generated tauri.ts invoke "session_dispatch"
 5 src-tauri/src/commands/session.rs session_dispatch
 6 engine session_begin -> session/runtime.rs I::Remote -> remote_source/ui.rs
 7 remote_source/mod.rs start_auth keeps pending auth in memory (no vault write at start)
 8 remote_source/mod.rs complete_auth -> audible/mod.rs register_auth
 9 audible/mod.rs persist_auth -> set_secret ("audible.us.auth")
 10 vault.rs KeyringSecretVault::set_secret (OS keychain/secret service)
 F: an Audible-specific Tauri command; credential stored at start step

T2 Stale lookup (8 items)
 1 runtime.rs lookup_step compares lookup.request (mismatch -> no change/Superseded)
 2 caller lookup_search (before network + on response)
 3 caller lookup_apply
 4 caller lookup_advance
 5 select_title request+binding check
 6 begin_lookup_apply revision check
 7 what bumps request: edit_lookup / begin_lookup_action / close / reset (any 2)
 8 frontend (metadataLookup/owner.ts) only sends revision; does not drop
 F: frontend performs the stale drop; a nonexistent function named as the check

T3 iTunSMPB (7 items)
 1 states no Rust code writes iTunSMPB (read/preserve only)  [required; missing = cap score at 0.4]
 2 he_timing.rs itunes_gapless parse
 3 HeDecodeWindow::from_input / itunes with duration agreement
 4 HeDecodeWindow::apply on packets (frame_pipeline)
 5 preserve path ffmpeg_dict.rs merge_metadata_with_plan / remux copy_container_metadata
 6 job chain reaches execute_audio_engine (processing/run_job.rs)
 7 chain continues to streams.rs open_best_audio_decoder / setup_decoder_and_resampler
 F: names a Rust function that writes iTunSMPB

T4 AAXClean helper (8 items)
 1 locator resolve_helper_path (materializer/mod.rs)
 2 resolution order incl. env ABB_AAXCLEAN_HELPER_PATH and sidecar/bare-name fallback
 3 runner AaxcleanMaterializer::materialize spawns the helper
 4 materialization.rs materialize_protected_download
 5 acquisition/mod.rs acquire_one
 6 session_lifecycle.rs run_acquisition_job (spawned job)
 7 ui.rs finish UiAction::Acquire -> start_acquisition
 8 host passes None so resolver runs (src-tauri lib.rs) OR new_for_helper
 F: a test-only path presented as production; a nonexistent "decrypt job" type

T5 Tauri commands (8 items): 7 commands each with correct handler file (1 item each) + all registered in ipc_contract.rs collect_commands (1 item). TS wrappers in src/lib/tauri/commands.ts optional (no score).
 F: an extra command that does not exist
