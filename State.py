#encode:utf-8

import queue
import random
import copy

from Agent import Agent
from GridMap import GridMap


dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

INF = 10000


class State():

  def reverse_direction(self, d):

    if d == 0:
      return 1
    if d == 1:
      return 0
    if d == 2:
      return 3
    if d == 3:
      return 2


  def enemyDirection(self, chaser:Agent, target:Agent):
    return self.reverse_direction(chaser.get_direction())


  def isOverlap(self, chaser:Agent, target:Agent):
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
  

  def isFind(self, chaser:Agent):
    return chaser.get_isFind()
  

  def nextDirection(self, chaser:Agent, target:Agent, grid:GridMap):
    
    if self.canHear(chaser, target, grid):
      chaser.set_isFind(True)

      q = queue.Queue()

      Visited = copy.deepcopy(grid.isWall)
    
      distance = [[-1 for i in range(grid.hight)] for i in range(grid.width)]

      Visited[target.x][target.y] = True
      q.put([target.x, target.y])

      while not q.empty():
        now = q.get()

        for i in range(4):

          if now[0] + dx[i] == chaser.get_x() and now[1] + dy[i] == chaser.get_y():
            return self.reverse_direction(i)
              

          if not Visited[now[0] + dx[i]][now[1] + dy[i]]:
            Visited[now[0] + dx[i]][now[1] + dy[i]] = True
            q.put([now[0]+dx[i], now[1]+dy[i]])


    if self.canWatch(chaser, target, grid):
      chaser.set_isFind(True)
      return chaser.get_direction()
    
    else:
      chaser.set_isFind(False)
      while True:
        if grid.canMove(chaser.get_x() + dx[chaser.get_direction()], chaser.get_y() + dy[chaser.get_direction()]):
          p = random.random()
          
          if p < chaser.direction_par:
            chaser.set_direction(random.randint(0,3))
            chaser.reset_direction_par()
            while not grid.canMove(chaser.get_x() + dx[chaser.get_direction()], chaser.get_y() + dy[chaser.get_direction()]):
              chaser.set_direction(random.randint(0,3))
          else:
            chaser.plus_direction_par()

          return chaser.get_direction()
        else:
          chaser.set_direction(random.randint(0,3))
  

  def getState(self, chaser:Agent, target:Agent):

    dire = self.enemyDirection(chaser, target)
    if not target.get_isFind():
      dire = 4
      
    return [target.get_x(), target.get_y, dire]
  

  def canMoveDirection(self, agent:Agent, grid:GridMap, dire):

    if agent.get_x()+dx[dire] < 0 or agent.get_y()+dy[dire] < 0 or agent.get_x()+dx[dire] >= grid.width or agent.get_y()+dy[dire] >= grid.hight:
      return False
    else:
      if grid.isWall[x+dx[dire]][y+dy[dire]]:
        return False
      else:
        return True