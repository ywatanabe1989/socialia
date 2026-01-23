# Template Project

Example structure for organizing social media content with Socialia.

## Structure

```
projects/template-project/
├── README.md           # This file
├── drafts/             # Work in progress
│   └── example.org     # Org mode draft file
├── scheduled/          # Ready, waiting for posting time
├── posted/             # Published posts (archive)
└── threads/            # Thread content files
```

## Workflow

### 1. Create drafts in org mode

```bash
socialia org init drafts/my-campaign.org --platform twitter
```

Edit the file with your content, set SCHEDULED timestamps.

### 2. Check draft status

```bash
socialia org status drafts/my-campaign.org
```

### 3. Schedule posts (auto-moves to scheduled/)

```bash
# Schedule with human-like timing fluctuation (±15 min)
socialia org schedule drafts/my-campaign.org --fluctuation 15
```

File automatically moves: `drafts/` → `scheduled/`

### 4. View scheduled posts

```bash
socialia schedule list           # Pending only
socialia schedule list --full    # All including history
```

### 5. Run scheduler daemon

```bash
socialia schedule daemon --interval 60
```

When posted, files move: `scheduled/` → `posted/`

## Quick Commands

```bash
# Post directly
socialia post twitter "Hello world!"

# Post from file
socialia post twitter "$(cat drafts/my-post.md)"

# Dry run
socialia post twitter "Test" --dry-run

# Cancel scheduled post
socialia schedule cancel <job-id>

# Sync org file with scheduler
socialia org sync drafts/my-campaign.org
```

## Creating Your Own Project

```bash
cp -r projects/template-project projects/myproject
```
