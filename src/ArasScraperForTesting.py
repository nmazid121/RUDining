import pymongo
from pymongo import MongoClient 
import requests
from bs4 import BeautifulSoup

def scrape_aras_hot_chicken():
    url = "https://arashotchicken.com/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all elements that contain menu items
            menu_items = soup.find_all('h4')  # This targets the menu item names

            # Iterate through each menu item and find its price
            for item in menu_items:
                # Find the price which is presumably within a div tag with class 'AixKWd' near the menu item
                price = item.find_next('div', class_='AixKWd')  # Adjust the selector based on the actual structure

                if price:
                    print(f"Food item: {item.get_text().strip()}: {price.get_text().strip()}")
                else:
                    print(f"{item.get_text().strip()}: Price not found")

        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


scrape_aras_hot_chicken()
arasClient = pymongo.MongoClient("mongodb+srv://chaz:chaz@rudining.h9cvsrb.mongodb.net/?retryWrites=true&w=majority")
# mydb = arasClient["myDatabase"]
print(arasClient.list_database_names())
mydb = arasClient["TestDatabase"]
mycol = mydb["TestCollection"]
mydict = [
    { "foodName": "BABY SPINACHBROCCOLI", "price" : "$1" },
          {"foodName": "Cheese", "price" : "$100"}
]


mycol.insert_many(mydict)

