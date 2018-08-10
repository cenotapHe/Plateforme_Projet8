# coding: utf-8

# Importation of the different module
import os
import json
import time

# Variable for time the script
debut = time.time()

# Variable for the main boucle
i = 1
i_max = 500 # Modification of this variable for create a biggest sql file
# (i_max = 100) => ~1500products
# (i_max = 200) => ~3000products
# etc, etc,...

# Variable for the category
count = 0
list_category = []
list_product = []
i_category = 0
name_category = ['fruits-based-foods', 'legumes-and-their-products', 'juices-and-nectars', 'biscuits', 'ice-creams-and-sorbets', 'chocolates', 'breakfast-cereals', 'meats', 'yogurts', 'french-cheeses', 'sauces', 'seafood', 'jams', 'breads', 'chips-and-fries']

# Main Boucle
while i <= i_max:

    # API request
    os.system("curl -X GET https://fr-en.openfoodfacts.org/category/{}/{}.json --output fichier2.json".format(
        name_category[i_category], str(i)))

    # Open the file from API
    try:
        json_data = open('fichier2.json')
        data = json.load(json_data)

    except UnicodeDecodeError:
        try:
            json_data.close()
            os.remove('fichier2.json')
        except FileNotFoundError:
            pass

    except FileNotFoundError:
        try:
            json_data.close()
            os.remove('fichier2.json')
        except FileNotFoundError:
            pass

    # Insert the file from API in variable
    try:
        exterieur = data['products']

        # Boucle for each page of the product in the JSON file
        k = 0
        try:
            while k <= 19:

                bibliotheque = exterieur[k]

                # For each product, enter all this caract in differents variables
                product_name = bibliotheque['product_name_fr'][:99]
                product_generic_name = name_category[i_category]
                product_nutriscore = bibliotheque['nutrition_grade_fr']
                product_stores = bibliotheque['stores']
                product_description = bibliotheque['ingredients_text_fr'][:999]
                product_image = bibliotheque['image_url']
                product_image = product_image[:len(product_image) - 7] + "full.jpg"
                product_nutrition = bibliotheque['image_nutrition_url']
                product_link = bibliotheque['url']

                # Catch the fake data of Open Food Facts
                if product_stores != '' and product_name != '':

                    # Modification of wrong caracter for the SQL file
                    h = 0
                    while h < len(product_name):
                        if product_name[h] == "'" or product_name[h] == '"' or product_name[h] == ';':
                            product_name = product_name[:h] + \
                                "," + product_name[h + 1:]
                        h += 1
                    h = 0
                    while h < len(product_stores):
                        if product_stores[h] == "'" or product_stores[h] == '"' or product_stores[h] == ';':
                            product_stores = product_stores[:h] + \
                                "," + product_stores[h + 1:]
                        h += 1
                    h = 0
                    while h < len(product_description):
                        if product_description[h] == "'" or product_description[h] == '"' or product_description[h] == ';':
                            product_description = product_description[:h] + \
                                "," + product_description[h + 1:]
                        h += 1


                    # Make or Open the SQL file
                    fichier2 = open("Set_of_Data.sql", "a")

                    number = str(i_category + 1)

                    # Creation of new category in the SQL file
                    if product_generic_name not in list_category:
                        fichier2.write("INSERT INTO catalogue_category\nVALUES (" + number + ", '" +
                                       product_generic_name + "');\n\n")

                        list_category.append(product_generic_name)

                    j = 0
                    while j < len(list_category):
                        if product_generic_name == list_category[j]:
                            product_number_category = j + 1
                        j += 1

                    # Insertion of nutriscore with Int()
                    product_nutriscore_number = ''

                    if product_nutriscore == 'a':
                        product_nutriscore_number = '1'
                    elif product_nutriscore == 'b':
                        product_nutriscore_number = '2'
                    elif product_nutriscore == 'c':
                        product_nutriscore_number = '3'
                    elif product_nutriscore == 'd':
                        product_nutriscore_number = '4'
                    else:
                        product_nutriscore_number = '5'


                    if product_name not in list_product:
                        # Creation of new product in the SQL file
                        fichier2.write("INSERT INTO catalogue_product\nVALUES ('" + str(count) + "', '" +
                                       product_name + "', '" +
                                       product_description + "', '" +
                                       product_nutriscore_number + "', '" +
                                       str(product_number_category) + "', '" +
                                       product_image + "', '" +
                                       product_nutrition + "', '" +
                                       product_link + "');\n\n")

                        # Census of all item listed in the SQL file
                        count += 1

                        list_product.append(product_name)

                k += 1

        except IndexError:
            pass

        try:
            fichier2.close()
        except NameError:
            pass

    except KeyError:
        pass
    except NameError:
        pass

    json_data.close()

    try:
        os.remove('fichier2.json')
    except FileNotFoundError:
        pass

    # Modification of the boucle for each category
    if i == i_max:
        i_category += 1
        i = 0

    # Break the boucle after each category
    if i_category >= len(name_category):
        break

    i += 1

# Information at the end of the script
print("Nombre de référence recencée(s) : " + str(count))
print(time.time() - debut)