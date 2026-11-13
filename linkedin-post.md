# Infrathon LinkedIn Post

Can long-horizon agents keep improving real-world AI infrastructure?

We introduce Infrathon, a benchmark of 25 real-world tasks across operators, modules, and complete training or serving workflows. Built with human experts using Infrathon-build, the tasks give agents 12–24 hours to implement, profile, and test solutions.

![Infrathon task categories](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/task-categories.png)

Public tests guide development, while a Controller checks instruction following and reward hacking before private evaluation.

We evaluate six models across 150 runs, with over 10,000 GPU-hours. Three findings:

**1️⃣ Claude Opus 5.5 leads all six models.**

Claude wins 17 of 25 tasks with a mean rank score of 91.2. GPT-6 Astra follows at 75.2, winning six tasks.

![Model rankings across 25 tasks](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/model-rankings.png)

**2️⃣ Infrathon can support knowledge discovery.**

On Quant-VideoGen KV Codec, Claude increases mean KV-cache compression from 6.82× to 19.86× compared with the human codec, averaged across WorldScore and MovieGen. Video quality improves on both datasets: higher mean PSNR and SSIM, and lower mean LPIPS.

Claude's codec transforms residuals using principal component analysis and applies entropy coding after quantization.

![Codec quality comparison and optimization trajectory](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/knowledge-discovery.png)

**3️⃣ Long Horizon vs. Short Horizon.**

At equal GPU-hour budgets, we compare one long run with the best of two or four shorter runs, using GPT-6 Astra and Claude Opus 5.5 on six tasks.

Longer horizons are more effective for module and system tasks, while short-horizon scaling remains competitive on operators. The long run wins nine of 12 task–model comparisons, including all four system comparisons.

![Long- vs. short-horizon performance comparison](https://raw.githubusercontent.com/InfrathonX/InfrathonX.github.io/main/assets/img/twitter/horizon-comparison.png)

Huge thanks to all our collaborators and the human experts who helped build Infrathon! Questions and feedback are welcome.

Homepage: <https://infrathonx.github.io/>

Blog: <https://infrathonx.github.io/blog.html>

Code: <https://github.com/InfrathonX/Infrathon>

Paper: <https://arxiv.org/abs/2611.11995>

Hugging Face: <https://huggingface.co/datasets/Infrathon/Infrathon>

Docker Hub: <https://hub.docker.com/r/infrathon/infrathon>
