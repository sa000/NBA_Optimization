import pandas as pd


class Player:


    def __init__(self, projection, variable):
        self.pulp_var = variable
        self.name = projection.Name
        self.team = projection.Team
        self.salary = projection.Salary
        self.projected = projection.Projected
        self.scored = projection.Scored
        self.position = {}
        self.pos=projection.Position #For output only
        self.count=0
        positions=['PG', 'SG', 'SF', 'PF', 'C']
        for pos in positions:
          if pos in projection.Position.split('/'):
              self.position[pos] = 1
          else:
              self.position[pos] = 0

