import math
import tkinter
from tkinter import messagebox
import numpy as np
import time

class Board_ui:
    '''
    棋盘UI
    '''
    def __init__(self,board):
        '''
        :param board: 当前棋盘状态
        time_begin: 对局开始时间
        canvas: 画布
        board_now: 当前棋盘，8*8 numpy.array
        text: 画布中文本框，用于显示AI落子位置与花费时间
        '''
        self.time_begin=time.time()
        self.board_now=board
        windows = tkinter.Tk()
        windows.title('Reversi board')
        canvas = tkinter.Canvas(windows, width=640, height=800, bg='white')
        self.canvas = canvas
        self.text=0
        for i in range(9):
            canvas.create_line(i * 80, 0, i * 80, 640, fill='black')
            canvas.create_line(0, i * 80, 640, i * 80, fill='black')
        canvas.create_oval(3 * 80, 3 * 80, 4 * 80, 4 * 80, fill='white', outline='black')
        canvas.create_oval(4 * 80, 3 * 80, 5 * 80, 4 * 80, fill='black', outline='black')
        canvas.create_oval(3 * 80, 4 * 80, 4 * 80, 5 * 80, fill='black', outline='black')
        canvas.create_oval(4 * 80, 4 * 80, 5 * 80, 5 * 80, fill='white', outline='black')
        button1 = tkinter.Button(text="重新开始",command=self.reset)
        button1.configure(width=20,height=3,activebackground="#33B5E5", relief='flat')
        canvas.create_window(245, 700, anchor='nw', window=button1)
        canvas.bind("<Button-1>", self.mouse_click)
        canvas.pack()
        if messagebox.askyesno("选择", "是否先手持黑子?")==True:
            self.player=1
        else:
            self.player=0
            think = self.canvas.create_text(320, 650, text="AI正在思考...", font=("Purisa", 10), tag="text")
            self.canvas.update()
            self.canvas.delete(think)
            time_start = time.time()
            ai = monte_carlo(self.board_now)
            board_next = ai.uct_search()
            time_end = time.time()
            if self.text != 0:
                self.canvas.delete(self.text)
            if board_next.pos[0] != None:
                self.text = self.canvas.create_text(320, 650, text="AI落子位置(%d,%d),花费时间:%.1fs" % (
                board_next.pos[0] + 1, board_next.pos[1] + 1, time_end - time_start), font=("Purisa", 10), tag="text")
            else:
                self.text = self.canvas.create_text(320, 650, text="AI无合法落子位置,花费时间:%.1fs" % (time_end - time_start),
                                                    font=("Purisa", 10), tag="text")
            self.update_board(board_next.board)

        windows.mainloop()

    def update_board(self,board_):
        '''
        :param board_:待更新的棋盘状态
        '''
        canvas=self.canvas
        self.board_now=board_
        board=board_.board
        for i in range(8):
            for j in range(8):
                if board[i][j]==0:
                    canvas.create_oval(j * 80, i * 80, (j+1) * 80, (i+1) * 80, fill='white', outline='black')
                elif board[i][j]==1 :
                    canvas.create_oval(j * 80, i * 80, (j + 1) * 80, (i + 1) * 80, fill='black', outline='black')
        if board_.win()==0:
            time_over=time.time()
            messagebox.showinfo("游戏结束","获胜方为白方！总用时%.1fs"%(time_over-self.time_begin))
        elif board_.win()==1:
            time_over = time.time()
            messagebox.showinfo("游戏结束","获胜方为黑方！总用时%.1fs"%(time_over-self.time_begin))
        elif board_.win()==0.5:
            time_over = time.time()
            messagebox.showinfo("游戏结束","平局！总用时%.1fs"%(time_over-self.time_begin))

        canvas.update()

    def mouse_click(self,event):
        '''
        鼠标点击事件，玩家落子后AI落子
        '''
        board_now=self.board_now
        if board_now.pass_step()==True:
            board_now.player=1-board_now.player
            messagebox.showinfo("提示", "无合法棋步!")
            bool=True
        else:
            y=event.x
            x=event.y
            y=int(y/80)
            x=int(x/80)
            if x<8 and y<8:
                bool=board_now.move(x,y)
                self.update_board(board_now)
        if bool==True and board_now.win()==-1:
            time_start=time.time()
            if self.text!=0:
                self.canvas.delete(self.text)
            think=self.canvas.create_text(320, 650, text="AI正在思考...", font=("Purisa", 10), tag="text")
            self.canvas.update()
            self.canvas.delete(think)
            ai = monte_carlo(self.board_now)
            board_next = ai.uct_search()
            time_end=time.time()
            if board_next.pos[0]!=None:
                self.text=self.canvas.create_text(320, 650, text="AI落子位置(%d,%d),花费时间:%.1fs"% (board_next.pos[0]+1,board_next.pos[1]+1,time_end-time_start), font=("Purisa", 10),tag="text")
            else:
                self.text=self.canvas.create_text(320, 650, text="AI无合法落子位置,花费时间:%.1fs" % (time_end - time_start), font=("Purisa", 10), tag="text")
            self.update_board(board_next.board)

    def reset(self):
        '''
        重置对局
        '''
        self.board_now=Board(fboard.copy())
        self.canvas.delete("all")
        for i in range(9):
            self.canvas.create_line(i * 80, 0, i * 80, 640, fill='black')
            self.canvas.create_line(0, i * 80, 640, i * 80, fill='black')

        self.canvas.create_oval(3 * 80, 3 * 80, 4 * 80, 4 * 80, fill='white', outline='black')
        self.canvas.create_oval(4 * 80, 3 * 80, 5 * 80, 4 * 80, fill='black', outline='black')
        self.canvas.create_oval(3 * 80, 4 * 80, 4 * 80, 5 * 80, fill='black', outline='black')
        self.canvas.create_oval(4 * 80, 4 * 80, 5 * 80, 5 * 80, fill='white', outline='black')
        button1 = tkinter.Button(text="重新开始", command=self.reset)
        button1.configure(width=20, height=3, activebackground="#33B5E5", relief='flat')
        self.canvas.create_window(245, 700, anchor='nw', window=button1)
        self.time_begin = time.time()
        if messagebox.askyesno("选择", "是否先手持黑子?")==True:
            self.player=1
        else:
            self.player=0
            think = self.canvas.create_text(320, 650, text="AI正在思考...", font=("Purisa", 10), tag="text")
            self.canvas.update()
            self.canvas.delete(think)
            time_start = time.time()
            ai = monte_carlo(self.board_now)
            board_next = ai.uct_search()
            time_end = time.time()
            if self.text != 0:
                self.canvas.delete(self.text)
            if board_next.pos[0] != None:
                self.text = self.canvas.create_text(320, 650, text="AI落子位置(%d,%d),花费时间:%.1fs" % (
                board_next.pos[0] + 1, board_next.pos[1] + 1, time_end - time_start), font=("Purisa", 10), tag="text")
            else:
                self.text = self.canvas.create_text(320, 650, text="AI无合法落子位置,花费时间:%.1fs" % (time_end - time_start),
                                                    font=("Purisa", 10), tag="text")
            self.update_board(board_next.board)

class Board:
    '''
    棋盘状态
    '''
    def __init__(self,board,player=1):
        '''
        :param board: 当前棋盘，8*8 numpy.array
        :param player: 当前玩家，默认为1（黑）
        '''
        self.player=player
        self.board=board

    def move(self,x,y):
        '''
        在(x,y)位置落子
        :param x: 横坐标
        :param y: 纵坐标
        '''
        valid,board_new=self.is_valid(x,y)
        if valid:
            self.board=board_new.copy()
            self.player=1-self.player
            return True
        else:
            self.board=self.board
            return False

    def is_valid(self,x,y):
        '''
        判断(x,y)处落子是否合法
        :param x: 横坐标
        :param y: 纵坐标
        '''
        dir_ = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        board_new=self.board.copy()
        if board_new[x][y]==1 or board_new[x][y]==0:
            return False,board_new
        board_new[x][y]=self.player
        valid=False
        for d in range(8):
            i = x + dir_[d][0]
            j = y + dir_[d][1]
            while 0 <= i and i < 8 and 0 <= j and j < 8 and board_new[i][j] == 1-self.player:
                i += dir_[d][0]
                j += dir_[d][1]
            if 0 <= i and i < 8 and 0 <= j and j < 8 and board_new[i][j] == self.player:
                while True:
                    i -= dir_[d][0]
                    j -= dir_[d][1]
                    if i == x and j == y:
                        break
                    valid = True
                    board_new[i][j] = self.player
        return valid,board_new

    def win(self):
        '''
        判断是否为终局状态
        '''
        board_now=self.board.copy()
        white_num=0
        black_num=0
        white_flag=0
        black_flag=0
        if self.pass_step():
            self.player=1-self.player
            if self.pass_step():
                for i in range(8):
                    for j in range(8):
                        if board_now[i][j] == 0:
                            white_num += 1
                        elif board_now[i][j] == 1:
                            black_num += 1
                if black_num > white_num:
                    return 1
                elif black_num < white_num:
                    return 0
                return 0.5
            else:
                self.player=1-self.player
        for i in range(8):
            for j in range(8):
                if board_now[i][j]==0:
                    white_flag=1
                elif board_now[i][j]==1:
                    black_flag=1
        if white_flag==0:
            return 1
        elif black_flag==0:
            return 0
        for i in range(8):
            for j in range(8):
                if board_now[i][j]==0:
                    white_num+=1
                elif board_now[i][j]==1:
                    black_num+=1
                else:
                    return -1
        if black_num>white_num:
            return 1
        elif black_num<white_num:
            return 0
        return 0.5

    def pass_step(self):
        for i in range(8):
            for j in range(8):
                if self.is_valid(i,j)[0]==True:
                    return False
        return True

'''
Roxanne优先级表
'''
roxanne_table = [[(0, 0), (0, 7), (7, 0), (7, 7)],
                 [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3), (3, 4), (3, 5),
                  (4, 2), (4, 3), (4, 4), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)],
                 [(2, 0), (3, 0), (4, 0), (5, 0), (2, 7), (3, 7), (4, 7), (5, 7),
                  (0, 2), (0, 3), (0, 4), (0, 5), (7, 2), (7, 3), (7, 4), (7, 5)],
                 [(2, 1), (3, 1), (4, 1), (5, 1), (2, 6), (3, 6), (4, 6), (5, 6),
                  (1, 2), (1, 3), (1, 4), (1, 5), (6, 2), (6, 3), (6, 4), (6, 5)],
                 [(0, 1), (1, 0), (1, 1), (1, 6), (0, 6), (1, 7),
                  (6, 1), (6, 0), (7, 1), (6, 6), (6, 7), (7, 6)]]

class monte_carlo:
    '''
    AI算法，基于UCT以及Roxanne策略
    '''
    class node:
        '''
        搜索树中结点
        '''
        def __init__(self,board,score,depth,parent=None,visit_num=0,pos=(None,None)):
            '''
            :param board: 棋盘状态
            :param score: 结点得分
            :param depth: 结点深度
            :param parent: 父节点
            :param visit_num: 结点访问次数
            :param pos: 最近一次落子位置(相较于父节点)
            child_nodes: 子节点列表
            '''
            self.child_nodes=[]
            self.board=board
            self.score=score
            self.visit_num=visit_num
            self.parent=parent
            self.depth=depth
            self.pos=pos

    def __init__(self,board):
        '''
        :param board: 棋盘状态
        '''
        self.board_now=board
        num=0
        for i in range(8):
            for j in range(8):
                if board.board[i][j]==-1:
                    num+=1
        self.fnode=self.node(board,0,64-num)

    def get_chiled_nodes(self,node):
        '''
        获取结点的子结点列表
        '''
        if node.board.pass_step():
            board_child=Board(node.board.board.copy(),1-node.board.player)
            child_node=self.node(board_child,0,node.depth+1,node,0)
            node.child_nodes.append(child_node)
        else:
            for i in range(8):
                for j in range(8):
                    if node.board.board[i][j]==-1:
                        if node.board.is_valid(i,j)[0]:
                            board_child=node.board.board.copy()
                            board_child=Board(board_child,node.board.player)
                            board_child.move(i,j)
                            child_node=self.node(board_child,0,node.depth+1,node,0,(i,j))
                            node.child_nodes.append(child_node)

    def uct_search(self):
        '''
        UCT算法
        max_iter_num: 算法迭代次数
        '''
        if self.fnode.depth<15:
            max_iter_num=60
        else:
            max_iter_num=150
        for i in range(max_iter_num):
            node_select=self.select_policy()
            node_final=self.simulate_policy(node_select)
            self.back_propagate(node_final)
        best=self.UCB1(self.fnode,1.414)
        return best

    def select_policy(self):
        '''
        选择及扩展
        '''
        node_select=self.fnode
        self.get_chiled_nodes(node_select)
        while node_select.board.win()==-1:
                if node_select.child_nodes[0].visit_num==0 and node_select.child_nodes[0].pos==(None,None):
                    return node_select.child_nodes[0]
                elif node_select.child_nodes[0].visit_num!=0 and node_select.child_nodes[0].pos==(None,None):
                    node_select=node_select.child_nodes[0]
                    if len(node_select.child_nodes) == 0:
                        self.get_chiled_nodes(node_select)
                else:
                    if node_select.depth>15:
                        for node in node_select.child_nodes:
                            if (node.pos in roxanne_table[0]) and node.visit_num==0:
                                return node
                    for node in node_select.child_nodes:
                        if (node.pos in roxanne_table[1]) and node.visit_num == 0:
                            return node
                    for node in node_select.child_nodes:
                        if (node.pos in roxanne_table[2]) and node.visit_num==0:
                            return node
                    for node in node_select.child_nodes:
                        if (node.pos in roxanne_table[3]) and node.visit_num==0:
                            return node
                    for node in node_select.child_nodes:
                        if (node.pos in roxanne_table[4]) and node.visit_num==0:
                            return node
                    node_select=self.UCB1(node_select,1.414)
                    if len(node_select.child_nodes)==0:
                        self.get_chiled_nodes(node_select)
        return node_select

    def simulate_policy(self, node_select_):
        '''
        模拟
        :param node_select_: 选择并扩展后得到的结点
        '''
        node_select = node_select_
        flag = 0
        while node_select.board.win() == -1:
            flag=0
            if len(node_select.child_nodes) == 0:
                self.get_chiled_nodes(node_select)
            for node in node_select.child_nodes:
                if (node.pos in roxanne_table[0]) and node.visit_num == 0:
                    node_select = node
                    flag = 1
                    break
            if flag != 1:
                for node in node_select.child_nodes:
                    if (node.pos in roxanne_table[1]) and node.visit_num == 0:
                        node_select = node
                        flag = 1
                        break
                if flag != 1:
                    for node in node_select.child_nodes:
                        if (node.pos in roxanne_table[2]) and node.visit_num == 0:
                            node_select = node
                            flag = 1
                            break
                    if flag != 1:
                        for node in node_select.child_nodes:
                            if (node.pos in roxanne_table[3]) and node.visit_num == 0:
                                node_select = node
                                flag = 1
                                break
                        if flag != 1:
                            for node in node_select.child_nodes:
                                if (node.pos in roxanne_table[4]) and node.visit_num == 0:
                                    node_select = node
                                    flag = 1
                                    break
                            if flag!=1:
                                node_select=node_select.child_nodes[0]
        return node_select

    def back_propagate(self,node_final):
        '''
        反向传播
        :param node_final: 模拟得到的终局结点
        '''
        node=node_final
        final_score=node_final.board.win()
        while node is not None:
            node.visit_num+=1
            if node.board.player==0:
                node.score+=final_score
            elif node.board.player==1:
                node.score-=final_score
            node=node.parent

    def UCB1(self,node,C):
        '''
        UCB1算法
        :param node: 当前结点
        :param C: 超参数C
        '''
        list=[]
        for child_node in node.child_nodes:
            if child_node.visit_num!=0:
                ucb=child_node.score/child_node.visit_num+math.sqrt(C*2*math.log(node.visit_num)/child_node.visit_num)
                list.append(ucb)
            else:
                list.append(-100)
        index=list.index(max(list))
        return node.child_nodes[index]
'''
初始化棋盘
'''
fboard=np.array([-1]*64).reshape(8,8)
fboard[3][3]=0
fboard[3][4]=1
fboard[4][3]=1
fboard[4][4]=0

class Play:
    '''
    启动游戏
    '''
    def __init__(self):
        self.begin()

    def begin(self):
        board=Board(fboard.copy())
        board_ui=Board_ui(board)

game=Play()

