#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

class Logger:

    def __init__(self, log_path, log_level='warning', log_name='logger'):

        # set the logger

        self.log_level = logging.DEBUG
        self.log_path = log_path

        if  log_level == 'info':
            self.log_level = logging.INFO
        elif  log_level == 'debug':
            self.log_level = logging.DEBUG
        elif  log_level == 'warning':
            self.log_level = logging.WARNING
        elif  log_level == 'error':
            self.log_level = logging.ERROR

        self.logger = logging.getLogger(log_name)
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



    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)


class Log:
    logger = Logger(log_path='/var/log/logger', log_level='debug', log_name='MediaParse')
