/*
SQLyog Community v11.1 Beta1 (32 bit)
MySQL - 5.1.50-community : Database - webpy_blog
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`webpy_blog` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `webpy_blog`;

/*Table structure for table `to_admin` */

DROP TABLE IF EXISTS `to_admin`;

CREATE TABLE `to_admin` (
  `username` varchar(40) NOT NULL,
  `password` varchar(40) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `to_attac` */

DROP TABLE IF EXISTS `to_attac`;

CREATE TABLE `to_attac` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL DEFAULT '',
  `path` varchar(500) NOT NULL,
  `createtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=289 DEFAULT CHARSET=utf8;

/*Table structure for table `to_attac_rel` */

DROP TABLE IF EXISTS `to_attac_rel`;

CREATE TABLE `to_attac_rel` (
  `att_id` int(10) unsigned NOT NULL,
  `rel_id` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`att_id`,`rel_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*Table structure for table `to_content` */

DROP TABLE IF EXISTS `to_content`;

CREATE TABLE `to_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL DEFAULT '',
  `content` longtext,
  `view_num` int(11) NOT NULL DEFAULT '0',
  `createtime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `modifytime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `is_md` tinyint(1) DEFAULT '0',
  `status` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;

/*Table structure for table `to_metas` */

DROP TABLE IF EXISTS `to_metas`;

CREATE TABLE `to_metas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL DEFAULT '',
  `type` varchar(10) NOT NULL DEFAULT 'tag',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

/*Table structure for table `to_rel` */

DROP TABLE IF EXISTS `to_rel`;

CREATE TABLE `to_rel` (
  `cid` int(11) NOT NULL,
  `mid` int(11) NOT NULL,
  PRIMARY KEY (`cid`,`mid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
