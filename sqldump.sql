-- MariaDB dump 10.19  Distrib 10.4.24-MariaDB, for Linux (x86_64)
--
-- Host: classmysql.engr.oregonstate.edu    Database: cs340_chaplygy
-- ------------------------------------------------------
-- Server version	10.6.7-MariaDB-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Cashiers`
--

DROP TABLE IF EXISTS `Cashiers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cashiers` (
  `cashier_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `day_total` int(4) NOT NULL,
  `day_worked` date NOT NULL,
  `lane` int(1) DEFAULT NULL,
  PRIMARY KEY (`cashier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cashiers`
--

LOCK TABLES `Cashiers` WRITE;
/*!40000 ALTER TABLE `Cashiers` DISABLE KEYS */;
INSERT INTO `Cashiers` VALUES (1,'Bran','Devin',26,'2022-05-01',8),(2,'Bryce','Mould',88,'2022-05-07',5),(3,'Fulton','Bloodworth',180,'2022-05-06',1),(4,'Cardea','Rayne',127,'2022-05-04',3),(5,'Darius','Appleton',187,'2022-04-14',2);
/*!40000 ALTER TABLE `Cashiers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Customers` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `reward_id` int(11) DEFAULT NULL,
  `customer_phone` varchar(16) DEFAULT NULL,
  `customer_email` varchar(328) DEFAULT NULL,
  `first_name` varchar(64) NOT NULL DEFAULT 'Anonymous ',
  `last_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `customer_phone` (`customer_phone`),
  UNIQUE KEY `customer_email` (`customer_email`),
  KEY `reward_id` (`reward_id`),
  CONSTRAINT `Customers_ibfk_1` FOREIGN KEY (`reward_id`) REFERENCES `Rewards` (`reward_id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customers`
--

LOCK TABLES `Customers` WRITE;
/*!40000 ALTER TABLE `Customers` DISABLE KEYS */;
INSERT INTO `Customers` VALUES (8,1,'(570) 279-3159','AlfElder@hello.com','Alf','Elder'),(9,2,'(321) 311-0246','RoyFox@hello.com','Roy','Fox'),(10,2,'(813) 829-2654','MorganFulton@hello.com','Morgan','Fulton'),(11,1,'(335) 408-1109','NyreeRussel@hello.com','Nyree','Russel'),(12,NULL,NULL,NULL,'Anonymous ',NULL);
/*!40000 ALTER TABLE `Customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Products`
--

DROP TABLE IF EXISTS `Products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Products` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `product_name` varchar(32) NOT NULL,
  `product_price` decimal(6,2) NOT NULL,
  `stock` int(3) NOT NULL,
  `type` varchar(32) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Products`
--

LOCK TABLES `Products` WRITE;
/*!40000 ALTER TABLE `Products` DISABLE KEYS */;
INSERT INTO `Products` VALUES (1,'Potato Chips',5.79,50,'Snack'),(2,'Chicken Tenders',19.29,15,'Poultry'),(3,'Doritos',3.99,30,'Snack'),(4,'Turkey',26.99,10,'Poultry '),(5,'Chimichanga',5.99,40,'Burrito');
/*!40000 ALTER TABLE `Products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Purchases`
--

DROP TABLE IF EXISTS `Purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Purchases` (
  `purchase_id` int(11) NOT NULL AUTO_INCREMENT,
  `purchase_date` datetime NOT NULL,
  `customer_id` int(11) NOT NULL,
  `cashier_id` int(11) NOT NULL,
  `total_price` decimal(6,2) NOT NULL,
  `purchase_complete` tinyint(1) NOT NULL,
  PRIMARY KEY (`purchase_id`,`date`),
  KEY `customer_id` (`customer_id`),
  KEY `product_id` (`cashier_id`),
  CONSTRAINT `Purchases_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `Customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Purchases_ibfk_2` FOREIGN KEY (`cashier_id`) REFERENCES `Cashiers` (`cashier_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Purchases`
--

LOCK TABLES `Purchases` WRITE;
/*!40000 ALTER TABLE `Purchases` DISABLE KEYS */;
INSERT INTO `Purchases` VALUES (1,'2022-05-13 09:22:16',9,1,15.00,1),(2,'2022-05-04 11:23:26',8,2,19.29,1),(3,'2022-05-07 09:25:26',8,3,26.99,1),(4,'2022-05-01 09:23:25',11,3,50.00,0);
/*!40000 ALTER TABLE `Purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Purchases_Products`
--

DROP TABLE IF EXISTS `Purchases_Products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Purchases_Products` (
  `purchase_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(3) DEFAULT NULL,
  PRIMARY KEY (`purchase_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `Purchases_Products_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `Products` (`product_id`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `Purchases_Products_ibfk_2` FOREIGN KEY (`purchase_id`) REFERENCES `Purchases` (`purchase_id`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Purchases_Products`
--

LOCK TABLES `Purchases_Products` WRITE;
/*!40000 ALTER TABLE `Purchases_Products` DISABLE KEYS */;
INSERT INTO `Purchases_Products` VALUES (1,2,5),(2,5,5),(3,3,1),(4,4,1);
/*!40000 ALTER TABLE `Purchases_Products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Rewards`
--

DROP TABLE IF EXISTS `Rewards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Rewards` (
  `reward_id` int(11) NOT NULL AUTO_INCREMENT,
  `reward_points` int(6) NOT NULL,
  `reward_discount` int(6) DEFAULT NULL,
  PRIMARY KEY (`reward_id`,`reward_points`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Rewards`
--

LOCK TABLES `Rewards` WRITE;
/*!40000 ALTER TABLE `Rewards` DISABLE KEYS */;
INSERT INTO `Rewards` VALUES (1,100,10),(2,10,1),(3,200,20);
/*!40000 ALTER TABLE `Rewards` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-05-12 17:52:09
