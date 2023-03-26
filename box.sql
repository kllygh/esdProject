-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 17, 2023 at 01:38 PM
-- Server version: 8.0.27
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `box`
--

-- --------------------------------------------------------

--
-- Table structure for table `box`
--

CREATE DATABASE IF NOT EXISTS `box` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `box`;

DROP TABLE IF EXISTS `box`;
CREATE TABLE IF NOT EXISTS `box` (
  `boxID` int NOT NULL,
  `boxName` varchar(30) NOT NULL,
  `restaurant_id` int NOT NULL,
  `cust_id` int NOT NULL,
  `postTime` datetime NOT NULL,
  `inventory` int NOT NULL,
  `collectionTime` datetime NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `description` varchar(64) DEFAULT NULL,
  `postName` varchar(64) NOT NULL,
  `postDate` date NOT NULL,
  PRIMARY KEY (`boxID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `box` (`boxID`, `boxName`, `restaurant_id`, `cust_id`, `postTime`, `inventory`, `collectionTime`, `price`, `description`, `postName`,`postDate`) VALUES
(1, 'Subway', 82763492, 23418923, '2023-03-26 21:43:02', 2, '2023-03-26 21:43:02', '11', 'nil', 'Subway-PS A','2023-03-26'),
(2, 'Subway', 82763492, 23418923, '2023-03-26 21:43:02', 2, '2023-03-26 21:43:02', '11', 'nil', 'Subway-PS B','2023-03-26'),
(3, 'SuShiExpress', 82763491, 23418923, '2023-03-26 21:43:02', 2, '2023-03-26 21:43:02', '11', 'nil', 'Sushi Express-PLQ A','2023-03-26'),
(4, 'SuShiExpress', 82763491, 23418923, '2023-03-18 21:43:02', 2, '2023-03-26 21:43:02', '11', 'nil', 'Sushi Express-PLQ A','2023-03-26'),
(5, 'SuShiExpress', 82763491, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Sushi Express-PLQ C','2023-03-26'),
(6, 'Saizeriya', 82763490, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Saizeriya-CCP A','2023-03-26'),
(7, 'Saizeriya', 82763490, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Saizeriya-CCP B','2023-03-26'),
(39, 'Yoshinoya', 82763493, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Yoshinoya- BJ A','2023-03-26'),
(8, 'Yoshinoya', 82763493, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Yoshinoya- BJ B','2023-03-26'),
(9, 'Stuffd', 82763494, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Stuffd- BM A','2023-03-24'),
(10, 'Stuffd', 82763494, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Stuffd- BM B','2023-03-24'),
(11, 'Stuffd', 82763494, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Stuffd- BM C','2023-03-24'),
(12, 'Maki-San', 82763495, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Maki-San- WD A','2023-03-24'),
(13, 'Maki-San', 82763495, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Maki-San- WD B','2023-03-24'),
(14, 'Maki-San', 82763495, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Maki-San- WD C','2023-03-24'),
(15, 'PastaMania', 82763496, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'PastaMania- CSM A','2023-03-24'),
(16, 'PastaMania', 82763496, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'PastaMania- CSM B','2023-03-24'),
(17, 'PastaMania', 82763496, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'PastaMania- CSM C','2023-03-24'),
(18, 'PastaMania', 82763496, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'PastaMania- CSM D','2023-03-24'),
(19, 'Guzman y Gomez', 82763497, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Guzman y Gomez- OG A','2023-03-24'),
(20, 'Guzman y Gomez', 82763497, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Guzman y Gomez- OG B','2023-03-24'),
(21, 'Guzman y Gomez', 82763497, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Guzman y Gomez- OG C','2023-03-24'),
(22, 'Kanshoku Ramen Bar', 82763498, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Kanshoku Ramen Bar- OG A','2023-03-24'),
(23, 'Cedele', 82763499, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Cedele- WP A','2023-03-24'),
(24, 'Cedele', 82763499, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Cedele- WP B','2023-03-24'),
(25, 'Green Dot', 82863491, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Green Dot- NP A','2023-03-24'),
(26, 'Bornga', 82863492, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Bornga- SC A','2023-03-24'),
(27, 'Green Signature', 82863493, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Green Signature- WP A','2023-03-24'),
(28, 'Pizza Hut', 82863494, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Pizza Hut- TM A','2023-03-24'),
(29, 'MOS Burger', 82863495, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'MOS Burger- JC A','2023-03-24'),
(30, 'Nakhon Kitchen Thai Restaurant', 82863496, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Nakhon Kitchen Thai Restaurant- K A','2023-03-24'),
(31, 'Papparich', 82863497, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Papparich- PP A','2023-03-24'),
(32, 'NamNam Noodle Bar', 82863498, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'NamNam Noodle Bar- RC A','2023-03-24'),
(33, 'Astons Specialties', 82863499, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Astons Specialties- C A','2023-03-24'),
(34, 'Tim Ho Wan', 82963490, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Tim Ho Wan- J A','2023-03-24'),
(35, 'Shin-Sapporo Ramen', 82963491, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Shin-Sapporo Ramen - OG A','2023-03-24'),
(36, 'Tori-Q', 82963492, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Tori-Q - J8 A','2023-03-24'),
(37, 'Four Leaves', 82963493, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Four Leaves - YTP A','2023-03-24'),
(38, 'Breadtalk', 82963494, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Breadtalk - JKC A','2023-03-24');


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


