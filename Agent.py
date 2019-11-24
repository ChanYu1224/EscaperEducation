#encode:utf-8

import random

from GridMap import GridMap

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]

class Agent(object):

  def __init__(self, stamina_max=5, x=-1, y=-1):
    self.x = x
    self.y = y
    self.stamina = stamina_max
    self.stamina_max = stamina_max
    self.direction = 0
    self.direction_par = 0.0
    self.isFind = False


  def plus_direction_par(self):
    self.direction_par += 0.01
  

  def reset_direction_par(self):
    self.direction_par = 0.0
  

  def get_x(self):
    return self.x
  

  def get_y(self):
    return self.y
  
  
  def get_stamina(self):
    return self.stamina
  

  def get_direction(self):
    return self.direction


  def get_isFind(self):
    return self.isFind


  def consume_stamina(self):
    self.stamina -= 1
  

  def recover_stamina(self):
    self.stamina += 1
  

  def set_direction(self, dire):
    self.direction = dire
  

  def set_isFind(self, isfind):
    self.isFind = isfind


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
  

  def Walk(self, direction):
    """
    決められた方向に歩く．
    """
    self.x += dx[direction]
    self.y += dy[direction]

