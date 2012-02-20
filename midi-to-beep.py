#!/usr/bin/env python
import argparse, csv

parser = argparse.ArgumentParser(description='Convert midi files to beep tunes')
parser.add_argument('-f', type=str, help='a filepath to the midi you want played')
parser.add_argument('-l', type=str, help='the length of the midi you would like translated to beep')
# Need an arguement to supress beep
# Need an arguement to print to console
args = parser.parse_args()
tempo = 120
tempoMultiplier = 2


def getDuration(row, noteStart):
    return str((int(row[1].strip()) - noteStart)* tempoMultiplier)

def getFreq(row):
    return str(midiNumToFreq(int(row[4].strip())))

def midiNumToFreq(midiNumber):
    return 440 * pow(2, (midiNumber-69)/float(12))

def buildBeep():
    csvFile = csv.reader(open(args.f, 'rb'))
    beepOut = 'beep'
    noteStart = 0
    for row in csvFile:
        if 'Note_on_c' in row[2]:
            if 0 == int(row[5].strip()):
                if noteStart:
                    beepOut += ' -n'
                beepOut += ' -f ' + getFreq(row) + ' -l ' + getDuration(row, noteStart)
            else:
                noteStart = int(row[1].strip())
                outputFile = open(args.f.replace('.csv', '.beep'), 'w')
        elif 'Tempo' in row[2]:
            tempo = int(row[3].strip())
    outputFile.write(beepOut)
    return

if not args.f:
    parser.print_help()
else:
    buildBeep()
