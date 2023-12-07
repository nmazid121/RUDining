import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "http://menuportal.dining.rutgers.edu/FoodPro/pickmenu.asp?sName=Rutgers+University+Dining&dtdate=12/6/2023&locationNum=03&locationName=Livingston+Dining+Commons&mealName=Dinner&naFlag="

# GET request to the URL
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements that contain food names
# Inspect the specific elements of the data that you want, so this one can be for the food names (This varies  depending on the website's structure)
food_items = soup.findAll('div', class_='col-1')


# Print each food item
for item in food_items:
    print(item.get_text().strip())

    