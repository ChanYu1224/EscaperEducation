#encode:utf-8

import numpy as np
from collections import deque
import random
import copy

from GridMap import GridMap
from Agent import Agent
from State import State
from Controller import Controller

alpha = 0.8
ganma = 0.2
epsilon = 0.95
turn = 100
episode = 10000


dx = [1, -1, 0, 0, 0]
dy = [0, 0, 1, -1, 0]

class Q_learning():

  def __init__(self, grid:GridMap):
    self.q = np.zeros((grid.width, grid.hight, 5, 4))
    self.st = deque()
    self.act = deque()
    self.reward = deque()
    self.total_reward = 0
    self.now_turn = 1
    self.now_episode = 1
    self.rewardHistory = []
  

  def getReward(self, chaser:Agent, target:Agent, state:State):
    if state.isOverlap(chaser, target):
      return -500
    elif self.now_turn >= turn:
      return 1000
    elif state.get_isFind():
      return -1
    elif state.get_isOutOfVision():
      return 100
    else:
      return 1
  

  def getNextReward(self, chaser:Agent, target:Agent, state:State, grid:GridMap, nextDirection:int):
    
    tmp_chaser = copy.deepcopy(chaser)
    tmp_target = copy.deepcopy(target)
    tmp_state = copy.deepcopy(state)

    tmp_target.Walk(nextDirection)
    tmp_chaser.Walk(tmp_state.nextDirection(chaser, target, grid))

    if state.isOverlap(tmp_chaser, tmp_target):
      return -500
    elif self.now_turn+1 == turn:
      return 500
    elif tmp_state.get_isFind():
      return -1
    elif tmp_state.get_isOutOfVision():
      return 50
    else:
      return 1


  def doAction(self, chaser:Agent, target:Agent, grid:GridMap, state:State):
    
    #状態を記録
    now_st = state.getState(chaser, target)
    self.st.append(now_st)
    
    #行動の決定
    action = -1
    p = random.random()
    if p > epsilon or (not np.any(self.q[now_st[0]][now_st[1]][now_st[2]])):
      while True:
        action = random.randint(0,3)
        if state.canMoveDirection(target, grid, action):
          break
    else:
      max_q = -100000000
      for i in range(4):
        if max_q < self.q[now_st[0]][now_st[1]][now_st[2]][i] and state.canMoveDirection(target, grid, i):
          max_q = self.q[now_st[0]][now_st[1]][now_st[2]][i]
          action = i

    #行動を実行・記録
    target.Walk(action)
    self.act.append(action)

    #Q値更新
    nextMax_q = -100000000
    for i in range(4):
      if nextMax_q < self.q[now_st[0]+dx[action]][now_st[1]+dy[action]][now_st[2]][i] and grid.canMove(now_st[0]+dx[action]+dx[i], now_st[1]+dy[action]+dy[i]):
        nextMax_q = self.q[now_st[0]+dx[action]][now_st[1]+dy[action]][now_st[2]][i]
    
    self.q[now_st[0]+dx[action]][now_st[1]+dy[action]][now_st[2]][i] = (1-alpha)*self.q[now_st[0]][now_st[1]][now_st[2]][action] + alpha*(self.getReward(chaser, target, state) + ganma*nextMax_q)


  def writeReward(self, chaser:Agent, target:Agent, state:State):

    #報酬を記録
    rw = self.getReward(chaser, target, state)
    self.total_reward += rw
    self.reward.append(rw)

  def proceedTurn(self, chaser:Agent, target:Agent, state:State, grid:GridMap, ctr:Controller):

    self.doAction(chaser, target, grid, state)
    ctr.chaseTarget(chaser, target, grid, state)
    self.writeReward(chaser, target, state)

    if state.isOverlap(chaser, target):
      self.rewardHistory.append(self.total_reward)
      ctr.gameSet(chaser, target, grid, state)
      self.now_turn = 1
      self.now_episode += 1
      self.total_reward = 0
    else:
      self.now_turn += 1
  

  def greedy_doAction(self, chaser:Agent, target:Agent, grid:GridMap, state:State):
    now_st = state.getState(chaser, target)

    action = 0
    max_q = -100000000
    for i in range(4):
      if max_q < self.q[now_st[0]][now_st[1]][now_st[2]][i] and state.canMoveDirection(target, grid, i):
        max_q = self.q[now_st[0]][now_st[1]][now_st[2]][i]
        action = i
    
    target.Walk(action)


  def greedy_proceedTurn(self, chaser:Agent, target:Agent, state:State, grid:GridMap, ctr:Controller):
    self.greedy_doAction(chaser, target, grid, state)
    ctr.chaseTarget(chaser, target, grid, state)

    if state.isOverlap(chaser, target) or self.now_turn == turn:
      ctr.gameSet(chaser, target, grid, state)
      self.now_turn = 1
    else:
      self.now_turn += 1
  

  def get_nowEpisode(self):
    return self.now_episode

  


    