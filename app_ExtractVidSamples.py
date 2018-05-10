

"""
Steps
- Get list of all files
- Check if it's a video file, by querying for 
- If it's a video file, try to extract part of it. (Duration: 30 sec to 3 min, ). 

"""

import os, sys
import glob
try:    #Python 3
    from subprocess import getoutput
except (ImportError, ValueError):     # Python 2
    from commands import getoutput
from progressbar import *
import random
import hashlib


def setupPaths():
    if os.name == 'nt':
        depsFolder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'deps')
        # print (depsFolder)
        os.environ['PATH'] = depsFolder + ";" + os.environ['PATH']
    return

def verifyPythonVersion():
    version_info = sys.version_info
    if not ((version_info.major == 3) and (version_info.minor >=4 )):
        print("ERROR: This app requies Python Version >=3.4.x. Exiting...")
        sys.exit(-1)

MAX_DUR = 180.0
MIN_DUR = 60.0

def randomWord(length):
    # Ref: https://stackoverflow.com/questions/2030053/random-strings-in-python
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))


def extractClips(FOLDER_INP, FOLDER_OUT):
    fileListAll = []
    # fileList = [y for x in os.walk(FOLDER_INP) for y in glob(os.path.join(x[0], '*.*'))]
    for x in os.walk(FOLDER_INP):
        #print("DIR: {}".format(x))
        pth = glob.escape(x[0])
        for y in glob.glob(os.path.join(pth, '*.*')):
            #print (y)
            if (os.path.isfile(y)):
                fileListAll.append(y)

    # print("Full File List")
    # print("\n".join(fileListAll))
    # print()

    countFileListAll = len(fileListAll)

    filesNonVid = []
    filesVid = []
    durVid = []
    filesVidSucceeded = []
    filesVidFailed = []

    print()
    print("(1) TOTAL NUMBER OF FILES: {}".format(countFileListAll) )

    print()
    print("(2) FIND COUNT OF PROBABLE VIDEO FILES")

    # widgets_old=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()]
    widgets = ['[', Percentage(), '->', FormatLabel(''), ' ', Bar('=', '[', ']'), ' ', RotatingMarker()]
    bar = ProgressBar(maxval=countFileListAll, widgets=widgets)

    bar.start()
    tmpCount = 0
    for (ind, file_name) in enumerate(fileListAll):

        # widgets[3] = FormatLabel('{0}/{1} ] <{2}>'.format(tmpCount, ind, file_name))
        widgets[3] = FormatLabel('{0}/{1} ] '.format(tmpCount, ind))
        bar.update(ind)
        cmd = 'mediainfo --Inform="Video;%Duration%" "' + file_name + '"'
        cmd_out = getoutput(cmd)
        if cmd_out != "":
            filesVid.append(file_name)
            dur_sec = float(cmd_out)/1000.0
            durVid.append(dur_sec)
            tmpCount += 1
        else:
            filesNonVid.append(file_name)
            pass
    bar.finish()
    print()


    totalFilesVid = len(filesVid)
    bar2 = ProgressBar(maxval=len(filesVid), widgets=widgets)

    print("(3): EXTRACTING SEGMENTS FROM VIDEO FILES")

    bar2.start()
    for (ind,(vid_file, dur)) in enumerate(zip(filesVid, durVid)):
        # widgets[3] = FormatLabel('{0}/{1} ] <{2}>'.format(ind, totalFilesVid, vid_file))
        widgets[3] = FormatLabel('{0}/{1} ] '.format(ind, totalFilesVid))
        bar2.update(ind)
        OUT_DUR = random.randint(MIN_DUR*10,MAX_DUR*10)/10.0
        LASTPOSSIBLE_START_POS = dur - OUT_DUR;
        if LASTPOSSIBLE_START_POS < 0.0:
            LASTPOSSIBLE_START_POS = 0.0

        START_POS = random.randint(0, int(LASTPOSSIBLE_START_POS*100.0))/100.0

        unique_hash_code = hashlib.md5(str.encode(vid_file)).hexdigest()
        tmp = os.path.splitext(os.path.basename(vid_file))
        new_filename = tmp[0] + "_" + unique_hash_code + tmp[1]
        out_file = os.path.join(FOLDER_OUT, new_filename)
        # ffmpeg -ss 5  -i /Volumes/dataDrive/work/yobi/data/samples/Sherlock.S04E01.The.Six.Thatchers.HDTV.x264-ORGANiC[ettv].mkv -t 5 -vcodec copy -acodec copy out.mkv
        #  ffmpeg -ss 5  -i /Volumes/dataDrive/work/yobi/data/samples/Sherlock.S04E01.The.Six.Thatchers.HDTV.x264-ORGANiC[ettv].mkv -t 1000 -vcodec copy -acodec copy -avoid_negative_ts 1 out.mkv
        cmd = 'ffmpeg -y -loglevel fatal '
        cmd += '-ss ' + str(START_POS) + ' '
        cmd += '-i "' + vid_file + '" '
        cmd += '-t ' + str(OUT_DUR) + ' '
        # cmd += '-c copy -avoid_negative_ts 1 '
        # cmd += '-vcodec copy -acodec copy -map 0:v -map 0:a:2 -avoid_negative_ts 1 '
        cmd += '-vcodec copy -acodec copy -map 0 -avoid_negative_ts 1 '
        cmd += ' "' + out_file + '" '

        ret = os.system(cmd)

        if ret == 0:
            filesVidSucceeded.append(vid_file)
        else:
            filesVidFailed.append(vid_file)
            pass
    bar2.finish()

    
    print()
    print("List of failed files: ")
    print("\n".join(filesVidFailed))



if __name__ == '__main__':
    verifyPythonVersion()
    
    if len(sys.argv) != 3:
        print("Correct Usage: {} <inp_folder> <out_folder>. Exiting...".format(sys.argv[0]))
        sys.exit(-1)

    FOLDER_INP = sys.argv[1]
    FOLDER_OUT = sys.argv[2]

    FOLDER_INP = os.path.abspath(FOLDER_INP)
    FOLDER_OUT = os.path.abspath(FOLDER_OUT)

    # Verify that both the folders exist
    if not os.path.isdir(FOLDER_INP):
        print("ERROR: Input folder doesn't exit. Exiting...")
        sys.exit(-1)

    # Verify that both the folders exist
    if not os.path.isdir(FOLDER_OUT):
        print("ERROR: Output folder doesn't exit. Exiting...")
        sys.exit(-1)

    # Verify that output folder exists outside of input folder
    if FOLDER_OUT.find(FOLDER_INP) != -1:
        print("ERROR: Output folder should not exist inside input folder. Exiting...")
        sys.exit(-1)

    setupPaths()
    extractClips(FOLDER_INP, FOLDER_OUT)


