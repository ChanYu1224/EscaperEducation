#encode:utf-8

import random

from GridMap import GridMap

class Agent(object):
  def __init__(self, stamina_max=5, x=-1, y=-1):
    self.x = x
    self.y = y
    self.stamina = stamina_max
    self.stamina_max = stamina_max
    self.direction = 0
    self.direction_change_par = 0.0

  def Spawn(self, grid:GridMap):
    """
    def Spawn(self, grid:GridMap)
      エージェントをグリッドマップ上にスポーンさせる

      grid: スポーンさせるグリッドマップ
    """
    while True:
      tmp_x = random.randint(0, grid.width-1)
      tmp_y = random.randint(0, grid.hight-1)

      if not grid.isWall[tmp_x][tmp_y]:
        self.x = tmp_x
        self.y = tmp_y
        return
    
