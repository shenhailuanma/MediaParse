#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import MySQLdb


from datetime import datetime
import time

from Log import Log


class Mysql_db:
    def __init__(self, host, port, user, passwd, db):
        try:

            self.local_db = None
            self.host = host
            self.port = port
            self.user = user
            self.passwd = passwd
            self.db     = db

            Factory.logger.debug("[Mysql_db] mysqlHost:%s, mysqlUser:%s, mysqlPassword:%s, mysqlDatabase:%s." 
                %(self.host, self.user, self.passwd, self.db))

            self.local_db = MySQLdb.connect(host=self.host, port=port,
                user=self.user, passwd=self.passwd, db=self.db,
                charset="utf8")

        except Exception,ex:
            summary = "connect to db %s failed. host=%s." %(config.mysqlDatabase, config.mysqlHost);
            Factory.logger.debug("[Mysql_db] error:%s." %(ex))
            raise summary, ex



