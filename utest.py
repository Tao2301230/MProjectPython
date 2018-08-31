
import unittest
import opentuner
import gl
from spark_tuner import GccFlagsTuner



import argparse

gl.spark_parameter = {'early-inlining-insns': ['IntegerParameter', '0-1000'],
                'align-functions': ['EnumParameter', 'on|off|default'],
                'align-jumps': ['EnumParameter', 'on|off|default'],
                'align-labels': ['EnumParameter', 'on|off|default'],
                'align-labels': ['EnumParameter', 'on|off|default'],
                'align-loops': ['EnumParameter', 'on|off|default'],
                'asynchronous-unwind-tables': ['EnumParameter', 'on|off|default'],
                'branch-count-reg': ['EnumParameter', 'on|off|default'],
                'branch-probabilities': ['EnumParameter', 'on|off|default'],
}

#default parameter:
        # --bail_threshold=500 --database=None --display_frequency=10 \
        # --generate_bandit_technique=False --label=None --list_techniques=False \
        # --machine_class=None --no_dups=False --parallel_compile=False \
        # --parallelism=4 --pipelining=0 --print_params=False \
        # --print_search_space_size=False --quiet=False --results_log=None \
        # --results_log_details=None --seed_configuration=[] --stop_after=None \
        # --technique=None --test_limit=5000"

args = opentuner.default_argparser().parse_args()
args.no_dups = True
args.pp=True
args.display_frequency=1
args.stop_after = 500
GccFlagsTuner.main(args)










