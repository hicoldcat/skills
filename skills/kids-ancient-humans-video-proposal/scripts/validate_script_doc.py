#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""validate_script_doc.py — 校验「儿童科普短视频选题包」Markdown 文档是否达标。

用法::

    python validate_script_doc.py 古代人类-20261014213045.md \
        --zh-keyword 古代人类 --en-keyword "Ancient Humans"

三级结论:
  PASS  合格
  WARN  参考提示 —— 不影响退出码
  FAIL  必须修复

FAIL 项（全部通过才返回退出码 0）:
  1. 文件名符合 ``<主题>-<YYYYMMDDHHmmss>.md``（不含平台名），时间戳可解析
  2. 选题块恰好 N 个（默认 10）且序号连续
  3. 总览表格行数与标题关键词
  4. 每个选题必备字段齐全；中文/英文标题含**连续**关键词
  5. 若填写了「单词数量（参考）」，标注值与实测值一致（该行本身可选）
  6. 中文旁白存在且为中文
  7. 中文贴文 30–80 汉字；英文贴文 20–50 词
  8. 中文话题标签 5–8 个；英文话题标签 3–6 个
  9. 儿童吸引力分析存在

WARN 项（仅供提示，不阻断交付）:
  - 英文旁白词数超出 [min, max]（默认 65–80）—— 原规范已将 65–80 降为参考范围，
    不再作为硬性限制
  - 文档中出现「第三部分」等额外章节 —— 规范要求只保留第一部分与第二部分

单词统计口径（与 content-spec 一致）:
  去掉 Markdown 标记后按空白切分，含字母或数字的 token 计 1 词；
  数字、缩写、带连字符的词各计 1 词。

仅使用 Python 标准库。
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------------- #
# 文本工具
# --------------------------------------------------------------------------- #

_PUNCT = re.compile(r"[\s\u3000()（）〔〕\[\]【】{}<>:：;；,，。.!！?？*_`~\-—–|/\\#]+")
_MD_STRIP = re.compile(r"[*_`>#\[\]()]+")
_WORDISH = re.compile(r"[A-Za-z0-9]")
_CJK = re.compile(r"[\u4e00-\u9fff]")
_TAG = re.compile(r"#[^\s#]+")


def norm_key(s: str) -> str:
    """归一化一行文本，用于字段标记识别（去空白/标点/Markdown 装饰，转小写）。"""
    return _PUNCT.sub("", s).lower()


def count_words(s: str) -> int:
    """按统一口径统计英文词数。"""
    s = _MD_STRIP.sub(" ", s)
    return sum(1 for t in re.split(r"\s+", s) if _WORDISH.search(t))


def count_cjk(s: str) -> int:
    return len(_CJK.findall(s))


def count_tags(s: str) -> int:
    return len(_TAG.findall(s))


def strip_tags(s: str) -> str:
    return _TAG.sub(" ", s)


# --------------------------------------------------------------------------- #
# 字段标记（顺序 = 识别优先级）
# --------------------------------------------------------------------------- #

FIELD_DEFS = [
    ("zh_title", ["中文标题"]),
    ("en_title", ["englishtitle"]),
    ("knowledge", ["核心知识点"]),
    ("en_vo", ["englishvoiceover"]),
    ("word_count", ["wordcount", "单词数量"]),
    ("zh_vo", ["中文旁白"]),
    ("zh_post", ["中文贴文"]),
    ("en_post", ["englishpost"]),
    ("zh_tags", ["中文话题标签"]),
    ("en_tags", ["英文话题标签"]),
    ("appeal", ["儿童吸引力分析"]),
]

FIELD_LABELS = {
    "zh_title": "中文标题",
    "en_title": "English Title",
    "knowledge": "核心知识点",
    "en_vo": "英文旁白",
    "word_count": "单词数量（参考）",
    "zh_vo": "中文旁白",
    "zh_post": "中文贴文",
    "en_post": "English Post",
    "zh_tags": "中文话题标签",
    "en_tags": "英文话题标签",
    "appeal": "儿童吸引力分析",
}

# 可由作者决定是否填写的字段（缺失不算 FAIL）
OPTIONAL_FIELDS = {"word_count"}

TOPIC_RE = re.compile(r"^##\s*选题\s*(\d+)\s*[:：]")
FILENAME_RE = re.compile(r"^(?P<theme>.+?)-(?P<ts>\d{14})\.md$")
LEGACY_FILENAME_RE = re.compile(r"^(?P<theme>.+?)-(?P<platform>[A-Za-z0-9_]+)-(?P<ts>\d{14})\.md$")
TABLE_ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|([^|]*)\|([^|]*)\|")


# --------------------------------------------------------------------------- #
# 解析
# --------------------------------------------------------------------------- #


def trailing_text(line: str) -> str:
    """取字段标记行中、最后一个 '**' 之后的正文（行内首段文字）。"""
    return line.rsplit("**", 1)[-1] if "**" in line else ""


def classify(line: str):
    """把一行判定为某个字段标记；返回 (field_key, 行内正文) 或 (None, None)。"""
    nk = norm_key(line)
    if not nk:
        return None, None
    for key, kws in FIELD_DEFS:
        if any(kw in nk for kw in kws):
            return key, trailing_text(line)
    return None, None


def split_topics(lines):
    """切出所有选题块。返回 [(num, heading, block_lines), ...]

    选题区在「下一个非选题的二级标题」处结束（如 `## 第三部分：...`），
    避免把结尾的质量检查清单误算进最后一个选题。
    """
    starts = []
    for i, line in enumerate(lines):
        m = TOPIC_RE.match(line.strip())
        if m:
            starts.append((i, int(m.group(1)), line.strip()))
    if not starts:
        return []

    cutoff = len(lines)
    for i in range(starts[0][0] + 1, len(lines)):
        s = lines[i].strip()
        if s.startswith("## ") and not TOPIC_RE.match(s):
            cutoff = i
            break

    blocks = []
    for i, (idx, num, heading) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else cutoff
        blocks.append((num, heading, lines[idx:min(end, cutoff)]))
    return blocks


def extract_fields(block_lines):
    """把选题块按字段切分，返回 {field_key: 正文文本}"""
    fields = {}
    current = None
    for line in block_lines[1:]:  # 跳过 "## 选题 N：..." 标题行本身
        key, rest = classify(line)
        if key:
            current = key
            fields.setdefault(key, [])
            if rest.strip():
                fields[key].append(rest)
        elif current:
            fields[current].append(line)
    return {k: "\n".join(v).strip() for k, v in fields.items()}


# --------------------------------------------------------------------------- #
# 校验
# --------------------------------------------------------------------------- #


PASS, WARN, FAIL = "PASS", "WARN", "FAIL"


class Report:
    def __init__(self):
        self.items = []  # (level, scope, message)

    def add(self, ok: bool, scope: str, msg: str):
        self.add_level(PASS if ok else FAIL, scope, msg)

    def warn(self, scope: str, msg: str):
        self.add_level(WARN, scope, msg)

    def add_level(self, level: str, scope: str, msg: str):
        self.items.append((level, scope, msg))

    @property
    def failures(self):
        return [i for i in self.items if i[0] == FAIL]

    @property
    def warnings(self):
        return [i for i in self.items if i[0] == WARN]

    def render(self) -> str:
        out = []
        last_scope = None
        for level, scope, msg in self.items:
            if scope != last_scope:
                out.append(f"\n[{scope}]")
                last_scope = scope
            out.append(f"  {level:<4}  {msg}")
        return "\n".join(out)


def check_filename(path: Path, prefix, rep: Report):
    """校验文件名符合 ``<主题>-<YYYYMMDDHHmmss>.md``（规范已去掉平台名）。"""
    name = path.name

    # 先识别「主题-平台-时间戳」旧格式，给出明确的迁移提示
    legacy = LEGACY_FILENAME_RE.match(name)
    if legacy:
        rep.add(False, "文件名",
                f"文件名含平台名「{legacy.group('platform')}」：{name}；"
                f"规范要求 `<主题>-<YYYYMMDDHHmmss>.md`，不包含生成平台名称")
        return

    m = FILENAME_RE.match(name)
    if not m:
        hint = "（主题名里不要带 `-` 和平台名）" if "-" in name else ""
        rep.add(False, "文件名", f"不符合 `<主题>-<YYYYMMDDHHmmss>.md`：{name}{hint}")
        return

    ts = m.group("ts")
    try:
        dt = datetime.strptime(ts, "%Y%m%d%H%M%S")
    except ValueError:
        rep.add(False, "文件名", f"时间戳无法解析为 YYYYMMDDHHmmss：{ts}")
        return
    if not (2000 <= dt.year <= 2100):
        rep.add(False, "文件名", f"时间戳年份异常：{dt.year}")
        return
    theme = m.group("theme")
    if prefix and theme != prefix:
        rep.add(False, "文件名", f"主题前缀「{theme}」与期望「{prefix}」不符")
        return
    rep.add(True, "文件名", f"{name}（主题={theme} 时间={dt:%Y-%m-%d %H:%M:%S}）")


def check_overview(lines, zh_kw, en_kw, want, rep: Report):
    rows = []
    for line in lines:
        m = TABLE_ROW_RE.match(line.strip())
        if m:
            rows.append((int(m.group(1)), m.group(2).strip(), m.group(3).strip()))
    rep.add(len(rows) == want, "总览表", f"表格数据行 {len(rows)} 行（要求 {want}）")
    for num, zh, en in rows:
        rep.add(zh_kw in zh, "总览表", f"第 {num} 行中文标题含连续「{zh_kw}」：{zh[:40]}")
        rep.add(en_kw.lower() in en.lower(), "总览表", f"第 {num} 行英文标题含连续「{en_kw}」：{en[:40]}")


def check_topic(num, fields, zh_kw, en_kw, lo, hi, rep: Report):
    scope = f"选题 {num}"

    missing = [k for k in FIELD_LABELS if k not in fields and k not in OPTIONAL_FIELDS]
    rep.add(not missing, scope, "必备字段齐全" + (f"（缺失：{', '.join(FIELD_LABELS[k] for k in missing)}）" if missing else ""))
    if missing:
        return

    # 标题关键词
    zh_title = fields["zh_title"].replace("\n", " ").strip()
    en_title = fields["en_title"].replace("\n", " ").strip()
    rep.add(zh_kw in zh_title, scope, f"中文标题含连续「{zh_kw}」")
    rep.add(en_kw.lower() in en_title.lower(), scope, f"英文标题含连续「{en_kw}」")

    # 英文旁白词数：65–80 为参考区间，越界只提示不阻断
    n = count_words(fields["en_vo"])
    if lo <= n <= hi:
        rep.add(True, scope, f"英文旁白 {n} 词（参考区间 {lo}–{hi}）")
    else:
        rep.warn(scope, f"英文旁白 {n} 词，超出参考区间 {lo}–{hi}（不阻断交付，仅提示）")

    # 词数标注：整行可选；一旦填写就必须与实测一致
    if "word_count" in fields:
        m = re.search(r"(\d+)", fields["word_count"])
        if not m:
            rep.add(False, scope, "「单词数量（参考）」行缺少数字")
        else:
            declared = int(m.group(1))
            rep.add(declared == n, scope,
                    f"词数标注 {declared} 与实测 {n} {'一致' if declared == n else '不一致'}")

    # 中文旁白
    zh_vo_cjk = count_cjk(fields["zh_vo"])
    rep.add(zh_vo_cjk >= 30, scope, f"中文旁白 {zh_vo_cjk} 汉字（要求 ≥30）")

    # 贴文
    zh_post_cjk = count_cjk(strip_tags(fields["zh_post"]))
    rep.add(30 <= zh_post_cjk <= 80, scope, f"中文贴文 {zh_post_cjk} 汉字（要求 30–80）")
    en_post_w = count_words(fields["en_post"])
    rep.add(20 <= en_post_w <= 50, scope, f"英文贴文 {en_post_w} 词（要求 20–50）")

    # 话题标签
    zh_t = count_tags(fields["zh_tags"])
    en_t = count_tags(fields["en_tags"])
    rep.add(5 <= zh_t <= 8, scope, f"中文话题标签 {zh_t} 个（要求 5–8）")
    rep.add(3 <= en_t <= 6, scope, f"英文话题标签 {en_t} 个（要求 3–6）")

    # 儿童吸引力分析
    appeal = fields["appeal"].strip()
    rep.add(len(appeal) >= 10 and count_cjk(appeal) >= 8, scope, "儿童吸引力分析为一句具体说明")


def validate(path: Path, zh_kw: str, en_kw: str, want: int, lo: int, hi: int, prefix=None) -> Report:
    rep = Report()
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    check_filename(path, prefix, rep)

    rep.add(len(text.strip()) > 0, "文件", f"文件大小 {path.stat().st_size} 字节")

    blocks = split_topics(lines)
    rep.add(len(blocks) == want, "选题数", f"共 {len(blocks)} 个选题块（要求 {want}）")
    nums = [b[0] for b in blocks]
    rep.add(nums == list(range(1, want + 1)), "选题数", f"序号：{nums}")

    check_overview(lines, zh_kw, en_kw, want, rep)

    for num, _heading, block_lines in blocks:
        check_topic(num, extract_fields(block_lines), zh_kw, en_kw, lo, hi, rep)

    if "第三部分" in text:
        rep.warn("结构", "文档含「第三部分」——规范要求交付文档只保留第一部分与第二部分"
                         "（质量检查清单属执行者自检，不写入输出）")
    else:
        rep.add(True, "结构", "文档只含第一部分与第二部分")
    for marker in ("此处省略", "其余选题类似", "以下略"):
        rep.add(marker not in text, "结构", f"未出现省略式表述「{marker}」")
    return rep


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="校验儿童科普短视频脚本 Markdown 文档")
    ap.add_argument("md_path", help="待校验的 .md 文件路径")
    ap.add_argument("--zh-keyword", default="古代人类", help="中文标题必须含有的连续关键词")
    ap.add_argument("--en-keyword", default="Ancient Humans", help="英文标题必须含有的连续关键词")
    ap.add_argument("--name-prefix", default=None,
                    help="文件名前缀（默认取 --zh-keyword），规范为 `<主题>-<YYYYMMDDHHmmss>.md`")
    ap.add_argument("--topics", type=int, default=10, help="要求的选题数量（默认 10）")
    ap.add_argument("--min", dest="lo", type=int, default=65,
                    help="英文旁白参考词数下限（默认 65；超出仅 WARN，不阻断）")
    ap.add_argument("--max", dest="hi", type=int, default=80,
                    help="英文旁白参考词数上限（默认 80；超出仅 WARN，不阻断）")
    ap.add_argument("--strict-words", action="store_true",
                    help="把词数越界从 WARN 升级为 FAIL（默认关闭）")
    args = ap.parse_args(argv)

    path = Path(args.md_path)
    if not path.is_file():
        print(f"FAIL  文件不存在：{path}")
        return 1

    prefix = args.name_prefix if args.name_prefix is not None else args.zh_keyword
    rep = validate(path, args.zh_keyword, args.en_keyword, args.topics, args.lo, args.hi, prefix)

    if args.strict_words:
        rep.items = [
            (FAIL, s, m.replace("（不阻断交付，仅提示）", "（--strict-words：已升级为 FAIL）"))
            if (lv == WARN and "参考区间" in m) else (lv, s, m)
            for lv, s, m in rep.items
        ]

    print(f"=== 校验：{path.name} ===")
    print(rep.render())

    total = len(rep.items)
    fails = rep.failures
    warns = rep.warnings
    print(f"\n=== 结果：{total - len(fails) - len(warns)} PASS / {len(warns)} WARN / {len(fails)} FAIL"
          f"（共 {total} 项）===")
    if warns:
        print("参考提示（不阻断交付）：")
        for _lv, scope, msg in warns:
            print(f"  ~ [{scope}] {msg}")
    if fails:
        print("需要修复：")
        for _lv, scope, msg in fails:
            print(f"  - [{scope}] {msg}")
        print("\nVERDICT: FAIL")
        return 1
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
