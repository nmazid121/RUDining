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
	
testDate = currentMonth + "/" + currentDay + "/" + year

print(testDate)
print("Enter campus: ")
campusInput = input()
print("Enter meal time: ")
mealInput = input()
print("Campus name: " + campusInput)
print("Meal time: " + mealInput)
campusName = campusInput
mealName = mealInput

locationName = ''
if (campusName == 'Livingston') :
    locationName = "Livingston+Dining+Commons"
    locationNum = '03'
if (campusName == 'Busch') :
    locationNum = '04'
    locationName = "Busch+Dining+Hall" 
if (campusName == 'Cook Doug') :
      locationName = "Neilson+Dining+Hall"
      locationNum = '05'
if (campusName == 'College Ave') :
      locationName = "The+Atrium"
      locationNum = '13'
      if (mealName == 'Lunch') :
            mealName = "Lunch+Entree"
      if (mealName == 'Breakfast') :
            mealName = "Breakfast+Entree"
      if (mealName == 'Dinner') :
            mealName = "Dinner+Entree"

print(locationName)
print("The meal time is " + mealName)
# URL of the website to scrape

diningHallLink = "https://menuportal23.dining.rutgers.edu/FoodPro/pickmenu.asp?sName=Rutgers+University+Dining&dtdate=" + testDate + "/&locationNum=" + locationNum + "&locationName=" + locationName + "&mealName=" + mealName + "&naFlag="
atriumLink = "https://menuportal23.dining.rutgers.edu/FoodPro/pickmenu.asp?locationNum=" + locationNum + "&locationName=" + locationName + "&dtdate=" + currentMonth + "/" + currentDay + "/" + year + "/" + "&mealName=" + mealName +"&sName=Rutgers+University+Dining"
# GET request to the URL
if (campusName == 'Livingston' or campusName == 'Busch' or campusName == 'Cook Doug') :
      response = requests.get(diningHallLink)

if (campusName == 'College Ave'):
      response = requests.get(atriumLink)


# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find elements that contain food names
# Inspect the specific elements of the data that you want, so this one can be for the food names (This varies  depending on the website's structure)
food_items = soup.findAll('div', class_='col-1')

f = file_object = open("test.txt", "w", newline="")
# Print each food item
for item in food_items:
    f.write(item.get_text().strip())

# andre thomas test 
print("The current month is " + currentMonth)
print("The current day is " + currentDay)   

print("I love danny")