import toml
import sys

from time import time, sleep
from clips import Environment


def run(config_file):
    config = toml.loads(config_file)

    # initialize sensors;
    #   - temperature/humidity
    #   - soil moisture
    #   - RTC clock
    #   - LCD display
    #   - Buzzer
    # TODO

    env = Environment()
    env.load(config['clips_file'])

    starttime = time()

    while True:
        # reset CLIPS. Set the fact base to its initial state
        env.reset()

        # TODO: read data from sensors and assert facts
        env.assert_string(f'(humidity-is {humidity})')
        env.assert_string(f'(temperature-is {temperature})')
        env.assert_string(f'(time-of-day-is {time_of_day})')
        env.assert_string(f'(soil-has-moisture {has_moisture})')

        # run clips
        env.run()

        # get output. should we water plant or not?
        water_plant = None
        for fact in env.facts():
            if fact.template.name == 'water-plant':
                water_plant = fact[0] == 'yes'

        if water_plant is None:
            print("Something wrong in CLIPS rules")
        else:
            # TODO: display on LCD and sound buzzer

        # execute above code every x seconds
        sleep(config['run_every'] - ((time() - starttime) % config['run_every']))


if __name__ == "__main__":
    try:
        config_file = sys.argv[1]
    except IndexError:
        print("Need to pass config file")
        exit(1)

    try:
        run(config_file)
    except KeyboardInterrupt:
        print("Terminating...")
