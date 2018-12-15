#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import subprocess
import ConfigParser

# ffprobe help:
# -v loglevel         set logging level
# -report             generate a report
# -max_alloc bytes    set maximum size of a single allocated block
# -cpuflags flags     force specific cpu flags
# -hide_banner hide_banner  do not show program banner
# -sources device     list sources of the input device
# -sinks device       list sinks of the output device
# -f format           force format
# -unit               show unit of the displayed values
# -prefix             use SI prefixes for the displayed values
# -byte_binary_prefix  use binary prefixes for byte units
# -sexagesimal        use sexagesimal format HOURS:MM:SS.MICROSECONDS for time units
# -pretty             prettify the format of displayed values, make it more human readable
# -print_format format  set the output printing format (available formats are: default, compact, csv, flat, ini, json, xml)
# -of format          alias for -print_format
# -select_streams stream_specifier  select the specified streams
# -sections           print sections structure and section information, and exit
# -show_data          show packets data
# -show_data_hash     show packets data hash
# -show_error         show probing error
# -show_format        show format/container info
# -show_frames        show frames info
# -show_format_entry entry  show a particular entry from the format/container info
# -show_entries entry_list  show a set of specified entries
# -show_log           show log
# -show_packets       show packets info
# -show_programs      show programs info
# -show_streams       show streams info
# -show_chapters      show chapters info
# -count_frames       count the number of frames per stream
# -count_packets      count the number of packets per stream
# -show_program_version  show ffprobe version
# -show_library_versions  show library versions
# -show_versions      show program and library versions
# -show_pixel_formats  show pixel format descriptions
# -show_private_data  show private data
# -private            same as show_private_data
# -bitexact           force bitexact output
# -read_intervals read_intervals  set read intervals
# -default            generic catch all option
# -i input_file       read specified file
# -find_stream_info   read and decode the streams to fill missing information with heuristics



class MediaParser:

    def __init__(self, ffprobe=None):
        # parse tools
        self.ffprobeBin = 'ffprobe'

        # parse data
        self.mediaInfoFile = "mediainfo.json"
        self.streamInfoFile = "streams.json"
        self.packetInfoFile = "packets.ini"
        self.frameInfoFile = "frames.ini"
        self.ffprobeLog = "frames.log"

        # parse result
        self.resultFile = "result.json"

        if ffprobe != None:
            self.ffprobeBin = ffprobe

        # the result dict, the parse result will be set in it
        self.parseResult = {}
        self.parseResult['fileName'] = ""
        self.parseResult['streams'] = []
        self.parseResult['packetCount'] = 0
        self.parseResult['frameCount'] = 0
        self.warnings = []


    def parse(self, file, destDir=None):

        if destDir != None:
            cmd = "mkdir -p " + destDir
            print("run command:" + cmd)
            os.system(cmd)
            if os.path.isdir(destDir):
                if not destDir.endswith("/"):
                    destDir = destDir + "/"

                self.mediaInfoFile = destDir + self.mediaInfoFile
                self.streamInfoFile = destDir + self.streamInfoFile
                self.packetInfoFile = destDir + self.packetInfoFile
                self.frameInfoFile = destDir + self.frameInfoFile
                self.ffprobeLog = destDir + self.ffprobeLog
                self.resultFile = destDir + self.resultFile


        self.parseResult['fileName'] = file



        ### prepare
        print("### prepare data")
        self.prepareDate(file, destDir)


        ### parse data
        print("### parsing data ...")
        # streams
        with open(self.streamInfoFile) as fstreams:
            streamsJson = json.load(fstreams)

            for streamOne in streamsJson['streams']:
                retStreamOne = self.defaultResultStreamInfo()
                retStreamOne['index'] = streamOne['index']
                retStreamOne['type'] = streamOne['codec_type']
                retStreamOne['codec'] = streamOne['codec_name']

                self.parseResult['streams'].append(retStreamOne)



        # packet count, size,  bitrate, 
        dataFile = ConfigParser.ConfigParser()
        dataFile.read(self.packetInfoFile)
        sections = dataFile.sections()

        for dataOne in sections:
            self.parseResult['packetCount'] += 1

            dataJson = {}

            for k,v in dataFile.items(dataOne):
                dataJson[k] = v
                if k == 'stream_index':
                    dataJson[k] = int(v)

            streamOne = self.parseResult['streams'][dataJson['stream_index']]

            streamOne['packetCount'] += 1
            
            # video gop
            # if dataJson['codec_type'] == 'video':


            


        # frames count
        dataFile = ConfigParser.ConfigParser()
        dataFile.read(self.frameInfoFile)
        sections = dataFile.sections()

        for dataOne in sections:
            self.parseResult['frameCount'] += 1

            dataJson = {}

            for k,v in dataFile.items(dataOne):
                dataJson[k] = v
                if k == 'stream_index':
                    dataJson[k] = int(v)

            streamOne = self.parseResult['streams'][dataJson['stream_index']]
            streamOne['frameCount'] += 1

        print("### parsing data over")

        ### write result
        with open(self.resultFile, 'w') as fp:
            json.dump(self.parseResult, fp, indent=4)




    def prepareDate(self, file, destDir):

        # get mediainfo 
        cmd = self.ffprobeBin + " -i " + file + " -show_format -print_format json > " + self.mediaInfoFile
        print(cmd)
        os.system(cmd)

        # get streams info 
        cmd = self.ffprobeBin + " -i " + file + " -show_streams -print_format json > " + self.streamInfoFile
        print(cmd)
        os.system(cmd)

        # get packets info
        cmd = self.ffprobeBin + " -i " + file + " -show_packets -print_format ini > " + self.packetInfoFile
        print(cmd)
        os.system(cmd)

        # get frames info
        cmd = self.ffprobeBin + " -i " + file + " -show_frames -print_format ini > " + self.frameInfoFile
        print(cmd)
        with open(self.ffprobeLog, "w") as fp:
            self.doCommand(cmd, fp)


    def doCommand(self, cmd, fp=None):
        try:
            child = subprocess.Popen(cmd,shell=True, stdout=fp, stderr=fp)
            child.wait()

            return 'success'
        except Exception,ex:
            return str(ex)
        

    def defaultResultStreamInfo(self):
        ret = {}
        ret['type'] = ""
        ret['index'] = -1
        ret['codec'] = ""

        ret['packetCount'] = 0
        ret['frameCount'] = 0

        # video gop
        ret['avgGop'] = 0
        ret['minGop'] = 0
        ret['maxGop'] = 0
        ret['gopList'] = ""

        # pts dt
        ret['maxDtPts'] = 0
        ret['minDtPts'] = 0

        # frame not decoded

        return ret





if __name__ == "__main__":

    mediaParser = MediaParser("~/bin/ffprobe")
    mediaParser.parse("~/workspace/transcoding-engine/streams/error001-h264-nal-data-erro.mp4", "/Users/hanxun.zx/gitbase/MediaParse/tools/temp")
    # mediaParser.parse("~/workspace/transcoding-engine/streams/after_transcode_duration_reduce.mp4", "/Users/hanxun.zx/gitbase/MediaParse/tools/temp")
