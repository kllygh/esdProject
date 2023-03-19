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
  `quantity` int NOT NULL,
  `collectionTime` datetime NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `description` varchar(64) DEFAULT NULL,
  `postName` varchar(64) NOT NULL,
  `postDate` date NOT NULL,
  PRIMARY KEY (`boxID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `box` (`boxID`, `boxName`, `restaurant_id`, `cust_id`, `postTime`, `quantity`, `collectionTime`, `price`, `description`, `postName`,`postDate`) VALUES
(1782487, 'Subway', 82763492, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Subway-PS','2023-03-19'),
(31243123, 'Subway', 82763492, 23418923, '2023-03-18 21:43:02', 2, '2023-03-18 21:43:02', '11', 'nil', 'Subway-PS','2023-03-19');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


