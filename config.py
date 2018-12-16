#!/usr/bin/env python
# -*- coding: utf-8 -*-



class Config:
    servicePort = 9090

    ###  Redis config ###
    redisHost = 'localhost'
    redisPort = 6379
    redisDb   = 0

    logLevel  = "info"
    logDir    = "/tmp/mediaParse/logs"

    parseTool = "ffprobe"

    parseTaskTempDataDir = "/tmp/media_parse/data"



