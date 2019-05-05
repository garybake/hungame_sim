import random


class Tribute():
    def __init__(self, id):
        self.id = id
        self.strength = random.randint(1, 100)
        self.alive = True
        self.district = int(id/2)

    def kill(self):
        self.alive = False

    def __str__(self):
        alive = '_' if self.alive else 'X'
        return '{}:{}:{}'.format(self.id, self.strength, alive)
