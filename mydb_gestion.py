# ! /usr/bin/env python3
# coding: utf-8

'''
    mydb_gestion.py
    Author: Jimi Bourgeois
    Version: 2019-04-22
    Describe: Database connect
'''

# Specific import modules
import pymysql.cursors

# Standard import modules
import urllib.request as req
import json

class db_request():
    """Management class of the SQL database
        - Creation of the database
        - Creation of 'Categories', 'Products' and 'Substitute' tables
        - Download Openfoodfacts API REST Data
        in the 'Categories' and 'Products' tables
        - Data management of the database.
    """

    def create_db(self):
        """Creation of the database"""
        
        # Connection to the SQL database
        self.db_connect = pymysql.connect("localhost","root","")
        db = self.db_connect.cursor()
        
        # Request for create database
        database_sql = "CREATE DATABASE IF NOT EXISTS `mydb`"
        db.execute(database_sql)
        print("La base de donnée a bien été créée")
    
    def create_tables(self):
        """Creation of 'Categories', 'Products' and 'Substitute' tables"""
        
        # Connection to the SQL database
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        # Request SQL of the "Categories" table
        table_cat = "CREATE TABLE IF NOT EXISTS `mydb`.`Categories` \
            (`category_id` INT NOT NULL AUTO_INCREMENT,\
            `category_name` VARCHAR(150) NOT NULL,\
            `category_url` VARCHAR(200) NOT NULL, \
            PRIMARY KEY (`category_id`)) ENGINE = InnoDB"
        
        # Request SQL of the "Products" table
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

        # Request SQL of the "Products" table
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
        print("La structure de la base de données a bien été créée")
        print("Merci de patienter pendant le chargement des données de l'API en local")

    def create_db_cat(self):
        """Download 'Categories' of API REST Data"""

        # Connection to the SQL database
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        # Opening API .json Categories Data
        url="https://fr.openfoodfacts.org/categories.json"
        u = req.urlopen(url)
        content = u.read()
        jsonstr = content.decode("UTF-8")
        dfAll = json.loads(jsonstr)

        # Loop to import the desired quantity of categories
        for categories in dfAll['tags'][:28]:
            categories_name = categories['name']
            categories_name = categories_name.replace("'", " ")
            if len(categories_name) >= 28:
                continue
            dfAll = (categories_name, categories['url'])

            # Insert data into the table 'Categories'
            insert_cat = "INSERT IGNORE INTO `mydb`.`Categories` \
                (category_name, category_url) VALUES ('{}', '{}')"\
                .format(categories_name, categories['url'])
            db.execute(insert_cat)
            self.db_connect.commit()

        # Returns the number of categories in the table        
        db.execute("SELECT COUNT(*) FROM `mydb`.`Categories`")
        sql_return = db.fetchone()
        print("\nLa base de données est chargée avec %s catégories de produits" % (sql_return))

    def create_db_prod(self):
        """Download 'Products' of API REST Data"""

        # Connection to the SQL database
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        # Request to select IDs and their category URLs
        db.execute("SELECT category_id, category_url FROM `mydb`.`Categories`")
        
        # Loop to create the ID + URL.json list
        for ligne in db.fetchall():
            list_id_cat = ligne[0]
            list_url_cat = ligne[1]
            list_url_cat += '.json'
            
            # Opens API .json data for each category
            url_prod = req.urlopen(list_url_cat)
            data = url_prod.read()
            dfAll = json.loads(data.decode("utf_8"))

            #  Loop for formatting product data by categories   
            for products in dfAll['products']:
                product_name = products.get('product_name', "")
                product_name = product_name.replace("'"," ")
                if product_name is "":
                    break
                
                # Formatting nutriscrore data
                product_nutri = products.get('nutrition_grades_tags', "")
                product_nutri = str(product_nutri)
                product_nutri = product_nutri.replace("[", "")
                product_nutri = product_nutri.replace("'", "")
                product_nutri = product_nutri.replace("]", "")

                # Search for non-referenced stores
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
                
                # Insert data into the table 'Products'
                insert_prod = "INSERT IGNORE INTO `mydb`.`Products`\
                    (product_name, product_shop, product_nutri, product_url, \
                    Categories_category_id) VALUES ('{}','{}','{}','{}','{}') \
                    ON DUPLICATE KEY UPDATE product_name = '{}'"\
                    .format(product_name, product_shop, product_nutri, \
                    product_url, list_id_cat, product_name)
                db.execute(insert_prod)
                self.db_connect.commit()
        
        # Returns the number of products in the table
        db.execute("SELECT COUNT(*) FROM `mydb`.`Products`")
        sql_return = db.fetchone()
        print("\nLa base de données est chargée avec %s produits" % (sql_return))

    def db_cleardata_cat(self):
        """Delete data of the table 'Categories'"""

        # Connection to the SQL database
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        # SQL query to delete the data from the table
        db.execute("DELETE FROM `mydb`.`Categories`")
        # Reset auto incrementation
        db.execute("ALTER TABLE `mydb`.`Categories` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\nLa table de données 'Categories' a été supprimée de la base")

    def db_cleardata_prod(self):
        """Delete data of the table 'Products'"""

        # Connection to the SQL database
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        # SQL query to delete the data from the table
        db.execute("DELETE FROM `mydb`.`Products`")
        # Reset auto incrementation
        db.execute("ALTER TABLE `mydb`.`Products` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\nLa table de données 'Products' a été supprimée de la base")

    def db_cleardata_sub(self):
        """Delete data of the table 'Substitute'"""

        # Connection to the SQL database
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()
        
        # SQL query to delete the data from the table
        db.execute("DELETE FROM `mydb`.`Substitute`")
        # Reset auto incrementation
        db.execute("ALTER TABLE `mydb`.`Substitute` AUTO_INCREMENT = 1")
        self.db_connect.commit()
        print("\nLa table de données 'Substitute' a été supprimée de la base")