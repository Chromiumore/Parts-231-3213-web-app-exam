-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: web-app-exam
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('c278c4c75491');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedbacks`
--

DROP TABLE IF EXISTS `feedbacks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedbacks` (
  `id` int NOT NULL AUTO_INCREMENT,
  `recipe_id` int NOT NULL,
  `user_id` int NOT NULL,
  `rating` int NOT NULL,
  `feedback_text` text NOT NULL,
  `created_at` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_feedbacks_user_id_users` (`user_id`),
  KEY `fk_feedbacks_recipe_id_recipes` (`recipe_id`),
  CONSTRAINT `fk_feedbacks_recipe_id_recipes` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_feedbacks_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedbacks`
--

LOCK TABLES `feedbacks` WRITE;
/*!40000 ALTER TABLE `feedbacks` DISABLE KEYS */;
INSERT INTO `feedbacks` VALUES (9,28,1,4,'Мне ***понравилось***','2025-06-26'),(10,28,2,2,'Не очень','2025-06-26');
/*!40000 ALTER TABLE `feedbacks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `files` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `mime_type` varchar(50) NOT NULL,
  `recipe_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_files_recipe_id_recipes` (`recipe_id`),
  CONSTRAINT `fk_files_recipe_id_recipes` FOREIGN KEY (`recipe_id`) REFERENCES `recipes` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `files`
--

LOCK TABLES `files` WRITE;
/*!40000 ALTER TABLE `files` DISABLE KEYS */;
INSERT INTO `files` VALUES (27,'0db0d731-a3cd-4b3c-bdc3-8aac424af9a7-01ae54d47f8e6b3b18a94e79012f5887.jpg','image/jpeg',27),(28,'cf8b492a-6160-4ab3-944c-adbe92d5dfcd-carbonara-2000x1200.jpg','image/jpeg',27),(29,'f1c59e93-1510-41f5-bac1-476829693359-images.jpg','image/jpeg',27),(30,'097ccfd9-6caf-4bde-a7d5-d3f0ef8ddad0-Без названия.jpg','image/jpeg',27),(31,'4a6745d8-49e1-4112-b45d-240d0890cfb4-big_608187.jpg','image/jpeg',28);
/*!40000 ALTER TABLE `files` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipes`
--

DROP TABLE IF EXISTS `recipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `time` int NOT NULL,
  `portions` int NOT NULL,
  `ingredients` text NOT NULL,
  `user_id` int NOT NULL,
  `steps` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_recipes_user_id_users` (`user_id`),
  CONSTRAINT `fk_recipes_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipes`
--

LOCK TABLES `recipes` WRITE;
/*!40000 ALTER TABLE `recipes` DISABLE KEYS */;
INSERT INTO `recipes` VALUES (27,'Паста Карбонара','Классическая итальянская паста с нежным сливочно-яичным соусом, хрустящим беконом и пармезаном.',20,2,'* Спагетти – 200 г\n* Бекон (или панчетта) – 100 г\n* Яйца – 2 шт.\n* Желток – 1 шт.\n* Тертый пармезан – 50 г\n* Чеснок – 1 зубчик\n* Соль, черный перец – по вкусу\n* Оливковое масло – 1 ст. л.',2,'1. Приготовьте пасту: В кипящую подсоленную воду добавьте спагетти и варите до состояния al dente (8–10 минут).\n2. Обжарьте бекон: На сковороде разогрейте оливковое масло, добавьте мелко нарезанный бекон и чеснок. Жарьте до хрустящей корочки.\n3. Сделайте соус: В миске смешайте яйца, желток, пармезан, соль и перец.\n4. Соедините ингредиенты: Откиньте пасту на дуршлаг, сохраните 50 мл воды. Добавьте спагетти в сковороду с беконом, перемешайте. Снимите с огня, влейте яичную смесь, быстро помешивая. Если соус густой, добавьте немного воды от варки пасты.\n5. Подавайте: Посыпьте пармезаном и черным перцем.'),(28,'Шоколадные маффины','Воздушные шоколадные кексы с жидкой серединкой.',30,6,'* Мука – 150 г\n* Какао – 50 г\n* Сахар – 100 г\n* Яйца – 2 шт.\n* Молоко – 100 мл\n* Растительное масло – 80 мл\n* Разрыхлитель – 1 ч. л.\n* Шоколадные кусочки – 50 г',3,'1. Смешайте сухие ингредиенты: Муку, какао, сахар, разрыхлитель.\n2. Добавьте жидкие: Влейте яйца, молоко, масло, перемешайте до однородности.\n3. Добавьте шоколад: В тесто вмешайте шоколадные кусочки.\n4. Выпекайте: Разлейте тесто по формочкам, выпекайте 20 минут при 180°C.\n5. Подавайте: Теплыми, можно с мороженым.');
/*!40000 ALTER TABLE `recipes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin','Администратор'),(2,'user','Пользователь');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(40) NOT NULL,
  `password_hash` varchar(256) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `middle_name` varchar(50) DEFAULT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_users_role_id_roles` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','Сергеев','Владислав','Дмитриевич',1),(2,'user','65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5','Зубенко','Михаил','Петрович',2),(3,'john','799ef92a11af918e3fb741df42934f3b568ed2d93ac1df74f1b8d41a27932a6f','Doe','John',NULL,2);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-27 12:09:47
