# Created by Jan Rummens at 8/01/2021
import sys
from nemonet.runner.vision_runner import Runner

if __name__ == '__main__':
    try:
        arg_dict = sys.argv[1]
        scenario_dict = eval(arg_dict)
        runner = Runner()
        runner.execute_scenario(scenario_dict['scenario'])
    except KeyError:
        print("Command line format arguments: \"{'scenario':'file.xml'}\"")
    except IndexError:
        print("Command line format arguments: \"{'scenario':'file.xml'}\"")
    finally:
        print(sys.exc_info()[0])

