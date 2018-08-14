#!/usr/bin/env python
#
# Optimize blocksize of apps/mmm_block.cpp
#
# This is an extremely simplified version meant only for tutorials
#
import adddeps  # fix sys.path

import opentuner
from opentuner import ConfigurationManipulator
from opentuner import IntegerParameter
from opentuner import MeasurementInterface
from opentuner import Result

import argparse


FLAGS_WORKING_CACHE_FILE = 'cc_flags.json'
PARAMS_DEFAULTS_CACHE_FILE = 'cc_param_defaults.json'
PARAMS_DEF_PATH = '~/gcc-4.9.0/gcc/params.def'
PARAMS_WORKING_CACHE_FILE = 'cc_params.json'



class GccFlagsTuner(MeasurementInterface):

  def manipulator(self):
    """
    Define the search space by creating a
    ConfigurationManipulator
    """
    manipulator = ConfigurationManipulator()
    manipulator.add_parameter(
      IntegerParameter('BLOCK_SIZE', 1, 3)),
      # IntegerParameter(param, range[0], range[1])),
      # BooleanParameter('')
    return manipulator

  def run(self, desired_result, input, limit):
    """
    Compile and run a given configuration then
    return performance
    """
    cfg = desired_result.configuration.data
    # print "cfg: " + cfg
    gcc_cmd = 'g++ mmm_block.cpp '
    gcc_cmd += ' -D{0}={1}'.format('BLOCK_SIZE', cfg['BLOCK_SIZE'])
    # gcc_cmd += ' -D{0}={1}'.format(param,cfg[param])
    gcc_cmd += ' -o ./tmp.bin'

    compile_result = self.call_program(gcc_cmd)
    assert compile_result['returncode'] == 0

    run_cmd = './tmp.bin'

    run_result = self.call_program(run_cmd)
    assert run_result['returncode'] == 0

    return Result(time=run_result['time'])

  def save_final_config(self, configuration):
    """called at the end of tuning"""
    print "Optimal block size written to mmm_final_config.json:", configuration.data
    self.manipulator().save_to_file(configuration.data,
                                    'mmm_final_config.json')


if __name__ == '__main__':
  argparser = argparse.ArgumentParser(parents=opentuner.argparsers())
  argparser.add_argument('source', help='source file to compile')
  argparser.add_argument('--compile-template',
                         default='{cc} {source} -o {output} -lpthread {flags}',
                         help='command to compile {source} into {output} with'
                              ' {flags}')
  argparser.add_argument('--compile-limit', type=float, default=30,
                         help='kill gcc if it runs more than {default} sec')
  argparser.add_argument('--scaler', type=int, default=4,
                         help='by what factor to try increasing parameters')
  argparser.add_argument('--cc', default='g++', help='g++ or gcc')
  argparser.add_argument('--output', default='./tmp.bin',
                         help='temporary file for compiler to write to')
  argparser.add_argument('--debug', action='store_true',
                         help='on gcc errors try to find minimal set '
                              'of args to reproduce error')
  argparser.add_argument('--force-killall', action='store_true',
                         help='killall cc1plus before each collection')
  argparser.add_argument('--memory-limit', default=1024 ** 3, type=int,
                         help='memory limit for child process')
  argparser.add_argument('--no-cached-flags', action='store_true',
                         help='regenerate the lists of legal flags each time')
  argparser.add_argument('--flags-histogram', action='store_true',
                         help='print out a histogram of flags')
  argparser.add_argument('--flag-importance',
                         help='Test the importance of different flags from a '
                              'given json file.')

  args = argparser.parse_args()
  GccFlagsTuner.main(args)

'''

argparser = opentuner.default_argparser()
# print argparser.parse_args()

param =   "--bail_threshold=500 --database=None --display_frequency=10 \
          --generate_bandit_technique=False --label=None --list_techniques=False \
          --machine_class=None --no_dups=False --parallel_compile=True \
          --parallelism=4 --pipelining=0 --print_params=False \
          --print_search_space_size=False --quiet=False --results_log=None \
          --results_log_details=None --seed_configuration=[] --stop_after=None \
          --technique=None --test_limit=5000"

argparser.add_argument(param)
# GccFlagsTuner.main(param)
GccFlagsTuner.main(argparser.parse_args())


argparser = opentuner.default_argparser()

print argparser
param = "--bail_threshold=1000 --database=None --display_frequency=10 \
         --generate_bandit_technique=False --label=None --list_techniques=False \
         --machine_class=None --no_dups=False --parallel_compile=True \
         --parallelism=4 --pipelining=0 --print_params=False \
         --print_search_space_size=False --quiet=False --results_log=None \
         --results_log_details=None --seed_configuration=[] --stop_after=None \
         --technique=None --test_limit=5000"
param1=['BAIL_THRESHOLD', '1000']

#
#print argparser.parse_args()
#argparser.add_argument(param1)
print argparser.parse_args(param1)
        # GccFlagsTuner.main(param)
# GFInstance = GccFlagsTuner()
# GFInstance.manipulator(argparser.parse_args())
# GFInstance.run()


'''