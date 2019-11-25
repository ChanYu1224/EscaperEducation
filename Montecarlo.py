#encode:utf-8

import numpy as np
from collections import deque
import random

from GridMap import GridMap
from Agent import Agent
from State import State

alpha = 0.1
gamma = 0.1
epsilon = 0.9


class Montecarlo():

  def __init__(self, grid:GridMap):
    self.q = np.zeros((grid.width, grid.hight, 5, 4))
    self.st = deque()
    self.act = deque()
    self.reward = deque()
    self.total_reward = 0
  

  def getReward(self, chaser:Agent, target:Agent, state:State):
    return


  def doAction(self, chaser:Agent, target:Agent, grid:GridMap, state:State):
    
    #状態を記録
    now_st = state.getState(chaser, target)
    self.st.append(now_st)
    
    #行動の決定
    action = -1
    p = random.random()
    if p > epsilon or (not np.any(self.q[now_st[0]][now_st[1]][now_st[2]])):
      action = random.randint(0,3)
      while not state.canMoveDirection(target, grid, action):
        action = random.randint(0,3)
    else:
      max_q = 0
      for i in range(4):
        if max_q < self.q[now_st[0]][now_st[1]][now_st[2]][i]:
          max_q = self.q[now_st[0]][now_st[1]][now_st[2]][i]
          action = i
    
    #行動を実行・記録
    target.Walk(action)
    self.act.append(action)


      
  


    
