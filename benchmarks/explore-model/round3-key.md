# Round 3 keys (de9aa91e). Score = items found with a correct code location / 8. Fabrication (invented function/file or false behavior stated as fact) -> task 0.
H1 settings survival
 1 owner abb-engine app_settings; hosts change via settings_dispatch / SettingsIntent
 2 stored in settings.toml in host config folder: app_settings/storage.rs load/save/settings_path
 3 saved shape kept apart from IPC types (storage.rs Saved* vs types.rs)
 4 load never fails: missing file -> defaults; damaged file logged, not used, replaced on next save
 5 no migration from builds before settings.toml
 6 old saved files protected by samples/ fixture(s) that must keep loading (+ contract tests); new field needs default; old values mapped in storage.rs
 7 failed save: stays in effect, save_error reported (runtime.rs write), retried on next change / Retry / shutdown
 8 shutdown returns ShutdownOutcome::SettingsUnsaved if last write fails (engine.rs)
 F: claims a version/migration system, or frontend/localStorage persistence of settings
H2 cancel cleanup
 1 cancel path: frontend -> cancel_work_operation command (src-tauri commands/work_runtime.rs) -> engine.rs cancel_work_operation -> work_runtime/runtime.rs cancel_operation
 2 per-title cancel flags; whole-op cancel sets all; child_job_id cancels one title
 3 processing observes flag via CancellationChecker at checkpoints -> Cancelled terminal outcome (processing/run/run_job.rs)
 4 encode output staged in a processing workspace under app cache (.abb-processing-<session>, audio/processor/staging.rs create_processing_workspace_dir), not at destination
 5 workspace registered for cleanup before cancellation is observed; cleanup failures tracked for retry
 6 abandoned workspaces swept: cleanup_abandoned_processing_sessions (audio/processor/mod.rs ~175)
 7 final artifact only written on successful commit (output_artifact/commit.rs); cancelled title never publishes a partial file
 8 empty ABB-created output folders removed by end_title (output_artifact/parent_dirs.rs) unless another run still claims them
 F: says partial output is left/truncated at destination; invents functions
H3 add a metadata field (narrator as model)
 1 session/metadata_form.rs MetadataField enum + form state
 2 abb-metadata-core/src/lib.rs metadata model (narrator stored as composer)
 3 MP4 tag write mapping: metadata/mp4ameta_bridge.rs and/or field_schema.rs / metadata_ops.rs / metadata_sinks.rs
 4 FFmpeg-dictionary path or reader: metadata/ffmpeg_dict.rs and/or reader.rs (read back / non-MP4)
 5 session state/lookup apply: session/state.rs and/or lookup.rs / metadata_lookup mapping
 6 generated bindings src/lib/generated/tauri.ts regenerated (export_bindings / check-generated-bindings), not hand-edited
 7 frontend field definition src/app/metadataSession/fields.ts
 8 tag preview labels src/ui/tagPreview/rows.ts
 F: says to hand-edit generated tauri.ts as the source of truth; names a frontend validator
