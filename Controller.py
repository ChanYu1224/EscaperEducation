#encode:utf-8

from GridMap import GridMap
from Agent import Agent
from State import State

class Controller():  

  def chaseTarget(self, chaser:Agent, target:Agent, grid:GridMap, state:State):

    dire = state.nextDirection(chaser, target, grid)
    chaser.Walk(dire)
  
  def gameSet(self, chaser:Agent, target:Agent, grid:GridMap, state:State):
    
    while state.isOverlap(chaser, target):
      chaser.Spawn(grid)
      target.Spawn(grid)