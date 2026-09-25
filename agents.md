# 智能体引导文档：战役汉化工作指南

本文档总结自提交 `a5e936c`（[1985] 文案修复）、`01dece8`（[BTL1] 编码转换）与 Retailation 战役整体汉化（windows-1251 源），供后续汉化任务参考。

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
- [ ] HTML 标签序列未变，且 `</a>`、`<br`、`href=` 计数与原文件一致（只查 `<a ` 抓不到标签被吃掉）
- [ ] HTML `<meta ... charset=...>` 已随转码改为 `utf-8`（原 windows-1250/1251 会误导渲染）
- [ ] 西里尔只剩注释；HTML 注释 `<! ... >` 须先从计数中剔除再比对
- [ ] 标点无残留半角句点接中文、无“空格+中文标点”（如 `</a>.`、`</a> ，`）

## 三、Retailation 战役经验（windows-1251 源）

### 1. 编码

- 源编码是 **windows-1251**（不是 BTL1 的 GB2312/GBK）。解码顺序按“先 UTF-8，再 cp1251，再 GBK”，以实测为准。
- 个别文件混入 **KOI8-R 乱码**（`18_Extraction.Eden\MISSION.SQM` 共 7 处，如 `бЬТПДТПН`→`Аэродром`）。可用 bigram 评分 + `encode('cp1251').decode('koi8-r')` 还原；改前先打印确认，避免把正常西里尔当乱码（`ЛИФТ`、`Г. Юрков` 这类是误报）。
- 转码后必须同步改 HTML meta charset，否则浏览器/游戏按 1251 解 UTF-8 字节。

### 2. 各文件的可译位置（Retailation 实测）

| 文件 | 可译位置 | 禁改 |
|---|---|---|
| `stringtable.csv` | row[1] 正文（表头 `LANGUAGE,English,Comment`，row[0]=键，row[2]=英文备注） | 键列、备注列、其他语言列 |
| `briefing.html` | 文本节点、属性值（按 offset 替换） | 标签、锚点 `name=`/`href=` |
| `mission.sqm` | Sensors/Markers 的 `text`、Groups 的 `description`、`briefingName`、Effects 的 `title`、`expActiv/expDesactiv` 内嵌串（按引号拆分，只译俄语片段） | **标识符 `name`（marker name、传感器 name）** |
| `description.ext` | `CfgSounds` 的 `titles[]` 字幕正文、`Campaign` 的 `name` | `$STR` 引用、类名、代码 |
| `.sqs` | 仅显示用文案 | 俄语注释（按约定保留原文）、逻辑 |

- CSV 字段内的换行是**字面 `\n`（反斜杠+n）**，不是真换行；引号普遍包裹字段，因此用 **span 级替换**，不要 `csv.writer` 重写（QUOTE_MINIMAL 会改变引号与格式）。
- Retailation 的 HTML 正文是**硬编码文案**（不走 `$STR_` 引用），与 1985/BTL1 的约定不同：已有硬编码正文保持原样译入，不要临时改成 stringtable 引用（会造成大量键新增与引用面改动）。
- `<! --- ... >` 这类畸形注释（`<` 与 `!` 之间有空格）不被渲染，其中的俄文/捷克文开发者注释**保留原文**，校验时须从西里尔计数中排除。
- `overview.html` 可能只有 `<img>` + `<title>Overview</title>`（文字烙在 `.paa` 图里）→ 无可译文本，不要硬加 `$STR_` 键。
- `description.ext` 可能引用**原版就不存在**的键（Retailation 有 59 个 `$STRM_` 无对应条目，64 处有效引用）→ 记录为遗留问题即可，没有原文就不要凭空编字幕。

### 3. 批量翻译工作流（可复用）

工具链放在临时目录（勿入库）：`extract.py` → `batches.py` → 子代理翻译 → `apply.py --apply` → `patch_charset.py` → `cleanup.py --apply` → `verify.py`；`restore.py` 从 `backup\` 还原原件。

- **译后不要再跑 `extract.py`**：文件已无西里尔，会把单元和 `.zh.json` 一起删掉。
- 翻译子代理可能**静默返回空结果**，重试同一批次即可成功。
- 给规则文件（`TRANSLATE_RULES.md`）先定死：译文禁实际换行、禁 `<>`、禁半角 `"`（CSV 回填时转 `""`）、`bare` 条目禁 `;`、保留 `%1`/`$STR_`/`marker:`/字面 `\n`、片段单元保持首尾空格（apply 用 `preserve_ws()` 补回）。
- 调试写回前**先 restore**：任何一次失败的 `--apply` 都会把文件写成半成品。

### 4. 踩坑复盘（写新脚本时对照）

1. `rec['ext']` 带点，比较必须写 `'.csv'` / `'.html'`。写成 `'csv'` 会**静默走错分支**：文件被 UTF-8 重编码却不替换内容，表面上“applied 124 files”正常。DEBUG 打印要放在分支**入口**，不是末尾。
2. 标点清理正则 `</a>[ 　]*\.` → `。` 会把 `</a>` 一起替换掉；必须用 lookbehind `(?<=</a>)[ 　]*\.`。同时 verify 要比对 `</a>`/`<br` 计数，只查 `<a ` 与 `href=` 抓不到。
3. 用 `csv.reader` 逐行比对时要跳过空行 `[]`，否则 `a[0]` 抛 IndexError。
4. 脚本加 `if __name__ == '__main__': sys.exit(main())`，否则 `import` 调试时会直接跑主流程。
5. 给文件做结构校验时，比较对象是**原始备份**（cp1251/GBK 解码）与新文件；两边都要先归一化“有意改动”的部分（如 charset），否则校验会把预期改动报成错误。
