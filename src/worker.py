#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.Log import Logger
from parser import Parser

import time

class Worker:
    def __init__(self):
        self.logger = Logger('/var/log/MediaParse_woker.log', 'debug', 'Worker')
        self.logger.debug('Worker init over.')

        self.parser = Parser()

    def run(self):
        self.logger.debug('Worker run start.')
        while True:
            # get task
            self.get_task()

            # to parse the meida
            

            # to put the parse data to database


            time.sleep(1)

        self.logger.debug('Worker run over.')

    def get_task(self):
        self.logger.debug('Worker get_task start.')
        self.logger.debug('Worker get_task over.')




if __name__ == "__main__":
    #logger = Logger('/var/log/MediaParse_woker.log', 'debug', 'Main')

    worker = Worker()
    worker.run()