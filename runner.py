from multiprocessing import Pool
import logging

from sim import Sim

SIM_COUNT = 10
TRIBUTE_COUNT = 500


def run_a_sim(run_id):
    logging.debug('**** Starting run {}'.format(run_id))
    sim = Sim(TRIBUTE_COUNT)
    while not sim.game_over():
        sim.epoch()
    logging.debug('**** Ending run {}'.format(run_id))
    output = {
        'run_id': run_id,
        'tributes': sim.compressed_result(),
        'ticks': sim.ticks
    }
    return output


def run_multi_sims(sim_count=3):
    """
    {
        run_id: 10
        tributes: {
            'winner': {'initial_strength': 37.0, 'led_pc': 0.12},
            'loosers': {'initial_strength': 53.12, 'led_pc': 0.11}
        },
        ticks: 100
    }
    """
    results = []
    with Pool() as P:
        results = P.map(run_a_sim, range(sim_count))
    return results


if __name__ == "__main__":
    data = {
        'sim_count': SIM_COUNT,
        'strongest_win': 0,
        'leader_win': 0,
        'fails': 0
    }
    results = run_multi_sims(SIM_COUNT)
    for r in results:
        try:
            ts_winner = r['tributes']['winner']
            ts_looser = r['tributes']['loosers']
            if ts_winner['initial_strength'] > ts_looser['initial_strength']:
                data['strongest_win'] += 1
            if ts_winner['led_pc'] > ts_looser['led_pc']:
                data['leader_win'] += 1
        except TypeError:
            # print(r)
            # Usually when there is no winner
            data['fails'] += 1
    print(data)
