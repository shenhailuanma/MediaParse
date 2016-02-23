#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import redis
import logging
import time
import random
import uuid
import math


class Logger:

    def __init__(self, log_path, log_level, log_name):

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


class Rqueue:
    '''
        This Class provides a simple task queue used by redis.
        :param  name: the queue name that set by user, example: 'test_queue', default: 'default_queue' 
        :param  queue_type: the queue type, support: 'fifo','lifo'
    '''
    def __init__(self, name='default_queue', queue_type='fifo', 
                redis_host='localhost', redis_port=6379, redis_db=0, 
                log_path='/var/log/Rqueue.log', log_level='warning', log_name='Rqueue'):
        # set logger
        self.logger = Logger(log_path, log_level, log_name)

        self.logger.debug('Rqueue log test')
        self.logger.info('Rqueue log test')
        self.logger.warning('Rqueue log test')
        self.logger.error('Rqueue log test')

        # 
        self.queue_name = 'Rqueue:' + name
        self.logger.info('queue name: %s' %(self.queue_name))

        self.queue_type = queue_type

        # connect redis
        self.logger.info('redis_host: %s' %(redis_host))
        self.logger.info('redis_port: %s' %(redis_port))
        self.logger.info('redis_db: %s' %(redis_db))
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.logger.info('redis: %s' %(self.redis))

        # create queue

    def get_queue_type(self):
        return self.queue_type

    def acquire_lock(self, lockname, acquire_timeout = 5, lock_timeout = 5):
        try:

            identifier = str(uuid.uuid4())
            lockname = "lock:" + lockname

            lock_timeout = int(math.ceil(lock_timeout))

            end = time.time() + acquire_timeout
            while time.time() < end:
                if self.redis.setnx(lockname, identifier):
                    self.redis.expire(lockname, lock_timeout)
                    return identifier
                elif not self.redis.ttl(lockname):
                    self.redis.expire(lockname, lock_timeout)

                time.sleep(0.01)

            return False
        except Exception,ex:
            self.logger.error("acquire_lock error:%s." %(ex))
            return False


    def release_lock(self, lockname, identifier):
        pipe = self.redis.pipeline(True)
        lockname = "lock:" + lockname

        while True:
            try:
                pipe.watch(lockname)
                if pipe.get(lockname) == identifier:
                    pipe.multi()
                    pipe.delete(lockname)
                    pipe.execute()
                    return True

                pipe.unwatch()
                break
            except Exception,ex:
                self.logger.error("release_lock error:%s." %(ex))
                pass


        return False

    '''
        Push one task to queue.
        :param  taek: the task data, example: 
        :param  name: the queue name that set by user, example: 'test_queue', default: 'default_queue' 
        :param  task_type: the task type that user can define some different name to ivision between different task.
    '''
    def push(self, task):
        try:

            if self.queue_type == 'fifo':
                self.__fifo_queue_push(task)

        except Exception,ex:
            self.logger.error("push error:%s." %(ex))


    def __fifo_queue_push(self, task):
        try:

            self.logger.debug('Push one task(%s) to fifo queue:%s' %(task, self.queue_name))
            # add to database
            pipe = self.redis.pipeline()
            pipe.lpush(self.queue_name, task)
            #pipe.hmset('camera_register:%s' %(params['uid']), params)
            pipe.execute()

        except Exception,ex:
            self.logger.error("__fifo_queue_push error:%s." %(ex))


    def pop(self):
        try:

            if self.queue_type == 'fifo':
                data = self.__fifo_queue_pop()
                return data

        except Exception,ex:
            self.logger.error("pop error:%s." %(ex))


    def __fifo_queue_pop(self):
        try:

            self.logger.debug('Pop one from fifo queue:%s' %(self.queue_name))
            # add to database
            data = self.redis.rpop(self.queue_name)

            return data 
        except Exception,ex:
            self.logger.error("__fifo_queue_pop error:%s." %(ex))


class DynamicRqueue:
    '''
        This Class provides a simple task queue used by redis.
        :param  name: the queue name that set by user, example: 'test_queue', default: 'default_queue' 
        :param  queue_type: the queue type, support: 'fifo','lifo'
    '''
    def __init__(self, name='default_queue', queue_type='fifo', 
                redis_host='localhost', redis_port=6379, redis_db=0, 
                log_path='/var/log/Rqueue.log', log_level='warning', log_name='Rqueue'):
        # set logger
        self.logger = Logger(log_path, log_level, log_name)

        self.logger.debug('Rqueue log test')
        self.logger.info('Rqueue log test')
        self.logger.warning('Rqueue log test')
        self.logger.error('Rqueue log test')

        # 
        self.queue_name = 'Rqueue:' + name
        self.logger.info('queue name: %s' %(self.queue_name))

        self.queue_type = queue_type

        # connect redis
        self.logger.info('redis_host: %s' %(redis_host))
        self.logger.info('redis_port: %s' %(redis_port))
        self.logger.info('redis_db: %s' %(redis_db))
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        self.logger.info('redis: %s' %(self.redis))

        # create queue


    def acquire_lock(self, lockname, acquire_timeout = 5, lock_timeout = 5):
        try:

            identifier = str(uuid.uuid4())
            lockname = "lock:" + lockname

            lock_timeout = int(math.ceil(lock_timeout))

            end = time.time() + acquire_timeout
            while time.time() < end:
                if self.redis.setnx(lockname, identifier):
                    self.redis.expire(lockname, lock_timeout)
                    return identifier
                elif not self.redis.ttl(lockname):
                    self.redis.expire(lockname, lock_timeout)

                time.sleep(0.01)

            return False
        except Exception,ex:
            self.logger.error("acquire_lock error:%s." %(ex))
            return False


    def release_lock(self, lockname, identifier):
        pipe = self.redis.pipeline(True)
        lockname = "lock:" + lockname

        while True:
            try:
                pipe.watch(lockname)
                if pipe.get(lockname) == identifier:
                    pipe.multi()
                    pipe.delete(lockname)
                    pipe.execute()
                    return True

                pipe.unwatch()
                break
            except Exception,ex:
                self.logger.error("release_lock error:%s." %(ex))
                pass


        return False

    '''
        Push one task to queue.
        :param  taek: the task data, example: 
        :param  name: the queue name that set by user, example: 'test_queue', default: 'default_queue' 
        :param  task_type: the task type that user can define some different name to ivision between different task.
    '''
    def push(self, key, data):
        try:

            if self.queue_type == 'fifo':
                pipe = self.redis.pipeline()
                pipe.zadd(self.queue_name, key, time.time())
                pipe.hmset("%s:%s" %(self.queue_name,key), data)
                pipe.execute()


        except Exception,ex:
            self.logger.error("push error:%s." %(ex))


    def pop(self, range_time=3600):
        try:

            if self.queue_type == 'fifo':
                data = None
                lock = self.acquire_lock(self.queue_name)
                if lock == False:
                    self.logger.error("acquire_lock error: lock == False.")
                    return []

                now = time.time()
                uid_list = self.redis.zrangebyscore(self.queue_name, now-range_time, now, 0, 1)
                self.release_lock(self.queue_name, lock)

                self.logger.debug("zrangebyscore return:%s." %(uid_list))


                if len(uid_list) > 0:
                    data = self.redis.hgetall("%s:%s" %(self.queue_name, uid_list[0]))
                    self.logger.debug("get data:%s." %(data))
                    result = self.redis.zrem(self.queue_name, uid_list[0])
          
                return data
            else:
                return None

        except Exception,ex:
            self.logger.error("pop error:%s." %(ex))
            return None

    def update(self, key, data):
        try:

            pipe = self.redis.pipeline()
            for one in data:
                pipe.hset("%s:%s" %(self.queue_name, key), one, data[one])

            pipe.execute()

        except Exception,ex:
            self.logger.error("update error:%s." %(ex))

    def get(self, key):
        try:
            return self.redis.hgetall("%s:%s" %(self.queue_name, key))
        except Exception,ex:
            self.logger.error("update error:%s." %(ex))
            return None


if __name__ == "__main__":
    #queue = Rqueue(log_path='/tmp/mylog', log_level='debug', name='fifo_test')
    #queue.push('test')
    #data = queue.pop('fifo_test')
    #queue.logger.info('data:%s' %(data))

    queue = DynamicRqueue(log_path='/tmp/mylog', log_level='debug', name='DynamicRqueue_test')

    data = {}
    data['key'] = time.time()
    queue.push('test_key2',data)

    print queue.get('test_key2')

    data['time'] = time.time()
    queue.update('test_key2',data)
    print queue.get('test_key2')

    time.sleep(5)
    ret = queue.pop()

    print ret

