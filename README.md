# CTFile Downloader

Download files from [Ctfile](https://www.ctfile.com) share links — directly, from source pages, or in batch from text files. CTFileDownloader is a Python package that allows users to download files from CTFile using URLs or batch processing. It is designed for efficient file downloading, handling both individual and batch URL inputs. If you find it useful, please consider starring the repository on GitHub to support the project!

Two editions:

| Edition | Script / EXE | Account | Speed |
|---------|--------------|---------|-------|
| **Free** | `ctfile_free.py` | None (public shares) | Standard guest download |
| **Pro** | `ctfile_pro.py` | VIP + browser cookies | VIP mirror URLs |


---

## Download (EXE)

Pre-built Windows executables are on the [Releases](https://github.com/SSujitX/ctfile-downloader/releases) page.

1. Download **CTFile Downloader Free.exe** and/or **CTFile Downloader Pro.exe**
2. Place the `.exe` in a folder of your choice
3. Run it — folders are created automatically next to the exe

> **Pro only:** copy `_ctfiledata/` with your `creds.json` and `cookies.json` next to the exe.

---

## Install (Python)

Requires **Python 3.13+** (see `pyproject.toml`).

### Option A — uv (recommended)

```bash
git clone https://github.com/SSujitX/ctfile-downloader.git
cd ctfile-downloader

uv sync
```

Run:

```bash
uv run python ctfile_free.py
uv run python ctfile_pro.py
```

### Option B — pip

```bash
git clone https://github.com/SSujitX/ctfile-downloader.git
cd ctfile-downloader

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -e .
```

Or install dependencies only:

```bash
pip install cloudscraper rich tqdm
```

Run:

```bash
python ctfile_free.py
python ctfile_pro.py
```

---

## Quick start

```
>>-- ENTER LINK:
```

| What you enter | What happens |
|----------------|--------------|
| **CTFile URL** | Downloads that file |
| **Source page URL** (e.g. LookAE) | Finds ctfile links on the page and downloads |
| **Comma-separated URLs** | Downloads each link in order |
| **Press Enter** (empty) | Batch mode — reads all `.txt` files in `CTFile Batch Text/` |

### Example URLs

**Direct CTFile link (with passcode):**

```
https://url62.ctfile.com/f/680462-17569802098418-e57278?p=6688
```

**Source page (ctfile link extracted automatically):**

```
https://www.lookae.com/warping-wheels-300/
```

**Multiple links:**

```
https://www.lookae.com/samurai-132/,
https://www.lookae.com/warping-wheels-300/
```

Invalid input (e.g. `234`) is rejected and the prompt appears again. Empty batch folder also loops back instead of exiting.

---

## Use cases

1. **Single file** — paste a ctfile share URL with `?p=passcode`
2. **LookAE / blog posts** — paste the article URL; the tool regex-scans HTML for ctfile links
3. **Batch overnight** — put one URL per line in `CTFile Batch Text/links.txt`, run the app, press Enter
4. **VIP speed (Pro)** — use browser session cookies for fast VIP mirror downloads
5. **Portable workflow** — build or download the `.exe`, keep batch txt files alongside it

---

## Folder structure

```
ctfile-downloader/
├── ctfile.ico                  # App icon (used by PyInstaller)
├── ctfile_free.py              # Free edition (guest download)
├── ctfile_pro.py               # Pro edition (VIP + cookies)
├── ctfile_test.py              # Dev / API experiments (not for end users)
├── exe.txt                     # PyInstaller build commands
├── pyproject.toml
├── uv.lock
│
├── CTFile Batch Text/          # Batch mode: .txt files, one URL per line
│   └── links.txt               # (example — you create this)
│
├── CTFile Downloaded/          # Finished downloads land here
│
└── _ctfiledata/                # Pro only — not committed to git
    ├── creds.json              # Your login (you create this)
    └── cookies.json            # Browser cookies (you create this)
```

| Folder / file | Created by | Purpose |
|---------------|------------|---------|
| `CTFile Batch Text/` | App on first run | Batch input `.txt` files |
| `CTFile Downloaded/` | App on first run | Saved files |
| `_ctfiledata/` | App on first run (Pro) | Credentials and session cookies |
| `ctfile.ico` | Included in repo | Windows exe icon |
| `dist/` | PyInstaller | Built executables (after build) |

---

## Pro setup (credentials + cookies)

Pro needs a VIP Ctfile account and a valid browser session.

### 1. `creds.json`

Create creds.json file inside _ctfiledata:

```bash
_ctfiledata\creds.json
```

```json
{
    "email": "your_email@example.com",
    "password": "your_password"
}
```

### 2. `cookies.json`

After logging in at [ctfile.com](https://www.ctfile.com), export cookies with a browser extension such as [Cookie Selector](https://chromewebstore.google.com/detail/cookie-selector/klmnplbabblfkhlganacalkafdbhchne).

```bash
_ctfiledata\cookies.json
```

Required keys:

```json
{
    "ua_checkmutilogin": "",
    "ctfile_session_pref": "",
    "ctfile_session": "",
    "ct_uid": ""
}
```

> Cookies expire. If Pro downloads fail with auth errors, log in again in the browser and re-export `cookies.json`.

> Pro requires `?p=passcode` in the ctfile URL. Free accepts shares with or without a passcode.

---

## Batch mode

1. Create `CTFile Batch Text/links.txt`
2. Add one URL per line (source pages or direct ctfile links)
3. Run the app and press **Enter** at the prompt
4. Each line is processed in order; failures are reported at the end

Example `links.txt`:

```
https://www.lookae.com/samurai-132/
https://url62.ctfile.com/f/680462-17569802098418-e57278?p=6688
https://www.lookae.com/warping-wheels-300/
```

---

## Build EXE (Windows)

`ctfile.ico` is confirmed in the project root and is used as the Windows executable icon.

Install PyInstaller (included in project deps):

```bash
uv sync
# or: pip install pyinstaller
```

Build both editions (commands from `exe.txt`):

```bash
pyinstaller --onefile --console --name "CTFile Downloader Pro" --icon "ctfile.ico" ctfile_pro.py
```

```bash
pyinstaller --onefile --console --name "CTFile Downloader Free" --icon "ctfile.ico" ctfile_free.py
```

Output:

```
dist/CTFile Downloader Pro.exe
dist/CTFile Downloader Free.exe
```

Use `--console` so `input()` works when the app prompts for a link. Do **not** use `--noconsole`.

For a release package, copy to a zip:

- The `.exe`(s)
- `CTFile Batch Text/` (can be empty)
- For Pro: include an empty `_ctfiledata/` folder (users add their own `creds.json` / `cookies.json`)

---

## How it works

### Free

```
Share URL → getfile.php → get_down_url.php → download (no login)
```

### Pro

```
Share URL → webapi getfile (cookies) → VIP mirrors (lt / dx / yd / us / cdn) → download
```

Pro tries mirrors in order until one succeeds.

---

## Limitations

- Link extraction uses regex on page HTML — JavaScript-rendered links may be missed
- Source pages with **multiple** ctfile links: the first matching link is used per URL
- Pro depends on **fresh cookies** from a logged-in browser session
- Ctfile rate limits and wait timers apply to guest (Free) downloads
- Windows-focused for `.exe` builds; Python scripts run on any OS with Python 3.13+

---

## Releases

| Resource | Link |
|----------|------|
| Latest release | [github.com/SSujitX/ctfile-downloader/releases/latest](https://github.com/SSujitX/ctfile-downloader/releases/latest) |
| Source code | [github.com/SSujitX/ctfile-downloader](https://github.com/SSujitX/ctfile-downloader) |
| Report issues | [github.com/SSujitX/ctfile-downloader/issues](https://github.com/SSujitX/ctfile-downloader/issues) |

---

## Disclaimer

CTFileDownloader is not for sale or for distribution. It is a tool to help users download files from CTFile.

The developer is not responsible for any misuse of this tool. Please ensure you comply with CTFile's terms of service when using the downloader.

## Star History

[![Star History Chart](https://api.star-history.com/chart?repos=SSujitX/ctfile-downloader&type=date&legend=top-left)](https://www.star-history.com/?repos=SSujitX%2Fctfile-downloader&type=date&legend=top-left)

![](https://api.visitorbadge.io/api/VisitorHit?user=SSujitX&repo=ctfile-downloader&countColor=%237B1E7A)