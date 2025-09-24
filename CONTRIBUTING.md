# Contributing to Reaper MCP Server 🎵

Thank you for your interest in contributing to the **Reaper MCP Server**! This document provides guidelines and information for contributors.

## 🇦🇹 Austrian Engineering Standards

We maintain **Austrian engineering quality** standards:
- **Precision**: Every line of code serves a purpose
- **Reliability**: Robust error handling and testing
- **Simplicity**: Clean, maintainable code without unnecessary complexity
- **Documentation**: Comprehensive and accessible

## 🚀 Quick Start

### Development Environment Setup

1. **Clone the repository**
   ```powershell
   git clone https://github.com/sandra/reaper-mcp.git
   cd reaper-mcp
   ```

2. **Set up Python environment**
   ```powershell
   # Create virtual environment
   python -m venv venv
   .\venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

3. **Install Reaper DAW**
   - Download from [reaper.fm](https://reaper.fm)
   - Configure OSC as described in README.md

4. **Run tests**
   ```powershell
   # Run all tests
   .\run_tests.ps1

   # Run specific test types
   .\run_tests.ps1 -TestType unit
   .\run_tests.ps1 -TestType integration
   ```

## 📋 Development Workflow

### 1. Choose an Issue
- Check [Issues](https://github.com/sandra/reaper-mcp/issues) for open tasks
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch
```powershell
# Create and switch to feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes
- Follow the [coding standards](#coding-standards)
- Write tests for new functionality
- Update documentation as needed
- Test your changes thoroughly

### 4. Commit Changes
```powershell
# Stage your changes
git add .

# Commit with conventional format
git commit -m "feat: add new transport control feature

- Add play/pause toggle functionality
- Update transport status tracking
- Add unit tests for new feature"
```

### 5. Push and Create PR
```powershell
# Push your branch
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## 💻 Coding Standards

### Python Style
- **Black** for code formatting (100 character line length)
- **isort** for import sorting
- **Flake8** for linting
- **MyPy** for type checking

### Code Quality
```python
# ✅ Good: Type hints, docstrings, error handling
async def get_track_info(track_id: int) -> Dict[str, Any]:
    """Get detailed information for specific track.

    Args:
        track_id: Track number (1-based indexing)

    Returns:
        Dictionary with track details

    Raises:
        ValidationError: If track_id is invalid
    """
    try:
        validated_id = TrackValidation.validate_track_id(track_id)
        # ... implementation
    except ValidationError as e:
        return {"error": str(e), "success": False}

# ❌ Bad: No types, poor error handling
def get_track(track_id):
    result = client.get_track(track_id)
    return result
```

### Naming Conventions
- **Functions**: `snake_case` (e.g., `get_track_info()`)
- **Classes**: `PascalCase` (e.g., `TrackValidation`)
- **Constants**: `UPPER_CASE` (e.g., `DEFAULT_OSC_PORT`)
- **Files**: `snake_case.py` (e.g., `transport_tools.py`)

### Error Handling
- **Validate inputs** at function boundaries
- **Use custom exceptions** for domain-specific errors
- **Log errors** with appropriate levels
- **Return structured error responses** for MCP tools

### Logging
```python
import logging

logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Detailed debugging information")
logger.info("General information about program execution")
logger.warning("Something unexpected happened")
logger.error("An error occurred that doesn't stop execution")
logger.critical("A serious error that may stop execution")
```

## 🧪 Testing

### Unit Tests
```python
# tests/unit/test_validation.py
import pytest
from reaper_mcp.validation import TrackValidation, ValidationError

class TestTrackValidation:
    def test_validate_track_id_valid(self):
        assert TrackValidation.validate_track_id(1) == 1

    def test_validate_track_id_invalid(self):
        with pytest.raises(ValidationError):
            TrackValidation.validate_track_id(0)
```

### Integration Tests
```python
# tests/integration/test_transport_integration.py
@pytest.mark.asyncio
async def test_play_transport_integration(self, mock_mcp, mock_reaper_client):
    with patch('reaper_mcp.transport.get_reaper_client', return_value=mock_reaper_client), \
         patch('reaper_mcp.transport.ensure_connected', return_value=True):

        from reaper_mcp.transport import register_transport_tools
        register_transport_tools(mock_mcp)

        result = await mock_mcp.play_transport()
        assert result['success'] is True
```

### Running Tests
```powershell
# Run all tests
.\run_tests.ps1

# Run with coverage
.\run_tests.ps1 -Coverage

# Run specific tests
pytest tests/unit/test_validation.py -v

# Run tests in verbose mode
.\run_tests.ps1 -Verbose
```

## 📚 Documentation

### Code Documentation
- **Docstrings** for all public functions and classes
- **Type hints** for function parameters and return values
- **Comments** for complex logic
- **Examples** in docstrings where helpful

### README Updates
Update README.md when:
- Adding new features
- Changing installation process
- Modifying configuration
- Adding new dependencies

### Changelog
- Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format
- Update CHANGELOG.md with every PR
- Categorize changes: Added, Changed, Fixed, Removed

## 🔧 Tools and Technologies

### Required Tools
- **Python 3.9+** with asyncio support
- **Reaper DAW** for testing
- **PowerShell 7+** for scripts
- **Git** for version control

### Development Tools
- **Black** - Code formatting
- **isort** - Import sorting
- **Flake8** - Linting
- **MyPy** - Type checking
- **pytest** - Testing framework
- **Coverage.py** - Test coverage

### MCP Development
- **FastMCP 2.1+** - MCP server framework
- **Claude Desktop** - For testing MCP integration
- **OSC Protocol** - For Reaper communication

## 🎵 Audio Testing Guidelines

### Reaper Setup for Testing
1. **OSC Configuration**:
   - Local IP: 127.0.0.1
   - Local Port: 8000
   - Remote Port: 8001
   - Pattern Config: Default.ReaperOSC
   - Enable "Send all feedback"

2. **Test Project**:
   - Create a simple project with 2-3 tracks
   - Add some audio or MIDI content
   - Save as test project

### Testing Checklist
- [ ] OSC connection established
- [ ] Transport controls work (play, stop, pause)
- [ ] Track operations function (mute, solo, arm)
- [ ] Project operations work (save, markers)
- [ ] Error handling tested
- [ ] Edge cases covered

## 📞 Getting Help

### Communication
- **Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

### Support
- Check existing issues and documentation first
- Provide detailed reproduction steps for bugs
- Include environment information
- Test with latest version before reporting

## 🎼 Commit Message Format

We use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples
```
feat(transport): add pause transport functionality

- Add pause_transport() tool
- Update transport status tracking
- Add unit tests

Closes #123
```

```
fix(validation): handle edge case in track ID validation

Track IDs at boundary values were causing validation errors.
Added proper boundary checking with clear error messages.
```

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass locally (`.\run_tests.ps1`)
- [ ] No new linting errors (`black --check`, `flake8`)
- [ ] Type checking passes (`mypy`)
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated
- [ ] Commit messages follow conventional format
- [ ] PR description is clear and detailed
- [ ] Appropriate labels added

## 🎯 Recognition

Contributors will be:
- Listed in CHANGELOG.md for significant contributions
- Acknowledged in release notes
- Invited to join as maintainers for substantial contributions

## 📜 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

---

Thank you for contributing to **Reaper MCP Server**! Your efforts help make professional audio automation accessible to everyone. 🎵🇦🇹

*"Sin temor y sin esperanza" - Practical audio automation without hype.*
