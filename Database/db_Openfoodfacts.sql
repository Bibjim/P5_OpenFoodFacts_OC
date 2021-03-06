-- MySQL Script generated by MySQL Workbench
-- ven. 19 avril 2019 00:09:19 CEST
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Categories` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(150) NOT NULL,
  `category_url` VARCHAR(200) NOT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(150) NOT NULL,
  `product_shop` VARCHAR(150) NULL,
  `product_nutri` VARCHAR(75) NULL,
  `product_url` VARCHAR(200) NOT NULL,
  `Categories_category_id` INT NOT NULL,
  PRIMARY KEY (`product_id`),
  INDEX `fk_Products_Categories_idx` (`Categories_category_id` ASC),
  UNIQUE INDEX `product_name_UNIQUE` (`product_name` ASC),
  CONSTRAINT `fk_Products_Categories`
    FOREIGN KEY (`Categories_category_id`)
    REFERENCES `mydb`.`Categories` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Substitute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Substitute` (
  `save_id` INT NOT NULL AUTO_INCREMENT,
  `save_product_id` INT NOT NULL,
  `save_product_sub_name` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`save_id`),
  INDEX `fk_Subtitute_Products1_idx` (`save_product_id` ASC),
  CONSTRAINT `fk_Data backup_Products1`
    FOREIGN KEY (`save_product_id`)
    REFERENCES `mydb`.`Products` (`product_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
