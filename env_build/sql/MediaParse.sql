
CREATE TABLE  IF NOT EXISTS `parse_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'the id of the parse_task',
  `state` varchar(16)  DEFAULT 'created' COMMENT 'the state of task',
  `error_code` int DEFAULT 0 COMMENT 'the error code if task error. 0: success.',
  `result` varchar(1000) DEFAULT NULL COMMENT 'the detail result for this task.',
  `create_time` datetime DEFAULT NULL COMMENT 'the start time of task',
  `start_time`  datetime DEFAULT NULL COMMENT 'the start time of task',
  `finish_time` datetime DEFAULT NULL COMMENT 'the finish time of task',
  `update_time` datetime DEFAULT NULL COMMENT 'the update time of task',
  `progress` float DEFAULT 0 COMMENT 'the progress of task [0,100]. e.g. 88.8 means 88.8%.',
  `report_url` varchar(1000) DEFAULT NULL COMMENT 'the report url for this task.',
  `params` varchar(1000) DEFAULT NULL COMMENT 'the user set parameters.',
  `source` varchar(1000) DEFAULT NULL COMMENT 'the source of this task.',

  `parse_result_id` int DEFAULT 0 COMMENT 'the parse_result_id of task.',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8;