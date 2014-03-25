#!/usr/bin/env python

import os
import subprocess as sub
import csv


def du_files_in_path(path):
    """
    Calls the command du for all files in passed in (PATH), checks for
    0-byte files, retuns a list (results), with size of file, filename,
    FAIL for 0-byte and PASS for non 0-byte files.

    Arguments:
        path - path command will be run against
    """

    # Runs the 'du' command for all files on the folder passed in as an
    # argument returns the results as a list to __main__

    lsdir = os.listdir(path)
    results = []

    row = 0
    for infile in lsdir:
        cmd = 'du %s' % infile
        p1 = sub.Popen([cmd], shell=True, stdout=sub.PIPE, stderr=None)

        for line in p1.stdout.readlines():
            line = line.replace("\n", "")
            line = line.split("\t", 1)
            results.append(line)
            
            # if first column of the current row (ie. size) == 0 then
            #   add a new column w/'FAIL' ELSE make it 'PASS'
            if results[row][0] == '0':
                results[row].append('FAIL')
            else:
                results[row].append('PASS')
            
            row = row + 1

    return results

       
def logstr2csv(logtxt, filename):
    """
    Uses the csv module to write a .csv results file.
    
    Arguments:
      logtxt (string) - text string to write to the csv
      filename - filename of the .csv file to write to
      
    """

    # Creates a csv file (filename) and logs the text (logtxt) to it
    outputfile = open(filename, "ab")
    
    resultWriter = csv.writer(outputfile, delimiter=',',
                              quotechar='"', quoting=csv.QUOTE_ALL)
    resultWriter.writerow(logtxt)
    

if __name__ == '__main__':

    # Get path from command line
    # path = sys.argv[1] - commented out while testing.

    for result in du_files_in_path("/home/justin/Python/"):
        print result
        logstr2csv(result, "results.csv")
