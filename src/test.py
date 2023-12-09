print("Enter campus: ")
campusInput = input()
print("Campus name, " + campusInput)
campusName = campusInput

campusLinkName = ''
if (campusName == 'Livingston') :
    campusLinkName = "Livingston+Dining+Commons"
if (campusName == 'Busch') :
    campusLinkName = "Busch+Dining+Hall" 

print(campusLinkName)