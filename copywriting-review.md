# 网页文案审阅与处理记录

更新日期：2026-11-09。

已按清单逐条处理 **52 项**：**39 项删改或移位**（含此前已删除的 H00），**13 项作为方法、计分和运行信息保留**。第二轮追加清理 **13 项**。本轮修改网页文案与说明位置，实验分数、轨迹和计分计算保持不变。

## 本轮结果

- 首页保留三个 finding 的结论、数字和重点强调，删除更新脚注、重复副标题及多余限定。
- 研究页面直接报告结果，删掉稿件版本自证、来源转述、否定式兜底和重复总结。
- 实验设置、统计分母与 token 定义放进可展开的详情。
- 任务页保留评分和运行要求，删除导入精度、数据处理过程等文案。
- 首页与独立 Interactive Results 页面同步；任务指南与结果数据的浏览器 bundle 已重建。

## 第二轮追加清理

| 编号 | 原文或旧写法 | 处理结果 | 位置 |
| --- | --- | --- | --- |
| N01 | We examine their full trajectories and best valid private-test scores. | 导语直接给出 6 个模型、25 个任务、12–24 小时和 Claude 的 17 个胜场。 | [site/main-results.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/main-results.html:26) |
| N02 | Can long-horizon optimization produce infrastructure solutions that improve on human designs? | 问句导语改为 Claude 的 codec 在压缩率和视频质量上超过 human codec。 | [site/knowledge-discovery.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/knowledge-discovery.html:26) |
| N03 | How do compute allocation, evaluation horizon, late improvements, and agent activity change the conclusions of an infrastructure benchmark? | 导语缩为本页的四个分析主题。 | [site/analysis.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:26) |
| N04 | The result depends on the model: | 删除泛化前缀，直接给出 Claude 和 Astra 的具体结果。 | [site/analysis.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:26) |
| N05 | and thus below the threshold of 1 | 正文保留 error-to-tolerance ratio < 0.4；通过阈值 1 放在图注说明。 | [site/agent-behavior.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:26) |
| N06 | Both models pass these numerical checks despite violating the required computation. | 删去图注中对正文结论的重复，图注只解释点的含义和通过阈值。 | [site/agent-behavior.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:26) |
| N07 | twenty kernel configurations appear to be compared | 直接写 20 个配置试验都复用了同一缓存实现，删掉 appear to。 | [site/agent-behavior.html:30](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:30) |
| N08 | The paper uses GPT-6.1 Sol in Codex | 直接写 GPT-6.1 Sol in Codex 执行审核。 | [site/framework.html:34](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/framework.html:34) |
| N09 | This quality-weighted score is distinct from compression ratio. | 删去重复区分，保留 R、q、评分公式及 human codec 的参考分。 | [data/task_metrics.json:729](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/task_metrics.json:729) |
| N10 | Task score and compression ratio are different quantities. | 删去重复区分；任务指标标题与公式已经明确是质量加权分数。 | [data/task_guides.json:2950](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/task_guides.json:2950) |
| N11 | Equal budgets / Equal-GPU-hour time allocations | 导航改为 Long vs. short，图标题改为 Long and short optimization runs。 | [site/analysis.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:26) |
| N12 | Performance on selected tasks / Twelve selected tasks span | 标题明确写 Performance on 12 tasks，图注删去重复的 selected。 | [site/main-results.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/main-results.html:26) |
| N13 | The paper’s experiments use | 直接写 Experiments use，删除对论文的来源转述。 | [site/framework.html:30](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/framework.html:30) |

## 原 52 项的逐条结果

原文片段保留作对照；源文件链接指向当前页面或字段的位置。

### H00 · 已处理

位置：[site/index.html:115](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/index.html:115) · [查看页面](http://localhost:8000/index.html#findings)

原文片段：

> At equal GPU-hours,

处理结果：已删首页 finding 的 At equal GPU-hours, 前缀。

### H01 · 已处理

位置：[site/index.html:160](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/index.html:160) · [查看页面](http://localhost:8000/index.html#leaderboard)

原文片段：

> Includes the updated quality-weighted QVG scores.

处理结果：已删除 QVG 更新脚注，榜单底部保留 100 分的定义。

### H02 · 已处理

位置：[site/index.html:115](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/index.html:115) · [查看页面](http://localhost:8000/index.html#findings)

原文片段：

> Overall performance, equal-budget optimization, and knowledge discovery.

处理结果：已删除 Key findings 下的重复副标题。

### M01 · 已处理

位置：[site/main-results.html:32](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/main-results.html:32) · [查看页面](http://localhost:8000/main-results.html#rankings)

原文片段：

> The scores below follow the current manuscript and agree with the interactive leaderboard after the quality-weighted QVG update.

处理结果：已删除分数与稿件版本一致的说明。

### M02 · 已处理

位置：[site/main-results.html:31](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/main-results.html:31) · [查看页面](http://localhost:8000/main-results.html#plateau-statistics)

原文片段：

> A run is counted once for each statistic.

处理结果：计数规则移到 Main Results → Statistics 折叠说明。

### M03 · 已处理

位置：[site/main-results.html:30](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/main-results.html:30) · [查看页面](http://localhost:8000/main-results.html#plateaus)

原文片段：

> A long period without a new record therefore does not establish that further optimization is exhausted.

处理结果：已删除否定式总结，保留 Qwen 的具体突破案例。

### M04 · 已处理

位置：[site/main-results.html:41](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/main-results.html:41) · [查看页面](http://localhost:8000/main-results.html#complete-trajectories)

原文片段：

> Original appendix trajectories from the current manuscript; six models per task.

处理结果：图注与替代文字改为 Task score trajectories across six models.

### M05 · 已处理

位置：[site/main-results.html:41](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/main-results.html:41) · [查看页面](http://localhost:8000/main-results.html#complete-trajectories)

原文片段：

> The remaining task trajectories from the current manuscript; six models per task.

处理结果：图注与替代文字改为 Task score trajectories across six models.

### K01 · 已处理

位置：[site/knowledge-discovery.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/knowledge-discovery.html:26) · [查看页面](http://localhost:8000/knowledge-discovery.html#setup)

原文片段：

> A controlled codec comparison

处理结果：标题缩为 Codec comparison。

### K02 · 已处理

位置：[site/knowledge-discovery.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/knowledge-discovery.html:26) · [查看页面](http://localhost:8000/knowledge-discovery.html#setup)

原文片段：

> The comparison measures compression and video quality, not compression alone.

处理结果：已删除 not compression alone 及重复解释。

### K03 · 已处理

位置：[site/knowledge-discovery.html:28](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/knowledge-discovery.html:28) · [查看页面](http://localhost:8000/knowledge-discovery.html#optimization)

原文片段：

> This produces a different codec design with higher compression and better measured video quality.

处理结果：改为 Claude’s codec improves compression and video quality.

### A01 · 已处理

位置：[site/analysis.html:36](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:36) · [查看页面](http://localhost:8000/analysis.html#ranking-budget)

原文片段：

> The preferred model depends on both the task and the available time.

处理结果：已删除末尾关于模型选择依赖任务与时间的重复总结。

### A02 · 已处理

位置：[site/analysis.html:36](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:36) · [查看页面](http://localhost:8000/analysis.html#second-half)

原文片段：

> Late gains are common but uneven: many runs make small refinements, while a smaller group makes substantial improvements.

处理结果：已删除 common but uneven 的概括，保留 3.05% 与 33 次提升的数据。

### A03 · 已处理

位置：[site/analysis.html:38](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:38) · [查看页面](http://localhost:8000/analysis.html#interactions)

原文片段：

> Activity alone does not establish optimization quality.

处理结果：已删除 Activity alone does not establish optimization quality.

### B01 · 已处理

位置：[site/agent-behavior.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:26) · [查看页面](http://localhost:8000/agent-behavior.html#requirements)

原文片段：

> The paper documents five rejected solutions.

处理结果：改为直接说明 Controller 拒绝下表中的五个提交。

### B02 · 已处理

位置：[site/agent-behavior.html:30](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:30) · [查看页面](http://localhost:8000/agent-behavior.html#validation)

原文片段：

> These cases separate two questions: whether an implementation passes a test, and whether the performance experiment actually measures the proposed change.

处理结果：已删除 These cases separate two questions 的总结。

### B03 · 已处理

位置：[site/agent-behavior.html:30](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:30) · [查看页面](http://localhost:8000/agent-behavior.html#improvement)

原文片段：

> These examples would be missed by stopping at the earlier completion statements; they are selected cases rather than a measured frequency over all runs.

处理结果：已删除整句案例频率免责声明，保留三个案例与具体提升。

### R01 · 已处理

位置：[site/archived-results.html:21](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/archived-results.html:21) · [查看页面](http://localhost:8000/archived-results.html)

原文片段：

> Explore model rankings and task trajectories, including the updated quality-weighted QVG scores.

处理结果：导语缩为 Explore model rankings and task trajectories.

### R02 · 已处理

位置：[site/archived-results.html:27](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/archived-results.html:27) · [查看页面](http://localhost:8000/archived-results.html#leaderboard)

原文片段：

> This explorer uses the selected dashboard runs with updated quality-weighted QVG scores. The other 24 tasks retain their original data. Overall scores now match the manuscript, including Sol at 54.4 and GLM at 8.0.

处理结果：已删除整段数据更新历史，保留 Main Results 导航链接。

### T01 · 已处理

位置：[data/task_metrics.json:730](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/task_metrics.json:730) · [查看页面](http://localhost:8000/task.html#qvg/metric-details)

原文片段：

> The supplied score tables have two decimal places; original timestamps and validity statuses are retained.

处理结果：已删除表格精度、时间戳和有效性状态的导入说明。

### H03 · 已处理

位置：[site/index.html:115](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/index.html:115) · [查看页面](http://localhost:8000/index.html#findings)

原文片段：

> than the human codec on both datasets.

处理结果：首页删去 on both datasets，保留与 human codec 的比较；详情页仍给出两个数据集。

### M06 · 已处理

位置：[site/main-results.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/main-results.html:26) · [查看页面](http://localhost:8000/main-results.html#setup)

原文片段：

> Performance is the highest finite, valid private-test score submitted within the task budget.

处理结果：改为 We report the best valid private-test score within each run’s budget.

### K04 · 已处理

位置：[site/knowledge-discovery.html:27](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/knowledge-discovery.html:27) · [查看页面](http://localhost:8000/knowledge-discovery.html#codec-evaluation)

原文片段：

> Both codecs and the uncompressed BF16 reference use the same inputs and generation settings.

处理结果：匹配输入与生成设置移到 Knowledge Discovery → Evaluation setup。

### A04 · 已处理

位置：[site/analysis.html:27](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:27) · [查看页面](http://localhost:8000/analysis.html#budget-setup)

原文片段：

> The comparison includes the continuously allocated Judge; T is 12 hours for operators and 24 hours for modules and systems.

处理结果：Judge 资源与 T 的时长移到 Analysis → Experiment setup。

### A05 · 已处理

位置：[site/analysis.html:27](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:27) · [查看页面](http://localhost:8000/analysis.html#budget-setup)

原文片段：

> using geometric means of task–model score ratios.

处理结果：几何平均的汇总方式移到 Analysis → Experiment setup。

### A06 · 已处理

位置：[site/analysis.html:27](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:27) · [查看页面](http://localhost:8000/analysis.html#budget-setup)

原文片段：

> The study reuses 12 main runs and adds 72 short runs.

处理结果：12 个复用运行与 72 个短运行移到 Analysis → Experiment setup。

### B04 · 已处理

位置：[site/agent-behavior.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:26) · [查看页面](http://localhost:8000/agent-behavior.html#requirements)

原文片段：

> All are rejected before private evaluation, illustrating why instruction checks complement numerical tests.

处理结果：保留 before private evaluation，删除 illustrating why 的阐释尾句。

### B05 · 已处理

位置：[site/agent-behavior.html:30](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:30) · [查看页面](http://localhost:8000/agent-behavior.html#improvement)

原文片段：

> In three selected runs, a stop hook prompts agents to continue after they declare completion.

处理结果：three selected runs 改为 three case studies。

### B06 · 已处理

位置：[site/agent-behavior.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/agent-behavior.html:26) · [查看页面](http://localhost:8000/agent-behavior.html#requirements)

原文片段：

> The Controller returns the reason for rejection without a private-test score.

处理结果：行为页删去重复的“拒绝不返回私有分数”；Framework 保留该机制。

### T02 · 已处理

位置：[data/task_guides.json:2951](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/task_guides.json:2951) · [查看页面](http://localhost:8000/task.html#qvg/metric)

原文片段：

> Failed quality or correctness checks are excluded.

处理结果：已从 QVG 主指标简介删去失败检查的尾句；Metric details 中保留有效性规则。

### T03 · 已处理

位置：[data/tasks.json:43](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/tasks.json:43) · [查看页面](http://localhost:8000/task.html#wan22/results)

原文片段：

> No submission during the run; performance is zero under the paper’s no-valid-result convention

处理结果：运行脚注缩为 No submission; score = 0.

### D01 · 已处理

位置：[site/docs.html:89](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/docs.html:89) · [查看页面](http://localhost:8000/docs.html#configuration)

原文片段：

> This example uses the same model and credentials for the Worker and the submission reviewer.

处理结果：缩为 Worker and reviewer use the same model and credentials.

### P01 · 已保留

位置：[site/index.html:176](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/index.html:176) · [查看页面](http://localhost:8000/index.html#score-notes)

原文片段：

> Exact ties share average rank; a run without a valid scored submission receives zero.

处理结果：保留在方法、计分或运行说明中。这直接定义排名与零分如何产生，删去会使读者无法复核 leaderboard。可以不放在首页主叙事里。

### P02 · 已保留

位置：[site/index.html:176](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/index.html:176) · [查看页面](http://localhost:8000/index.html#score-notes)

原文片段：

> The 95% task-bootstrap confidence intervals use 10,000 resamples for the full suite and 3,000 for filtered groups.

处理结果：保留在方法、计分或运行说明中。图上展示了置信区间，方法至少应有一处说明。

### P03 · 已保留

位置：[site/index.html:176](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/index.html:176) · [查看页面](http://localhost:8000/index.html#score-notes)

原文片段：

> excluding tool responses, repeated code-diff displays, and reasoning traces.

处理结果：保留在方法、计分或运行说明中。这是 visible tokens 的统计范围；不宜把这些数字改称全部 tokens。

### P04 · 已处理

位置：[site/index.html:176](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/index.html:176) · [查看页面](http://localhost:8000/index.html#score-notes)

原文片段：

> filtered totals sum rounded per-task values (≈).

处理结果：过滤后 token 总数的近似值说明移到对应表格单元格的悬停提示，保留 ≈ 标记。

### P05 · 已处理

位置：[site/analysis.html:27](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:27) · [查看页面](http://localhost:8000/analysis.html#budget-setup)

原文片段：

> GPT-6 Astra and Claude Opus 5.5 each optimize six tasks under equal GPU-hour budgets.

处理结果：等 GPU-hour 的比较设置移到 Analysis → Experiment setup，主结果直接给结论。

### P06 · 已处理

位置：[site/analysis.html:37](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:37) · [查看页面](http://localhost:8000/analysis.html#gain-statistics)

原文片段：

> Scores start at zero, so this count includes runs that do not yet have a scored submission at halfway.

处理结果：零分初始化与后半程首次得分的计数口径移到 Analysis → Statistics。

### P07 · 已保留

位置：[site/analysis.html:36](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:36) · [查看页面](http://localhost:8000/analysis.html#second-half)

原文片段：

> Among runs with a positive first-half score, the median later gain is 3.05%;

处理结果：保留在方法、计分或运行说明中。3.05% 的中位数只对这个子集计算。可以移到图注，但删掉限定会改变数字的含义。

### P08 · 已处理

位置：[site/analysis.html:37](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/analysis.html:37) · [查看页面](http://localhost:8000/analysis.html#gain-statistics)

原文片段：

> This timing analysis uses runs with positive final scores.

处理结果：正最终分数的筛选条件移到 Analysis → Statistics。

### P09 · 已处理

位置：[site/knowledge-discovery.html:27](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/knowledge-discovery.html:27) · [查看页面](http://localhost:8000/knowledge-discovery.html#codec-evaluation)

原文片段：

> Quality metrics compare the first segment generated with compressed KV against the BF16 reference.

处理结果：PSNR/SSIM/LPIPS 的首段视频测量范围移到 Knowledge Discovery → Evaluation setup。

### P10 · 已保留

位置：[site/knowledge-discovery.html:26](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/knowledge-discovery.html:26) · [查看页面](http://localhost:8000/knowledge-discovery.html#setup)

原文片段：

> 200 samples per dataset

处理结果：保留在方法、计分或运行说明中。样本量是结果的上下文，比较设置中保留即可，首页 finding 无需重复。

### P11 · 已保留

位置：[data/task_metrics.json:730](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/task_metrics.json:730) · [查看页面](http://localhost:8000/task.html#qvg/metric-details)

原文片段：

> Scores were recomputed after the original runs. Agents optimized the original compression-only metric.

处理结果：保留在方法、计分或运行说明中。区分运行时优化的目标与事后展示的质量加权分数。T01 的精度和导入细节可以删，这两句涉及实际实验流程。

### P12 · 已保留

位置：[data/tasks.json:41](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/tasks.json:41) · [查看页面](http://localhost:8000/task.html#mamba2/results)

原文片段：

> Run on different hardware from the rest of the cohort

处理结果：保留在方法、计分或运行说明中。是实际部署差异，宜用简短脚注呈现。

### P13 · 已处理

位置：[data/tasks.json:44](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/tasks.json:44) · [查看页面](http://localhost:8000/task.html#qvg/results)

原文片段：

> Different deployment and review settings

处理结果：将笼统的部署差异具体写为 GLM QVG 使用 PyroMind、8 个 Judge GPU、无 LLM integrity review。

### P14 · 已保留

位置：[data/tasks.json:42](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/data/tasks.json:42) · [查看页面](http://localhost:8000/task.html#minference/results)

原文片段：

> Agent edited the submission-hook state during the run

处理结果：保留在方法、计分或运行说明中。说明该运行发生的具体行为；属于记录事实。

### F01 · 已保留

位置：[site/framework.html:30](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/framework.html:30) · [查看页面](http://localhost:8000/framework.html#definition)

原文片段：

> Cases and scoring code remain inaccessible to the agent.

处理结果：保留在方法、计分或运行说明中。这说明 Work/Judge 隔离，是框架的功能。不能把所有隐私测试说明都当成防御句。

### F02 · 已保留

位置：[site/framework.html:34](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/framework.html:34) · [查看页面](http://localhost:8000/framework.html#protocol)

原文片段：

> Private evaluation uses disjoint samples and additional task types.

处理结果：保留在方法、计分或运行说明中。定义 public/private 的区别；对复现和理解泛化测试有用。

### F03 · 已处理

位置：[site/framework.html:34](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/framework.html:34) · [查看页面](http://localhost:8000/framework.html#execution)

原文片段：

> The Controller enforces task-specific submission limits and frequency, copies only allowed files, and reviews each submission before private testing.

处理结果：压缩 Controller 描述，保留文件检查、提交限制与私有评测前审核。

### D02 · 已保留

位置：[site/docs.html:89](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/docs.html:89) · [查看页面](http://localhost:8000/docs.html#configuration)

原文片段：

> The FP8 example saves submission archives without a candidate-history store. Miles and Concurrent serving also need Candidate history.

处理结果：保留在方法、计分或运行说明中。不同 launcher 的真实要求，删除后用户可能漏配 candidate history。

### D03 · 已保留

位置：[site/docs.html:116](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/docs.html:116) · [查看页面](http://localhost:8000/docs.html#assets)

原文片段：

> For private or gated datasets and models, grant access to your Hugging Face account and sign in before fetching:

处理结果：保留在方法、计分或运行说明中。这是实际登录步骤，处理下载失败的操作要求。

### D04 · 已保留

位置：[site/docs.html:122](/home/zhengyuhu/research-project/1108-Infrathon-homepage/homepage-code/site/docs.html:122) · [查看页面](http://localhost:8000/docs.html#containers)

原文片段：

> choose the host hardware: h100-94gb-400w for H100 NVL or h100-80gb-700w for H100 SXM.

处理结果：保留在方法、计分或运行说明中。镜像与硬件规格有关；与主结论无关，但属于正常安装说明。

## 保留的实验与任务信息

以下信息继续可查：

- Rank score、平均名次、零分处理和置信区间定义。
- Visible output tokens 的统计范围、近似值与 first-score 时间口径。
- 长短程实验的模型、任务、运行数量、GPU-hour 与 Judge 预算设置。
- 135/150、3.05% 和达到最终表现 90% 所需时间的统计分母。
- QVG 的视频测量范围、样本量和事后质量加权评分。
- 不同硬件、部署与审查设置的运行脚注。
- 25 个任务的数值有效性、模型约束和实际启动要求。

## 已确认的首页 finding

1. **Claude Opus 5.5 achieves the best performance.**
2. **Long Horizon vs. Short Horizon**
   - Longer horizons are more effective for module and system tasks, while short-horizon TTS remains competitive on operators.
3. **Infrathon can support knowledge discovery**

## 复核范围

复核了首页、Main Results、Knowledge Discovery、Analysis、Agent Behavior、Framework、Docs、Task List、25 个动态任务页、Run log 与独立 Interactive Results。已检查正文、折叠说明、图注、替代文字、任务指标和运行脚注。原始论文图表中的文字与维护用的数据来源记录保持原样。
