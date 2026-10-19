# Agent Skills 🧰

[English](README.md) | 中文

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Built for Agents](https://img.shields.io/badge/Built%20for-AI%20Agents-blue)
![Maintained](https://img.shields.io/badge/Maintained-yes-success)
![GitHub stars](https://img.shields.io/github/stars/hicoldcat/skills?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/hicoldcat/skills)

一个面向 AI 编程代理的 skill 合集。

> 🚀 开源、实用、易扩展。

## 当前可用的 Skills ✨

### random-image-placeholder

基于 [Lorem Picsum](https://picsum.photos/) 生成随机/可复现的占位图 URL（可选下载到本地）。

**适用场景：**

- 做 UI mock / 文档 / demo，需要图片但不想托管静态资源
- 测试/快照需要可复现图片（使用 `seed`）
- 用户提到 picsum / 占位图 / grayscale / blur / seed / id

**示例：**

```bash
python skills/random-image-placeholder/scripts/picsum.py url --seed avatar-42 --width 400 --height 400 --grayscale --blur 2
```

```bash
python skills/random-image-placeholder/scripts/picsum.py download --seed avatar-42 --width 120 --height 80 --out ./tmp/picsum_test.jpg
```

相关文档：

- `skills/random-image-placeholder/README.md`
- `skills/random-image-placeholder/SKILL.md`

### kids-ancient-humans-video-proposal

围绕「古代人类」主题，一次性生成**完整的 10 个儿童科普短视频选题包**——中英双语标题、英文旁白（65–80 词为参考区间，非硬性）+ 中文译文、抖音/小红书/X/YouTube Shorts 社媒文案与话题标签，以及每个选题的儿童吸引力分析。产出为一份 Markdown 文件，交付前必须通过自带校验脚本。主题与中英关键词均为参数，同一套流程可迁移到其他科普主题。

**适用场景：**

- 需要儿童科普短视频选题、脚本，或中英双语旁白脚本
- 需要抖音 / 小红书 / YouTube Shorts / X 的社媒文案与话题标签
- 主题为 古代人类 / Ancient Humans 的儿童科普内容
- 需要"10 个选题"并配中英双语旁白的场景

**示例：**

```bash
python skills/kids-ancient-humans-video-proposal/scripts/validate_script_doc.py "古代人类-20261014213045.md" --zh-keyword 古代人类 --en-keyword "Ancient Humans"
```

```bash
python skills/kids-ancient-humans-video-proposal/scripts/validate_script_doc.py "海洋生物-20261014213045.md" --zh-keyword 海洋生物 --en-keyword "Ocean Animals"
```

相关文档：

- `skills/kids-ancient-humans-video-proposal/README.md`
- `skills/kids-ancient-humans-video-proposal/SKILL.md`

### idiom-fable-story-shorts

把成语和寓言做成 **10 条 30 秒英语讲故事短视频**——一条视频一个故事，用 **55–70 个简单英文单词**（硬性上限）讲完，配中文译文、3–5 个核心单词，以及抖音 / 小红书 / X / YouTube Shorts 的社媒文案与话题标签。每次产出一份 Markdown 文件，交付前必须通过自带校验脚本。

重点在**讲故事，不在讲道理**：孩子看完能复述"谁做了什么、结果怎样"，也就懂了这个成语的意思。不做科学解读，也不把一个成语拆成多集。

**适用场景：**

- 想把成语 / 寓言做成儿童英语短视频（成语故事英语、寓言故事英语、英语启蒙故事）
- 需要中英双语故事旁白，或给孩子的英语讲故事脚本
- 需要儿童故事类内容的抖音 / 小红书 / YouTube Shorts / X 文案与话题标签
- 需要"10 个选题"并配中英双语旁白的场景

**示例：**

```bash
python skills/idiom-fable-story-shorts/scripts/validate_script_doc.py \
  "成语寓言-20261019102313.md" --name-prefix "成语寓言" --min 55 --max 70
```

```bash
python skills/idiom-fable-story-shorts/scripts/validate_script_doc.py \
  "狐狸-20261019102313.md" --name-prefix "狐狸" --min 55 --max 70
```

相关文档：

- `skills/idiom-fable-story-shorts/README.md`
- `skills/idiom-fable-story-shorts/SKILL.md`

## 安装 📦

常见有三种方式：

1. **通过 ClawHub 安装（推荐给使用者）**
   - 打开：`https://clawhub.ai/hicoldcat/random-image-placeholder`
   - 在页面点击安装/导入按钮，将 skill 加入你的代理工作区
2. **通过 skills.sh CLI 安装**
   - 运行：

```bash
npx skills add https://github.com/hicoldcat/skills --skill random-image-placeholder
```

3. **源码方式（适合本地开发）**
   - clone 仓库后直接使用 `skills/` 下的 skill 文件与脚本

## 使用 🧪

安装/导入后，skill 会根据你的编辑器/代理规则自动可用。若 skill 自带脚本，建议在需要“确定性输出”时直接运行脚本获得稳定结果。

## Skill 结构 🗂️

每个 skill 通常包含：

- `SKILL.md`：给代理的使用说明
- `scripts/`：可选的辅助脚本（更稳定、可复用）
- `references/`：可选的参考资料
- `assets/`：可选的资源文件

## 许可 📄

MIT，见 [LICENSE](LICENSE)。
