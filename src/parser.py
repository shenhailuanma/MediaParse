#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import subprocess
import logging

from utility import Utility

from common.Log import Log

class Parser:
    '''
        the Parser that can parse the media files.
    '''
    def __init__(self, url=None):
        '''
            init the parser
        '''

        ### the needed tools
        self.parse_tool = '/bin/ffprobe'

        ### the params will be set by self.
        
        # media_frames_info is very important, it's the base parse source of others.
        self.media_frames_info = None 

        self.media_info = None



        ### others
        # get utility
        self.utility = Utility()


        Log.logger.debug('Parser init over.')


    def set_parse_tool(self, path=None):
        '''
            set the parse tool path which will be used to parse the meida streams.
        '''
        try:
            if path != None:
                self.parse_tool = path
                Log.logger.info("set_parse_tool, path:%s." %(path))
            else:
                Log.logger.warning("set_parse_tool, path is None.")
                return 'error','set_parse_tool, path is None.'

            return 'success','ok'
        except Exception,ex:
            Log.logger.error("set_parse_tool error:%s" %(ex))
            return 'error',str(ex)


    def do_parse(self):
        '''
            parse the meida which has been set in media_url.
            return parse data.
        '''
        try:

            return 'success','ok'
        except Exception,ex:
            Log.logger.error("do_parse error:%s" %(ex))
            return 'error',str(ex)


    def file_media_parse_frames_data(self, source, destion):
        '''
            parse the meida which has been set in media_url.
            return parse data.
        '''
        try:
            
            cmd = '%s -show_frames  -i %s   -print_format json > %s' %(self.parse_tool, source, destion)
            Log.logger.info("file_media_parse_frames_data, cmd:%s." %(cmd))
            ret,data = self.utility.do_command(cmd)

            return 'success',data

        except Exception,ex:
            Log.logger.error("file_media_parse_frames_data error:%s" %(ex))
            return 'error',str(ex)

    def file_media_parse_packets_data(self, source, destion):
        '''
            parse the meida which has been set in media_url.
            return parse data.
        '''
        try:
            
            cmd = '%s -show_packets  -i %s   -print_format json > %s' %(self.parse_tool, source, destion)
            Log.logger.info("file_media_parse_packets_data, cmd:%s." %(cmd))
            ret,data = self.utility.do_command(cmd)

            return 'success',data

        except Exception,ex:
            Log.logger.error("file_media_parse_packets_data error:%s" %(ex))
            return 'error',str(ex)

    def has_been_parsed(self):
        '''
            If the url has been parsed, return True; Else return False.
        '''

    def get_media_info(self, url=None):
        '''
            Get the meida info of the url.
            If the self.media_url has be set and has run method 'do_parse', than just return the self.media_info;
            If the self.media_url has not be set, than to run command to get the url info and return the value.
            The return value is use JSON object.
        '''
        try:
            # command: ffprobe -print_format json -show_format -show_streams -show_error
            cmd = '%s -print_format json -show_format -show_streams -show_error -i %s' %(self.parse_tool, url)
            ret,data = self.utility.do_command(cmd)

            return 'success',data
        except Exception,ex:
            Log.logger.error("get_media_info error:%s" %(ex))
            return 'error',str(ex)


    def get_video_frames_pts(self, first=None, last=None):
        '''
            This method will return the video frames's PTS list.
            the 'first' and 'last' id defined the range of the PTS that user want to get.
            If 'first' == None, the first value of PTS is the first video frames's PTS;
            IF 'last' == None, the last value of PTS is the last video frames's PTS;
        '''

    def get_video_frames_dts(self, first=None, last=None):
        '''
            This method will return the video frames's DTS list.
            the 'first' and 'last' id defined the range of the DTS that user want to get.
            If 'first' == None, the first value of DTS is the first video frames's DTS;
            IF 'last' == None, the last value of DTS is the last video frames's DTS;
        '''   

    def get_video_frames_duration(self, first=None, last=None):
        '''
            This method will return the video frames's duration list.
            the 'first' and 'last' id defined the range of the duration that user want to get.
            If 'first' == None, the first value of duration is the first video frames's duration;
            IF 'last' == None, the last value of duration is the last video frames's duration;
        '''   



if __name__ == "__main__":

    # set Log
    Log.logger.set_logger('/var/log/Parser.log', 'debug', 'Main')
    Log.logger.info("logger test.")
    Log.logger.debug("logger test.")
    Log.logger.warning("logger test.")
    Log.logger.error("logger test.")

    parser = Parser()

    json_file_path = '/tmp/out.json'
    #meifa_file_path = '/root/out024.mkv'
    meifa_file_path = '/root/cctv5.ts'

    parser.set_parse_tool('/root/MediaParse/_release/bin/ffprobe')

    ret,data = parser.get_media_info(meifa_file_path)
    Log.logger.debug("get_media_info ret:%s, data:%s." %(ret,data))

    Log.logger.debug("begin file_media_parse_frames_data.")
    ret,data = parser.file_media_parse_frames_data(meifa_file_path, json_file_path)
    Log.logger.debug("end of file_media_parse_frames_data.")
    # load the json file
    Log.logger.debug("begin to load json file:%s." %(json_file_path))
    json_data = json.load(file(json_file_path))
    Log.logger.debug("load json over, data len:%s." %(len(json_data['frames'])))


    #Log.logger.debug("begin file_media_parse_packets_data.")
    #ret,data = parser.file_media_parse_packets_data(meifa_file_path, json_file_path)
    #Log.logger.debug("end of file_media_parse_packets_data.")


    # load the json file
    #Log.logger.debug("begin to load json file:%s." %(json_file_path))
    #json_data = json.load(file(json_file_path))
    #Log.logger.debug("load json over, data len:%s." %(len(json_data['packets'])))

    # file data to database

    

