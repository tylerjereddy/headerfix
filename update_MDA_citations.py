import os

new_lines = ['# R. J. Gowers, M. Linke, J. Barnoud, T. J. E. Reddy,\n',
             '# M. N. Melo, S. L. Seyler, D. L. Dotson, J. Domanski,\n',
             '# S. Buchoux, I. M. Kenney, and O. Beckstein. MDAnalysis:\n',
             '# A Python package for the rapid analysis of molecular\n',
             '# dynamics simulations. In S. Benthall and S. Rostrup\n',
             '# editors, Proceedings of the 15th Python in Science\n',
             '# Conference, pages 102-109, Austin, TX, 2016. SciPy.\n']

files_changed = 0
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
        with open(current_filepath, 'r') as input_file:
            file_lines = input_file.readlines()
            for line in file_lines:
                if 'cite' in line and '#' in line: # focus on the comment lines, mostly in header metadata
                    print 'current_filepath:', current_filepath, 'cite line:', line
                    line_index = file_lines.index(line)

                    new_file_lines = file_lines[:line_index + 1] + new_lines + ['\n'] + file_lines[line_index + 1:]
                    write_new_file += 1


        if write_new_file > 0:
            with open(current_filepath, 'w') as output_file:
                output_file.writelines(new_file_lines)
            files_changed += 1

print 'Done; files changed:', files_changed

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
