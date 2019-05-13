from multiprocessing import Pool
import logging

from sim import Sim

TRIBUTE_COUNT = 100 


def process_result(r):
    winner = None
    led_pc = []
    initial_strength = []
    for t in r['tributes']:
        if t['alive']:
            wled_pc = t['led_ticks']/float(r['ticks'])
            winner = {
                'initial_strength': t['initial_strength'],
                'led_pc': wled_pc
            }
        else:
            led_pc.append(t['led_ticks']/float(r['ticks']))
            initial_strength.append(t['initial_strength'])

    if winner is None:
        return None
    output = {
        'winner': winner,
        'loosers': {
            'initial_strength': sum(initial_strength)/len(initial_strength),
            'led_pc': sum(led_pc)/len(led_pc)
        }
    }
    print(output)
    return output


def run_a_sim(run_id):
    print('**** Starting run {}'.format(run_id))
    sim = Sim(TRIBUTE_COUNT)
    while not sim.game_over():
        sim.epoch()
    print('**** Ending run {}'.format(run_id))
    output = {
        'run_id': run_id,
        'tributes': sim.collate_results(),
        'ticks': sim.ticks
    }
    return output


def run_multi_sims(sim_count=3):
    results = []
    with Pool() as P:
        results = P.map(run_a_sim, range(sim_count))
    for r in results:
        process_result(r)


if __name__ == "__main__":
    # logging.debug('gary')
    run_multi_sims(10)
