#encoding:utf-8

import pygame
from pygame.locals import *
import sys,os
import numpy as np
import time
import copy

def cell_update(x,y,A):
    status = A[x][y]
    count = 0
    X,Y = A.shape
    for i in range(-1,2):
        for j in range(-1,2):
            if i != 0 or j != 0:
                #端処理
                if x+i < 0:
                    if 0 <= y+j < Y:
                        if A[X-1][y+j] == 1:
                            count += 1
                elif x+i >= X:
                    if 0 <= y+j < Y:
                        if A[0][y+j] == 1:
                            count += 1
                elif y+j < 0:
                    if A[x+i][Y-1] == 1:
                        count += 1
                elif y+j >= Y:
                    if A[x+i][0] == 1:
                        count += 1
                elif A[x+i][y+j] == 1:
                    count += 1
    if status == 0 and count == 3:#誕生
        return 1
    elif status == 1:
        if count == 2 or count == 3:#生存(維持)
            return 1
        elif count<=1 or count >= 4:#過疎 or 過密
            return 0
        else:print("error")
    return 0

def cell_update2(x,y,A_):
    status = A_[x+1][y+1]
    count = np.count_nonzero(A_[x:x+3,y:y+3] == 1)
    count -= status
    if status == 0 and count == 3:#誕生
        return 1
    elif status == 1:
        if count == 2 or count == 3:#生存(維持)
            return 1
        elif count<=1 or count >= 4:#過疎 or 過密
            return 0
        else:print("error")
    return 0

def status_update(A):#A.shape
    X,Y = A.shape
    B = np.zeros((X,Y),dtype = "bool")
    # 周囲をコピー
    A_ = copy.deepcopy(A)
    upper = np.concatenate([[A[-1,-1]],A[-1],[A[-1,0]]],axis = 0)
    lower = np.concatenate([[A[0,-1]],A[0],[A[0,0]]],axis = 0)
    right = A[:,0].reshape((Y,-1))
    left = A[:,-1].reshape((Y,-1))
    A_ = np.concatenate([left,A_,right], axis = 1)
    A_ = np.concatenate([[upper],A_,[lower]], axis = 0)
    for i in range(X):
        for j in range(Y):
            # B[i][j] = cell_update(i,j,A)
            B[i][j] = cell_update2(i,j,A_)
    return B

def printlife(A):#表示機能
    X,Y = A.shape
    for i in range(len(A[0])):
        for j in range(len(A[1])):
            if A[i][j]==1:
                print(" ■",end="")
            else:
                print(" □",end="")
        print("")
    print("")
    return 0

def load_life(life,A):
    try:
        for i in range(len(life)):
            x,y=life[i]
            A[x,y]=1
    except:
        print(sys.exc_info())
    return A

def main():
    state = False
    button = False
    X = 600
    Y = 600
    cell_size = 6
    pygame.init()
    screen = pygame.display.set_mode((X,Y))
    pygame.display.set_caption("LIFE GAME")
    A = np.zeros((int(X/cell_size),int(Y/cell_size)), dtype = "bool")
    #life_game　図鑑　wikipedia参照　https://ja.wikipedia.org/wiki/%E3%83%A9%E3%82%A4%E3%83%95%E3%82%B2%E3%83%BC%E3%83%A0
    #グライダー銃
    life = [[1,25],[2,23],[2,25],[3,13],[3,14],[3,21],[3,22],[3,35],[3,36],[4,12],[4,16],[4,21],[4,22],\
    [4,35],[4,36],[5,1],[5,2],[5,11],[5,17],[5,21],[5,22],[6,1],[6,2],[6,11],[6,15],[6,17],[6,18],\
    [6,23],[6,25],[7,11],[7,17],[7,25],[8,12],[8,16],[9,13],[9,14]]
    #どんぐり
    life_2 = [[41,42],[42,44],[43,41],[43,42],[43,45],[43,46],[43,47]]
    #ダイハード
    life_3 = [[22,28],[23,22],[23,23],[24,23],[24,27],[24,28],[24,29]]
    #horizontal_line
    life_4 = []
    for i in range(Y//cell_size):
        life_4.append([(X//cell_size)//2,i])
        # life_4.append(i)
    #vertical_line
    life_5 = []
    for i in range(X//cell_size):
        life_5.append([i,(X//cell_size)//2])
    # life_6 = convert.convert(X,Y,cell_size)
    A = load_life(life,A)
    sleep_time = 0
    while(1):
        before = time.time()
        screen.fill((0,0,0))
        #vertical line
        for i in range(int(X/cell_size)):
            pygame.draw.line(screen,(0,95,0),(i*cell_size,0),(i*cell_size,Y),1)
        #horizontal line
        for j in range(int(Y/cell_size)):
            pygame.draw.line(screen,(0,95,0),(0,j*cell_size),(X,j*cell_size),1)
        #イベント処理
        for event in pygame.event.get():
            #カーソル操作時
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                x_pix,y_pix = event.pos
                A[y_pix//cell_size][x_pix//cell_size] = not(A[y_pix//cell_size][x_pix//cell_size])
                button = True
            if event.type == MOUSEBUTTONUP and event.button == 1:
                button = False
            if  event.type == MOUSEMOTION and button == True:
                x_pix,y_pix = event.pos
                A[y_pix//cell_size][x_pix//cell_size] = 1
                # not(A[y_pix//cell_size][x_pix//cell_size])
            #終了用イベント
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #キー入力時
            if event.type == pygame.KEYDOWN:
                #終了機能
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_BACKSPACE:
                    A = np.zeros((int(X/cell_size),int(Y/cell_size)))
                if event.key == K_1: load_life(life,A)
                if event.key == K_2: load_life(life_2,A)
                if event.key == K_3: load_life(life_3,A)
                if event.key == K_4: load_life(life_4,A)
                if event.key == K_5: load_life(life_5,A)
                if event.key == K_6:pass
                if event.key == K_7:pass
                if event.key == K_8:pass
                if event.key == K_9:pass
                if event.key == K_0: A=np.zeros((A.shape))
                #pause機能
                if event.key == pygame.K_SPACE: state=not(state)
                if event.key == K_RIGHT: sleep_time = max(0,sleep_time - 0.1)
                if event.key == K_LEFT: sleep_time += 0.02
        #cell表示
        x,y = np.where(A == 1)
        for i,v in enumerate(x):
            # print(x[k],y[k])
            pygame.draw.rect(screen,(0,95,0),(y[i]*cell_size,x[i]*cell_size,cell_size,cell_size))
            #最初の２変数はx,y座標、後ろの２変数は長方形のサイズ
        pygame.display.update()

        #running

        if state == 0:
            A = status_update(A)
            time.sleep(sleep_time)
        #pause
        elif state == 1:
            pass
        # print(time.time() - before)

if __name__ == "__main__":
    main()
