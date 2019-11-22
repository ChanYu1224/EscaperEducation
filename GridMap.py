#encode:utf-8

class GridMap():
  def __init__(self, w: int, h: int, isWall: list, screen_size: tuple, cells_size: tuple):
    self.width = w
    self.hight = h
    
    self.isWall = isWall

    #GUI上の座標の計算
    self.pos_x = [0 for _ in range(w+1)]
    self.pos_y = [0 for _ in range(h+1)]

    #縦横の比
    aspect = cells_size[0] / cells_size[1]

    #指定したサイズ内にグリッドが収まるように自動調整する 
    if w >= h*aspect:
      self.cell_size = cells_size[0] // w
    else:
      self.cell_size = cells_size[1] // h
    
    begin_x = (screen_size[0]-self.cell_size*w) // 2
    begin_y = (screen_size[1]-self.cell_size*h) // 2

    #各セル位置の計算
    for i in range(w+1):
      self.pos_x[i] = begin_x + self.cell_size*i
    for i in range(h+1):
      self.pos_y[i] = begin_y + self.cell_size*i
  
  
  def canMove(self, x, y):
    
    if x < 0 or y < 0 or x >= self.width or y >= self.hight:
      return False
    else:
      if self.isWall[x][y]:
        return False
      else:
        return True