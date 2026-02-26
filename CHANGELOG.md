# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Beat Selection Service (random 3-5 beats, 30-day duplicate prevention)
- Email Template Service (placeholder replacement)
- Gmail Service (send with attachments, rate limiting)
- Full CLI: list-artists, send-beats (with --dry-run), show-history
- Unit tests for beat selection and email template (33 tests total)
- Database schema documentation (docs/DATABASE_SCHEMA.md)

### Changed
- main.py: full send-beats workflow (fetch artists/beats, select, email, log)
- README: project status 100% complete

### Fixed
- database_service.py: context manager __enter__/__exit__ syntax

### Security

## [0.1.0] - 2025-01-XX

### Added
- Initial project setup
- Google Cloud OAuth integration
- Basic CLI structure
- Documentation (README, setup guides, system design)

[Unreleased]: https://github.com/zohayb23/ContactAutomation/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/zohayb23/ContactAutomation/releases/tag/v0.1.0
