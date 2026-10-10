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
