# 餐厅密码学家 Demo：面向投资人的阶段性进展说明

> 项目工作组 · 2026 年 8 月

## 一句话介绍

我们在 [Proof Lab](https://github.com/epistemic-frontier/proof-lab) 中，用一个经典匿名通信
协议完成了一条从自然语言问题、有限模型、自动生成证明，到独立内核验证和 CI 合并的完整
工作链。在已有基础设施上，本轮从发现形式证明缺口到补齐证明并合并，大约用了
**2～3 小时**。

## 这是一个什么问题

“餐厅密码学家”由现代密码学先驱 David Chaum 于 1988 年提出。故事很简单：三位密码学家
吃完饭后，只知道账单要么由 NSA 支付，要么由三人中的一人支付。他们希望确认是哪一种
情况，却不暴露具体是谁付了钱。

三人通过两两共享的随机硬币，各自公开一位经过掩码的信息。三位公开信息合在一起，可以
判断“NSA 付款”还是“有人付款”；但单独看公开结果，无法区分是哪位密码学家付款。这是
匿名通信中的经典思想，后来通常称为 DC-net。

原始论文：[David Chaum, *The Dining Cryptographers Problem*](https://ir.cwi.nl/pub/2438)。

## 我们完成了什么

我们没有只运行几个示例，而是把三人协议展开为一个完整的有限世界：

```text
4 种付款者 × 8 种共享硬币组合 = 32 个可能世界
```

在这 32 个世界上，我们完成了三层工作。

第一层是协议模型。系统逐一检查公开结果是否正确，以及外部观察者在听完消息后还能把哪些
人视为付款者。模型还精确比较了三位付款者产生公开消息的概率分布。

第二层是形式证明。Proof Lab 生成了两个实际进入 Metamath 验证器的定理：

- `dc_parity_table`：覆盖全部 32 个世界，证明协议的公开奇偶性始终正确；
- `dc_payer_bijection_table`：覆盖 24 个付款者转换情形，证明不同付款者之间存在保持完整
  公开消息不变的有限双射。

第三层是反例测试。我们故意破坏三人之间的共享秘密结构，使 Carol 失去掩码。协议仍能正确
判断“是否有人付款”，但 Carol 的身份会被直接暴露。这个反例说明：功能正确不等于安全，
而我们的验证框架能够在同一套模型中同时处理正面证明与反面攻击。

## 证明过程是什么样的

这里的“证明”不是程序输出一个 `true`。证明构造器先遍历 32 个世界，为每一行递归构造 XOR
的命题逻辑推导，再把 32 个独立定理合取成一个根定理。下面是简化后的核心循环：

```python
proof = ProofBuilder(system, "dc_parity_table")
rows = []
for payer in PAYERS:
    for raw_coins in product((False, True), repeat=3):
        coins = (raw_coins[0], raw_coins[1], raw_coins[2])
        parity = _parity(_statements(payer, coins))
        row, value = _evaluate(proof, parity, label=f"r{len(rows):02d}")
        rows.append(row)

conclusion = _join(proof, tuple(rows), label="parity_join")
return proof.build(conclusion)
```

其中 `_evaluate` 不是普通求值器：它为每一个真假分支引用 `df-xor`、`xnor`、双条件、否定等
已经验证的逻辑定理；`_join` 再用合取引入定理 `pm3.2i` 连接各行。完整过程可直接查看
[证明构造器](https://github.com/epistemic-frontier/proof-lab/blob/main/src/proof_lab/tasks/task_06_dining_cryptographers/proofs/finite_tables.py#L227-L446)。

构造完成后，ProofScaffold 发射 Metamath 证明文本，独立的 `mmverify` 从公理和已验证定理重新
检查整个依赖链。CI 中最终出现：

```text
verifying dc_parity_table
verifying dc_payer_bijection_table

OK
mmverify OK rc=0
```

形式表和协议模型没有共用同一个 transcript 实现；另一个
[32 世界桥接测试](https://github.com/epistemic-frontier/proof-lab/blob/main/tests/test_dining_cryptographers_proofs.py#L64-L75)
逐世界检查二者是否采用相同的付款者与硬币约定。这让投资人既能看到最终结果，也能沿链接
查看证明是怎样生成、怎样接入协议语义、又怎样被独立复核的。

## 这项进展说明了什么

这个 demo 本身不是商业产品，也不是一个困难的新数学定理。它的价值在于展示了一条小而
完整、可以复核的生产流程：

1. 把自然语言中的协议和安全目标拆成明确的对象、假设与结论；
2. 用有限模型穷尽状态空间，而不是依赖随机抽样或几个手选案例；
3. 把适合形式化的部分生成真正的证明对象，交给小型独立内核复查；
4. 对尚未进入内核的部分明确标注证据等级，不把程序运行结果冒充形式证明；
5. 把代码、证明、引用、声明账本、测试和 CI 结果保存在同一个可追踪版本中。

第一版工作先完成了有限语义模型。随后复核发现 Task 6 尚未真正发射 Metamath proof，我们
没有沿用含混表述，而是立即补上两个证明、增加独立桥接测试，并重新划清形式证明与计算证据
的边界。这次纠正本身也反映了项目的工程纪律：结论必须能追溯到与其强度相匹配的证据。

## 当前结果

截至本说明形成时：

- 32 个标准世界全部通过协议正确性和知识状态检查；
- 两个 Task 6 根定理由 `mmverify` 接受；
- 正式包中 6 个声明定理全部发射，声明但未发射的数量为 0；
- 34 个 Python 测试、类型检查、代码检查和数据 schema 检查全部通过；
- 两个 GitHub CI job 均通过后完成合并；
- 协议来源、局部建模选择和证据边界均有独立文档记录。

相关记录：

- [中文技术说明](https://github.com/epistemic-frontier/proof-lab/blob/main/tasks/task_06_dining_cryptographers/README.zh-CN.md)
- [完整证明源码](https://github.com/epistemic-frontier/proof-lab/blob/main/src/proof_lab/tasks/task_06_dining_cryptographers/proofs/finite_tables.py)
- [形式与语义桥接测试](https://github.com/epistemic-frontier/proof-lab/blob/main/tests/test_dining_cryptographers_proofs.py)
- [形式证明合并提交](https://github.com/epistemic-frontier/proof-lab/commit/4f9b18cb60ab6583bfd43e553a8df5ac4eeece69)
- [CI 记录](https://github.com/epistemic-frontier/proof-lab/actions)

## 时间与能力边界

本轮约 **2～3 小时**，指的是在 ProofScaffold、命题逻辑库、有限 S5 解释器和已有协议 demo
基础上，完成缺口识别、证明构造、桥接审计、测试、CI 和合并的时间。它不包括底层证明工具
和逻辑库此前的建设成本。

目前由 Metamath 内核直接验证的是协议奇偶性表和付款者双射表。公开宣告后的知识关系、候选
付款者集合、精确计数与坏拓扑搜索，仍是指定有限模型上的穷尽计算。它们不是抽样，但还不是
模态逻辑内核中的定理。我们没有把这个三人 demo 描述成一般匿名通信系统的完整安全审计。

## 下一步

下一阶段的重点不是继续堆叠玩具例子，而是提高这条流程的自动化程度：让有限可能世界、知识
关系和公开宣告可以自动下降为可检查的命题证明，并为有限计数生成证明证书。完成这一步后，
更多知识推理、协议验证和有限安全分析任务就能复用同一条形式化生产线。

对我们而言，这个 demo 最重要的阶段结论是：现有基础设施已经能够在数小时尺度内，把一个
有明确文献来源的自然语言问题推进为可运行、可反驳、可生成证明、可由独立内核验证且可经 CI
交付的版本化成果。
