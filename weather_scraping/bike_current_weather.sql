-- MySQL dump 10.13  Distrib 8.0.42, for macos15 (x86_64)
--
-- Host: localhost    Database: bike
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `current_weather`
--

DROP TABLE IF EXISTS `current_weather`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `current_weather` (
  `dt` bigint NOT NULL,
  `feels_like` float DEFAULT NULL,
  `humidity` int DEFAULT NULL,
  `pressure` int DEFAULT NULL,
  `temp` float DEFAULT NULL,
  `weather_id` int DEFAULT NULL,
  `weather_main` varchar(50) DEFAULT NULL,
  `weather_description` varchar(100) DEFAULT NULL,
  `wind_speed` float DEFAULT NULL,
  `wind_gust` float DEFAULT NULL,
  `rain_1h` float DEFAULT NULL,
  `clouds_all` int DEFAULT NULL,
  PRIMARY KEY (`dt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `current_weather`
--

LOCK TABLES `current_weather` WRITE;
/*!40000 ALTER TABLE `current_weather` DISABLE KEYS */;
INSERT INTO `current_weather` VALUES (1770920126,2.91,97,986,6.64,803,'Clouds','broken clouds',6.17,0,0,75),(1770946554,0.61,97,986,5.62,803,'Clouds','broken clouds',9.26,0,0,75),(1770947177,0.78,96,986,5.75,803,'Clouds','broken clouds',9.26,0,0,75),(1770947779,0.78,96,986,5.75,803,'Clouds','broken clouds',9.26,0,0,75),(1770948431,0.87,97,986,5.75,803,'Clouds','broken clouds',8.94,0,0,75),(1770972445,-2.48,94,994,3.68,500,'Rain','light rain',11.18,0,0.45,75),(1770981282,-2.35,92,998,3.7,803,'Clouds','broken clouds',10.8,0,0,75),(1770982056,-2.68,93,998,3.45,803,'Clouds','broken clouds',10.8,0,0,75),(1770983054,-2.22,92,999,3.78,803,'Clouds','broken clouds',10.73,0,0,75),(1770987003,-1.71,88,1000,4.08,803,'Clouds','broken clouds',10.29,0,0,75),(1770990992,-1.29,82,1001,4.48,803,'Clouds','broken clouds',10.73,0,0,75),(1770994740,-0.58,73,1003,4.93,803,'Clouds','broken clouds',10.29,0,0,75),(1770998384,-0.89,75,1004,4.48,803,'Clouds','broken clouds',9.26,0,0,75),(1771001857,-0.59,74,1005,4.47,802,'Clouds','scattered clouds',8.23,13.89,0,40),(1771017180,-2.84,80,1011,1.72,801,'Clouds','few clouds',5.14,0,0,20),(1771021782,-3.01,81,1012,1.1,801,'Clouds','few clouds',4.12,0,0,20),(1771025354,-3.6,82,1013,0.62,801,'Clouds','few clouds',4.12,0,0,20),(1771029081,-4.39,82,1015,-0.02,601,'Snow','snow',4.12,0,0,20),(1771032151,-5.07,83,1015,-0.3,801,'Clouds','few clouds',4.63,0,0,20),(1771035795,-4.88,83,1015,-0.42,801,'Clouds','few clouds',4.12,0,0,20),(1771039545,-4.6,83,1016,-0.19,801,'Clouds','few clouds',4.12,0,0,20),(1771043409,-3.68,81,1017,0.26,801,'Clouds','few clouds',3.6,0,0,20),(1771047114,-3.44,83,1017,-0.29,801,'Clouds','few clouds',2.57,0,0,20),(1771050714,-3.29,83,1018,-0.65,801,'Clouds','few clouds',2.06,0,0,20),(1771053793,-4.64,83,1018,-0.88,801,'Clouds','few clouds',3.09,0,0,20),(1771057915,-3.57,84,1018,-0.4,803,'Clouds','broken clouds',2.57,0,0,75),(1771061152,-3.89,83,1018,0.57,803,'Clouds','broken clouds',4.47,0,0,75),(1771064826,0.44,80,1018,2.98,803,'Clouds','broken clouds',2.57,0,0,75),(1771068715,2.05,78,1017,4.33,803,'Clouds','broken clouds',2.57,0,0,75),(1771071991,2.98,73,1017,5.12,803,'Clouds','broken clouds',2.57,0,0,75),(1771075747,3.1,70,1016,5.22,803,'Clouds','broken clouds',2.57,0,0,75),(1771079382,2.06,59,1015,5.22,803,'Clouds','broken clouds',4.12,0,0,75),(1771082645,1.02,59,1014,5.15,803,'Clouds','broken clouds',6.17,0,0,75),(1771086716,0.2,73,1012,4.81,500,'Rain','light rain',7.2,12.35,0.65,75),(1771089800,-0.79,76,1012,4.87,501,'Rain','moderate rain',10.8,16.98,2.51,75),(1771093388,-2.04,86,1011,3.22,501,'Rain','moderate rain',7.72,0,3.99,75),(1771097377,-2.56,90,1010,2.82,500,'Rain','light rain',7.72,0,0.27,75),(1771100556,-1.93,89,1007,3.31,500,'Rain','light rain',7.72,0,0.15,75),(1771104392,-1.18,87,1005,4.02,803,'Clouds','broken clouds',8.23,0,0,75),(1771107964,-0.74,84,1005,5.34,803,'Clouds','broken clouds',13.38,21.09,0,75),(1771111782,0.01,84,1004,5.97,300,'Drizzle','light intensity drizzle',13.89,20.06,0,75),(1771115263,2.36,82,1003,7.23,803,'Clouds','broken clouds',10.8,16.46,0,75),(1771118634,3.95,84,1003,7.72,803,'Clouds','broken clouds',7.2,0,0,75),(1771122528,3.96,88,1002,7.73,803,'Clouds','broken clouds',7.2,0,0,75),(1771126182,5.67,89,1001,8.81,803,'Clouds','broken clouds',6.17,0,0,75),(1771129873,5.86,89,1000,8.82,803,'Clouds','broken clouds',5.66,0,0,75),(1771133192,5.58,89,1000,8.44,803,'Clouds','broken clouds',5.14,0,0,75),(1771137013,5.97,87,998,8.58,803,'Clouds','broken clouds',4.63,0,0,75),(1771140600,5.47,87,998,8.78,803,'Clouds','broken clouds',6.69,0,0,75),(1771144300,5.53,86,997,8.83,500,'Rain','light rain',6.69,0,0.68,40),(1771147524,4.39,90,997,8.4,803,'Clouds','broken clouds',8.75,0,0,75),(1771151382,5.02,89,996,8.78,803,'Clouds','broken clouds',8.23,0,0,75),(1771155073,5.53,85,994,9.06,802,'Clouds','scattered clouds',7.72,0,0,40),(1771158696,6.42,81,993,9.85,802,'Clouds','scattered clouds',8.23,0,0,40),(1771162028,9.56,74,993,10.52,802,'Clouds','scattered clouds',8.75,0,0,40),(1771165921,6.23,77,993,9.89,802,'Clouds','scattered clouds',9.26,0,0,40),(1771169192,6.01,77,993,9.81,803,'Clouds','broken clouds',9.77,0,0,75),(1771172570,4.31,83,992,8.12,803,'Clouds','broken clouds',7.72,0,0,75),(1771176201,3.71,86,993,7.66,803,'Clouds','broken clouds',7.72,0,0,75);
/*!40000 ALTER TABLE `current_weather` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-15 18:21:05
