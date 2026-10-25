# USER SCANNER — 20 Platform Username Availability Checker

> **Professional, high-performance OSINT username intelligence and availability checker built in Python with a modern cyberpunk / dark hacker-style CustomTkinter GUI.**

---

## ⚡ Overview

**USER SCANNER** allows security researchers, developers, brand creators, and OSINT investigators to instantly verify whether a given username handle is registered or available across the **top 20 social, developer, media, and creator platforms**.

Designed with ethical guidelines at its core, the tool uses official public APIs and safe HTTP inspection methods with strict anti-false-positive algorithms. It never guesses availability when verification is blocked by rate-limits or bot-walls, ensuring 100% reliable intelligence.

---

## 🚀 The 20 Monitored Platforms

| # | Platform | Category | Inspection Route / Strategy |
|---|---|---|---|
| 1 | **Instagram** | Social / Photo | Web profile metadata inspection + login gate detection |
| 2 | **GitHub** | Developer | Official REST API (`/users/{username}`) + rate-limit tracking |
| 3 | **Twitter / X** | Social / Microblog | Public handle route + suspended account detection |
| 4 | **Snapchat** | Social / Messaging | Public `add/{username}` route presence |
| 5 | **YouTube** | Video / Media | Official handle route (`/@{username}`) |
| 6 | **Facebook** | Social Network | Mobile route inspection + login-wall detection |
| 7 | **Telegram** | Messaging | Public `t.me/{username}` channel/user inspection |
| 8 | **Pinterest** | Social / Visual | Public user profile status |
| 9 | **Reddit** | Social / Forum | JSON API (`/user/{username}/about.json`) + bot-wall handling |
| 10 | **TikTok** | Social / Video | Public `@handle` inspection + geo-block detection |
| 11 | **LinkedIn** | Professional | Vanity profile route + HTTP 999 anti-bot detection |
| 12 | **Twitch** | Streaming | Public channel route verification |
| 13 | **Medium** | Publishing | Public author handle verification (`/@{username}`) |
| 14 | **SoundCloud** | Music / Audio | Public artist / profile route |
| 15 | **Dev.to** | Developer | Official Dev.to REST API (`/api/users/by_username`) |
| 16 | **GitLab** | Developer | Public profile route |
| 17 | **Spotify** | Music / Audio | Public user profile route |
| 18 | **Vimeo** | Video / Media | Public video channel inspection |
| 19 | **Patreon** | Creator | Creator page presence verification |
| 20 | **Dribbble** | Design | Designer portfolio verification |

---

## 🛡️ Anti-False-Positive Assurance

1. **Strict Non-Ambiguity**:
   When platforms (e.g. Facebook, Reddit, Medium, TikTok) return 403, 429, Cloudflare challenges, or require login credentials, the status is reported as **`COULD NOT VERIFY`** with the diagnostic reason. The application **never** claims a username is available when the response cannot be confirmed.
2. **Pre-Flight Syntax Validation**:
   Checks username constraints locally before sending requests:
   - Eliminates useless network traffic.
   - Accurately reports why a handle cannot exist on a specific platform (e.g. GitHub disallows underscores; X disallows >15 characters; Snapchat must start with a letter).
3. **No Private Scraping**:
   - Uses only public endpoints.
   - Never requests passwords, session tokens, or private user data.
   - Does not attempt CAPTCHA bypassing.

---

## 💻 Installation & Setup on Windows

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.10, 3.11, 3.12, 3.13).
- Verify Python and pip in PowerShell:
  ```powershell
  python --version
  pip --version
  ```

### 2. Navigate to the Project
```powershell
cd "C:\Users\ACER\.gemini\antigravity\scratch\user_scanner"
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 🎮 Running the Program

### Launch the GUI
```powershell
python main.py
```

### Run in CLI / Headless Mode
```powershell
# Quick terminal scan
python main.py -u cyber_ninja

# Scan and export directly to CSV
python main.py -u alex -o alex_scan.csv
```

### Run Automated Tests
```powershell
python test_scanner.py
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Enter` | Trigger scan for the current target in the search bar |
| `Ctrl + C` | Copy formatted intelligence report to clipboard |
| `Ctrl + E` | Open file dialog to export results to CSV |
