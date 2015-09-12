#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import subprocess
import logging

from utility import Utility

class Parser:
    '''
        the Parser that can parse the media files.
    '''
    def __init__(self, ffprobe_path, url=None):
        '''
            init the parser
        '''

        ### the needed tools
        self.parse_tool = '/bin/ffprobe'



        ### the params need be set by user.
        self.media_url = url



        ### the params will be set by self.
        
        # media_frames_info is very important, it's the base parse source of others.
        self.media_frames_info = None 

        self.media_info = None



        ### others
        # get utility
        self.utility = Utility()

        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = 'Parser.log'

        self.logger = logging.getLogger('Parser')
        self.logger.setLevel(self.log_level)

        # create a handler for write the log to file.
        fh = logging.FileHandler(self.log_path)
        fh.setLevel(self.log_level)

        # create a handler for print the log info on console.
        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)

        # set the log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        self.logger.info('init over.')

    def set_media_url(self, url=None):
        '''
            set the media url that want to be parsed.
        '''
        try:
            if url != None:
                self.media_info = url
            else:
                self.logger.warning("set_media_url, path is None.")
                return 'error','set_media_url, path is None.'

            return 'success','ok'
        except Exception,ex:
            self.logger.error("set_media_url error:%s" %(ex))
            return 'error',str(ex)

    def set_parse_tool(self, path=None):
        '''
            set the parse tool path which will be used to parse the meida streams.
        '''
        try:
            if path != None:
                self.parse_tool = path
            else:
                self.logger.warning("set_parse_tool, path is None.")
                return 'error','set_parse_tool, path is None.'

            return 'success','ok'
        except Exception,ex:
            self.logger.error("set_parse_tool error:%s" %(ex))
            return 'error',str(ex)


    def do_parse(self):
        '''
            parse the meida which has been set in media_url.
        '''

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
            self.logger.error("get_media_info error:%s" %(ex))
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

    parser = Parser()
