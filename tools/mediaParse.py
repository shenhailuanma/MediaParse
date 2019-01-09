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
        self.resultDir = './'
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
                self.resultDir = destDir
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
                if k == 'pts_time':
                    dataJson[k] = float(v)
                if k == 'dts_time':
                    dataJson[k] = float(v)
                if k == 'flags':
                    dataJson[k] = v


            if dataJson.has_key('stream_index'):

                streamOne = self.parseResult['streams'][dataJson['stream_index']]

                # packet count
                streamOne['packetCount'] += 1
                
                warmTsJumpTooLargeDt = 5.0
                warmTsJumpBackDt = -1.0

                # pts
                dt = dataJson['pts_time'] - streamOne['lastPts']
                if dt > streamOne['maxPtsDt']:
                    streamOne['maxPtsDt'] = dt

                if  dt < warmTsJumpBackDt:
                    newItem = {}
                    newItem['pts_time'] = dataJson['pts_time']
                    newItem['dt'] = dt
                    streamOne['warmTsJumpBack'].append(newItem)
                
                if dt > warmTsJumpTooLargeDt:
                    newItem = {}
                    newItem['pts_time'] = dataJson['pts_time']
                    newItem['dt'] = dt
                    streamOne['warmTsJumpTooLarge'].append(newItem)

                streamOne['lastPts'] = dataJson['pts_time']

                # dts
                dt = dataJson['dts_time'] - streamOne['lastDts']
                if dt > streamOne['maxDtsDt']:
                    streamOne['maxDtsDt'] = dt
                if  dt < warmTsJumpBackDt:
                    newItem = {}
                    newItem['dts_time'] = dataJson['dts_time']
                    newItem['dt'] = dt
                    streamOne['warmDtsJumpBack'].append(newItem)
                
                if dt > warmTsJumpTooLargeDt:
                    newItem = {}
                    newItem['dts_time'] = dataJson['dts_time']
                    newItem['dt'] = dt
                    streamOne['warmDtsJumpTooLarge'].append(newItem)

                streamOne['lastDts'] = dataJson['dts_time']
                

                # video gop
                if dataJson['codec_type'] == 'video':
                    if streamOne['lastGopSize'] > 0 and dataJson['flags'] == 'K_':
                        streamOne['gopList'].append(streamOne['lastGopSize'])
                        streamOne['lastGopSize'] = 0
                    
                    streamOne['lastGopSize'] += 1
            else:
                print("Not found stream_index:" + str(dataOne))


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
                if k == 'pkt_pts_time':
                    dataJson['pts_time'] = float(v)

            if dataJson.has_key('stream_index'):
                streamOne = self.parseResult['streams'][dataJson['stream_index']]
                streamOne['frameCount'] += 1

                warmTsJumpTooLargeDt = 5.0
                warmTsJumpBackDt = -1.0

                # pts
                # if  dataJson['pts_time'] - streamOne['lastPtsFrame'] < warmTsJumpBackDt:
                #     newItem = {}
                #     newItem['pts_time'] = dataJson['pts_time']
                #     newItem['dt'] = dataJson['pts_time'] - streamOne['lastPtsFrame']
                #     streamOne['warmTsJumpBackFrame'].append(newItem)
                
                # if dataJson['pts_time'] - streamOne['lastPtsFrame'] > warmTsJumpTooLargeDt:
                #     newItem = {}
                #     newItem['pts_time'] = dataJson['pts_time']
                #     newItem['dt'] = dataJson['pts_time'] - streamOne['lastPtsFrame']
                #     streamOne['warmTsJumpTooLargeFrame'].append(newItem)

                # streamOne['lastPtsFrame'] = dataJson['pts_time']


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
        cmd = self.ffprobeBin + " -i " + file + " -show_packets -print_format xml > " + self.packetInfoFile + '.xml'
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
        # ret['avgGop'] = 0
        # ret['minGop'] = 0
        # ret['maxGop'] = 0
        ret['lastGopSize'] = 0
        ret['gopList'] = []
        

        # pts dt
        ret['lastPts'] = 0.0
        ret['warmTsJumpTooLarge'] = []
        ret['warmTsJumpBack'] = []
        ret['maxPtsDt'] = 0.0

        ret['lastDts'] = 0.0
        ret['warmDtsJumpTooLarge'] = []
        ret['warmDtsJumpBack'] = []
        ret['maxDtsDt'] = 0.0

        # ret['lastPtsFrame'] = 0.0
        # ret['warmTsJumpTooLargeFrame'] = []
        # ret['warmTsJumpBackFrame'] = []


        # frame not decoded

        return ret





if __name__ == "__main__":

    mediaParser = MediaParser("~/bin/ffprobe")
    # mediaParser.parse("~/workspace/transcoding-engine/streams/trans.mp4", "/Users/hanxun.zx/gitbase/MediaParse/tools/temp")
    mediaParser.parse("/Users/hanxun.zx/Downloads/transcode-not-stop-20190108.mp4", "/Users/hanxun.zx/gitbase/MediaParse/tools/temp")
