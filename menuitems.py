import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import datetime as theCENTER
import os
import sys
import argparse

doIExist = True
str1 = ""
# tries to open prefrences and set schoolName and menuSelection variables
try:
	with open("{}/preferences.json".format(os.path.dirname(os.path.realpath(__file__))), "r") as f:
		preferences = json.load(f)
		schoolName = preferences["schoolName"]
		try:
			menuSelection = preferences["menu"]
		except:
			pass
# if not it asks for the school name and verifies that it exists
except:
	doIExist = False
	schoolName = input(
		"What's your myschooldining code? Found after the url on their site. \nExample: For myschooldining.com/theneclientwschool, thenewschool would be your code\n")
	while True:
		soup = BeautifulSoup(requests.get("http://myschooldining.com/{}".format(schoolName)).text, "html.parser")
		try:
			if soup.h1.text == "Hmm...doesn't look like that's here...":
				schoolName = input("That's not a valid code. Please try again.\t")
		except:
			break

# puts the menu in soup thing
soup = BeautifulSoup(requests.get("http://myschooldining.com/{}".format(schoolName)).text, "html.parser")


def pickMenuSelector():
	global menuSelection
	# finds the button div
	menuCenter = soup.findAll("span", attrs={"class": "section-title"})
	menuCenter = menuCenter[1]
	# finds the buttons
	button = menuCenter.findAll("button", attrs={"class": "change-school"})
	# if 1 button, use that button
	if len(button) == 1:
		date = determineWhichMenuToGrab()
		litButton = button[0].get("id")
		formatAndPrintDatData(litButton, date)
	# if more button, ask user which button to use
	else:
		if doIExist == False:
			for i in range(0, len(button)):
				print("{}. {}".format(i + 1, button[i].text))
			menuSelection = int(input("Which menu do you want? Type in the number next to your chosen menu\t")) - 1
			print()
		litButton = button[menuSelection].get("id")
		return litButton


def determineWhichMenuToGrab(plusser):
	todayzers = datetime.today().hour
	datezers = datetime.today()
	datezers += theCENTER.timedelta(plusser)

	if datetime.today().weekday() == 6 or datetime.today().weekday() == 5:
		while datezers.weekday() != 0:
			datezers += theCENTER.timedelta(1)
	elif todayzers > 12 and datezers.weekday() != 4:
		datezers += theCENTER.timedelta(1)
	elif todayzers > 12 and datezers.weekday() == 4:
		while datezers.weekday() != 0:
			datezers += theCENTER.timedelta(1)
	elif todayzers <= 12:
		pass
	return datezers


def isInt(numero):
	try:
		int(numero)
		return True
	except:
		return False


def formatAndPrintDatData(litbutton, date, lastOne):
	global str1
	# what day is it?
	day = str(date.day)
	# sets up classes
	day = "day-" + day
	menuClass = "menu-" + litbutton
	# finds the menu location
	menu = soup.find("div", class_="{} {} menu-location".format(day, menuClass))
	# finds all menu items
	menu = menu.findAll("span", class_="no-print")
	# if its a category, get rid of it.
	menu = [i for i in menu if not i["class"] == ["month-category", "no-print"]]
	# no more whitespace and print everything
	print()
	# f = open("e.txt", "w")
	# f.close()
	# f = open("e.txt", "a")
	str1 += date.strftime('%A, %B %d, %Y') 
	str1 += "\n"
	# f.close()
	for i in range(0, len(menu)):
		menu[i] = menu[i].text
		menu[i] = menu[i].replace("\xa0", "")
		menu[i] = menu[i].replace("\n", "")
		menu[i] = menu[i].replace("							 ", "")
		# f = open("e.txt", "a")
		# print(menu[i])
		# f.write(menu[i] + "\n")

		str1 += menu[i] + "\n"

	print()
	# ask to save info if info doesn't exist
	if doIExist == False and lastOne == True:
		choice = "Netscape Navigator"
		while choice != "y" and choice != "n":
			choice = input("\nWould you like to save your info so you won't have to enter it next time? (y/n)").lower()
		if choice == "y":
			saveDatData()


# save data
def saveDatData():
	with open("{}/preferences.json".format(os.path.dirname(os.path.realpath(__file__))), "w") as fp:
		try:
			json.dump({"schoolName": schoolName, "menu": menuSelection}, fp)
		except:
			json.dump({"schoolName": schoolName}, fp)


def weekers():
	datezers = datetime.today()
	plusser = 0
	while datezers.weekday() != 0:
		if datezers.weekday() >= 5:
			datezers += theCENTER.timedelta(1)
		else:
			datezers -= theCENTER.timedelta(1)
	menu = datezers
	for i in range(0, 4):
		try:
			formatAndPrintDatData(menuChoice, menu + theCENTER.timedelta(i), False)
		except:
			print("Couldn't get data for {}".format(print((menu + theCENTER.timedelta(i)).strftime('%A, %B %d, %Y'))))
	try:
		formatAndPrintDatData(menuChoice, menu + theCENTER.timedelta(4), True)
	except:
		print("Couldn't get data for {}".format(print(((menu + theCENTER.timedelta(4)).strftime('%A, %B %d, %Y')))))


plusser = 0;

menuChoice = pickMenuSelector()

parser = argparse.ArgumentParser()
parser.add_argument("-t", action="store_true", default=False, help="See tomorrow's menu!")
parser.add_argument("-w", action="store_true", default=False, help="See the menu for the whole week")
parser.add_argument("-f", type=int, default=0,
					help="See the menu in the future! Following -f, type how many days in the future you need.")
args = parser.parse_args()

if args.t:
	plusser += 1
elif args.f > 0:
	plusser += args.f

if args.w:
	weekers()
else:
	menu = determineWhichMenuToGrab(plusser)
	try:
		formatAndPrintDatData(menuChoice, menu, True)
	except:
		print("Couldn't get data for {}".format(print(menu.strftime('%A, %B %d, %Y'))))


def return_s():
	global str1
	return str1
