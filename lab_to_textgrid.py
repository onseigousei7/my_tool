#!/usr/bin/python

import sys
import re

import os
import glob

def convert_lab_to_textgrid(input_path, output_path):

    inf = open(input_path, 'r')
    outf = open(output_path, 'w', encoding='utf-16')

    # get info from .lab
    labs = []
    for line in inf:
        if not re.search('^\s*\d+\s*\d+\s*\S+', line): #regular expresion for "space number space number space word"
            continue
        tokens = line.split()
        time = tokens[1].strip()
        label = tokens[2].strip()
        time = float(time)
        labs.append((str(time/10000000), label))

    maxtime = str(labs[-1][0])

    # boilerplate
    outf.write('File type = "ooTextFile"\n')
    outf.write('Object class = "TextGrid"\n')
    outf.write('\n')
    outf.write('xmin = 0\n')
    outf.write('xmax = ' + maxtime + '\n')
    outf.write('tiers? <exists>\n')
    outf.write('size = 1\n')
    outf.write('item []:\n')
    outf.write('    item [1]:\n')
    outf.write('        class = "IntervalTier"\n')
    outf.write('        name = "labels"\n')
    outf.write('        xmin = 0\n')
    outf.write('        xmax = ' + maxtime + '\n')
    outf.write('        intervals: size = ' + str(len(labs)) + '\n')

    # intervals
    count = 0
    prevtime = '0'
    for elt in labs:
        count += 1
        outf.write('        intervals [' + str(count) + ']:\n')
        outf.write('            xmin = ' + prevtime + '\n')
        outf.write('            xmax = ' + elt[0] + '\n')
        outf.write('            text = "' + elt[1] + '"\n')
        prevtime = elt[0]

    inf.close()
    outf.close()

def convert_lab_to_textgrid_short(input_path, output_path):

    inf = open(input_path, 'r')
    outf = open(output_path, 'w', encoding='utf-16')

    # get info from .lab
    labs = []
    for line in inf:
        if not re.search('^\s*\d+\s*\d+\s*\S+', line): #regular expresion for "space number space number space word"
            continue
        tokens = line.split()
        time = tokens[1].strip()
        label = tokens[2].strip()
        time = float(time)
        labs.append((str(time/10000000), label))

    maxtime = str(labs[-1][0])

    # boilerplate
    outf.write('File type = "ooTextFile short"\n')
    outf.write('"TextGrid"\n')
    outf.write('\n')
    outf.write('0\n')
    outf.write(maxtime + '\n')
    outf.write('<exists>\n')
    outf.write('1\n')

    outf.write('"IntervalTier"\n')
    outf.write('"phones"\n')
    outf.write('0\n')
    outf.write(maxtime + '\n')
    outf.write(str(len(labs)) + '\n')

    # intervals
    count = 0
    prevtime = '0'
    for elt in labs:
        count += 1
        outf.write(prevtime + '\n')
        outf.write(elt[0] + '\n')
        outf.write('"' + elt[1] + '"\n')
        prevtime = elt[0]

    inf.close()
    outf.close()

def convert_files(lab_folder):
    targetPattern = '{}/*.lab'.format(lab_folder)
    input_paths = glob.glob(targetPattern)

    for input_path in input_paths:
        base, ext = os.path.splitext(input_path)
        basename = os.path.basename(base)
        if ext == '.lab':
            output_path = '{}/{}.TextGrid'.format(lab_folder, basename)
            convert_lab_to_textgrid_short(input_path, output_path)
