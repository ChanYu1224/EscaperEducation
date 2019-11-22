#encode:utf-8

import queue

from Agent import Agent
from GridMap import GridMap


dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

INF = 10000


class State():

  def checkOverlap(self, chaser:Agent, target:Agent):
    return chaser.x == target.x and chaser.y == target.y
  
  def canHear(self, searcher:Agent, target:Agent, grid:GridMap):

    for i in range(-2,3):
      for j in range(-2,3):
        if not grid.canMove(searcher.x + i, searcher.y + j):
          continue
        elif searcher.x + i == target.x and searcher.y + j == target.y:
          return True
    
    return False
  
  def canWatch(self, searcher:Agent, target:Agent, grid:GridMap):
    
    q = queue.Queue()

    for i in range(4):

      move = 1
      while grid.canMove(searcher.x + dx[i]*move, searcher.y + dy[i]*move):
        if searcher.x + dx[i]*move == target.x and searcher.y + dy[i]*move == target.y:
          searcher.direction = i
          return True
        q.put([searcher.x + dx[i]*move, searcher.y + dy[i]*move])
        move += 1
      
      if i == 0 or i == 1:
        right = INF
        left = -INF

        while not q.empty():
          now = q.get()

          move = 1
          while grid.canMove(now[0], now[1] + move) and right >= move:
            if now[0] == target.x and now[1] + move == target.y:
              searcher.direction = i
              return True
            move += 1
          
          right = min(right, move)
          

          move = -1
          while grid.canMove(now[0], now[1] + move) and left <= move:
            if now[0] == target.x and now[1] + move == target.y:
              searcher.direction = i
              return True         
            move += -1
          
          left = max(left, move)

      else:
        right = INF
        left = -INF

        while not q.empty():
          now = q.get()

          move = 1
          while grid.canMove(now[0] + move, now[1]) and right >= move:
            if now[0] + move == target.x and now[1] == target.y:
              searcher.direction = i
              return True
            move += 1
          
          right = min(right, move)
          
          move = -1
          while grid.canMove(now[0] + move, now[1]) and left <= move:
            if now[0] + move == target.x and now[1] == target.y:
              searcher.direction = i
              return True
            move += -1

          left = max(left, move)
    
    return False