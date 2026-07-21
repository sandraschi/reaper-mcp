
## [Unreleased] — 2026-07-13

### Fixed
- Security: CORS `allow_origins=["*"]` → fleet standard with explicit origins + unconditional regex (Tailscale, LAN, Tauri)
- Security: `build.ps1` now bundles `.env.example` instead of `.env` (was leaking dev API keys)
- Security: `tauri.conf.json` resources updated to `.env.example`
- Tauri: `tauri.conf.json` targets changed from `["msi", "nsis"]` to `["nsis"]`
- Tauri: `backend.rs` `free_port()` upgraded with image-name kill, UAC escalation, 240s poll loop, stream watching
- Tauri: `build.ps1` bundles `.env.example` (NOT `.env`)
- Metadata: `glama.json` updated (FastMCP version, tools count)
- Layout: `.env.template` → `.env.example` (fleet convention)
- Bare `except ImportError: pass` → logged warning in `mcp_app.py`

### Added
- `llms.txt` and `llms-full.txt` (fleet packaging standard)
- `@mcp.resource("status://reaper/config")` for live config snapshot
- `.cursorrules` for session context injection
- CHANGELOG synced with current changes

## [Unreleased] — 2026-06-14

### Added
- Tauri native wrapper (native/ directory) with bundle.resources + std::process::Command
- CUA-NSIS: just cua-nsis-test recipe, scripts/cua-smoke.py, scripts/cua-nsis-config.json
- Tauri CORS: tauri://localhost origins for WebView API access
- NSIS installer at dist/ and native/target/release/bundle/nsis/

### Changed
- Frontend API calls use absolute http://127.0.0.1:{port} URLs in production build
- CORS middleware includes allow_origin_regex for tauri.localhost
# Changelog

All notable changes to **Reaper MCP Server** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.2.0] - 2026-03-08

### Added
- **FastMCP 3.1**: Full alignment; `fastmcp>=3.1`, single-backend pattern (REST + MCP at `/mcp`).
- **Prompts**: Seven session templates (`reaper_record_session`, `reaper_mix_session`, `reaper_export_project`, `reaper_transport_control`, `reaper_track_operations`, `reaper_project_help`, `reaper_system_help`).
- **Skills**: Optional `SkillsDirectoryProvider` for `reaper_mcp/skills`; bundled `reaper-daw-workflow` SKILL.
- **Server module**: `reaper_mcp/server.py` for ASGI (`uvicorn reaper_mcp.server:app`) and stdio (`mcp.run()`); `reaper_mcp/mcp_app.py` single MCP instance with portmanteau tools and prompts.
- **FastAPI mount**: Backend mounts MCP at `/mcp` via `mcp.http_app()`; REST at `/api/v1/tools` (list/call).

### Changed
- **Webapp**: Frontend uses REST (GET/POST `/api/v1/tools`) on port 10797; removed JSON-RPC `/messages`. `mcp_client.ts` uses `VITE_BACKEND_URL` (default localhost:10797). Status, Help, ReaScript, Tools pages use REST response shape `{ status, result?, message? }`.
- **Backend**: Tools router prefix `/tools` under `/api/v1` (full path `/api/v1/tools`). Start script runs backend from project root with `uv run --project $ProjectRoot`.
- **Stdio**: `python -m reaper_mcp` / `reaper-mcp` CLI runs MCP stdio server (`mcp.run()`); web backend via `uvicorn reaper_mcp.server:app`.
- **ReaScript**: Removed unused `Context` parameter from `reaper_reascript`; ruff/format fixes (B904, N812, S102, S104).

### Fixed
- **ASGI load**: Resolve "Could not import module reaper_mcp.server" by adding `server.py` and running backend from project root.
- **Dependencies**: Added `fastapi`, `uvicorn[standard]` to `pyproject.toml`.

### Documentation
- **README**: FastMCP 3.1, five portmanteau tools, prompts/skills/agentic, sampling note, web_sota ports 10796/10797 and `/mcp`. Architecture blurb updated.

## [2.1.0] - Unreleased

### Added
- **ReaScript JSON Support**: `reaper_reascript` now returns structured JSON via `_result` variable
- **Extensive Testing Scaffold**: Added `conftest.py` with mocks, unit tests, and E2E verification
- **Webapp Launcher Tool**: `start_webapp` tool added to `reaper_system` for self-actuation
- **Improved Status Page**: Enhanced documentation and monitoring in the SOTA dashboard

### Technical Improvements
- Refactored frontend communication to use robust JSON-RPC via `mcp_client`
- Added `verify_e2e.py` for headless stdio verification
- Fixed E402 and F841 linting issues across the codebase

### Changed
- **Error handling** improved with validation and graceful degradation
- **Code quality** enhanced with type hints and comprehensive error handling
- **Testing infrastructure** upgraded to modern pytest with coverage reporting

### Technical Improvements
- Added validation module with comprehensive parameter checking
- Implemented MCP server health checks and status tools
- Added resource management for OSC connections
- Enhanced transport control with better error recovery
- Improved track management with bulk operations support

## [1.0.0] - 2025-01-01

### Added
- **Initial release** of Reaper MCP Server 🎵
- **FastMCP 2.1 compliance** for Claude Desktop integration
- **Real OSC integration** with Reaper DAW bidirectional communication
- **Transport control**: play, stop, pause, record, position tracking
- **Track management**: mute, solo, arm, bulk operations
- **Project automation**: save, markers, rendering control
- **Austrian engineering quality** 🇦🇹 - precision and reliability
- **Comprehensive documentation** and setup guides
- **Development testing** script for OSC connection validation

### Technical Details
- **Python 3.9+** async/await patterns
- **OSC protocol** communication over UDP
- **Windows-first** design with PowerShell compatibility
- **Structured error handling** with user-friendly messages
- **Modular architecture** for easy extension

---

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities

## Version Guidance
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

---

*"Sin temor y sin esperanza" - Practical audio automation without hype.* 🎼🇦🇹

