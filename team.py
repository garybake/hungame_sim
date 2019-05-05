
class Team():

    def __init__(self, members):
        self._tributes = []
        for tribute in members:
            self._tributes.append(tribute)

    def __len__(self):
        return len(self._tributes)

    def __getitem__(self, position):
        return self._tributes[position]

    def __str__(self):
        members = str([t.id for t in self])
        return 'S: {} \t M: {} '.format(self.strength, members)

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

    def merge_in_team(self, other_team):
        if other_team == self:
            return
        for t in other_team:
            mt = other_team.pop()
            self.append(mt)
