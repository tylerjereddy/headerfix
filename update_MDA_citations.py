import os

new_header = ['# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-\n',
              '# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4\n',
              '#\n',
              '# MDAnalysis --- http://www.mdanalysis.org\n',
              '# Copyright (c) 2006-2016 The MDAnalysis Development Team and contributors\n',
              '# (see the file AUTHORS for the full list of names)\n',
              '#\n',
              '# Released under the GNU Public Licence, v2 or any higher version\n',
              '#\n',
              '# Please cite your use of MDAnalysis in published work:\n',
              '#\n',
              '# R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy, M. N. Melo, S. L. Seyler,\n',
              '# D. L. Dotson, J. Domanski, S. Buchoux, I. M. Kenney, and O. Beckstein.\n',
              '# MDAnalysis: A Python package for the rapid analysis of molecular dynamics\n',
              '# simulations. In S. Benthall and S. Rostrup editors, Proceedings of the 15th\n',
              '# Python in Science Conference, pages 102-109, Austin, TX, 2016. SciPy.\n',
              '#\n',
              '# N. Michaud-Agrawal, E. J. Denning, T. B. Woolf, and O. Beckstein.\n',
              '# MDAnalysis: A Toolkit for the Analysis of Molecular Dynamics Simulations.\n',
              '# J. Comput. Chem. 32 (2011), 2319--2327, doi:10.1002/jcc.21787\n',
              '#\n']

files_changed = 0
old_counter = 0
list_files_skipped_new_scheme = []
for dirpath, dirnames, filenames in os.walk('/Users/treddy/python_modules/MDAnalysis/MDA_dev/mdanalysis'):
    if 'sphinx' in dirpath or 'html' in dirpath:
        continue
    for filename in filenames:
        if filename[-3:] == 'pyc' or filename[-4:] == 'html': # don't alter byte-compiled files
            continue
        elif 'doctree' in filename:
            continue
        current_filepath = os.path.join(dirpath, filename)
        write_new_file = 0
        old_line_counted = 0
        with open(current_filepath, 'r') as input_file:
            file_lines = input_file.readlines()
            for line in file_lines:
                if 'cite' in line and '#' in line:
                    old_counter += 1
                    old_line_counted += 1
                if 'Mode' in line and '#' in line and 'tab-width' in line: # focus on header metadata lines
                    print 'current_filepath:', current_filepath, 'header line:', line
                    start_line_index = file_lines.index(line)
                    write_new_file += 1
                elif 'Comput' in line and 'Chem' in line and '(2011)' in line:
                    end_line_index = file_lines.index(line) + 1
                    write_new_file += 1

        if write_new_file == 2:
            new_file_lines = file_lines[:start_line_index + 2] + new_header[2:] + file_lines[end_line_index + 1:]
            with open(current_filepath, 'w') as output_file:
                output_file.writelines(new_file_lines)
            files_changed += 1
        elif old_line_counted:
            list_files_skipped_new_scheme.append(current_filepath)

print 'Done; files changed:', files_changed
print 'old_counter:', old_counter
print 'list_files_skipped_new_scheme:', list_files_skipped_new_scheme

# now do another QC pass:

list_problematic_files = []
for dirpath, dirnames, filenames in os.walk('/Users/treddy/python_modules/MDAnalysis/MDA_dev/mdanalysis'):
    for filename in filenames:
        current_filepath = os.path.join(dirpath, filename)
        with open(current_filepath, 'r') as input_file:
            lines = input_file.readlines()
            Gowers_counter = 0
            Reddy_counter = 0
            for line in lines:
                if 'Gowers' in line:
                    Gowers_counter += 1
                if 'Reddy' in line:
                    Reddy_counter += 1
        if Gowers_counter > 1 and Reddy_counter > 1: # most likely too many citation injections into metadata
            list_problematic_files.append(current_filepath)

print 'QC check; num problematic files in full package:', len(list_problematic_files)
print 'problematic files:', list_problematic_files
