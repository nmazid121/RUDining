import requests
import datetime
from bs4 import BeautifulSoup


currentDate =datetime.datetime.now()

day = currentDate.strftime("%d")

month = currentDate.strftime("%m")

year = currentDate.strftime("%Y")

currentDay = day
if (day[0] == '0') :
	currentDay = day.replace('0', '')

currentMonth = month
if (month[0] == '0') :
	currentMonth = month.replace('0', '')
# URL of the website to scrape

liviLink = "http://menuportal.dining.rutgers.edu/FoodPro/pickmenu.asp?sName=Rutgers+University+Dining&dtdate=" + currentMonth + "/" + currentDay + "/" + year + "/" + "&locationNum=03&locationName=Livingston+Dining+Commons&mealName=Dinner&naFlag="
# GET request to the URL
response = requests.get(liviLink)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements that contain food names
# Inspect the specific elements of the data that you want, so this one can be for the food names (This varies  depending on the website's structure)
food_items = soup.findAll('div', class_='col-1')


# Print each food item
for item in food_items:
    print(item.get_text().strip())

# andre thomas test 
print(currentMonth)
print(currentDay)
