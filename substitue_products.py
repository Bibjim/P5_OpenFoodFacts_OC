# ! /usr/bin/env python3
# coding: utf-8

'''
    substitute_products.py
    Author: Jimi Bourgeois
    Version: 2019-07-22
'''

# Specific import modules
import pymysql.cursors

# Standard import modules
import time

class db_menu():
    """This class is used to search for substitute products in the database
    and save them to the database via SQL queries.
    It is also used to display the products saved in the database.
    """

    def search_prod(self):
        """Product search and backup function in the database"""

        # Connection to the SQL database
        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()
        
        # Category selection display loop
        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous afficher la liste de catégories ? O/n ")
            if choice.upper() == "N":
                print("\nRetour au menu principal")
                break
            elif choice.upper() == "O":
                choice_cat = True
                print("\n Liste des catégories:\n")
                # Defining the query to return the list of categories
                show_list_cat = "SELECT category_id, category_name \
                    FROM `mydb`.`Categories`"
                # Command to execute the request
                db.execute(show_list_cat)
                # Variable assignment loop
                for ligne in db.fetchall():
                    list_id_cat = ligne[0]
                    list_name_cat = ligne[1]
                    # View category list
                    print(list_id_cat,'-', list_name_cat)

                # Product Selection Loop
                choice_cat = 0
                while choice_cat == 0:
                    choice_cat = input("\nSélectionner une catégorie de produit (Q pour annuler): ")

                    if choice_cat.upper() == "Q":
                        choice = False
                        break

                    elif choice_cat.isdigit() == False or int(choice_cat) >= 29 \
                        or int(choice_cat) == 0:
                        print("\nMerci de bien vouloir entrer un chiffre compris entre 1 et 28\n")
                        time.sleep(2)
                        choice_cat = 0
                    
                    # Definition of the request to return 
                    # the list of products of the selected category
                    show_list_prod_select = f"SELECT product_id, \
                        product_name, \
                        product_nutri \
                        FROM `mydb`.`Products` \
                        WHERE Categories_category_id = {choice_cat}"
                    
                    # Execution command of the SQL query
                    db.execute(show_list_prod_select)
                    for ligne in db.fetchall():
                        list_id_prod = ligne[0]
                        list_name_prod = ligne[1]
                        nutriscore_prod = ligne[2]
                        # Uppercase display
                        nutriscore_prod = nutriscore_prod.upper()
                        # Display of the list of products and nutriscores
                        print(list_id_prod,"-", list_name_prod, \
                            "- Nutriscore:",nutriscore_prod)
                    
                    # SQL query to determine the maximum and minimum value
                    # the product ID for the selected category
                    vmax = f"SELECT MAX(product_id) \
                        FROM `mydb`.`Products` \
                        WHERE Categories_category_id = {choice_cat}"
                    db.execute(vmax)
                    for maxv in db.fetchall():
                        max_id_prod = maxv[0]

                    vmin = f"SELECT MIN(product_id) \
                        FROM `mydb`.`Products` \
                        WHERE Categories_category_id = {choice_cat}"
                    db.execute(vmin)
                    for minv in db.fetchall():
                        min_id_prod = minv[0]
                    
                    # Display loop for selecting the product to substitute
                    choice_sub = 0
                    while choice_sub == 0:
                        choice_sub = input("\nSélectionner un produit à substituer (Q pour annuler): ")

                        if choice_sub.upper() == "Q":
                            choice = 0
                            break
                        # Selects the product selection choice for the selected category
                        elif choice_sub.isdigit() == False or \
                            int(choice_sub) > max_id_prod or \
                            int(choice_sub) < min_id_prod or int(choice_sub) == 0:
                            print("\nMerci de bien vouloir entrer un chiffre compris dans la liste des produits")
                            time.sleep(2)
                            choice_sub = 0

                        # Definition of the request to return the list of
                        # Substitute products of the selected category
                        show_list_sub_select = f"SELECT * FROM `mydb`.`Products`\
                            WHERE product_id = {choice_sub}"
                        
                        # Execution command of the SQL query
                        db.execute(show_list_sub_select)
                        for ligne_sub in db.fetchall():
                            sub_name = ligne_sub[1]
                            sub_nutri = ligne_sub[3]
                            # Uppercase display
                            sub_nutri = sub_nutri.upper()
                            
                            # Definition of the request to return the product 
                            # with the highest nutriscores of the selected category
                            list_best_nutri = f"SELECT * FROM `mydb`.`Products`\
                                WHERE Categories_category_id = {choice_cat} \
                                AND product_nutri <= '{sub_nutri}' \
                                ORDER BY product_nutri ASC"
                            
                            db.execute(list_best_nutri)
                            result = db.fetchall()
                            best = (result)[0]
                            bestnutri = (best)[3]
                            # Uppercase display
                            bestnutri = bestnutri.upper()
                            # Case where the user chooses one of the products 
                            # with the highest nutriscore of the category
                            if sub_nutri == bestnutri:
                                print("\nLe produit sélectionné a le meilleur nutriscore de cette catégorie")
                                print("Veuillez sélectionner un autre produit dans la liste")
                                choice_sub = 0
                            # Case where the user selects a substitutable product  
                            else:
                                best_id = (best)[0]
                                best_name = (best)[1]
                                best_nutriscore = (best)[3]
                                best_nutriscore = best_nutriscore.upper()
                                best_shop = (best)[2]
                                best_url = (best)[4]
                                # Returns the selected product and its substitute
                                print("\nProduit sélectionné:",sub_name,\
                                    ". Nutriscore:",sub_nutri)
                                print("Substitue:",best_name,". Nutriscore:",\
                                    best_nutriscore)
                                print("Magasin(s):",best_shop)
                                print("Infos produit:",best_url)
                                # Backup loop in the SQL database
                                save_choice1 = 0
                                while save_choice1 is 0:
                                    save_choice1 = input("\nSouhaitez-vous sauvegarder le produit dans la base ? O/n ")
                                    if save_choice1.upper() == "N":
                                        print("\nRetour au menu principal")
                                        time.sleep(2)
                                        break
                                    elif save_choice1.upper() == "O":
                                        # Insertion request in the "Substitute" table
                                        save_sub = "INSERT IGNORE INTO \
                                            `mydb`.`Substitute` \
                                            (save_product_id, save_product_sub_name) \
                                            VALUES ('{}','{}')".format(best_id, sub_name)
                                        db.execute(save_sub)
                                        self.db_connect.commit()
                                        print("\nLe produit a bien été sauvegardé dans vos favoris")
                                        print("Retour au menu principal")
                                        time.sleep(2)
                                        break
                                


    def search_substitute(self):

        self.db_connect = pymysql.connect("localhost","root","","mydb")
        db = self.db_connect.cursor()

        # Buckle of choice of display of substitute products
        choice = 0
        while choice is 0:
            choice = input("\nVoulez vous afficher vos produits favoris ? O/n ")
            if choice.upper() == "N":
                print("\nRetour au menu principal")
                time.sleep(2)
                break
            elif choice.upper() == "O":
                # Request to display the list of substitute products
                save_show = "SELECT * FROM PRODUCTS INNER JOIN SUBSTITUTE ON \
                    PRODUCTS.product_id = SUBSTITUTE.save_product_id \
                    INNER JOIN CATEGORIES ON PRODUCTS.Categories_category_id = \
                    CATEGORIES.category_id WHERE SUBSTITUTE.save_product_id"
                db.execute(save_show)
                for results in db.fetchall():
                    name_sub = results[8]
                    name_save = results[1]
                    nutri_save = results[3]
                    nutri_save = nutri_save.upper()
                    shop_save = results[2]
                    url_save = results[4]
                    cat_save = results[10]
                    # Return the list of substitute products
                    print("\nProduit substitué:",name_sub)
                    print("Substitue:",name_save,". Nutriscore:",nutri_save)
                    print("Catégorie:",cat_save)
                    print("Magasin(s):",shop_save)
                    print("Infos produit:",url_save)
                print("\nRetour au menu principal")
                time.sleep(2)
                break
