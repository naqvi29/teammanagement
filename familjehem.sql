-- Adminer 4.6.2 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP TABLE IF EXISTS `assignment`;
CREATE TABLE `assignment` (
  `sno` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `date` varchar(255) NOT NULL,
  `time` varchar(255) NOT NULL,
  `des` varchar(10000) NOT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `assignment` (`sno`, `user_id`, `user_name`, `title`, `date`, `time`, `des`) VALUES
(1,	3,	'uuuuuser2 ka username',	'asasa',	'2021-07-31',	'8:00 PM',	'asasas'),
(2,	2,	'user2',	'ques title changed',	'2021-09-11',	'09:29 AM',	'ques desc 1'),
(3,	1,	'uuusername2',	'ques for user 2',	'2021-09-11',	'09:29:19',	'ques description90'),
(4,	1,	'uuusername2',	'ques for user 2',	'2021-09-11',	'09:29:19',	'ques description90'),
(5,	1,	'uuusername2',	'ques for user 2',	'2021-09-11',	'09:29:19',	'ques description90'),
(6,	1,	'uuusername2',	'ques for user 2',	'2021-09-11',	'09:29:19',	'ques description90'),
(7,	1,	'uuusername2',	'ques for user 2',	'2021-09-11',	'09:29:19',	'ques description90'),
(8,	1,	'uuusername2',	'ques for user 2',	'2021-09-11',	'09:29:19',	'ques description90'),
(9,	2,	'quesname2',	'ques for user 2',	'2021-09-11',	'09:29:19',	'ques description90'),
(10,	2,	'quesname2',	'ques for user 2',	'2021-09-11',	'09:29:19',	'ques description90'),
(11,	1,	'username1',	'ques title 1',	'2021-09-11',	'09:29:19',	'ques desc 1'),
(12,	1,	'username1',	'ques title 1',	'2021-09-11',	'09:29 AM',	'ques desc 1'),
(13,	1,	'username1',	'ques title 1',	'2021-09-11',	'09:29 AM',	'ques desc 1'),
(14,	1,	'username1',	'ques title 909',	'2021-09-11',	'09:29 AM',	'ques desc 1'),
(15,	1,	'username1',	'ques title 909',	'2021-09-11',	'09:29 AM',	'ques desc 1'),
(16,	3,	'user2',	'ques title 909',	'2021-09-11',	'09:29 AM',	'ques desc 1'),
(17,	3,	'user2',	'ques title 909',	'2021-09-11',	'09:29 AM',	'ques desc 1'),
(18,	1,	'fname1',	'quess101',	'2021-07-31',	'2:27 PM',	'ques desc 1'),
(19,	4,	'passajk1',	'newitl 12 july',	'2021-07-30',	'5:00 PM',	'desc up[date chal rhaha'),
(20,	7,	'Ajalil',	's1',	'2021-07-21',	'12:53 PM',	's2'),
(21,	7,	'Ajalil',	's1',	'2021-07-21',	'12:53 PM',	's2'),
(22,	7,	'Ajalil',	's1',	'2021-07-21',	'12:53 PM',	's2'),
(23,	1,	'fname1',	'asasas',	'2021-07-31',	'12:56 PM',	'asasas'),
(24,	1,	'fname1',	'q2',	'2021-07-30',	'1:54 PM',	'q2t'),
(25,	11,	'Ali Bhai',	'q1',	'2021-07-24',	'1:22 PM',	'zdd'),
(26,	11,	'Ali Bhai',	'q1',	'2021-07-24',	'1:22 PM',	''),
(27,	10,	'Abdul Jalil',	'aas',	'2021-07-31',	'7:56 PM',	'asasas'),
(28,	10,	'Abdul Jalil',	'new name',	'2021-07-31',	'3:03 PM',	'aaas'),
(29,	9,	'Abdul Jalil',	'asasas',	'2021-07-31',	'8:05 PM',	'asas'),
(30,	10,	'Abdul Jalil',	'done',	'2021-07-31',	'2:03 PM',	'don'),
(31,	10,	'Abdul Jalil',	'done',	'2021-07-31',	'2:03 PM',	'don'),
(32,	11,	'Ali Bhai',	'testing',	'2021-07-27',	'5:38 PM',	'this is testing');

DROP TABLE IF EXISTS `schadule`;
CREATE TABLE `schadule` (
  `sno` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `time` varchar(255) DEFAULT NULL,
  `date` varchar(255) NOT NULL,
  `des` varchar(1000) NOT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `schadule` (`sno`, `user_id`, `user_name`, `title`, `time`, `date`, `des`) VALUES
(1,	3,	'user2',	'a',	'1:41 PM',	'2021-07-10',	'aa'),
(2,	1,	'user1',	'109 sch',	'12:24 PM',	'2021-07-31',	'ok'),
(3,	1,	'user1',	'sch ka titles',	'09:29:10',	'2021-09-11',	'schedescription90'),
(4,	2,	'user2',	'sch ka titles',	'09:29:19',	'2021-09-11',	'schedescription90'),
(5,	1112,	'user2',	'sch ka titles',	'09:29:19',	'2021-09-11',	'schedescription90'),
(6,	2,	'uuuuuser2 ka username',	'sch for user 2',	'09:29:19',	'2021-09-11',	'schedescription90'),
(7,	3,	'uuuuuser2 ka username',	'sch for user 3',	'09:29:19',	'2021-09-11',	'schedescription90'),
(9,	1,	'fname1',	'titl909	',	'6:30 PM',	'2021-07-02',	'desc90'),
(10,	1,	'fname1',	'titl909	80000',	'6:30 PM',	'2021-07-02',	'desc90 8000000'),
(11,	1,	'fname1',	'titl909	80000',	'6:30 PM',	'2021-07-02',	'desc90 8000000'),
(12,	1,	'fname1',	'titl909	80000',	'6:30 PM',	'2021-07-31',	'desc90 8000000'),
(13,	1,	'fname1',	'titl909	80000',	'6:30 PM',	'2021-07-31',	'desc90 8000000'),
(14,	1,	'fname1',	'titl909	80000',	'6:30 PM',	'2021-07-31',	'desc90 8000000'),
(15,	1,	'fname1',	'titl909	80000',	'6:30 PM',	'2021-07-31',	'desc90 8000000'),
(16,	1,	'fname1',	'titl909	80000',	'6:30 PM',	'2021-07-31',	'desc90 8000000'),
(17,	1,	'fname1',	'new task 100',	'12:00 PM',	'2021-07-31',	'task desc'),
(19,	2,	'name',	'titles',	'10:90 PM',	'2101-10-11',	'description'),
(20,	2,	'',	'titles',	'10:90 PM',	'2101-10-11',	'description'),
(21,	9,	'Abdul Jalil',	'aukaa',	'2:26 PM',	'2021-07-31',	'asassa'),
(22,	9,	'usernanme2',	'ok',	'2:03 PM',	'2021-07-31',	'ok'),
(23,	9,	'usernanme2',	'ok',	'2:03 PM',	'2021-07-31',	'ok'),
(24,	9,	'usernanme2',	'ok',	'2:03 PM',	'2021-07-31',	'ok'),
(25,	9,	'usernanme2',	'ok',	'2:03 PM',	'2021-07-31',	'ok'),
(26,	9,	'usernanme2',	'ok',	'2:03 PM',	'2021-07-31',	'ok'),
(27,	11,	'Ali Bhai',	'task1',	'7:00 PM',	'2021-07-31',	'desc task 1'),
(28,	13,	'Bilal',	'drivning saad',	'19:12',	'2021-07-26 15:12:36.745252',	'Drive saad to indie'),
(29,	13,	'Bilal',	'drivning saad',	'19:12',	'2021-07-26 15:12:36.745252',	'Drive saad to indie'),
(30,	13,	'Bilal',	'drivning saad',	'19:12',	'2021-07-26 15:12:36.745252',	'Drive saad to indie'),
(31,	19,	'webtrica',	'111',	'TimeOfDay(14:51)',	'2021-08-31 14:51:45.033590',	'111'),
(32,	19,	'webtrica',	'task',	'10:40 PM',	'2021-09-29',	'12'),
(33,	11,	'Ali Bhai',	'fråga',	'TimeOfDay(21:09)',	'2021-09-12 21:09:12.346930',	'hdjslsls '),
(34,	11,	'Ali Bhai',	'fråga',	'TimeOfDay(21:09)',	'2021-09-12 21:09:12.346930',	'hdjslsls ');

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `sno` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(70) NOT NULL,
  `user_name` varchar(70) NOT NULL,
  `password` varchar(70) NOT NULL,
  `role` varchar(100) NOT NULL,
  `img` varchar(255) NOT NULL,
  PRIMARY KEY (`sno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `user` (`sno`, `name`, `user_name`, `password`, `role`, `img`) VALUES
(11,	'Ali Bhai',	'user1',	'pass1',	'User A',	'2021 07 13-18 17_Screenshot_1609923040.png'),
(12,	'Abdul Jalil',	'user2',	'pass2',	'User B',	'2021 07 14-17 36_Screenshot_1609923040.png'),
(13,	'Bilal',	'user3',	'pass3',	'User C',	'2021 07 14-18 22_Screenshot_1609923040.png'),
(15,	'user55',	'1234',	'fname55',	'User C',	'2021 07 15-19 00_image_picker2689479490522898783.jpg'),
(16,	'user3',	'pass2',	'Bilal',	'User B',	'2021-07-15-22:18_Screenshot_1609923040.png'),
(17,	'uer',	'user',	'pass',	'User B',	'2021-07-15-23:09_image_picker9071422235810865660.jpg'),
(18,	'tester1',	'tester1',	'123',	'User A',	'2021-07-26-19:12_image_picker4341458467791975754.jpg'),
(19,	'webtrica',	'webtrica@gmail.com',	'webtrica',	'User B',	'2021-07-26-19:40_image_picker8168265818632232539.jpg'),
(20,	'name',	'useremail',	'passss',	'User D',	'2021-08-31-18:09_image_picker936784503290796018.jpg');

-- 2021-10-29 09:27:44
