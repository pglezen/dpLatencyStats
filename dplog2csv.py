import re
import sys
import os.path

import numpy as np
import pandas as pd

usage = """Usage: dplog2csv.py [-v] [-f] <base name> [-o output name]

  Description: Converts a DataPower latency log to a comma-separated-value
               file.  The default input file is <base-name>.log.  The
               default output file is <base-name>.csv.

 <base name> : The base file name of the DataPower latency log file not
               including the file extension which is assumed to be .log.
  Options:
          -v : verbose
          -f : force overwrite of existing ouput file (otherwise append).

  Example: python dplog2csv.py  latency-2015-02-01

           This assumes input of latency-2015-02-01.log and creates a CSV
           file named latency-2015-02-01.csv.
        """

# Regular expression for selecting DataPower latency log entries
# and carving them up for field-by-field analysis.  For a detailed
# description see 
#
#     https://gist.github.com/pglezen/b724ee99d6cd4edb0217
#
reg = re.compile(r'\w\w\w (\w\w\w \d\d \d\d\d\d \d\d:\d\d:\d\d) \[0x80e00073\]\[latency\]\[info\] \w+\(([^)]+)\): tid\((\d+)\).+ Latency:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+\[(https?://[^/]+)([^?]+)?(\?.+)?\]')

def to_csv(latency_filename, csv_filename, append=False):
  """" Convert latency records to CSV format and store them
       to a .csv file."""
  csvmode = 'a' if append else 'w'
  lines_processed = 0
  csv_mode = 'a' if append  else 'w'
  latfile = open(latency_filename, 'r')
  csvfile = open(csv_filename, csvmode)

  if not append:
    csvfile.write('Time,ProxyName,TxnID,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,url,uri,q\n')

  for line in latfile:
    fields = reg.match(line)
    if fields != None:
      csvline = ','.join(fields.groups())
      csvfile.write(csvline + '\n')
      lines_processed += 1

  print("Processed {0} lines.".format(lines_processed))
  latfile.close()
  csvfile.close()


def print_usage():
  print(usage)

def parse_args_and_run():
  """ Parse the argv parameters and run to_csv."""
  overwrite = False    # overwrite existing file
  input_base  = None
  output_file = None
  if len(sys.argv) < 1  or  '-h' in sys.argv  or  '--help' in sys.argv:
    print_usage()
    sys.exit()

  if '-v' in sys.argv:
    print('verbose mode')
    verbose = True
    sys.argv.remove('-v')

  if '-f' in sys.argv:
    print('over-write mode')
    overwrite = True
    sys.argv.remove('-f')

  if '-o' in sys.argv:
    output_file_index = sys.argv.index('-o') + 1
    if len(sys.argv)-1 >= output_file_index:
      output_file = sys.argv[output_file_index]
      del sys.argv[output_file_index-1:output_file_index+1]
      print("Overriding default output file name with {0}".format(output_file))
    else:
      print("Value of -o argument is missing.")
      print_usage()
      exit()

  # By this point, the base file argument should be the only one left.
  # It should be at index 1 since the other ones were removed.
  #
  if len(sys.argv) > 1:
    input_base = sys.argv[1]
    if '.' in input_base:
      print("Tip: Input file assumes a base of .log")
      input_file = input_base
      input_base = input_file[:input_file.index('.')]
    else:
      input_file = input_base + '.log'

    print("Input file: {0}".format(input_file))

    if not output_file:
      output_file = input_base + '.csv'
    print("Ouput file: {0}".format(output_file))

  else:
    print("Missing base file name.")
    print_usage()
    sys.exit()

  append_file = not overwrite  and  os.path.isfile(output_file)
  print("append_file = {0}".format(append_file))
  to_csv(input_file, output_file, append=append_file)

####################################################
#
# If this module is run as the main program, 
# i.e. as python dplog2.py, then run the code.
# Otherwise, simply make the functions available
# for use by any script that imports this module.
# In most cases, this would be the to_csv function.
#
if __name__ == '__main__':
  parse_args_and_run()
