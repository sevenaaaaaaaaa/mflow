# Published content archived out of MFlow

- Date: 2026-08-01
- Reason: reduce Lovart MFlow vault size; keep only unpublished / in-progress GenFlow assets here
- Destination: `~/Lovart Local Dev/Backup/mflow-published-2026-08-01/`
- Selection rule: file confirmed present in Sanity production (`blog` / `compositePage`) by language + slug

## Moved

- Blog: 971 markdown files (mostly `Lovart-Blog-Pipeline/01-Drafts` already on Sanity)
- Page Gen: 2880 JSON files (flat root tools/features mirrors + published Pages + archive ndjson)
- Manifest: `MOVE_MANIFEST.json` / `MOVED_FILES.txt` inside the backup folder

## Still in MFlow (intentional)

- Unpublished blog drafts / root drafts not matched in Sanity
- Page Gen `Pages/drafts/` and unpublished JSON
- Governance docs, scripts, indexes, storyline docs

## Restore

Copy specific files back from the backup path into `1-3 GenFlow/` if needed for rewrite. Do not Sanity `--replace`.
