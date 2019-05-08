import random


class Tribute():
    def __init__(self, id):
        self.id = id
        self.strength = float(random.randint(1, 100))
        self.alive = True
        self.district = int(id/2)

    def kill(self, reason=None):
        self.alive = False
        self.death_reason = reason

    def fatigue(self):
        if random.random() < 0.5:
            self.strength -= self.strength/10
            if self.strength <= 1:
                self.kill('Fatigue')

    def __str__(self):
        alive = '_' if self.alive else 'X'
        return '{}:{}:{}'.format(self.id, self.strength, alive)
