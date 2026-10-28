# Migration status

**IN PROGRESS — not yet a complete checkout.**

Source: KillQuest Sites v180, commit `6ebe5805e1950c232ba129a3fa77f8c98d70ff8d`.
Target: https://github.com/hotkot/killquest, branch `main`.
Date: 2026-10-28.

The original snapshot has 3,159 tracked files (1,051,510,858 bytes), including the playable `dist/`, authoring art/audio, archived media, scripts, checks, balance notes and desktop wrapper. Runtime behavior is unchanged.

Transfer uses the connected GitHub plugin. No command-line GitHub authorization is required. Files are content-addressed by original Git blob SHA; checkpoint commits will retain completed batches. The final verification will compare every migrated blob against the inventory. The original commit log will be retained as provenance; the GitHub import is a current-tree snapshot rather than a claim that all original commit objects were imported.

Read docs/HANDOFF.md and AGENTS.md for development continuation. Do not describe the migration as complete until this document is updated with final counts and validation.
