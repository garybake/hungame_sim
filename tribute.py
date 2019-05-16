"""Holds tribute class."""
import random
import logging


class Tribute():
    """An individial tribute in a game.

    TODO: store the current tick at tribute level
    """
    def __init__(self, id):
        """
        :param id: Unique identifier of tribute
        :type id: int
        """
        self.id = id
        self.initial_strength = float(random.randint(1, 100))
        self.strength = float(self.initial_strength)
        self.alive = True
        self.death_reason = None
        self.death_tick = None
        self.district = int(id/2)
        self.led_ticks = 0

    def __str__(self):
        """Returns basic details.

        :returns: List of attributes
        :rtype: string
        """
        alive = '_' if self.alive else 'X'
        return '{0}:{1:.2f}:{2}:{3}'.format(
            self.id, self.strength, alive, self.led_ticks)

    def kill(self, reason=None, tick=None):
        """Kill the tribute.

        :param reason: Reason for death
        :type id: string
        :param tick: Current time tick
        :type id: int
        """
        if not self.alive:
            # Cant die twice
            return
        self.alive = False
        self.death_reason = reason
        self.death_tick = tick
        logging.debug('Death {0}@{1} {2}'.format(
            self, tick, self.death_reason))

    def fatigue(self, tick=None):
        """Apply fatigue.

        Over time randomly remove strength
        :param tick: Current time tick
        :type id: int
        """
        if not self.alive:
            return

        if random.random() < 0.5:
            self.strength -= self.strength/20
            if self.strength <= 1:
                self.kill('Fatigue', tick)

    def outcome_str(self):
        """Formatted string of status at end of game.

        :returns: List of end attributes
        :rtype: string
        """
        reason = self.death_reason if self.death_reason else 'WINNER'
        tick = self.death_tick if self.death_tick else '_'
        return '{0}:{1}:{2}'.format(self, tick, reason)

    def stats(self):
        """ Summary of agent.

        Used during the end process to capture end state of tributes

        Example
        {
            'id': 10,
            'initial_strength': 35,
            'strength': 12,
            'alive': false,
            'led_ticks': 300,
            'death_reason': 'Environment',
            'death_tick': 250
        }

        :returns: List of attributes
        :rtype: dict
        """
        return {
            'id': self.id,
            'initial_strength': self.initial_strength,
            'strength': self.strength,
            'alive': self.alive,
            'led_ticks': self.led_ticks,
            'death_reason': self.death_reason,
            'death_tick': self.death_tick
        }
