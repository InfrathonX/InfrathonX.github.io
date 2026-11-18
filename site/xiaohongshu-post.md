# 给Agent一天，探索RSI

华盛顿大学（UW）、艾伦人工智能研究所（AI2）、RadixArk、Pyromind Dynamics 等机构的研究者共同推出 Infrathon。

🏠 Homepage：<https://infrathonx.github.io/>

📝 Blog：<https://infrathonx.github.io/blog.html>

📄 Paper：<https://arxiv.org/abs/2611.11995>

🤗 Hugging Face Daily Papers：<https://huggingface.co/papers/2611.11995>

💻 Code：<https://github.com/InfrathonX/Infrathon>

📦 Dataset：<https://huggingface.co/datasets/Infrathon/Infrathon>

🐳 Docker Hub：<https://hub.docker.com/r/infrathon/infrathon>

让 Agent 连续改代码、跑实验，能把 AI infra 优化到什么程度？

我们做了 Infrathon：25 项真实任务、6 个模型、150 次运行，主实验预算超过 1 万 GPU 小时。任务覆盖算子、模块和完整训练／推理系统，每次给 Agent 12–24 小时。

我们得到三个主要结论👇

1️⃣ **Claude Opus 5.5 在六个模型中整体领先，平均排名分数为 91.2**

Claude 在 25 项任务中拿下 17 项第一；GPT-6 Astra 的平均排名分数为 75.2，拿下 6 项第一。分数按单项任务排名计算，再对 25 项任务等权平均。

2️⃣ **Infrathon 可以支持知识发现**

在视频 KV 缓存压缩任务中，Claude Opus 5.5 经过 24 小时迭代，将平均压缩比从人工方案的 6.82× 提升到 19.86×，同时改善视频质量：两个数据集上的 PSNR、SSIM 更高，LPIPS 更低。

评测在 WorldScore 和 MovieGen 上各使用 200 个样本。核心改动包括对聚类后的残差做 PCA 变换，并在量化后使用熵编码。

3️⃣ **长程优化与短程优化的比较**

在相同 GPU 小时预算下，我们用 Astra 和 Claude 在六项任务上，对比“一次长运行”和“两次或四次独立短运行取最佳”。

长运行在 12 个任务—模型组合中的 9 个上胜出，包括全部 4 个系统级组合。**模块和系统任务更受益于长运行；算子任务上，多次短运行仍有竞争力。**

做 Agent、推理加速、GPU 优化的朋友，欢迎试试 Infrathon，也欢迎交流你最想交给 Agent 的优化任务！

#RSI #AIAgent #AIInfra #大模型 #推理加速 #GPU优化 #论文分享

---

配图可直接使用项目网站的 [KV 缓存压缩对比与优化轨迹图](https://infrathonx.github.io/assets/img/homepage/qvg-intro.svg)。

![KV 缓存压缩对比与优化轨迹图](https://infrathonx.github.io/assets/img/homepage/qvg-intro.svg)
