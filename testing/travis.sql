CREATE DATABASE IF NOT EXISTS `dashr_collection` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `dashr_collection`;
CREATE TABLE IF NOT EXISTS `dashr` (
  `pin` int(11) NOT NULL,
  `data` longtext,
  `dashr_create_time` datetime NOT NULL,
  `session_time` datetime
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE IF NOT EXISTS `serial_pin` (
  `serial` int(11) NOT NULL,
  `pin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE `dashr`
  ADD PRIMARY KEY (`pin`);
ALTER TABLE `dashr`
  ADD PRIMARY KEY (`dashr_create_time`);
ALTER TABLE `serial_pin`
  ADD PRIMARY KEY (`serial`);
INSERT INTO TABLE `serial_pin` VALUES (261122326, 435), (261791206, 9307);
