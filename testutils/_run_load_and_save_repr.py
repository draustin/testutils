import getopt
import sys

from testutils import load_and_save_repr

# For command line use.
try:
    opts, args = getopt.getopt(sys.argv[1:], 'r:')
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)
for o, a in opts:
    if o == '-r':
        print('loading and saving', a)
        load_and_save_repr(a)
sys.exit(0)
