import random
import math

from tribute import Tribute
from team import Team


ENV_ATTACK_PC = 0.01
MAX_ENV_SURVIVE_PC = 0.99

TEAM_JOIN_START_PC = 0.9
TEAM_JOIN_EPOCH_PC = 0.1


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
        self.join_teams(pc_teams=TEAM_JOIN_START_PC)

    def join_teams(self, pc_teams):
        # pc_teams is the percent of teams to merge
        team_count = len(self.teams)
        if team_count > 1:
            joins = math.ceil(team_count * pc_teams)
            # Low number of teams forces joins to often
            # so we use roll the dice
            if joins > 2 or random.random() > 0.5:
                for i in range(joins):
                    if len(self.teams) > 1:
                        t1 = random.choice(self.teams)
                        t2 = random.choice(self.teams)
                        t1.merge_in_team(t2)
        self.prune_teams()

    def prune_teams(self):
        for team in self.teams:
            team.prune_dead()

        self.teams = [t for t in self.teams if not t.is_empty()]

    def update_leader_stats(self):
        for team in self.teams:
            leader = team.leader
            if len(team) > 1 and leader.alive:
                team.leader.led_ticks += 1

    def print_all_teams(self):
        for team in self.teams:
            print(team)

    def game_over(self):
        return len(self.tributes_left()) <= 1

    def tributes_left(self):
        return [t for t in self.tributes if t.alive]

    def tributes_left_count(self):
        return len(self.tributes_left())

    def environment_death(self, tick=None):
        for t in self.tributes:
            if random.random() < ENV_ATTACK_PC:
                if (t.strength/100.0 * MAX_ENV_SURVIVE_PC < random.random()):
                    t.kill('Environment', tick)
        self.prune_teams()

    def split_team(self, tick=None):
        try:
            tm = random.choice(self.teams)
            tm.split_team(tick)
            self.prune_teams()
        except IndexError:
            pass

    def apply_fatigue(self, tick):
        for t in self.tributes:
            t.fatigue(tick)
        self.prune_teams()

    def epoch(self):
        self.ticks += 1
        print()
        print('**** EPOCH {} ****'.format(self.ticks))
        self.environment_death(self.ticks)
        self.join_teams(pc_teams=TEAM_JOIN_EPOCH_PC)
        self.split_team(self.ticks)
        self.apply_fatigue(self.ticks)
        self.update_leader_stats()
        self.print_all_teams()

    def print_final(self):
        print()
        print()
        for t in self.tributes:
            print(t.outcome_str())

    def collate_results(self):
        return [t.stats() for t in self.tributes]


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

    sim.print_final()
    # print(sim.collate_results())
