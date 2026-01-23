# Socialia MCP Server Instructions

Social media automation with platform-specific content strategies.

## PLATFORM CONTENT STRATEGIES

When composing posts, follow these platform-specific strategies for maximum engagement:

### Twitter/X (280 chars)
- **Hook first**: Lead with curiosity, controversy, or value (NOT announcements)
- **Format**: Short sentences. Line breaks. Visual hierarchy.
- **Emoji**: At least 1 per tweet for visual appeal (🔧 🚀 ✨ 💡 🎯)
- **Links**: ALWAYS include GitHub/project URL for discoverability
- **Hashtags**: 3-5 for SEO, ALWAYS at the end, never mid-sentence
  - Mix broad + specific: #Python #OpenSource #DevTools #CLI #Automation
  - More hashtags = better discoverability on Twitter/X
- **Avoid**: "Just released", "Check out", "New version" - boring intros

```
BAD:  "SciTeX v2.15.0 released! New audio relay for remote AI agents. pip install scitex[audio] #Python #AI"

GOOD: "Your AI agent on a remote server can now speak to you locally.

Audio relay in SciTeX bridges the gap.

github.com/ywatanabe1989/scitex

#AIAgents #Python"
```

**Templates:**
- Problem → Solution: "Tired of X? Now you can Y. #hashtag"
- Curiosity gap: "The one thing most developers miss about X... #hashtag"
- Counter-intuitive: "Why X is actually better than Y #hashtag"
- Tutorial teaser: "How to X in 3 steps (thread): #hashtag"

### LinkedIn (3,000 chars)
- **Hook**: First 2 lines visible before "see more" - make them count
- **Format**: Short paragraphs (1-2 sentences). Lots of whitespace.
- **Tone**: Professional but human. Share learnings, not announcements.
- **Hashtags**: 3-5 at the very end. Use industry terms.
  - #ArtificialIntelligence #MachineLearning #SoftwareDevelopment #OpenSource #TechInnovation
- **CTA**: Ask a question or invite discussion at the end

```
BAD:  "Excited to announce SciTeX v2.15.0 with new audio features!"

GOOD: "Remote AI development has a UX problem.

When your agent runs on a server, you lose audio feedback entirely.

We solved this with audio relay - your remote agent speaks to your local machine.

Here's what we learned building it:
• Challenge 1...
• Challenge 2...

What's the biggest UX gap you face with remote AI tools?

#ArtificialIntelligence #RemoteDevelopment #Python #OpenSource"
```

### Reddit
- **Title is everything**: Descriptive, specific, follows subreddit culture
- **Body**: Provide value first. Self-promotion last (10:1 rule).
- **Tone**: Authentic, not corporate. Redditors detect marketing.
- **Hashtags**: NOT used on Reddit
- **Subreddit rules**: Check sidebar before posting

```
BAD Title:  "Check out my new Python package!"
GOOD Title: "I built a Python tool that lets remote AI agents play audio on your local machine"
```

### YouTube
- **Title**: Keyword-rich, curiosity-driven, under 60 chars ideal
- **Description**: First 2 lines matter (shown in search). Keywords naturally.
- **Tags**: Relevant, mix of broad and specific
- **Hashtags**: 3-5 in description, helps discoverability

## MCP Tools

- `social_post`: Post to twitter/linkedin/reddit/youtube
- `social_delete`: Delete a post
- `analytics_track`: Track events in Google Analytics
- `analytics_pageviews`: Get page view metrics
- `analytics_sources`: Get traffic sources
- `analytics_realtime`: Get realtime active users

## CLI Equivalents

All MCP tools map to CLI commands:
```bash
socialia post twitter "content"
socialia post linkedin "content"
socialia delete twitter <post_id>
socialia analytics track <event>
```
