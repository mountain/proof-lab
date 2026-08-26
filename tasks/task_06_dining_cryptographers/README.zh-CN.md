# 餐厅密码学家：从匿名通信故事到可核验的有限证明

[面向投资人的简要介绍与进展汇报](INVESTOR_BRIEF.zh-CN.md)

这份说明回答三个容易混在一起的问题：餐厅密码学家协议从哪里来；Proof Lab
具体验证了什么；其中哪些结论已经进入 Metamath 内核，哪些仍然依赖 Python
有限模型计算。

## 1. 历史背景

David Chaum 在 1988 年的论文《The Dining Cryptographers Problem: Unconditional Sender and
Recipient Untraceability》中提出了这个著名故事。三位密码学家吃完饭后得知：账单要么由
NSA 支付，要么由三人中的一人支付。他们希望公开确认是哪一种情形，却不泄露究竟是哪位
密码学家付款。

这个小故事并不只是逻辑游戏。Chaum 用它说明：参与者可以借助预先共享的随机秘密，公开
发送彼此抵消的消息，从而暴露一个总体事实，同时隐藏单个发送者的身份。这一思想后来通常
被称为 Dining Cryptographers network，或 DC-net，是匿名通信研究中的经典出发点之一。

原始来源：

- David Chaum, “The Dining Cryptographers Problem: Unconditional Sender and Recipient
  Untraceability,” *Journal of Cryptology* **1**(1), 1988, 65–75：
  [CWI 记录](https://ir.cwi.nl/pub/2438)，[DOI](https://doi.org/10.1007/BF00206326)。

本仓库只处理论文中最初等的三人情形，不声称覆盖 Chaum 论文中的一般网络、串谋模型或
多轮构造。

## 2. 三枚共享硬币怎样隐藏付款者

Alice、Bob、Carol 两两相邻；每一对私下共享一枚独立且均匀的硬币：

```text
Alice ----- c_AB ----- Bob
   \                     /
    c_CA               c_BC
      \                 /
              Carol
```

每个人只看得到与自己相邻的两枚硬币。未付款者如实公开两枚硬币是否不同，付款者说反话。
把“不同”记为 `1`、“相同”记为 `0`，第 `i` 位参与者的公开比特为：

```text
s_i = XOR(与 i 相邻的两枚硬币) XOR [i 是付款者].
```

三个人的公开比特再做一次 XOR，每枚共享硬币都出现两次，因而彼此抵消：

```text
s_A XOR s_B XOR s_C
  = [Alice 付款] XOR [Bob 付款] XOR [Carol 付款].
```

所以偶数奇偶性表示 NSA 付款，奇数奇偶性表示某位密码学家付款。公开消息泄露了“是否有人
付款”这一位信息，却没有直接写出付款者的身份。

但这行代数只解释了协议直觉，还没有回答两个更严格的问题：每一种有限执行是否都正确；
观察者在听完消息后究竟能排除哪些世界。Task 6 分别处理这两层。

## 3. 32 个有限可能世界

一个完整世界由付款者和三枚硬币构成：

```text
(payer, c_AB, c_BC, c_CA)
```

付款者有 `NSA / Alice / Bob / Carol` 四种可能，三枚硬币有 `2³` 种赋值，因此标准模型恰好
包含：

```text
4 × 2³ = 32 个世界。
```

仓库中的有限 S5 模型把“知道”解释为可能世界之间的不可区分关系：

- 每位密码学家知道自己相邻的两枚硬币，以及自己是否付款；
- 外部观察者 Eve 起初不知道任何私有硬币，所以她的初始信息集合包含全部 32 个世界；
- 三位密码学家的三比特 transcript 被视为一次同时、真实的公开宣告；
- 宣告之后，只保留会产生同一 transcript 的世界。

这是标准的可能世界与公开宣告语义。语义背景可参阅 Fagin、Halpern、Moses、Vardi 的
*Reasoning About Knowledge*（[MIT Press](https://mitpress.mit.edu/9780262061629/reasoning-about-knowledge/)），
Plaza 的 “Logics of Public Communications”
（[DOI](https://doi.org/10.1007/s11229-007-9168-7)），以及 van Ditmarsch、van der Hoek、Kooi
的 *Dynamic Epistemic Logic*（[DOI](https://doi.org/10.1007/978-1-4020-5839-4)）。

## 4. 真正进入 Metamath 的两个证明

Task 6 现在向正式包导出两个定理，而不再把 Python 枚举本身称为 proof。

### 4.1 `dc_parity_table`

这个定理把全部 32 个付款者—硬币组合的奇偶性结论合取在一起。每一行的 XOR 结果都由
命题逻辑引理构造；NSA 付款的八行得到偶数结果，三位密码学家付款的二十四行得到奇数结果。

### 4.2 `dc_payer_bijection_table`

匿名性不仅需要“总奇偶性正确”，还需要不同付款者能够产生相同的完整公开 transcript。
这里使用一个具体双射：把付款者沿某条共享边从一端移到另一端，同时翻转这条边上的秘密
硬币，三位参与者的公开比特全部保持不变。

仓库检查三组付款者转移：

```text
Alice → Bob，翻转 c_AB
Bob → Carol，翻转 c_BC
Carol → Alice，翻转 c_CA
```

每组遍历八种硬币赋值，共形成 `3 × 8 = 24` 个 transcript 保持行。翻转同一条边两次会回到
原世界，因此该映射确实是有限集合之间的双射，而不只是单向配对。

证明构造器位于：

```text
src/proof_lab/tasks/task_06_dining_cryptographers/proofs/finite_tables.py
```

它没有使用 `.raw` 步骤，也没有加入“协议正确”之类的专用假设。由于当前依赖的
`metamath-logic` 版本没有完整导出真值常量所需的定义，证明保守地以定理 `φ → φ` 表示真，
以它的否定表示假；XOR 节点由 `df-xor`、`xnor`、双条件和否定引理推出，最后用 `pm3.2i`
把所有独立行合取为两个根定理。最终生成的 `.mm` 文件由 `mmverify` 重新检查，而不是信任
Python 构造器的计算结果。

## 5. 两种独立表示之间怎样衔接

形式真值表与 S5 协议模型是两套独立实现。若二者共用同一个 transcript 函数，它们即使同时
写错也可能彼此“验证”通过。因此测试只开放一个很窄的观察接口，在全部 32 个世界逐一比较：

```text
formal_transcript_bits(payer, coins)
    == transcript_for(TRIANGLE_TOPOLOGY, world)
```

这个桥接测试不代替 Metamath 证明；它审计的是“形式表中的第几位硬币、哪位付款者”确实与
语义模型采用相同约定。内核负责检查命题推导，测试负责检查形式编码与所描述协议之间的对应。

## 6. 计算模型另外核验了什么

在 Metamath 两个有限表之外，Python 模型还穷尽检查了：

1. 公开 transcript 之后，Eve 知道是 NSA 付款还是某位密码学家付款；
2. 当密码学家付款时，Eve 仍把 Alice、Bob、Carol 三人都保留为候选者；
3. 任一诚实未付款者仍把另外两人都保留为候选者；
4. 在独立均匀硬币假设下，三位付款者诱导完全相同的 transcript 计数分布；
5. 若删除 Carol 的两条共享边，协议仍满足奇偶性正确，却出现六个匿名性反例。

最后一项是有意加入的红队校准：它说明“功能正确”并不自动推出“安全”。

## 7. 证据边界

当前可以严格称作 Metamath 证明的只有：

- 32 行协议奇偶性表；
- 24 行付款者双射与 transcript 保持表。

知识关系、公开宣告后的模型收缩、候选者集合投影、精确计数和坏拓扑搜索仍由 Python 有限模型
核验。它们是对指定有限模型的穷尽计算，不是抽样实验，但也还不是模态逻辑内核中的定理。
下一步若要越过这条边界，需要实现一个能产生证明对象的有限模态逻辑到命题逻辑的 lowering，
并为计数聚合生成可检查证书。

## 8. 本轮实现过程与用时

这项工作分成两个连续阶段：最初的 PR #2 建立 32 世界 S5 模型、正确性与匿名性检查以及坏拓扑
反例；随后审计发现其中没有 Task 6 的 Metamath proof，PR #3 才补入上述两个正式定理、独立
桥接测试、声明账本和证据边界文档。

在 ProofScaffold、`metamath-logic`、有限 S5 解释器和 Task 6 语义 demo 已经存在的基础上，
从识别缺口到完成两个证明构造器、处理真值常量依赖问题、跑通完整 `mmverify`、CI 并合并，
大约用了 **2～3 小时**。这个数字描述的是本轮集成与形式化工作，不包括此前底层证明工具、
逻辑库和有限模型框架的建设时间。

PR #3 在两个 CI job 都成功后以 squash 方式合并：

- [PR #3：add formal proofs for Dining Cryptographers](https://github.com/epistemic-frontier/proof-lab/pull/3)
- [合并提交 `4f9b18c`](https://github.com/epistemic-frontier/proof-lab/commit/4f9b18cb60ab6583bfd43e553a8df5ac4eeece69)

合并前的结果为：34 个 Python 测试通过，task/claim schema 通过；正式包覆盖率为 6 个声明定理、
279 个实际发射定理、0 个声明但未发射的定理，并明确出现：

```text
verifying dc_parity_table
verifying dc_payer_bijection_table

OK
mmverify OK rc=0
```

复现命令：

```bash
uv run --frozen python -m proof_lab.tasks.task_06_dining_cryptographers
uv run --frozen pytest -q
uv run --frozen skfd verify proof-lab --level 1 --coverage declared
```

因此，这个 demo 的准确表述是：它已经包含两个由 Metamath 内核接受的有限命题证明，并以
穷尽有限 S5 模型补充知识与攻击证据；它还不是一个完整的模态安全证明。
