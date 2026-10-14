# kids-ancient-humans-video-proposal

Generate a complete **10-topic kids' science short-video proposal** about Ancient Humans —
each topic with bilingual titles, an English voiceover plus Chinese translation
(65–80 words is a **guideline, not a hard limit**), social posts and hashtags for
Douyin / Xiaohongshu / X / YouTube Shorts, and a one-line child-appeal rationale.

Output is a real `.md` file that must pass the bundled validator before delivery.
The theme and its bilingual keywords are parameters, so the same workflow transfers to
other science topics.

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
  "古代人类-20261014213045.md" \
  --zh-keyword 古代人类 --en-keyword "Ancient Humans"
```

Exit code `0` = no failures, `1` = at least one failure (with a repair list printed).
Warnings never affect the exit code.

Useful flags:

| Flag | Default | Meaning |
|---|---|---|
| `--zh-keyword` | `古代人类` | Contiguous keyword required in every Chinese title |
| `--en-keyword` | `Ancient Humans` | Contiguous keyword required in every English title |
| `--name-prefix` | value of `--zh-keyword` | Expected filename prefix (spec: `<theme>-<YYYYMMDDHHmmss>.md`) |
| `--topics` | `10` | Required number of topic sections |
| `--min` / `--max` | `65` / `80` | **Reference** voiceover word-count band (out-of-band ⇒ WARN only) |
| `--strict-words` | off | Escalate out-of-band word counts from WARN to FAIL |

## Results: PASS / WARN / FAIL

- **PASS** — check satisfied
- **WARN** — advisory only, does not block delivery. Raised when an English voiceover falls
  outside the 65–80 reference band, or when the document contains an extra section such as
  「第三部分」 (the spec keeps only Part 1 and Part 2 in the delivered file)
- **FAIL** — must be fixed

## What the validator checks

FAIL-level:

1. Filename matches `<theme>-<YYYYMMDDHHmmss>.md` (**no platform segment**), timestamp parseable
2. Exactly 10 topic sections, numbering contiguous
3. Overview table has 10 data rows; both titles carry the contiguous keyword
4. Per topic: required fields present, titles carry the keyword
5. If the 「单词数量（参考）」 line is present, its value matches the measured word count
   (the line itself is optional)
6. Chinese voiceover present; Chinese post 30–80 hanzi; English post 20–50 words
7. Chinese hashtags 5–8; English hashtags 3–6
8. Child-appeal rationale present; no elided sections

WARN-level:

- English voiceover outside the 65–80 reference band
- Document contains an extra section beyond Part 1 / Part 2

Word counting rule (fixed, so results are reproducible): strip Markdown marks, split on
whitespace, count every token containing a letter or digit. Numbers, abbreviations and
hyphenated words each count as one word.

## Files

| Path | Purpose |
|---|---|
| `SKILL.md` | Triggers, defaults, Step 0–7 workflow, hard rules, science-accuracy red lines |
| `references/content-spec.md` | Full authoring spec (audience, titles, voiceover, posts, hashtags, safety, format & naming) |
| `references/output-template.md` | Markdown skeleton — field markers are load-bearing for the validator |
| `scripts/validate_script_doc.py` | Validator; standard library only |

## Requirements

- Python **3.10+** (standard library only — no third-party dependencies)
