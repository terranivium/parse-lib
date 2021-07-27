# 2021 Krotos Ltd.
# Wesley Scott

import glob
import os
import csv
import wave
import contextlib
from wavinfo import WavInfoReader

lib_path = "Audio Files/**/*.wav"

file_id = 0
basename = None
duration = 0
rate = 0
designer = None
description = None
info = None

# fieldnames for no wav metadata
partial_fieldnames = ['recid',
            'file_name', 
            'duration', 
            'samplerate']

# fieldnames for presence of wav metadata
full_fieldnames = ['recid',
            'file_name', 
            'duration', 
            'samplerate', 
            'designer', 
            'description']

# Write new metadata csv
with open('metadata.csv', mode='w') as csv_file:

    # check for wav metadata
    for file in glob.glob(lib_path):
        info = WavInfoReader(file)

    # set fieldnames
    if info.info is None:
        writer = csv.DictWriter(csv_file, fieldnames=partial_fieldnames)
    else:
        writer = csv.DictWriter(csv_file, fieldnames=full_fieldnames)

    writer.writeheader()
    
    for file in glob.glob(lib_path, recursive=True):
        
        basename = os.path.basename(file)

        if info.info is not None:
            info = WavInfoReader(file)
            designer = info.info.artist
            description = info.info.comment

        # Audio specifc data (sr and length)
        with contextlib.closing(wave.open(file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        # only write required fields
        if info.info is None:
            writer.writerow({'recid' : file_id, 
                            'file_name': basename, 
                            'duration': duration, 
                            'samplerate': rate})
        else:
            writer.writerow({'recid' : file_id, 
                            'file_name': basename, 
                            'duration': duration, 
                            'samplerate': rate, 
                            'designer': designer, 
                            'description': description})

        file_id += 1

    # print last idx for easy count
    print('\n*****************************')
    print('Files parsed: ' + str(file_id))
    print('*****************************\n')