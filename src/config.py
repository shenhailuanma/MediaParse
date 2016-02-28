#!/usr/bin/env python
# -*- coding: utf-8 -*-



class config:
    ###  Redis config ###
    redis_host = 'localhost'
    redis_port = 6379
    redis_db   = 0

    log_level  = "debug"
    log_dir    = "/tmp/media_parse/logs"

    parse_tool = "ffprobe"

    task_tmp_data_dir = "/tmp/media_parse/data"

