#encode:utf-8

import numpy as np
from collections import deque
import random

from GridMap import GridMap
from Agent import Agent
from State import State
from Controller import Controller

alpha = 0.1
gamma = 0.1
epsilon = 0.95
turn = 100
episode = 10000


class Montecarlo():

  def __init__(self, grid:GridMap):
    self.q = np.zeros((grid.width, grid.hight, 5, 4))
    self.st = deque()
    self.act = deque()
    self.reward = deque()
    self.total_reward = 0
    self.now_turn = 1
    self.now_episode = 1
  

  def getReward(self, chaser:Agent, target:Agent, state:State):
    if state.isOverlap(chaser, target):
      return -500
    elif self.now_turn == turn:
      return 500
    elif state.get_isFind():
      return -1
    elif state.get_isOutOfVision():
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


  def writeReward(self, chaser:Agent, target:Agent, state:State):

    #報酬を記録
    rw = self.getReward(chaser, target, state)
    self.total_reward += rw
    self.reward.append(rw)


  def updateQValue(self):
    
    while len(self.st):
      tmp_state = self.st.pop()
      tmp_act = self.act.pop()
      tmp_reward = self.reward.pop()

      self.total_reward = tmp_reward + self.total_reward * gamma
      self.q[tmp_state[0]][tmp_state[1]][tmp_state[2]][tmp_act] = (1-alpha)*self.q[tmp_state[0]][tmp_state[1]][tmp_state[2]][tmp_act] + self.total_reward


  def proceedTurn(self, chaser:Agent, target:Agent, state:State, grid:GridMap, ctr:Controller):

    self.doAction(chaser, target, grid, state)
    ctr.chaseTarget(chaser, target, grid, state)
    self.writeReward(chaser, target, state)

    if state.isOverlap(chaser, target):
      ctr.gameSet(chaser, target, grid, state)
      self.updateQValue()
      self.now_turn = 1
      self.now_episode += 1
    else:
      self.now_turn += 1

  


    
