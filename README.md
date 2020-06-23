Salt Configuration Management Database
=========================================

![Status: Stable](https://img.shields.io/badge/status-stable-green.svg)
![Build Status](http://build.electricmonk.nl/job/ansible-cmdb/shield)
![Activity: Active dev](https://img.shields.io/badge/activity-active%20dev-green.svg)

关于
-----
Leoncmdb配置管理数据库是通过是基于salt管理集群中所有机器。通过django crontab配合salt定时获取和管理主机信息。

功能
--------
* 支持通过页面管理和安装agent，通过管理员审批入库。
* 通过调用salt API登录主机执行命令
* 主机信息资源管理

文档
-------
* agent 目录
    * 集成agent脚本，对主机安装agent。
* asset 目录
    * 增删改查主机信息
* corefunc 目录
    * 主要方法存放位置
* saltapi
    * salt调用相关
static 目录
    * 存放HTML，js等静态文件存放位置