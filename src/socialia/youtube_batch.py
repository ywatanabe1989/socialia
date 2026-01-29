"""Batch YouTube video upload with YAML configuration."""

import os
from pathlib import Path
from typing import Optional

import yaml

from .youtube import YouTube


# Default video presets for common use cases
PRESETS = {
    "scitex-demo": {
        "category_id": "28",  # Science & Technology
        "privacy_status": "unlisted",
        "default_tags": [
            "scitex",
            "AI research",
            "research automation",
            "scientific computing",
            "MCP",
            "Claude AI",
        ],
    },
    "tutorial": {
        "category_id": "27",  # Education
        "privacy_status": "unlisted",
        "default_tags": ["tutorial", "how-to", "guide"],
    },
    "presentation": {
        "category_id": "28",  # Science & Technology
        "privacy_status": "unlisted",
        "default_tags": ["presentation", "conference", "talk"],
    },
}


def load_video_config(config_path: str) -> dict:
    """
    Load video upload configuration from YAML file.

    Expected YAML format:
    ```yaml
    defaults:
      category_id: "28"
      privacy_status: unlisted
      tags:
        - scitex
        - research

    videos:
      - path: /path/to/video.mp4
        title: Video Title
        description: |
          Multi-line description
          with details
        tags:
          - extra-tag
      - path: /path/to/another.mp4
        title: Another Video
    ```
    """
    with open(config_path) as f:
        return yaml.safe_load(f)


def generate_config_from_directory(
    directory: str,
    preset: str = "scitex-demo",
    output_path: Optional[str] = None,
) -> dict:
    """
    Scan directory for MP4 files and generate upload config.

    Args:
        directory: Path to directory containing MP4 files
        preset: Preset name for default settings
        output_path: Optional path to save YAML config

    Returns:
        dict with generated configuration
    """
    directory = Path(directory)
    mp4_files = sorted(directory.glob("**/*.mp4"))

    preset_config = PRESETS.get(preset, PRESETS["scitex-demo"])

    config = {
        "defaults": {
            "category_id": preset_config["category_id"],
            "privacy_status": preset_config["privacy_status"],
            "tags": preset_config["default_tags"],
        },
        "videos": [],
    }

    for mp4 in mp4_files:
        # Generate title from filename
        name = mp4.stem.replace("-", " ").replace("_", " ").title()
        config["videos"].append(
            {
                "path": str(mp4),
                "title": name,
                "description": f"Demo video: {name}",
                "tags": [],
            }
        )

    if output_path:
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    return config


class YouTubeBatch:
    """Batch upload videos to YouTube."""

    def __init__(
        self, config: Optional[dict] = None, config_path: Optional[str] = None
    ):
        """
        Initialize batch uploader.

        Args:
            config: Configuration dict
            config_path: Path to YAML config file
        """
        self.youtube = YouTube()
        self.config = config or {}
        self.results = []

        if config_path:
            self.config = load_video_config(config_path)

    @property
    def defaults(self) -> dict:
        """Get default settings from config."""
        return self.config.get("defaults", {})

    @property
    def videos(self) -> list:
        """Get video list from config."""
        return self.config.get("videos", [])

    def validate(self) -> dict:
        """
        Validate configuration and credentials.

        Returns:
            dict with 'valid' bool and 'errors' list
        """
        errors = []

        # Check credentials
        if not self.youtube.validate_credentials():
            errors.append("YouTube credentials not configured")

        # Check videos
        if not self.videos:
            errors.append("No videos configured")

        for i, video in enumerate(self.videos):
            path = video.get("path")
            if not path:
                errors.append(f"Video {i + 1}: missing 'path'")
            elif not os.path.exists(path):
                errors.append(f"Video {i + 1}: file not found: {path}")

            if not video.get("title"):
                errors.append(f"Video {i + 1}: missing 'title'")

        return {"valid": len(errors) == 0, "errors": errors}

    def upload_one(self, video_config: dict, dry_run: bool = False) -> dict:
        """
        Upload a single video.

        Args:
            video_config: Video configuration dict
            dry_run: If True, don't actually upload

        Returns:
            Upload result dict
        """
        path = video_config["path"]
        title = video_config.get("title", Path(path).stem)
        description = video_config.get("description", "")

        # Merge tags: defaults + video-specific
        tags = list(self.defaults.get("tags", []))
        tags.extend(video_config.get("tags", []))
        tags = list(dict.fromkeys(tags))  # Remove duplicates, preserve order

        category_id = video_config.get(
            "category_id", self.defaults.get("category_id", "28")
        )
        privacy = video_config.get(
            "privacy_status", self.defaults.get("privacy_status", "unlisted")
        )
        thumbnail = video_config.get("thumbnail")

        if dry_run:
            return {
                "success": True,
                "dry_run": True,
                "path": path,
                "title": title,
                "description": description[:100] + "..."
                if len(description) > 100
                else description,
                "tags": tags,
                "category_id": category_id,
                "privacy_status": privacy,
            }

        result = self.youtube.post(
            text=description,
            video_path=path,
            title=title,
            tags=tags,
            category_id=category_id,
            privacy_status=privacy,
            thumbnail_path=thumbnail,
        )

        result["path"] = path
        result["title"] = title
        return result

    def upload_all(
        self,
        dry_run: bool = False,
        callback=None,
        stop_on_error: bool = False,
    ) -> list:
        """
        Upload all videos in configuration.

        Args:
            dry_run: If True, don't actually upload
            callback: Optional callback(index, total, result) called after each upload
            stop_on_error: If True, stop on first error

        Returns:
            List of upload results
        """
        self.results = []
        total = len(self.videos)

        for i, video in enumerate(self.videos):
            result = self.upload_one(video, dry_run=dry_run)
            result["index"] = i + 1
            self.results.append(result)

            if callback:
                callback(i + 1, total, result)

            if stop_on_error and not result.get("success"):
                break

        return self.results

    def summary(self) -> dict:
        """
        Get upload summary.

        Returns:
            dict with success/failed counts and details
        """
        successful = [r for r in self.results if r.get("success")]
        failed = [r for r in self.results if not r.get("success")]

        return {
            "total": len(self.results),
            "successful": len(successful),
            "failed": len(failed),
            "urls": [r.get("url") for r in successful if r.get("url")],
            "errors": [
                {"title": r.get("title"), "error": r.get("error")} for r in failed
            ],
        }


def create_scitex_config(
    video_dir: str = "/home/ywatanabe/proj/scitex-cloud/media/videos",
    output_path: Optional[str] = None,
) -> dict:
    """
    Create upload configuration for SciTeX demo videos.

    Args:
        video_dir: Directory containing demo videos
        output_path: Optional path to save YAML config

    Returns:
        Configuration dict
    """
    # Standard footer for all videos
    CROSS_REFERENCES = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔬 SciTeX Demo Series
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

▶ Automated Research Demo (40 min) - Full AI-driven research workflow
▶ CrossRef Local Demo - 167M+ papers local database
▶ FigRecipe Demo - Publication-ready figures
▶ SciTeX Writer Demo - LaTeX manuscript compilation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Resources
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 Website: https://scitex.ai
📺 All Demos: https://scitex.ai/demos/
💻 GitHub: https://github.com/ywatanabe1989/scitex
📖 Documentation: https://scitex.ai/docs/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ Tags
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#SciTeX #AI #Research #Automation #Science #MCP #ClaudeAI #Python
#MachineLearning #DataScience #AcademicWriting #ScientificComputing
"""

    videos_meta = {
        "scitex-automated-research-demo.mp4": {
            "title": "SciTeX: Automated Research by AI Agent | 40-min Full Demo",
            "description": f"""🤖 AI agent conducting a COMPLETE research workflow with minimal human intervention.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This demo showcases an AI agent leveraging the SciTeX MCP (Model Context Protocol) server to execute an entire research pipeline autonomously.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ What the AI Agent Does
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Literature discovery and retrieval
📊 Data analysis (3×3 factorial design, N=180)
📈 Statistical testing (ANOVA + post-hoc comparisons)
🎨 Generation of 4 publication-ready figures
📝 Creation of a 21-page manuscript
✍️ Peer review response preparation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️ Duration: 40 minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{CROSS_REFERENCES}""",
            "tags": [
                "automated research",
                "AI agent",
                "manuscript generation",
                "full demo",
            ],
            "priority": 1,
        },
        "crossref-local-v0.3.1-demo.mp4": {
            "title": "CrossRef Local v0.3.1 | 167M+ Academic Papers Database Demo",
            "description": f"""📚 Local database with 167M+ academic papers for lightning-fast literature search.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CrossRef Local brings the entire CrossRef database to your local machine, enabling instant full-text search across 167M+ academic papers without API rate limits.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Features
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Full-text search across paper metadata
🔗 Fast DOI lookup and resolution
📊 Citation count enrichment
💾 Local caching for offline use
⚡ No API rate limits

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💻 GitHub: https://github.com/ywatanabe1989/crossref-local
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{CROSS_REFERENCES}""",
            "tags": [
                "crossref",
                "literature database",
                "doi lookup",
                "academic search",
            ],
            "priority": 2,
        },
        "figrecipe-v0.14.0-demo.mp4": {
            "title": "FigRecipe v0.14.0 | Publication-Ready Scientific Figures Demo",
            "description": f"""🎨 Create publication-ready scientific figures with automatic data export.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FigRecipe is a declarative figure generation library that creates publication-quality plots while automatically exporting the underlying data for reproducibility.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Features
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📐 Declarative figure specification
📁 Automatic CSV export for reproducibility
📊 20+ plot types supported
🎭 Publication-ready styling
🔧 Matplotlib-based, highly customizable

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💻 GitHub: https://github.com/ywatanabe1989/figrecipe
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{CROSS_REFERENCES}""",
            "tags": [
                "data visualization",
                "matplotlib",
                "publication figures",
                "reproducibility",
            ],
            "priority": 3,
        },
        "scitex-writer-v2.2.0-demo.mp4": {
            "title": "SciTeX Writer v2.2.0 | LaTeX Manuscript Compilation Demo",
            "description": f"""📝 Automated LaTeX manuscript compilation with figure and bibliography management.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SciTeX Writer automates the entire manuscript compilation process, from organizing figures and tables to managing bibliographies and generating multiple output formats.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Features
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Automatic figure and table management
📚 BibTeX bibliography integration
📄 Multiple output formats (PDF, DOCX)
📋 Journal template support
🔄 Revision tracking and diff generation
✍️ Peer review response automation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{CROSS_REFERENCES}""",
            "tags": ["latex", "manuscript", "academic writing", "bibliography"],
            "priority": 4,
        },
    }

    config = {
        "defaults": {
            "category_id": "28",  # Science & Technology
            "privacy_status": "unlisted",
            "tags": [
                "scitex",
                "AI research",
                "research automation",
                "scientific computing",
                "MCP",
                "Model Context Protocol",
                "Claude AI",
                "python",
            ],
        },
        "videos": [],
    }

    video_dir = Path(video_dir)

    # Add videos with metadata, sorted by priority
    for filename, meta in sorted(
        videos_meta.items(), key=lambda x: x[1].get("priority", 99)
    ):
        path = video_dir / filename
        if path.exists():
            config["videos"].append(
                {
                    "path": str(path),
                    "title": meta["title"],
                    "description": meta["description"],
                    "tags": meta["tags"],
                }
            )

    if output_path:
        with open(output_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    return config
