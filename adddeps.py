# it does not work on windows
import os
target = os.path.join(0, #os.path.dirname(__file__),
                      '/home/tao/opentuner/opentuner/utils/adddeps.py')
execfile(target, dict(__file__=target))