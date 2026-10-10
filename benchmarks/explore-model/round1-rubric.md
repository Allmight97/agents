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
