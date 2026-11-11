# Infrathon Twitter Thread

保留 `twitter.html` 的 1 条开场帖和 7 条串文，包括原文、列表和表格。
每帖末尾的配图、下载链接属于发布说明，不是发帖正文。下载 PNG 后，在 X 发帖时将它们作为媒体附件上传。
原稿多条正文超过普通推文的 280 字符；这里保留完整长推文稿，未改写或拆帖。[X 发帖说明](https://help.x.com/en/using-x/how-to-post)。

## 配图下载

[一次下载全部 PNG（ZIP）](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/infrathon-twitter-images.zip)

| 帖子 | 附件 | PNG |
| --- | --- | --- |
| [2/7] | 任务类别图 | [下载](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/task-categories.png) |
| [3/7] | Infrathon 框架图 | [下载](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/framework.png) |
| [4/7] | 模型排名图 | [下载](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/model-rankings.png) |
| [5/7] | Codec 对比与优化过程 | [下载](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/knowledge-discovery.png) |
| [6/7] | 长短运行对比图 | [下载](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/long-vs-short.png) |
| [5/7] | 压缩率与视频质量对比表 | [下载](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/knowledge-discovery-metrics.png) |
| [6/7] | 长短程最终得分比例表 | [下载](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/horizon-comparison.png) |

第 [5/7]、[6/7] 帖各附一张表格 PNG，发推时可用表格图代替 Markdown 表格。
所有 PNG 均小于 5 MB。[X 图片上传说明](https://help.x.com/en/using-x/posting-gifs-and-pictures)。

---

## 开场帖

**Infrathon** benchmarks frontier agents on real-world AI infrastructure tasks over **12–24 hours**. **Claude Opus 5.5 increases KV-cache compression from 6.82× to 19.86× with better video quality**, and longer runs outperform short-run scaling on module and system tasks.

Homepage: <https://infrathonx.github.io/>

Blog: <https://infrathonx.github.io/blog.html>

Code: <https://github.com/InfrathonX/Infrathon>

Paper: <https://arxiv.org/abs/2611.11995>

Hugging Face: <https://huggingface.co/datasets/Infrathon/Infrathon>

Docker Hub: <https://hub.docker.com/r/infrathon/infrathon>

---

## [1/7]

**Can Frontier Agents Solve Diverse, Long-Horizon AI Infrastructure Tasks?**

AI infrastructure optimization requires repeated implementation, profiling, and testing. Agents must preserve correctness, recover from failed experiments, and keep searching when early attempts stall.

Existing evaluations often focus on specific components or shorter runs. We introduce **Infrathon** to study whether frontier agents can keep improving real-world AI infrastructure over **12–24 hours**.

---

## [2/7]

We construct **25 real-world tasks** with human experts using **Infrathon-build**, drawing on open-source infrastructure and research projects:

- **11 operator-level tasks** optimize computational primitives with **12-hour** budgets.
- **5 module-level tasks** optimize interacting components with **24-hour** budgets.
- **9 system-level tasks** optimize end-to-end training or serving workflows with **24-hour** budgets.

Tasks use metrics like **TFLOP/s** without fixed upper bounds.

> 配图附件（不属于正文）：[任务类别图 PNG](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/task-categories.png)

![任务类别图](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/task-categories.png)

---

## [3/7]

Infrathon supports continuous optimization through three components:

- **Work:** agents develop solutions and run public tests.
- **Controller:** checks instruction following and reward hacking before accepting solutions for private evaluation.
- **Judge:** runs private tests in a separate environment and returns results.

Agents use the feedback to revise their code and continue optimizing within the time budget.

> 配图附件（不属于正文）：[Infrathon 框架图 PNG](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/framework.png)

![Infrathon 框架图](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/framework.png)

---

## [4/7]

**1️⃣ Claude Opus 5.5 leads all six models with a mean rank score of 91.2.**

Across **150 runs** covering all **25 tasks**, with over **10,000 GPU-hours**, Claude wins **17 tasks**. GPT-6 Astra follows with a mean rank score of **75.2** and **six task wins**.

Because tasks use different metrics, we aggregate within-task ranks with equal task weights.

> 配图附件（不属于正文）：[模型排名图 PNG](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/model-rankings.png)

![模型排名图](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/model-rankings.png)

---

## [5/7]

**2️⃣ Infrathon can support knowledge discovery.**

On **Quant-VideoGen KV Codec**, Claude increases mean KV-cache compression from **6.82× to 19.86×** compared with the human codec, averaged across WorldScore and MovieGen. Video quality also improves on both datasets: **higher PSNR and SSIM, and lower LPIPS**.

| Dataset / video model | Compression (×) ↑ | PSNR (dB) ↑ | SSIM ↑ | LPIPS ↓ |
| --- | --- | --- | --- | --- |
| WorldScore / HY-WorldPlay | 6.75 → **20.89** | 31.15 → **36.33** | 0.923 → **0.975** | 0.059 → **0.023** |
| MovieGen / LongCat-Video | 6.88 → **18.83** | 23.67 → **26.95** | 0.836 → **0.884** | 0.126 → **0.085** |

Mean values: Human → Claude. Quality metrics use the uncompressed BF16 reference.

The human codec quantizes residual values individually after clustering. Claude transforms the residuals using **principal component analysis** and applies **entropy coding after quantization**.

> 配图附件（不属于正文）：[Codec 对比与优化过程 PNG](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/knowledge-discovery.png) · [压缩率与视频质量对比表 PNG](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/knowledge-discovery-metrics.png)

![Codec 对比与优化过程](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/knowledge-discovery.png)

---

## [6/7]

**3️⃣ Long Horizon vs. Short Horizon**

We compare one long run with the best of two or four independent shorter runs at **equal GPU-hour budgets**, using GPT-6 Astra and Claude Opus 5.5 on six tasks.

**Longer horizons are more effective for module and system tasks, while short-horizon test-time scaling remains competitive on operators.**

| Task level | Best of two / one long run | Best of four / one long run |
| --- | --- | --- |
| Operator | 101.3% | 102.6% |
| Module | 96.5% | 96.9% |
| System | **79.4%** | **77.3%** |

Geometric means of task–model score ratios. 100% means equal performance at equal total GPU-hours.

The long run wins **nine of 12 task–model comparisons**, including **all four system comparisons**.

> 配图附件（不属于正文）：[长短运行对比图 PNG](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/long-vs-short.png) · [长短程最终得分比例表 PNG](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/horizon-comparison.png)

![长短运行对比图](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/long-vs-short.png)

---

## [7/7]

Questions and feedback are welcome! If you find this work useful, please consider starring the repository and citing our paper.

Huge thanks to all our collaborators and the human experts who helped build Infrathon!

---
