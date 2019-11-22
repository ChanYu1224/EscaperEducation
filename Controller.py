#encode:utf-8
import queue
import random
import copy

from GridMap import GridMap
from Agent import Agent
from State import State

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

INF = 10000

class Controller():  

  def nextDirection(self, chaser:Agent, target:Agent, grid:GridMap, state:State):
    
    if state.canHear(chaser, target, grid):
      q = queue.Queue()

      Visited = copy.deepcopy(grid.isWall)
    
      distance = [[-1 for i in range(grid.hight)] for i in range(grid.width)]

      Visited[target.x][target.y] = True
      q.put([target.x, target.y])

      while not q.empty():
        now = q.get()

        for i in range(4):

          if now[0] + dx[i] == chaser.x and now[1] + dy[i] == chaser.y:
            return [-dx[i], -dy[i]]

          if not Visited[now[0] + dx[i]][now[1] + dy[i]]:
            Visited[now[0] + dx[i]][now[1] + dy[i]] = True
            q.put([now[0]+dx[i], now[1]+dy[i]])


    if state.canWatch(chaser, target, grid):
      return [dx[chaser.direction], dy[chaser.direction]]
    
    else:
      while True:
        if grid.canMove(chaser.x + dx[chaser.direction], chaser.y + dy[chaser.direction]):
          p = random.random()
          
          if p < chaser.direction_change_par:
            chaser.direction = random.randint(0,3)
            chaser.direction_change_par = 0.0
          else:
            chaser.direction_change_par += 0.01

          return [dx[chaser.direction], dy[chaser.direction]]
        else:
          chaser.direction = random.randint(0,3)
  

  def chaseTarget(self, chaser:Agent, target:Agent, grid:GridMap, state:State):

    dire = self.nextDirection(chaser, target, grid, state)

    chaser.x += dire[0]
    chaser.y += dire[1]