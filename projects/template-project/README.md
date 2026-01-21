# Template Project

Example structure for organizing social media content with Socialia.

## Structure

```
projects/template-project/
├── README.md           # This file
├── drafts/             # Posts in progress
├── posted/             # Published posts (archive)
└── threads/            # Thread content files
```

## Usage

```bash
# Post from file
socialia post twitter "$(cat drafts/my-post.md)"

# Post a thread (separate posts with ---)
socialia thread twitter --file threads/my-thread.txt

# Dry run first
socialia post twitter "Test" --dry-run
```

## Creating Your Own Project

```bash
cp -r projects/template-project projects/myproject
```

Add to `.gitignore` exceptions to track your project:

```gitignore
projects/*
!projects/template-project/
!projects/myproject/
```
