#!/usr/bin/env python
#
# Optimize blocksize of apps/mmm_block.cpp
#
# This is an extremely simplified version meant only for tutorials
#
import adddeps  # fix sys.path

import opentuner
from opentuner import ConfigurationManipulator
from opentuner import IntegerParameter, EnumParameter
from opentuner import MeasurementInterface
from opentuner import Result, resultsdb
from opentuner.resultsdb.models import *
import logging


import gl

class GccFlagsTuner(MeasurementInterface):
    def transformation(self, dict):
        self.int_param = []
        self.enum_param = []
        for i in dict:
            if dict[i][0] == 'IntegerParameter':
                min, max = dict[i][1].split('-')
                l = (str(i), min, max)
                self.int_param.append(l)
            elif dict[i][0] == 'EnumParameter':
                enums_values = dict[i][1].split('|')
                self.enum_param.append([str(i), enums_values])
        # print 'int_param'
        # print self.int_param
        # print 'enum_param'
        # print self.enum_param

    def manipulator(self):

        """
        Define the search space by creating a
        ConfigurationManipulator
        """

        self.transformation(gl.spark_parameter)

        manipulator = ConfigurationManipulator()

        manipulator.add_parameter(
            IntegerParameter('BLOCK_SIZE', 1, 1))

        # print 'in manipulator'
        for flag in self.enum_param:
            # print flag[0], flag[1]
            manipulator.add_parameter(
                EnumParameter(flag[0],
                              flag[1]))
        for i in self.int_param:
            manipulator.add_parameter(
                IntegerParameter(i[0], int(i[1]), int(i[2])))

        return manipulator

    def run(self, desired_result, input, limit):
        log = logging.getLogger(__name__)

        """
        Compile and run a given configuration then
        return performance
        """
        cfg = desired_result.configuration.data
        # print "cfg: " + cfg
        gcc_cmd = 'g++ mmm_block.cpp '

        gcc_cmd += ' -D{0}={1}'.format('BLOCK_SIZE', cfg['BLOCK_SIZE'])


        for flag in self.enum_param:
            # print 'flag ' + flag[0]
            if cfg[flag[0]] == 'on':
                gcc_cmd += ' -f{0}'.format(flag[0])
            elif cfg[flag[0]] == 'off':
                gcc_cmd += ' -fno-{0}'.format(flag[0])

        for i in self.int_param:
            # print i[0], cfg[i[0]]
            gcc_cmd += ' --param {0}={1}'.format(i[0], cfg[i[0]])

        # logging.debug(gcc_cmd)
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





