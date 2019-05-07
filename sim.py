import random
import copy

from tribute import Tribute
from team import Team


ENV_DEATH_CHANCE = 0.1


# class Epoch():
#     def __init__(self, teams, tributes):
#         self.teams = teams
#         self.tributes = self.tributes

#     def environment_death(self):
#         for t in self.tributes:
#             if random.random() < ENV_DEATH_CHANCE:
#                 t.kill('Environment')


class Sim():
    def __init__(self, tribute_count=24):
        self.teams = []
        self.tributes = self._create_tributes(tribute_count)
        self.history = []
        self.initialise_teams()
        self.snapshot()

    def _create_tributes(self, count):
        tributes = []
        for i in range(count):
            t = Tribute(id=i)
            tributes.append(t)
        return tributes

    def initialise_teams(self):
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

    def snapshot(self):
        current_state = copy.deepcopy(self.teams)
        self.history.append(current_state)

    def game_over(self):
        return len(self.tributes_left()) <= 1

    def tributes_left(self):
        return [t for t in self.tributes if t.alive]

    def tributes_left_count(self):
        return len(self.tributes_left())

    def environment_death(self):
        for t in self.tributes:
            if random.random() < ENV_DEATH_CHANCE:
                t.kill('Environment')

    def epoch(self):
        self.environment_death()

        current_state = copy.deepcopy(self.teams)
        self.history.append(current_state)

if __name__ == "__main__":
    sim = Sim()
    sim.print_all_teams()

    while not sim.game_over():
        sim.epoch()

    print("Epochs: {}".format(len(sim.history)))
    if sim.tributes_left_count() == 1:
        print('*** The Winner {} ***'.format(sim.tributes_left()[0]))
    else:
        print('*** No Winner This Year ***')
