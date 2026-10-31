# Local Windows EXE builder

On a Windows x64 machine, install **Python 3.7 or newer** (including Tcl/Tk;
standard python.org installations include it) and **Node.js 22 or newer**.
Restart your terminal after installing them. Keep the complete repository,
including `dist`, `desktop`, and `checks`.

Double-click **`desktop/Builder.bat`**. Alternatively, from the repository root:

```sh
python desktop/compiler.py
```

The window uses a dark theme for its controls, log panel and scrollbar, with a
dark native title bar on supported Windows versions. It provides these actions:

| Button | Action |
| --- | --- |
| Build | Download and verify the official pinned Electron 45.2.1 Windows x64 runtime, then copy the current game into a fresh portable EXE folder. |
| Test | Check shipped JavaScript syntax, eight focused game regression suites, desktop URL isolation, builder failure paths, packaged file hashes, EXE architecture, and source freshness. Requires a completed Build. |
| Package | Verify the build and produce an integrity-checked portable ZIP. Requires a completed Build. |
| Run | Verify the build and launch `KillQuest.exe` on Windows. |
| Deploy | Run Build → Test → Package → Run in order, stopping on any failure. This runs locally; it does not upload or publish anything. |

Progress and failures appear in the window. Buttons are disabled during an
operation; closing waits until the operation finishes. Close the running game
before rebuilding. The tool supports paths containing spaces.

Outputs:

- `desktop/output/KillQuest-Windows-x64/KillQuest.exe` — launchable game, with
  required adjacent runtime files and `resources/app/game`.
- `desktop/output/KillQuest-Windows-x64.zip` — share/extract the whole ZIP,
  rather than copying only the EXE.
- `desktop/output/KillQuest-Windows-x64/build-info.json` — runtime version,
  official runtime checksum, and hashes for all included files.

The first Build requires HTTPS access to `github.com` and GitHub release asset
hosts. Later builds reuse the verified runtime in `desktop/.cache`. TLS and SHA256
verification remain enabled. If a download fails, fix connectivity and retry;
partial downloads are discarded. Do not replace checksums to bypass a failure.
Node is used only for tests; the packaged game contains its own runtime.
Builds and downloads are ignored by Git. No npm install or game bundler is needed.

Every action also works from a terminal:

```sh
python desktop/compiler.py build
python desktop/compiler.py test
python desktop/compiler.py package
python desktop/compiler.py run
python desktop/compiler.py deploy
```

The old `desktop/build_windows.py` now forwards to the same commands. Its
historical cache/destination argument interface has been retired. Build, Test
and Package can run on Linux/macOS for cross-packaging; Run requires Windows.
The game is bundled with Electron rather than translated to native machine code.

Automated checks cover the game model and package integrity. They do not prove
Windows launch, video/audio/autoplay, visual rendering, or physical controller
behavior. After Deploy, play the game on your machine to verify these. Builds
are unsigned; no code signing or installer is configured. The current source's
migration status is still documented separately in `docs/MIGRATION.md`.
