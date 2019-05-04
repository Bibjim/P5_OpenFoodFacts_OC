# ! /usr/bin/env python3
# coding: utf-8


"""
!!!! OpenFoodFacts App !!!!
Author: Jimi Bourgeois
Version: 20190419
Project: Project 5 OpenClassrooms
Code language: Python3
Coding: Utf-8
"""

import urllib.request
import json
import time
import os
import sys

from mydb_gestion import *


main_app_loop = True

def clear_prompt():
    """ Clear the prompt """
    if sys.platform == "Linux":
        os.system("clear")


while main_app_loop is True:
    choice = 0
    clear_prompt()
    
    print("\nWelcome to the Database OpenFoodFacts.com (FR version)\n")
    print("What do you want to do ?\n")
    print("1 - Load the database locally* ?")
    print("2 - Search for a product in the categories ?")
    print("3 - Access saved products ?")
    print("4 - Clear backup products ?")
    print("\n *When using for the first time, load the database locally for the application to work")
    
    while choice == 0:
        choice = input("\nYour choise (Type Q to exit): ")

        if choice.upper() == "Q":
            main_app_loop = False
            break

        # Check if the input is a digit and between 0 and 5
        elif choice.isdigit() == False or int(choice) >= 5 or int(choice) == 0:
            print("\nYou must enter a number between 1 and 4\n")
            time.sleep(2)
            break

        # Run the input choice
        elif int(choice) == 1:
            dfcat = db_request()
            dfcat.create_db_cat()
        #elif int(choice) == 2:
        #    search_prod = db_request()
        #    search_prod.db_products()
        #elif int(choice) == 3:
        #    access_saved = db_request()
        #    access_saved.db_saved()
        #elif int(choice) == 4:
        #    clear_backup = db_request()
        #    clear_backup.db_cleardata()