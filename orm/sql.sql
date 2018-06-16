create table `t_class`(
  `id` int(11) primary key auto_increment NOT NULL,
  `name` varchar(128) NOT NULL DEFAULT '' COMMENT '名称',
  `product` varchar(128) NOT NULL DEFAULT '' COMMENT '产品名称',
  `output` varchar(128) NOT NULL DEFAULT '' COMMENT '输出设备名称',
  `describe` text DEFAULT NULL COMMENT '描述',
  `version` int(11) NOT NULL DEFAULT 0 COMMENT '版本',
  `is_pub` tinyint  NOT NULL DEFAULT 0 COMMENT '是否发布',
  `create_time` datetime  NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)ENGINE=MyISAM DEFAULT CHARSET=utf8;
