-- MySQL dump 10.13  Distrib 5.5.49, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: educacional_prediction
-- ------------------------------------------------------
-- Server version	5.5.49-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aluno`
--

DROP TABLE IF EXISTS `aluno`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aluno` (
  `MATRICULA` varchar(50) NOT NULL,
  `SIT_MATRICULA` int(2) DEFAULT NULL,
  `RENDA_FAMILIAR` int(2) DEFAULT NULL,
  `ANO_CONCLUSAO_2_GRAU` int(5) DEFAULT NULL,
  `TIPO_ESCOLA_ORIGEM` int(2) DEFAULT NULL,
  `RENDA_PER_CAPITA` int(2) DEFAULT NULL,
  `COD_ESTADO_CIVIL` int(1) DEFAULT NULL,
  `N_FILHOS` int(2) DEFAULT NULL,
  `SEXO` int(1) DEFAULT NULL,
  `DESC_CIDADE` int(1) DEFAULT NULL,
  `DT_NASCIMENTO` varchar(45) DEFAULT NULL,
  `PROFISSAO` int(1) DEFAULT NULL,
  `NIVEL_FALA_INGLES` int(1) DEFAULT NULL,
  `NIVEL_COMPREENSAO_INGLES` int(1) DEFAULT NULL,
  `NIVEL_ESCRITA_INGLES` int(1) DEFAULT NULL,
  `NIVEL_LEITURA_INGLES` int(1) DEFAULT NULL,
  `CURSO` varchar(4) DEFAULT NULL,
  `ANO_INGRESSO` int(11) DEFAULT NULL,
  `IDADE_INGRESSO` int(2) DEFAULT NULL,
  PRIMARY KEY (`MATRICULA`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aluno`
--

LOCK TABLES `aluno` WRITE;
/*!40000 ALTER TABLE `aluno` DISABLE KEYS */;
INSERT INTO `aluno` VALUES ('20171011080257',0,1,2012,0,0,1,2,1,0,'24/03/1994',1,1,1,1,1,'si',2017,23),('201721048579',0,1,2012,0,0,0,4,1,0,'24/03/1994',1,1,1,1,1,'si',2017,23);
/*!40000 ALTER TABLE `aluno` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usuario` (
  `id_user` int(11) NOT NULL,
  `login` varchar(45) DEFAULT NULL,
  `nome` varchar(45) DEFAULT NULL,
  `senha` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (0,'admin','Gestor Educacional','admin2017');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-03-30 23:19:10
