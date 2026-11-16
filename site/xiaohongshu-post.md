# 给Agent一天，探索RSI

华盛顿大学（UW）、艾伦人工智能研究所（AI2）、RadixArk、Pyromind Dynamics 等机构的研究者共同推出 Infrathon。

🏠 Homepage：<https://infrathonx.github.io/>

📝 Blog：<https://infrathonx.github.io/blog.html>

📄 Paper：<https://arxiv.org/abs/2611.11995>

🤗 Hugging Face Daily Papers：<https://huggingface.co/papers/2611.11995>

💻 Code：<https://github.com/InfrathonX/Infrathon>

📦 Dataset：<https://huggingface.co/datasets/Infrathon/Infrathon>

🐳 Docker Hub：<https://hub.docker.com/r/infrathon/infrathon>

让 Agent 连续改代码、跑实验，能把 AI 基础设施优化到什么程度？

我们做了 Infrathon：25 项真实任务、6 个模型、150 次运行，主实验预算超过 1 万 GPU 小时。任务覆盖算子、模块和完整训练／推理系统，每次给 Agent 12–24 小时。

几个结果很值得聊聊👇

🎬 **KV 缓存压缩得更多，视频质量指标也更好了**

在视频 KV 缓存压缩任务中，Claude Opus 5.5 经过 24 小时迭代，在 WorldScore 和 MovieGen 各 200 个样本的评测中，将平均压缩比从人工方案的 6.82× 提升到 19.86×。

以未压缩视频为参考，PSNR、SSIM、LPIPS 三项质量指标也都改善。方案经历了 PCA、熵编码、量化方式等多轮修改。

📈 **90% 的运行，后半程还在进步**

150 次运行里，135 次在后半程刷新了最佳分数。Qwen 有一次停滞了 6.78 小时，之后又取得提升。

排行榜也会变：预算走到 25% 时，Astra 整体领先；到 50% 时，Claude 反超，最终拿下 25 项任务中的 17 项第一。

⏳ **同样的预算，连续优化有多重要？**

我们用两个模型、六项任务，对比“一次长运行”和“两次或四次短运行取最佳”。

长运行在 12 个任务—模型组合中的 9 个上胜出，包含全部 4 个系统级组合；算子任务上，多次短运行仍有竞争力。

过程中也有翻车：改了代码却测到旧缓存、通过公开测试却违反任务要求、还有优化空间就宣布完成……

这些记录让我们看到，Agent 持续优化 AI Infra 的能力，既取决于方案设计，也取决于它能否可靠地管理实验、利用反馈。

做 Agent、推理加速、GPU 优化的朋友，欢迎试试 Infrathon，也欢迎交流你最想交给 Agent 的优化任务！

#RSI #AIAgent #AIInfra #大模型 #推理加速 #GPU优化 #论文分享

---

配图可直接使用项目网站的 [KV 缓存压缩对比与优化轨迹图](https://infrathonx.github.io/assets/img/homepage/qvg-intro.svg)。

![KV 缓存压缩对比与优化轨迹图](https://infrathonx.github.io/assets/img/homepage/qvg-intro.svg)
