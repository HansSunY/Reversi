# 人工智能导论大作业-黑白棋AI

## 实验内容

实验基于python tkinter库实现了一个图形化黑白棋人机对局程序，并实现了实时显示AI落子位置及思考时间等功能。其中AI部分实现了基于Minmax和Roxanne优先级策略的MCTS算法，在与人类玩家的对局中有较好的表现。

## 程序设计思路

实验基于python语言编写，程序划分为四个层次，分别由Board、Board_ui、monte_carlo和Play四个class定义。

### class Board

Board类定义棋盘状态（由一个8*8的numpy数组表示)及当前玩家，该类中方法包括在指定坐标位置落子、判断落子是否合法、判断当前对局状态等（是否获胜、是否有合法位置落子）。

### class Board_ui

Board_ui类使用tkinter库初始化绘制并动态更新棋盘UI，绑定鼠标点击事件，实现人类玩家点击位置落子操作以及玩家和AI轮流落子操作；同时实现按钮功能、弹窗功能及信息文本（AI落子时间、落子位置）的更新展示。

### class monte_carlo

monte_carlo类实现黑白棋AI算法，具体算法设计在后文详细介绍。

### class Play

Play类为整个程序的入口，负责初始化并启动程序。

## 算法设计

实验基于MCTS+Roxanne策略编写黑白棋AI，具体实现如下

### Roxanne策略

Roxanne在《Analysis of Monte Carlo Techniques in Othello》文中结合行动力、稳定子和各位置的权值等因素，给出了一张优先级表，如下所示：

![img](https://camo.githubusercontent.com/50f5c13d3df3d4d1d08e690549d786335ac3d60e329400d285cf93fc17885e12/687474703a2f2f692e696d6775722e636f6d2f347830716b35642e706e67)

本次实验将Roxanne优先级策略应用于MCTS的扩展和模拟过程中，以期更高效地选择最优棋步。

### MCTS

实验使用基于Minmax搜索的蒙特卡洛树算法，即UCT算法。在搜索树中的每个结点均包含当前棋盘状态、子结点列表、父结点、收益分数、结点访问次数以及结点深度。本实验中UCT算法每轮迭代分为以下四个步骤：

- 选择 从搜索树的根节点向下递归选择一个存在尚未被扩展子结点的结点，选择过程由UCB1算法实现。更新结点访问次数。
- 扩展 如果上步选择结点非终止结点，则使用Roxanne优先级策略扩展一个优先级更高的后继结点。
- 模拟 从扩展到的后继结点出发，模拟扩展搜索树，直到找到终止结点。其中模拟过程中也使用Roxanne优先级策略选择每一步的子节点。
- 反向传播 用模拟所得的胜负结果回溯更新模拟路径上结点的收益分数和访问次数。

考虑到初始棋盘状态下模拟过程所需时间成本较高，故在棋盘当前状态深度较浅时，适当减少迭代次数。设置迭代次数如下：

- 当根节点深度depth小于15时，设置迭代次数为60。
- 当根节点深度depth大于等于15时，设置迭代次数为150。

## 功能展示

### 选择是否先手并开始游戏

<img src="C:\Users\拂晓\AppData\Roaming\Typora\typora-user-images\image-20220427084920987.png" alt="image-20220427084920987" style="zoom:50%;" />

### 玩家落子后AI开始思考并落子

棋盘下方提示AI正在思考

<img src="C:\Users\拂晓\AppData\Roaming\Typora\typora-user-images\image-20220427085306209.png" alt="image-20220427085306209" style="zoom:50%;" />

AI落子并在棋盘下方显示落子位置（x，y）及花费时间

<img src="C:\Users\拂晓\AppData\Roaming\Typora\typora-user-images\image-20220427110751494.png" alt="image-20220427110751494" style="zoom: 50%;" />

<img src="C:\Users\拂晓\AppData\Roaming\Typora\typora-user-images\image-20220427085450954.png" alt="image-20220427085450954" style="zoom:50%;" />





### 当无合法棋步时给出提示并交换下棋方

<img src="C:\Users\拂晓\AppData\Roaming\Typora\typora-user-images\image-20220427085848162.png" alt="image-20220427085848162" style="zoom:50%;" />

### 游戏结束

显示获胜方及对局总时间

<img src="C:\Users\拂晓\AppData\Roaming\Typora\typora-user-images\image-20220427102140337.png" alt="image-20220427102140337" style="zoom:50%;" />

### 点击“重新开始”按钮重新开始游戏

<img src="C:\Users\拂晓\AppData\Roaming\Typora\typora-user-images\image-20220427090211133.png" alt="image-20220427090211133" style="zoom:50%;" />

## 代码及注释

见附件

## 实验中的重难点

1. 程序层次的设计。本人认为应注重策略与机制相分离的原则，尽力保证每个模块（UI、Board、AI）之间的独立性，同时保证每个模块之间的接口简洁和高效。如果编写前没有设计一个好的层次框架，那么在编写过程中会遇到很多问题，本人在实验中深有体会。
2. 对于各种终局情况的考虑和特殊处理。对于一些较为“特殊”的终局状态，如在终局前双方均无合法步数可走等，如果不做特殊处理，会导致出现子节点列表为空等情况。很多细节在实际编程中都要考虑到。
3. AI算法时间优化。本人一方面关注UCT算法中的迭代次数，考虑到棋局开始之初的模拟路径较长，可以适当减小迭代次数，实验中简单实现了一个分段的迭代次数；另一面，在模拟阶段结点depth较小时，会判断是否有必要考虑角点（前几步不可能落在角点），这样可以减少模拟阶段的判断次数，提高效率。本人在这方面的尝试较浅，日后需要更多的探索。