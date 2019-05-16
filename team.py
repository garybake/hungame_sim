"""Holds team class."""
import random
import logging


class Team():
    """Collection of tributes."""

    def __init__(self, members=None):
        self._tributes = []
        if members:
            for tribute in members:
                self._tributes.append(tribute)

    def __len__(self):
        return len(self._tributes)

    def __getitem__(self, position):
        return self._tributes[position]

    def __str__(self):
        members = str([t.id for t in self])
        leader = self.leader
        return 'S:{0} \t L:{1}  \t M:{2}'.format(
            self.strength, leader.id, members)

    def pop(self):
        if self.is_empty():
            return

        to_remove = self._tributes[-1]
        self._tributes = self._tributes[:-1]
        return to_remove

    def append(self, tribute):
        self._tributes.append(tribute)

    def is_empty(self):
        return len(self) == 0

    def prune_dead(self):
        self._tributes = [t for t in self._tributes if t.alive]

    @property
    def strength(self):
        return sum([t.strength for t in self])

    @property
    def leader(self):
        strongest = self._tributes[0]
        for t in self._tributes:
            if t.strength > strongest.strength:
                strongest = t
        return t

    def merge_in_team(self, other_team):
        logging.debug('* Merge {}:{} and {}:{} *'.format(
            self.strength, len(self), other_team.strength, len(other_team)))
        if other_team == self:
            return
        for t in other_team:
            mt = other_team.pop()
            self.append(mt)

    def kill_team(self, tick=None):
        for t in self:
            t.kill('Team death', tick)

    def split_team(self, tick=None):
        """
        Split the team and kill the weaker split
        Winner suffers fatigue
        """
        if len(self) <= 1:
            raise IndexError("Team too small")

        t1 = Team()
        t2 = Team()
        for t in self:
            if random.random() < 0.5:
                t1.append(t)
            else:
                t2.append(t)

        if (len(t1) == 0) or (len(t2) == 0):
            # No split occured
            return

        if t1.strength > t1.strength:
            t2.kill_team(tick)
            logging.debug('* Split {}:{} *vs* {}:{} t1 wins *'.format(
                t1.strength, len(t1), t2.strength, len(t2)))
            for t in t1:
                t.fatigue(tick)
        else:
            t1.kill_team(tick)
            for t in t2:
                t.fatigue(tick)
            logging.debug('* Split {}:{} *vs* {}:{} t2 wins *'.format(
                t1.strength, len(t1), t2.strength, len(t2)))
