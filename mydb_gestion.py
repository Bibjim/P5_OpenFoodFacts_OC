# ! /usr/bin/env python3
# coding: utf-8

'''
    mydb_gestion.py
    Author: Jimi Bourgeois
    Version: 2019-04-22
    Describe: Database connect
'''

import urllib.request as req
import json
import pymysql.cursors

from substitue_products import *

class db_request():

    def create_db(self):

        self.db_connect = pymysql.connect("localhost","root","")
        db = self.db_connect.cursor()

        database_sql = "CREATE DATABASE IF NOT EXISTS `mydb`"
        db.execute(database_sql)
        print("La base de donnée a bien été créée")
    
    def create_tables(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        table_cat = "CREATE TABLE IF NOT EXISTS `mydb`.`Categories` \
            (`category_id` INT NOT NULL AUTO_INCREMENT,\
            `category_name` VARCHAR(150) NOT NULL,\
            `category_url` VARCHAR(200) NOT NULL, \
            PRIMARY KEY (`category_id`)) ENGINE = InnoDB"

        table_prod = "CREATE TABLE IF NOT EXISTS `mydb`.`Products`\
            (`product_id` INT NOT NULL AUTO_INCREMENT,\
            `product_name` VARCHAR(150) NOT NULL,\
            `product_shop` VARCHAR(150) NULL,\
            `product_nutri` VARCHAR(75) NULL,\
            `product_url` VARCHAR(200) NOT NULL,\
            `Categories_category_id` INT NOT NULL,\
            PRIMARY KEY (`product_id`),\
            INDEX `fk_Products_Categories_idx` (`Categories_category_id` ASC),\
            UNIQUE INDEX `product_name_UNIQUE` (`product_name` ASC),\
            CONSTRAINT `fk_Products_Categories`\
            FOREIGN KEY (`Categories_category_id`)\
            REFERENCES `mydb`.`Categories` (`category_id`)\
            ON DELETE NO ACTION\
            ON UPDATE NO ACTION)\
            ENGINE = InnoDB"

        table_sub = "CREATE TABLE IF NOT EXISTS `mydb`.`Substitute` \
            (`save_id` INT NOT NULL AUTO_INCREMENT,\
            `save_product_id` INT NOT NULL,\
            `save_product_sub_name` VARCHAR(150) NOT NULL,\
            PRIMARY KEY (`save_id`),\
            INDEX `fk_Subtitute_Products1_idx` (`save_product_id` ASC),\
            CONSTRAINT `fk_Data backup_Products1`\
            FOREIGN KEY (`save_product_id`)\
            REFERENCES `mydb`.`Products` (`product_id`)\
            ON DELETE NO ACTION ON UPDATE NO ACTION)"
        db.execute(table_cat)
        db.execute(table_prod)
        db.execute(table_sub)
        print("La Structure de la base de données à bien été créée")

    def create_db_cat(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        url="https://fr.openfoodfacts.org/categories.json"
        u = req.urlopen(url)
        content = u.read()
        jsonstr = content.decode("UTF-8")
        dfAll = json.loads(jsonstr)

        for categories in dfAll['tags'][:30]:
            categories_name = categories['name']
            categories_name = categories_name.replace("'", " ")
            if len(categories_name) >= 30:
                continue
            dfAll = (categories_name, categories['url'])

            insert_cat = "INSERT IGNORE INTO `mydb`.`Categories` \
                (category_name, category_url) VALUES ('{}', '{}')"\
                .format(categories_name, categories['url'])
            db.execute(insert_cat)
            self.db_connect.commit()

                
        db.execute("SELECT COUNT(*) FROM `mydb`.`Categories`")
        sql_return = db.fetchone()
        print("\n*****************************************************************")
        print("* La base de données est chargée avec %s catégories de produits *" % (sql_return))
        print("*****************************************************************")

    def create_db_prod(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        db.execute("SELECT category_id, category_url FROM `mydb`.`Categories`")
        
        for ligne in db.fetchall():
            list_id_cat = ligne[0]
            list_url_cat = ligne[1]
            list_url_cat += '.json'
            
            url_prod = req.urlopen(list_url_cat)
            data = url_prod.read()
            dfAll = json.loads(data.decode("utf_8"))
                
            for products in dfAll['products']:
                product_name = products.get('product_name', "")
                product_name = product_name.replace("'"," ")
                if product_name is "":
                    break
                
                product_nutri = products.get('nutrition_grades_tags', "")
                product_nutri = str(product_nutri)
                product_nutri = product_nutri.replace("[", "")
                product_nutri = product_nutri.replace("'", "")
                product_nutri = product_nutri.replace("]", "")

                if 'stores' in products:
                    product_shop = str(products['stores'])
                    product_shop = product_shop.replace(" ", "-")
                    product_shop = product_shop.replace("'", "")
                    product_shop = product_shop.replace(",", " ")
                    if product_shop is "":
                        product_shop = ("Shop inconnu")
               
                else:
                    product_shop = ("Shop inconnu")
                product_url = products['url']

                insert_prod = "INSERT IGNORE INTO `mydb`.`Products`\
                    (product_name, product_shop, product_nutri, product_url, \
                    Categories_category_id) VALUES ('{}','{}','{}','{}','{}') \
                    ON DUPLICATE KEY UPDATE product_name = '{}'"\
                    .format(product_name, product_shop, product_nutri, \
                    product_url, list_id_cat, product_name)
                db.execute(insert_prod)
                self.db_connect.commit()
        
        db.execute("SELECT COUNT(*) FROM `mydb`.`Products`")
        sql_return = db.fetchone()
        print("\n***************************************************")
        print("* La base de données est chargée avec %s produits *" % (sql_return))
        print("***************************************************")

    def show_list_cat(self):
        
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        print("\n Liste des catégories:\n")
        db.execute("SELECT category_id, category_name FROM `mydb`.`Categories`")
        for ligne in db.fetchall():
            list_id_cat = ligne[0]
            list_name_cat = ligne[1]
            print(list_id_cat,'-', list_name_cat)

    def show_list_prod(self):
        
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        print("\n Liste des produits par catégories:\n")
        db.execute("SELECT product_name, Categories_category_id FROM `mydb`.`Products`")
        for ligne in db.fetchall():
            list_name_prod = ligne[0]
            list_id_cat = ligne[1]
            print(list_id_cat,"-",list_name_prod)

    def db_cleardata_cat(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Categories`")
        db.execute("ALTER TABLE `mydb`.`Categories` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n*********************************************************************")
        print("* !!!La table de données 'Categories' a été supprimée de la base!!! *")
        print("*********************************************************************")

    def db_cleardata_prod(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Products`")
        db.execute("ALTER TABLE `mydb`.`Products` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n*******************************************************************")
        print("* !!!La table de données 'Products' a été supprimée de la base!!! *")
        print("*******************************************************************")

    def db_cleardata_sub(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        db.execute("DELETE FROM `mydb`.`Substitute`")
        db.execute("ALTER TABLE `mydb`.`Substitute` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\n*********************************************************************")
        print("* !!!La table de données 'Substitute' a été supprimée de la base!!! *")
        print("*********************************************************************")
