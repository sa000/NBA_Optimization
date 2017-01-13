
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
          self.position[pos]=0
        # for pos in positions:
        #   if pos in projection.Position.split('/'):
        #       self.position[pos] = 1
        #   else:
        #       self.position[pos] = 0
        if 'PG' in self.pos or 'SG' in self.pos and not 'SF' in self.pos:
          if self.salary>6000:
            self.position['PG']=1
          else:
            self.position['SG']=1
        # if 'SG' in self.pos:
        #   positions['SG']=1
        #SG/SF case
        if 'SG' in self.pos and 'SF' in self.pos:
          if self.salary<6000:
            self.position['SF']=1
            self.position['PF']=1
          elif self.salary>=6000 and self.salary<=7000:
            self.position['SF']=1
        #Pure SF
        if 'SF' in self.pos and not 'SG' in self.pos and not 'PF' in self.pos:
          if self.salary<7000:
            self.position['SF']=1
        #PF/C Case
        if 'PF' in self.pos and 'C' in self.pos:
          if self.salary>7000:
            self.position['PF']=1
        #PURE PF
        if 'PF' in self.pos and not 'SF' in self.pos and not 'C' in self.pos:
          if self.salary>7000:
            self.position['PF']=1
        #Pure C
        if 'C' in self.pos and not 'PF' in self.pos:
          self.position['C']=1
