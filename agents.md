# 智能体引导文档：战役汉化工作指南

本文档总结自提交 `a5e936c`（[1985] 文案修复）与 `01dece8`（[BTL1] 编码转换），供后续汉化任务参考。

## 一、需要汉化的文件

### 每关任务目录内（通用模式）

| 文件 | 内容 |
|---|---|
| `stringtable.utf8.csv` / `stringtable.csv` | 主要文案：任务简报、无线电对话、提示（STR_HINT）、任务目标、胜负文本、字幕文本 |
| `briefing.utf8.html` / `briefing.html` | 简报页面；正文必须用 `$STR_...` 引用 stringtable 键，**禁止硬编码文案** |
| `overview.utf8.html` / `overview.html` | 关卡选择界面的概述；`<title>` 应引用 `$STR_..._OVERVIEW_001` |
| `description.ext` | `CfgSounds` 中声音字幕 `titles[] = { 0, $STRCAMP_xxx }`；`Campaign` 类的 `name` 等 |
| `mission.sqm` / `MISSION.SQM` | 内嵌文案字段，如 `briefingName`（BTL1 关卡） |

注意：1985 战役文件名带 `.utf8` 后缀（`stringtable.utf8.csv`、`briefing.utf8.html`、`overview.utf8.html`）；BTL1 不带。

### 战役根目录

| 文件 | 内容 |
|---|---|
| `1985/stringtable.utf8.csv` | 关卡名称表（`STRCN_xx` 键） |
| `BTL1/description.ext` | `Campaign` 类的 `name`（战役标题） |
| `BTL1/overview.html` | 战役根概述页 |
| `BTL1/MISSION.SQM` | 战役根任务文件内嵌文案 |

### 不需要汉化 / 不要修改的文件

- 二进制资源：`.paa`、`.pac`、`.jpg`、`sound/*.ogg`、`vssver.scc` 等
- 原版多语言简报：`briefing.German.html`、`briefing.French.html`、`briefing.Italian.html`
- 脚本逻辑文件 `.sqs`（除非其中确有需本地化的显示文案，且通过 `localize` 引用 stringtable）
- BTL1 `stringtable.csv` 中的 German / French / Italian 列

## 二、执行汉化工作时的注意事项

### 1. 编码

- 所有文本文件一律使用 **UTF-8 无 BOM**。**不要添加 BOM 头。**
- BTL1 原文件多为 GB2312/GBK 编码，使用已提供的脚本转换：
  - `BTL1/convert_encoding.py`：处理 `overview.html`、`stringtable.csv`、`briefing.html`
  - `BTL1/convert_mission_sqm.py`：处理 `mission.sqm`
- 转换逻辑：先尝试按 UTF-8 解码；若带 BOM 则去除 BOM；若 UTF-8 失败再依次尝试 GB2312、GBK。
- 遗留问题：`BTL1/overview.html` 的 meta charset 仍为 `windows-1250`，修改该文件时应一并改为 `utf-8`。
- 1985 战役根目录原 `stringtable.csv` 为乱码编码，已删除并替换为 `stringtable.utf8.csv`。

### 2. 换行符

- **换行优先遵循文件内原有换行**：编辑已有文件时，保持其原有的换行风格（LF 或 CRLF），不要整体转换。
- 写文件时使用与原文件一致的换行方式；参考 `convert_encoding.py` 中 `newline=''` 的做法（保留原换行，不额外转换）。
- CSV 值内部的换行：简报等多行文本在 CSV 中按原有格式处理；HTML 内换行用 `<br>`。

### 3. CSV 格式

- 表头为 `LANGUAGE,English`（1985 单语言）或多语言列 `LANGUAGE,English,German,French,Italian`（BTL1）。
- 含逗号、换行或双引号的字段必须用双引号包裹。
- 字段内的双引号转义为两个双引号 `""`（常见于 HTML 属性，如 `<a href=""marker:xxx"">`）。
- stringtable 中的键名必须与 HTML / `description.ext` 中的 `$STR_...` 引用一一对应。
- BTL1 汉化内容只填入 **English 列**（第一数据列），不要改动其他语言列。

### 4. HTML 简报结构

- 正文文案不硬编码，统一替换为 `$STR_CAMPAIGN_...` 引用，文案本体写在 stringtable 中。
- 保留并维护锚点结构：`<a name="Intel">`、`<a href="#Intel">`、`<a href="#Main">`、`<a href="marker:xxx">` 等。
- 修改简报时检查内部引用完整性（曾修复 02 关简报 `<a href="#Intel">` 引用缺失）。
- `overview` 的 `<title>` 应引用 `$STR_..._OVERVIEW_001`，而非硬编码中文。

### 5. CfgSounds 声音字幕（description.ext）

- 每个声音类需要填写 `name = "33v01";`（与类名一致）。
- `titles[] = { 0, $STRCAMP_33v01 };` 引用 stringtable 中同名键，确保字幕可显示。

### 6. 文案内容与逻辑一致性

- 无线电对话中的路线/方向描述必须与任务目标（OBJ）一致（曾修复 35 关东/西线路引用颠倒）。
- 日期汉化为中文格式（如 `July 3, 1985` → `1985年7月3日`）。
- 人名、地名、部队代号（Kolgujev、Morton、La Trinite、Zulu、Papa Bear 等）保留原文，不强行音译。
- 修改文案时注意上下文语义连贯，避免张冠李戴。

### 7. mission.sqm

- 关注 `briefingName` 等字符串字段的汉化与编码。
- 文件名大小写不敏感但保持一致（`MISSION.SQM` vs `mission.sqm`）。
- 触发器 `name` 字段等内嵌文本也需保证 UTF-8 编码正确。

### 8. 验证清单

每次汉化或修改后自查：

- [ ] `$STR_...` 引用的键在对应 stringtable 中存在
- [ ] HTML 锚点 `href="#..."` 的目标 `name="..."` 存在
- [ ] 文件为 UTF-8 无 BOM（可用二进制读取确认开头无 `EF BB BF`）
- [ ] CSV 可被正确解析（列数一致、引号配对）
- [ ] 换行风格与修改前一致
- [ ] 未误改二进制文件与其他语言列
