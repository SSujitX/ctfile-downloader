# Changelog

All notable changes to CTFile Downloader are documented here.

## [2.0.0] - 2026-06-06

### Added

- **Free edition** (`ctfile_free.py` / `CTFile Downloader Free.exe`) — guest downloads, no account
- **Pro edition** (`ctfile_pro.py` / `CTFile Downloader Pro.exe`) — VIP mirrors with cookie auth
- Source page URL support — paste blog/article links (e.g. LookAE); ctfile links are extracted automatically
- Comma-separated multi-URL input
- Batch mode via `CTFile Batch Text/` `.txt` files
- Auto-created folders: `CTFile Batch Text/`, `CTFile Downloaded/`, `_ctfiledata/` (Pro)
- Pro mirror failover across VIP mirrors (lt / dx / yd / us / cdn)
- Download progress bars (`tqdm`) and rich console output
- `pyproject.toml` + `uv.lock` for dependency management

### Changed

- Rewritten from package layout to standalone scripts
- Replaced `config.yml` with `_ctfiledata/creds.json` + `cookies.json` (Pro)
- Switched from `requests` to `cloudscraper`
- Python requirement: **3.13+**
- Two separate Windows EXEs instead of one

### Removed

- `ctfiledownloader.py` and `ctfile_downloader/` package
- `config.yml` setup flow

### Breaking changes

| v1.x | v2.0.0 |
|------|--------|
| Single Pro-only app | Free + Pro editions |
| `config.yml` credentials | `_ctfiledata/creds.json` + `cookies.json` |
| Direct CTFile links only | Source pages + comma-separated URLs |
| One EXE | `CTFile Downloader Free.exe` + `CTFile Downloader Pro.exe` |

---

## [1.0.0]

- Initial release
- Download files from CTFile via URL or batch `.txt` files
- VIP mirror support (Telecom / Unicom)
- `config.yml` for premium account credentials
- Single Windows EXE build
