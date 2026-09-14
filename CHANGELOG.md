# Changelog

All notable changes to the sentibank project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- Python 3.10 or later is required: spaCy, a core dependency, no longer supports Python 3.9.
- CI installs the package from its pyproject ranges and tests Python 3.10 to 3.13.

## [1.1.1] - 2026-09-15

### Documentation
- README and documentation restyled to the socius conventions (hero and banner images, badge row, no emoji); documentation language kept plain.
- SO-CAL page removed from the documentation and the README table (the dictionary itself remains available in the package as `SO-CAL_v2011`).
- Documentation is now built and published automatically by a GitHub Actions workflow (`.github/workflows/docs.yml`).
- Corrected the 1.0.0 and 1.1.0 release dates and refreshed citation metadata.
- Fixed README typos and the dictionary identifier used in the label-based example.

## [1.1.0] - 2025-08-28

### Fixed
- **GitHub Actions Workflow**: Fixed PyPI publishing workflow trigger timing issue
- **Release Process**: Ensured proper workflow execution on release publication

### Improved
- **CI/CD Pipeline**: Added manual workflow dispatch option for flexible publishing
- **Release Management**: Streamlined version management across all configuration files

### Documentation
- **Version Alignment**: Synchronized version numbers across pyproject.toml, setup.py, and __init__.py

## [1.0.0] - 2025-08-27

### Added
- **Major Refactoring**: Complete overhaul of the codebase for improved maintainability
- **Type Hints**: Full type annotations throughout the codebase for better IDE support
- **Error Handling**: Comprehensive exception handling for file operations and data loading
- **Caching System**: Built-in caching mechanism for loaded dictionaries to improve performance
- **Logging Infrastructure**: Structured logging with configurable levels and output
- **CLI Interface**: Command-line tool with `list`, `analyze`, `info`, and `export` commands
- **Modern Packaging**: Migration to pyproject.toml with proper metadata and dependencies
- **Test Suite**: Comprehensive pytest-based testing infrastructure with fixtures and mocking
- **CI/CD Pipeline**: GitHub Actions workflows for testing, linting, and publishing
- **Examples**: Complete examples directory with usage demonstrations
- **Documentation**: Enhanced docstrings and type information

### Changed
- **BREAKING**: Refactored `load` class with new method signatures and return types
- **Architecture**: Centralized lexicon path mappings to eliminate code duplication
- **File Handling**: Migration from `os.path` to `pathlib.Path` for better path handling
- **Version Sync**: Synchronized version numbers between setup.py and __init__.py

### Fixed
- **Code Duplication**: Eliminated repeated lexicon_paths dictionaries in archive.py
- **Version Mismatch**: Fixed inconsistent version numbers across package files
- **Incomplete Methods**: Properly implemented the benchmark() method with clear documentation
- **gitignore Issues**: Resolved conflicts with test.py tracking

### Documentation
- **CLAUDE.md**: Added comprehensive guide for future development
- **Examples**: Created practical usage examples for common scenarios
- **Type Stubs**: Added type information for better IDE integration
- **CLI Help**: Comprehensive help text and usage examples

### Infrastructure
- **GitHub Actions**: Automated testing on multiple Python versions and operating systems
- **Code Quality**: Added black, isort, flake8, and mypy configuration
- **Testing**: pytest configuration with coverage reporting
- **Publishing**: Automated PyPI publishing workflow

### Breaking Changes
- Method signatures in `load` class now include type hints
- Error handling may raise different exception types
- Some internal APIs have been refactored

### Migration Guide
For users upgrading from previous versions:
1. Update import statements if using internal APIs
2. Handle new exception types in error handling code
3. Review CLI usage if using command-line features

## [0.2.4] - Previous Release
### Added
- Initial release with basic dictionary loading functionality
- Support for multiple sentiment lexicons
- Basic sentiment analysis utilities

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/) format.
For the full list of changes, see the [GitHub releases](https://github.com/socius-org/sentibank/releases).