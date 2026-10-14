# kids-ancient-humans-video-proposal

Generate a complete **10-topic kids' science short-video proposal** about Ancient Humans —
each topic with bilingual titles, a 65–80 word English voiceover plus Chinese translation,
social posts and hashtags for Douyin / Xiaohongshu / X / YouTube Shorts, and a one-line
child-appeal rationale.

Output is a real `.md` file that must pass the bundled validator before delivery.

## When to use

Trigger when the request involves any of:

- 儿童科普短视频 / 儿童科学短视频选题与脚本
- 中英双语旁白脚本 (bilingual voiceover scripts)
- 抖音 / 小红书 / YouTube Shorts / X 社媒文案与话题标签
- 古代人类 / Ancient Humans 主题的儿童科普内容

Not for: adult-oriented science writing, single-topic requests, or video editing/voiceover production.

## Quick start

Run the validator against a generated proposal:

```bash
python skills/kids-ancient-humans-video-proposal/scripts/validate_script_doc.py \
  "古代人类-workbuddy-20261014213045.md" \
  --zh-keyword 古代人类 --en-keyword "Ancient Humans"
```

Exit code `0` = all checks passed, `1` = at least one failure (with a repair list printed).

Useful flags:

| Flag | Default | Meaning |
|---|---|---|
| `--zh-keyword` | `古代人类` | Contiguous keyword required in every Chinese title |
| `--en-keyword` | `Ancient Humans` | Contiguous keyword required in every English title |
| `--topics` | `10` | Required number of topic sections |
| `--min` / `--max` | `65` / `80` | Allowed English voiceover word count |

## What the validator checks

1. Filename matches `<theme>-<platform>-<YYYYMMDDHHmmss>.md`, timestamp parseable
2. Exactly 10 topic sections, numbering contiguous
3. Overview table has 10 data rows; both titles carry the contiguous keyword
4. Per topic: all 10 fields present, titles carry the keyword
5. English voiceover word count in range **and** the declared `Word count:` line matches the measured value
6. Chinese voiceover present; Chinese post 30–80 hanzi; English post 20–50 words
7. Chinese hashtags 5–8; English hashtags 3–6
8. Child-appeal rationale present; no elided sections

Word counting rule (fixed, so results are reproducible): strip Markdown marks, split on
whitespace, count every token containing a letter or digit. Numbers, abbreviations and
hyphenated words each count as one word.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | Triggers, defaults, Step 0–7 workflow, hard rules, science-accuracy red lines |
| `references/content-spec.md` | Full authoring spec (audience, titles, voiceover, posts, hashtags, safety, file format) |
| `references/output-template.md` | Markdown skeleton — field markers are load-bearing for the validator |
| `scripts/validate_script_doc.py` | Hard gate; standard library only |

## Requirements

- Python **3.10+** (standard library only — no third-party dependencies)
