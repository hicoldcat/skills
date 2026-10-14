# Agent Skills 🧰

English | [中文](README.zh-CN.md)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Built for Agents](https://img.shields.io/badge/Built%20for-AI%20Agents-blue)
![Maintained](https://img.shields.io/badge/Maintained-yes-success)
![GitHub stars](https://img.shields.io/github/stars/hicoldcat/skills?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/hicoldcat/skills)

A collection of skills for AI coding agents.

> 🚀 Open source, practical, and easy to extend.

## Available Skills ✨

### random-image-placeholder

Generate stable or random image placeholder URLs (and optionally download them) using [Lorem Picsum](https://picsum.photos/).

**Use when:**

- Building UI mockups / docs / demos that need images without hosting assets
- You need reproducible images for tests/snapshots (use `seed`)
- The user mentions picsum, placeholder images, grayscale, blur, seed, id

**Examples:**

```bash
python skills/random-image-placeholder/scripts/picsum.py url --seed avatar-42 --width 400 --height 400 --grayscale --blur 2
```

```bash
python skills/random-image-placeholder/scripts/picsum.py download --seed avatar-42 --width 120 --height 80 --out ./tmp/picsum_test.jpg
```

Docs:

- `skills/random-image-placeholder/README.md`
- `skills/random-image-placeholder/SKILL.md`

### kids-ancient-humans-video-proposal

Generate a complete **10-topic kids' science short-video proposal** for the Ancient Humans theme — bilingual titles, an English voiceover plus Chinese translation (65–80 words is a **guideline, not a hard limit**), social posts and hashtags for Douyin / Xiaohongshu / X / YouTube Shorts, and a one-line child-appeal rationale per topic. Output is a Markdown file that must pass a bundled validator before delivery. The theme and its bilingual keywords are parameters, so the same workflow works for other science topics.

**Use when:**

- The user wants 儿童科普短视频 topics/scripts or 中英双语旁白脚本 (bilingual voiceover scripts)
- You need 抖音 / 小红书 / YouTube Shorts / X social copy and hashtags
- The topic is 古代人类 / Ancient Humans for a kids' science channel
- The user asks for "10 video topics" with bilingual voiceover scripts

**Examples:**

```bash
python skills/kids-ancient-humans-video-proposal/scripts/validate_script_doc.py "古代人类-20261014213045.md" --zh-keyword 古代人类 --en-keyword "Ancient Humans"
```

```bash
python skills/kids-ancient-humans-video-proposal/scripts/validate_script_doc.py "海洋生物-20261014213045.md" --zh-keyword 海洋生物 --en-keyword "Ocean Animals"
```

Docs:

- `skills/kids-ancient-humans-video-proposal/README.md`
- `skills/kids-ancient-humans-video-proposal/SKILL.md`

## Installation 📦

Two common ways:

1. **Install from ClawHub (recommended for end users)**
   - Open: `https://clawhub.ai/hicoldcat/random-image-placeholder`
   - Click the install/import button on the page to add the skill to your agent workspace
2. **Install via skills.sh CLI**
   - Run:

```bash
npx skills add https://github.com/hicoldcat/skills --skill random-image-placeholder
```

3. **Use from source (for local development)**
   - Clone this repo and use the skill files/scripts directly under `skills/`

## Usage 🧪

Skills are automatically available once installed/imported (depending on your editor/agent). If a skill includes helper scripts, run them directly when a deterministic result is needed.

## Skill Structure 🗂️

Each skill contains:

- `SKILL.md` - Instructions for the agent
- `scripts/` - Helper scripts for automation (optional)
- `references/` - Supporting documentation (optional)
- `assets/` - Bundled assets (optional)

## License 📄

MIT. See [LICENSE](LICENSE).
