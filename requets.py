# ! /usr/bin/env python3
# coding: utf-8

'''
    create_database.py
    Author: Jimi Bourgeois
    Version: 2019-04-19
    Describe: Requets of the all program
'''

# Requets of create database structure
# Create database name
db_mydb = """CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ; """

# Requet of create table "categories"
table_categories = """CREATE TABLE IF NOT EXISTS `mydb`.`Categoris` (`category_id` INT NOT NULL AUTO_INCREMENT, `category_name` VARCHAR(150) NOT NULL, `category_url` VARCHAR(200) NOT NULL, PRIMARY KEY (`category_id`)) ENGINE = InnoDB; """

# Requet of create table "products"
table_products = """
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
ENGINE = InnoDB; """

# Requet of create table "Substitute"
table_substitute = """
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
    ON UPDATE NO ACTION); """