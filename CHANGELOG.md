# Changelog

All notable changes to **Reaper MCP Server** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
