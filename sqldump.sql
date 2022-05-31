-- phpMyAdmin SQL Dump
-- version 5.1.3-2.el7.remi
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 31, 2022 at 10:33 PM
-- Server version: 10.6.7-MariaDB-log
-- PHP Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_chaplygy`
--

-- --------------------------------------------------------

--
-- Table structure for table `Cashiers`
--
-- Creation: May 12, 2022 at 11:24 PM
-- Last update: May 31, 2022 at 09:36 PM
--

DROP TABLE IF EXISTS `Cashiers`;
CREATE TABLE `Cashiers` (
  `cashier_id` int(11) NOT NULL,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `day_total` int(4) NOT NULL,
  `day_worked` date NOT NULL,
  `lane` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `Cashiers`:
--

--
-- Dumping data for table `Cashiers`
--

INSERT INTO `Cashiers` (`cashier_id`, `first_name`, `last_name`, `day_total`, `day_worked`, `lane`) VALUES
(2, 'Bryce', 'Mould', 88, '2022-05-07', 5),
(3, 'Fulton', 'Bloodworth', 180, '2022-05-06', 1),
(4, 'Cardea', 'Rayne', 127, '2022-05-04', 3),
(5, 'Darius', 'Appleton', 187, '2022-04-14', 2),
(22, 'Jim', 'Halpert', 138, '2022-05-27', 7),
(23, 'Creed', 'Bratton', 156, '2022-05-19', 9),
(24, 'Creed', 'Bratton', 156, '2022-05-19', 9),
(25, 'Creed', 'Bratton', 156, '2022-05-19', 7),
(26, 'Pam', 'Beesley', 169, '2022-05-17', 3),
(27, 'New', 'Cashier', 200, '2022-05-29', 9),
(28, 'TEst', 'testint', 333, '2022-05-29', 3),
(29, 'doritos', 'nacho', 12, '0001-01-01', 2),
(30, 'doritos', 'ranch', 12, '2222-02-02', 2),
(31, 'cash', 'ier', 200, '2022-05-31', 14);

-- --------------------------------------------------------

--
-- Table structure for table `Customers`
--
-- Creation: May 31, 2022 at 09:25 PM
-- Last update: May 31, 2022 at 09:26 PM
--

DROP TABLE IF EXISTS `Customers`;
CREATE TABLE `Customers` (
  `customer_id` int(11) NOT NULL,
  `reward_id` int(11) DEFAULT NULL,
  `customer_phone` varchar(16) DEFAULT NULL,
  `customer_email` varchar(328) DEFAULT NULL,
  `first_name` varchar(64) NOT NULL DEFAULT 'Anonymous ',
  `last_name` varchar(64) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `Customers`:
--   `reward_id`
--       `Rewards` -> `reward_id`
--

--
-- Dumping data for table `Customers`
--

INSERT INTO `Customers` (`customer_id`, `reward_id`, `customer_phone`, `customer_email`, `first_name`, `last_name`) VALUES
(8, 15, '(570) 279-3159', 'AlfElder@hello.com', 'Alf', 'Elder'),
(9, 2, '(321) 311-0246', 'RoyFox@hello.com', 'Roy', 'Fox'),
(10, 2, '(813) 829-2654', 'MorganFulton@hello.com', 'Morgan', 'Fulton'),
(11, NULL, '(335) 408-1109', 'NyreeRussel@hello.com', 'Nyree', 'Russel'),
(12, NULL, NULL, NULL, 'Anonymous ', NULL),
(181, NULL, '903-999-9999', 'jim@none.com', 'jim', 'halpert'),
(183, NULL, '3333333333', 'ABC@abc.org', 'Sample', 'sample2'),
(186, NULL, '5554443333', 'thisemail@email.org', 'Milo', 'Asamplename'),
(188, 3, '3423543244', 'doe@gmail.com', 'joe', 'doe'),
(195, 2, '999-777-1234', 'ryanh@none.com', 'Ryan', 'Howard'),
(291, 3, '541-999-9999', 'new@none.com', 'New ', 'Customer'),
(320, 2, '12345678', 'random@email.com', 'Test', 'Testing'),
(321, NULL, '3452498912', 'eriksonl@none.com', 'Laef', 'Erikson'),
(322, NULL, '33333', 'email.com', 'Char', 'H'),
(325, 2, '4321', 'email@.com', 'trhhr', 'rthrthr');

-- --------------------------------------------------------

--
-- Table structure for table `Products`
--
-- Creation: May 12, 2022 at 11:24 PM
-- Last update: May 31, 2022 at 09:37 PM
--

DROP TABLE IF EXISTS `Products`;
CREATE TABLE `Products` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(32) NOT NULL,
  `product_price` decimal(6,2) NOT NULL,
  `stock` int(3) NOT NULL,
  `type` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `Products`:
--

--
-- Dumping data for table `Products`
--

INSERT INTO `Products` (`product_id`, `product_name`, `product_price`, `stock`, `type`) VALUES
(2, 'Chicken Tenders', '19.29', 15, 'Poultry'),
(3, 'Doritos', '3.99', 30, 'Snack'),
(4, 'Turkey', '26.99', 10, 'Poultry '),
(5, 'Chimichanga', '5.99', 40, 'Burrito'),
(21, 'Mac aronie', '5.99', 50, 'Pasta'),
(30, 'New Product', '50.00', 50, 'Test'),
(52, 'Coffee', '3.75', 200, 'Beverage');

-- --------------------------------------------------------

--
-- Table structure for table `Purchases`
--
-- Creation: May 13, 2022 at 12:38 AM
-- Last update: May 31, 2022 at 09:47 PM
--

DROP TABLE IF EXISTS `Purchases`;
CREATE TABLE `Purchases` (
  `purchase_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `customer_id` int(11) NOT NULL,
  `cashier_id` int(11) NOT NULL,
  `total_price` decimal(6,2) NOT NULL,
  `purchase_complete` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `Purchases`:
--   `customer_id`
--       `Customers` -> `customer_id`
--   `cashier_id`
--       `Cashiers` -> `cashier_id`
--

--
-- Dumping data for table `Purchases`
--

INSERT INTO `Purchases` (`purchase_id`, `date`, `customer_id`, `cashier_id`, `total_price`, `purchase_complete`) VALUES
(77, '2022-05-29 11:53:02', 8, 4, '500.00', 0),
(78, '2022-05-29 11:55:59', 9, 26, '123.00', 1),
(81, '2022-05-31 12:56:50', 11, 3, '50.00', 1),
(82, '2022-05-31 14:05:04', 181, 23, '200.00', 1);

-- --------------------------------------------------------

--
-- Table structure for table `Purchases_Products`
--
-- Creation: May 29, 2022 at 06:22 PM
-- Last update: May 31, 2022 at 09:47 PM
--

DROP TABLE IF EXISTS `Purchases_Products`;
CREATE TABLE `Purchases_Products` (
  `purchase_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(3) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `Purchases_Products`:
--   `product_id`
--       `Products` -> `product_id`
--   `purchase_id`
--       `Purchases` -> `purchase_id`
--

--
-- Dumping data for table `Purchases_Products`
--

INSERT INTO `Purchases_Products` (`purchase_id`, `product_id`, `quantity`) VALUES
(77, 3, 3),
(77, 4, 2),
(77, 21, 1),
(78, 21, 3),
(78, 30, 1),
(81, 2, 3),
(81, 5, 1),
(81, 21, 2),
(82, 2, 5),
(82, 3, 3),
(82, 4, 1),
(82, 5, 2);

-- --------------------------------------------------------

--
-- Table structure for table `Rewards`
--
-- Creation: May 12, 2022 at 11:24 PM
-- Last update: May 31, 2022 at 09:36 PM
--

DROP TABLE IF EXISTS `Rewards`;
CREATE TABLE `Rewards` (
  `reward_id` int(11) NOT NULL,
  `reward_points` int(6) NOT NULL,
  `reward_discount` int(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- RELATIONSHIPS FOR TABLE `Rewards`:
--

--
-- Dumping data for table `Rewards`
--

INSERT INTO `Rewards` (`reward_id`, `reward_points`, `reward_discount`) VALUES
(2, 10, 1),
(3, 200, 20),
(15, 50, 5),
(16, 15, 1),
(18, 10, 1),
(39, 300, 30),
(42, 5, 5),
(43, 100, 10);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Cashiers`
--
ALTER TABLE `Cashiers`
  ADD PRIMARY KEY (`cashier_id`);

--
-- Indexes for table `Customers`
--
ALTER TABLE `Customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `customer_phone` (`customer_phone`),
  ADD UNIQUE KEY `customer_email` (`customer_email`),
  ADD UNIQUE KEY `last_name` (`last_name`),
  ADD UNIQUE KEY `first_name_3` (`first_name`,`last_name`) USING BTREE,
  ADD KEY `reward_id` (`reward_id`);

--
-- Indexes for table `Products`
--
ALTER TABLE `Products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `Purchases`
--
ALTER TABLE `Purchases`
  ADD PRIMARY KEY (`purchase_id`,`date`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`cashier_id`);

--
-- Indexes for table `Purchases_Products`
--
ALTER TABLE `Purchases_Products`
  ADD PRIMARY KEY (`purchase_id`,`product_id`),
  ADD KEY `Purchases_Products_ibfk_1` (`product_id`);

--
-- Indexes for table `Rewards`
--
ALTER TABLE `Rewards`
  ADD PRIMARY KEY (`reward_id`,`reward_points`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Cashiers`
--
ALTER TABLE `Cashiers`
  MODIFY `cashier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `Customers`
--
ALTER TABLE `Customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=333;

--
-- AUTO_INCREMENT for table `Products`
--
ALTER TABLE `Products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `Purchases`
--
ALTER TABLE `Purchases`
  MODIFY `purchase_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=84;

--
-- AUTO_INCREMENT for table `Rewards`
--
ALTER TABLE `Rewards`
  MODIFY `reward_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Customers`
--
ALTER TABLE `Customers`
  ADD CONSTRAINT `Customers_ibfk_1` FOREIGN KEY (`reward_id`) REFERENCES `Rewards` (`reward_id`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Constraints for table `Purchases`
--
ALTER TABLE `Purchases`
  ADD CONSTRAINT `Purchases_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Purchases_ibfk_2` FOREIGN KEY (`cashier_id`) REFERENCES `Cashiers` (`cashier_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `Purchases_Products`
--
ALTER TABLE `Purchases_Products`
  ADD CONSTRAINT `Purchases_Products_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `Purchases_Products_ibfk_2` FOREIGN KEY (`purchase_id`) REFERENCES `Purchases` (`purchase_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
