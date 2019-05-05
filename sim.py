import random

from tribute import Tribute
from team import Team


class Sim():
    def __init__(self, tribute_count=24):
        self.tributes = self._create_tributes(tribute_count)
        self.initialise_teams()

    def _create_tributes(self, count):
        tributes = []
        for i in range(count):
            t = Tribute(id=i)
            tributes.append(t)
        return tributes

    def initialise_teams(self):
        self.teams = []
        for t in self.tributes:
            new_team = Team([t])
            self.teams.append(new_team)
        self.shuffle_teams()

    def shuffle_teams(self, count=18):
        max_shuffle = len(self.teams) - count
        for i in range(max_shuffle):
            team_count = len(self.teams)
            t1 = self.teams[random.randint(0, team_count-1)]
            t2 = self.teams[random.randint(0, team_count-1)]
            t1.merge_in_team(t2)
        self.prune_teams()

    def prune_teams(self):
        for team in self.teams:
            team.prune_dead()

        self.teams = [t for t in self.teams if not t.is_empty()]

    def print_all_teams(self):
        for team in self.teams:
            print(team)

if __name__ == "__main__":
    sim = Sim()
    sim.print_all_teams()
