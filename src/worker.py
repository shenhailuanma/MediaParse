#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common.Log import Logger
from parser import Parser
from common.Rqueue import Rqueue

import time
import ConfigParser
import json
import redis


class Worker:
    def __init__(self):
        self.logger = Logger('/var/log/MediaParse_woker.log', 'debug', 'Worker')
        self.logger.debug('Worker init over.')

        self.parser = Parser()
        self.parser.set_parse_tool('/root/MediaParse/_release/bin/ffprobe')

        self.task_queue = Rqueue(name='parse_task')
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def run(self):
        self.logger.debug('Worker run start.')
        while True:
            try:
                # get task
                task = self.get_parse_task()
                self.logger.debug('get task: %s.' %(task))

                if task != None:
                    self.do_parse_task(task)

            except Exception,ex:
                self.logger.error("error:%s" %(ex))

            time.sleep(3)

        self.logger.debug('Worker run over.')

    def get_parse_task(self):
        try:
            self.logger.debug('Worker get_parse_task start.')
            task_id = None

            task_id = self.task_queue.pop()
            self.logger.debug('Worker task_id:%s.' %(task_id))

            data = None
            if task_id != None:
                data = self.redis.hgetall("parse_task:%s" %(task_id))
                self.logger.debug('task data : %s' %(json.dumps(data)))
                data['id'] = task_id

            return data
        except Exception,ex:
            self.logger.error("error:%s" %(ex))
            return None

    def do_parse_task(self, task_info):
        try:
            self.logger.debug('Worker do_parse_file start.')

            # check must params


            if task.has_key('url'):      
                # to parse the meida
                ret,data = self.parser.get_media_info(task['url'])
                self.logger.debug("get_media_info ret:%s, data:%s." %(ret,data))

                json_file_path = "/tmp/mdeia_parse_%s" %(task['id'])
                self.logger.debug("begin file_media_parse_frames_data.")
                ret,data = self.parser.file_media_parse_frames_data(task['url'], json_file_path)
                self.logger.debug("end of file_media_parse_frames_data.")
                # load the json file
                self.logger.debug("begin to load json file:%s." %(json_file_path))
                json_data = json.load(file(json_file_path))
                self.logger.debug("load json over, data len:%s." %(len(json_data['frames'])))

                # to put the parse data to database
                cnt = 0
                for element in json_data['frames']:
                    if cnt > 3:
                        break
                    self.logger.debug("put packet:%s." %(json.dumps(element)))
                    pipe = self.redis.pipeline()
                    pipe.rpush("media_data:%s" %(task['id']), element)
                    pipe.execute()
                    cnt += 1

        except Exception,ex:
            self.logger.error("error:%s" %(ex))
            self.clean_parse_task(task_info)


    def clean_parse_task(self, task_info):
        try:
            self.logger.debug('Worker clean_parse_task start.')


        except Exception,ex:
            self.logger.error("error:%s" %(ex))  

    def update_prase_task(self, task_info, update_info):
        try:
            self.logger.debug('Worker clean_parse_task start.')


        except Exception,ex:
            self.logger.error("error:%s" %(ex))     




if __name__ == "__main__":
    #logger = Logger('/var/log/MediaParse_woker.log', 'debug', 'Main')

    worker = Worker()
    worker.run()