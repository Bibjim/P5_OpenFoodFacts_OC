# ! /usr/bin/env python3
# coding: utf-8

'''
    mydb_gestion.py
    Author: Jimi Bourgeois
    Version: 2019-04-19
    Describe: Database connect
'''

import urllib.request as req
import json
import pymysql.cursors

class db_request():

    def create_db_cat(self):

        self.db_connect = pymysql.connect("localhost","user_db","pw_db","mydb")
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
        data = (categories_name, categories['url'])

        db.execute("INSERT IGNORE INTO `mydb`.`Categories` (category_name, category_url) VALUES ('{}', '{}')".format(
            categories_name, categories['url']))
        self.db_connect.commit()

                
        db.execute("SELECT COUNT(*) FROM `mydb`.`Categories`")
        sql_return = db.fetchone()
        print("Database loaded with %s product categories" % (sql_return))