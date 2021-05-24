from heapq import heapify, heappush
from openal import *
import os
import sys
import time
import subprocess
import csv
import json

start = time.time()
inp = sys.argv[3]
print(f"{time.time() - start:.2f}: Processing {inp}")
outdir = f"output/{inp.split('.')[0]}"
if not os.path.isdir(outdir):
    print(f"{time.time() - start:.2f}: Splitting instruments")
    subprocess.run(["spleeter", "separate", "-p", "spleeter:4stems", "-o", "output", "-i", f"audio/{inp}"], stderr=subprocess.DEVNULL)
    os.mkdir(f"{outdir}/mono")
    print(f"{time.time() - start:.2f}: Separating channels")
    for file in os.listdir(outdir):
        fname = file.split(".")[0]
        mroot = f"{outdir}/mono/{fname}"
        subprocess.run(["ffmpeg", "-i", f"{outdir}/{file}", "-map_channel", "0.0.0", f"{mroot}_left.wav", "-map_channel", "0.0.1", f"{mroot}_right.wav"], stderr=subprocess.DEVNULL)
else:
    print(f"{time.time() - start:.2f}: Using existing processed audio")

print(f"{time.time() - start:.2f}: Determining HRTF profile from {sys.argv[1]}")
with open(f"config/{sys.argv[1]}") as m_data:
    measures = json.load(m_data)

with open("data/AntrhopometricMeasures.csv") as p_data:
    profiles = csv.DictReader(p_data)
    scores = []
    heapify(scores)
    for row in profiles:
        score = 0
        for measure in measures:
            if measure in row:
                score += abs(measures[measure] - float(row[measure]))
        heappush(scores, (score, int(row["SubjectID"])))

profile = scores[0][1]

print(f"{time.time() - start:.2f}: Initializing HRTF with profile HUTUBS_{profile}")
oalInit()
oalInitHRTF(requested_hrtf=f"HUTUBS_{profile}")

print(f"{time.time() - start:.2f}: Preparing soundstage using {sys.argv[2]}")
# (Left < Right, Down < Up, Front < Back)
with open(f"config/{sys.argv[2]}") as l_data:
    layout = json.load(l_data)
    instruments = layout["instruments"]
    volume = layout["volume"]
    space = layout["space"]

sources = []

for instrument in instruments:
    sources.append(oalOpen(f"{outdir}/mono/{instrument[0]}.wav"))
    sources[-1].set_source_relative(True)
    sources[-1].set_position(instrument[1] * space)
    sources[-1].set_direction(tuple([-1 * i for i in instrument[1]]))
    sources[-1].set_gain(instrument[2] * volume)

print(f"{time.time() - start:.2f}: Playing music")
for source in sources:
    source.play()

while any([source.get_state() == al.AL_PLAYING for source in sources]):
    time.sleep(1)

print(f"{time.time() - start:.2f}: Playback ended")
oalQuit()
