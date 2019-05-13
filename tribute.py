import random


class Tribute():
    def __init__(self, id):
        self.id = id
        self.strength = float(random.randint(1, 100))
        self.alive = True
        self.death_reason = None
        self.death_tick = None
        self.district = int(id/2)
        self.led_ticks = 0

    def kill(self, reason=None, tick=None):
        if not self.alive:
            # Cant die twice
            return
        self.alive = False
        self.death_reason = reason
        self.death_tick = tick
        print('Death {0}@{1} {2}'.format(self, tick, self.death_reason))

    def fatigue(self, tick=None):
        if not self.alive:
            return

        if random.random() < 0.5:
            self.strength -= self.strength/20
            if self.strength <= 1:
                self.kill('Fatigue', tick)

    def __str__(self):
        alive = '_' if self.alive else 'X'
        return '{0}:{1:.2f}:{2}:{3}'.format(self.id, self.strength, alive, self.led_ticks)

    def outcome_str(self):
        reason = self.death_reason if self.death_reason else 'WINNER'
        tick = self.death_tick if self.death_tick else '_'
        return '{0}:{1}:{2}'.format(self, tick, reason)

    def stats(self):
        return {
            'id': self.id,
            'strength': self.strength,
            'alive': self.alive,
            'led_ticks': self.led_ticks,
            'death_reason': self.death_reason,
            'death_tick': self.death_tick
        }
