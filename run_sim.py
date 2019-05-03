#!/usr/bin/env python3

import random

# we assume there are 10 players of strength 1 to 24.
# A group has strength of the combined members. 
# Each timestamp there is a chance of people/group meeting or a chance a team can split and sub teams fight. 
# The outcome of the meeting can be fight or join up 
# There's a good chance you can beat someone of lower strength (though not definite)


class Tribute():
    def __init__(self, id):
        self.id = id
        self.strength = random.randint(1, 100)
        self.alive = True
        self.team = int(id/2)

    def environment_death(self):
        if random.randint(1, 110) > self.strength:
            self.alive = False
            print("Death by environment: {}".format(self.id))


class Team(list):

    def __init__(self, members):
        for t in members:
            self.append(t)

    def is_empty(self):
        return len(self) == 0

    # def make_empty(self):
    #     # TODO
    #     pass

    def strength(self):
        return sum([t.strength for t in self])

    def __str__(self):
        members = str([t.id for t in self])
        return 'S: {} \t M: {} '.format(self.strength(), members)

    # def merge_in_team(self, other_team):
    #     # TODO other_team needs removing
    #     if other_team == self:
    #         return
    #     self.extent(other_team)
    #     other_team = 

    #     self.teams[team_id1].extend(self.teams[team_id2])
    #     self.teams[team_id2] = Team([])
    #     self.remove_empty_teams()


class Teams():
    def __init__(self):
        self.teams = []

    def initialise_teams(self, tributes, count=18):
        self.teams = []

        # Start with each tribute is a team
        for t in tributes:
            new_team = Team([t])
            self.teams.append(new_team)

        # Shuffle to create some teamups
        max_shuffle = len(self.teams) - count
        for i in range(max_shuffle):
            team_count = len(self.teams)
            t1 = random.randint(0, team_count-1)
            t2 = random.randint(0, team_count-1)
            self.merge_teams(t1, t2)

        print('Created {} teams'.format(len(self.teams)))

    def remove_empty_teams(self):
        # TODO remove dead from teams
        new_teams = []
        for team in self.teams:
            if not team.is_empty():
                new_teams.append(team)
        # print('Team count {}'.format(len(self.new_teams)))
        if len(new_teams) < len(self.teams):
            print('Removed {} teams'.format(len(self.teams) - len(new_teams)))
        self.teams = new_teams

    def merge_teams(self, team_id1, team_id2):
        if team_id1 == team_id2:
            return
        self.teams[team_id1].extend(self.teams[team_id2])
        self.teams[team_id2] = Team([])
        self.remove_empty_teams()

    def print_teams(self):
        for team in self.teams:
            print(str(team))


class sim():
    def __init__(self, tribute_count=24):
        self.tributes = self._create_tributes(tribute_count)
        self.teams = Teams()
        self.teams.initialise_teams(self.tributes)
        self.teams.print_teams()

    def _create_tributes(self, count):
        tributes = []
        for i in range(count):
            t = Tribute(id=i)
            tributes.append(t)

        print('Created {} tributes.'.format(len(tributes)))
        return tributes

    def alive_tributes(self):
        return [t for t in self.tributes if t.alive]

    def alive_count(self):
        return len(self.alive_tributes())

    def environment_deaths(self):
        for t in self.alive_tributes():
            t.environment_death()
        self.teams.remove_empty_teams()


def run_epoch():
    s = sim()
    tick = 0
    game_over = False
    # game_over = True
    while not game_over:
        print('*** Start tick: {}'.format(tick))

        if s.alive_count() == 1:
            print()
            winner = s.alive_tributes()[0]
            print('****** Winner {}:{} ******'.format(winner.id, winner.strength))
            game_over = True
            break

        if s.alive_count() == 0:
            print()
            print('****** No Winner ******')
            game_over = True
            break

        print('Alive: {}'.format(s.alive_count()))
        print('Teams: {}'.format(len(s.teams.teams)))
        s.environment_deaths()
        print()
        tick += 1

print('Starting')
run_epoch()
