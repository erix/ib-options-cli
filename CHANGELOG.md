# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-13

### Added
- `--min-dte` and `--max-dte` filters for days to expiration
- DTE (days to expiration) column in output table
- Examples for DTE filtering in documentation

### Changed
- Updated README with DTE filter examples
- Updated QUICKREF with DTE usage

## [1.0.0] - 2026-02-13

### Added
- Initial release
- Stock quote functionality
- Options chain queries
- Delta filters (`--min-delta`, `--max-delta`)
- Volume and OI filters (`--min-volume`, `--min-oi`)
- Moneyness filters (`--otm-only`, `--itm-only`)
- Specific expiration support (`--expiration`)
- Connection options (host, port, client-id)
- Paper and live trading support
- Comprehensive documentation
- AI assistant integration guides
- Example scripts
- MIT License

[1.1.0]: https://github.com/YOUR_USERNAME/ib-options-cli/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/YOUR_USERNAME/ib-options-cli/releases/tag/v1.0.0
