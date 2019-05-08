import random
import copy

from tribute import Tribute
from team import Team


MAX_ENV_SURVIVE_CHANCE = 0.9


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
        self.ticks = 0
        self.teams = []
        self.tributes = self._create_tributes(tribute_count)
        self.history = []
        self.initialise_teams()

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
        self.join_teams()

    def join_teams(self, join_count=4):
        for i in range(join_count):
            if len(self.teams) > 1:
                t1 = random.choice(self.teams)
                t2 = random.choice(self.teams)
                t1.merge_in_team(t2)
        self.prune_teams()

    def prune_teams(self):
        for team in self.teams:
            team.prune_dead()

        self.teams = [t for t in self.teams if not t.is_empty()]

    def print_all_teams(self):
        for team in self.teams:
            print(team)

    def game_over(self):
        return len(self.tributes_left()) <= 1

    def tributes_left(self):
        return [t for t in self.tributes if t.alive]

    def tributes_left_count(self):
        return len(self.tributes_left())

    def environment_death(self):
        for t in self.tributes:
            if (t.strength/100.0 * MAX_ENV_SURVIVE_CHANCE < random.random()):
                t.kill('Environment')
        self.prune_teams()

    def split_team(self):
        tm = random.choice(self.teams)
        try:
            tm.split_team()
            self.prune_teams()
        except IndexError:
            pass

    def apply_fatigue(self):
        for t in self.tributes:
            t.fatigue()
        self.prune_teams()

    def epoch(self):
        self.ticks += 1
        print()
        print('**** EPOCH {} ****'.format(self.ticks))
        self.environment_death()
        self.join_teams(2)
        self.split_team()
        self.apply_fatigue()
        self.print_all_teams()

if __name__ == "__main__":
    sim = Sim(100)
    sim.print_all_teams()

    while not sim.game_over():
        sim.epoch()

    print("Epochs: {}".format(sim.ticks))
    if sim.tributes_left_count() == 1:
        print('*** The Winner {} ***'.format(sim.tributes_left()[0]))
    else:
        print('*** No Winner This Year ***')
