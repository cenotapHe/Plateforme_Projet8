# importation for counting the time
import time
# importation for using SQL with Python
import psycopg2
# importation for using API with Python
import requests

# Variable for time the script
start = time.time()

try:
    # creation of the connexion to the database
    conn = psycopg2.connect(database="plateforme_projet8_db", user="dev_projet8",
                            password="password_env_dev", host='', port="5432")
    cur = conn.cursor()

    # Variable of the both ID
    product_id = 1
    category_id = 1

    list_name_category = ['charcuteries', 'chocolats', 'pates-a-tartiner', 'biscuits', 'sauces', 'legumes-et-derives', 'produits-de-la-mer',
                          'boissons-aux-fruits', 'confitures-et-marmelades', 'yaourts', 'pains', 'fromages-de-france', 'boissons-gazeuses', 'volailles', 'glace']
    list_name_category_done = []
    list_name_product_done = []

    for name_category in list_name_category:

        for j in range(1, 35):

            if name_category not in list_name_category_done:
                cur.execute("INSERT INTO catalogue_category VALUES (" +
                            str(category_id) + ", '" + name_category.capitalize() + "')")
                conn.commit()
                list_name_category_done.append(name_category)

            r = requests.get(
                'https://fr.openfoodfacts.org/categorie/{}/{}.json'.format(name_category, str(j)))

            for i in range(20):

                try:

                    product_name = r.json()['products'][i]['product_name'][:99]
                    product_description = r.json(
                    )['products'][i]['ingredients_text_fr'][:999]
                    product_nutriscore_letter = r.json(
                    )['products'][i]['nutrition_grades']
                    product_category = category_id
                    product_picture = r.json()['products'][i]['image_url']
                    product_picture = product_picture[:len(
                        product_picture) - 7] + "full.jpg"
                    product_nutrition = r.json()[
                        'products'][i]['image_ingredients_url']
                    product_url = r.json()['products'][i]['url']

                    # Modification of wrong caracter for the SQL file
                    h = 0
                    while h < len(product_name):
                        if product_name[h] == "'" or product_name[h] == '"' or product_name[h] == ';':
                            product_name = product_name[:h] + \
                                " " + product_name[h + 1:]
                        h += 1
                    h = 0
                    while h < len(product_description):
                        if product_description[h] == "'" or product_description[h] == '"' or product_description[h] == ';':
                            product_description = product_description[:h] + \
                                " " + product_description[h + 1:]
                        h += 1

                    if product_nutriscore_letter == "a":
                        product_nutriscore = 1
                    elif product_nutriscore_letter == "b":
                        product_nutriscore = 2
                    elif product_nutriscore_letter == "c":
                        product_nutriscore = 3
                    elif product_nutriscore_letter == "d":
                        product_nutriscore = 4
                    else:
                        product_nutriscore = 5

                    if product_name not in list_name_product_done:
                            # execution of SQL
                        cur.execute("INSERT INTO catalogue_product VALUES (" +
                                    str(product_id) + ", '" + product_name + "', '" + product_description + "', " + str(product_nutriscore) + ", " + str(category_id) + ", '" + product_picture + "', '" + product_nutrition + "', '" + product_url + "')")
                        conn.commit()

                        product_id += 1

                        list_name_product_done.append(product_name)
    					

                except KeyError:
                    pass

                except IndexError:
                	pass

        category_id += 1

    # ending connexion to the database
    conn.close()

except :
    pass


print("Nombre de catégories différentes : " + str(category_id))
print("Nombre de référence recencée(s) : " + str(product_id))
print("Script effectué en : " + str(time.time() - start) + " secondes")
