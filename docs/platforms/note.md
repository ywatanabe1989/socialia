# Note.com (Japan) API Automation

## Status: Unofficial Only - Complex

## Overview

Note.com is a popular Japanese blogging platform (40M+ MAU). There is **no official API** - only unofficial endpoints discovered through reverse engineering.

## Platform Info

- Launched: 2014 in Japan
- Users: 40.66 million MAU (2022)
- Content: Text, images, audio, video
- Enterprise: "note pro" (¥50,000/month)

## Unofficial API Access

### Authentication

Note.com uses cookie-based authentication. You need to:
1. Log in via browser/Selenium
2. Extract session cookies
3. Use cookies for API requests

### Method 1: Selenium Login

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import time

# Login with Selenium
driver = webdriver.Chrome()
driver.get("https://note.com/login")

# Fill login form
driver.find_element(By.NAME, "login").send_keys("your_email")
driver.find_element(By.NAME, "password").send_keys("your_password")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

time.sleep(3)  # Wait for login

# Extract cookies
cookies = {c['name']: c['value'] for c in driver.get_cookies()}
driver.quit()

# Use cookies for API requests
session = requests.Session()
session.cookies.update(cookies)
```

### Method 2: Manual Cookie Extraction

1. Log in to note.com in browser
2. Open DevTools (F12) → Application → Cookies
3. Copy relevant cookies (`_note_session`, etc.)

## API Endpoints (Unofficial)

```python
BASE_URL = "https://note.com/api"

# Get user info
GET /v1/users/{username}

# Create draft (requires HTML body)
POST /v3/notes

# Upload image
POST /v1/photos
```

## Creating a Post (Draft)

```python
import requests

headers = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

# Note: Body must be HTML, not Markdown
post_data = {
    "note": {
        "name": "記事のタイトル",  # Title
        "body": "<p>記事の本文</p>",  # Body in HTML
        "status": "draft",  # draft or published
        "type": "TextNote"
    }
}

response = session.post(
    "https://note.com/api/v3/notes",
    headers=headers,
    json=post_data
)
```

## Warnings

1. **Unofficial API may change** without notice
2. **Don't overload servers** - be respectful
3. **Terms of Service** - may violate ToS
4. **Account risk** - potential ban

## Alternative: note pro

For corporate use, "note pro" (¥50,000/month) includes:
- Scheduled posting
- Comment management
- Custom design
- Support services

## Recommended Approach

1. **Manual posting** for important content
2. **Draft automation** only (review before publish)
3. **Consider note pro** for business needs
4. **Use other platforms** for automation priority

## Japanese Resources

- [非公式API解説](https://note.com/taku_sid/n/n1b1b7894e28f) - Detailed API guide
- [API一覧 2023](https://note.com/ego_station/n/n85fcb635c0a9) - Endpoint list

## Environment Variables

```bash
NOTE_EMAIL=
NOTE_PASSWORD=
# Or
NOTE_SESSION_COOKIE=
```

## Sources

- [Note Platform Guide](https://www.ulpa.jp/post/note-the-japanese-blogging-platform-a-complete-guide)
- [Note for Companies](https://tamkox.com/insights/japanese-blog-platform-note)
