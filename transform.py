from bs4 import BeautifulSoup
import urllib.request
import csv

response = urllib.request.urlopen('https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions')
html = response.read()
soup = BeautifulSoup(html, "html.parser")
#Code snippet to retrieve the required html file
 
table = soup.findAll("table",{"class":"wikitable sortable"})[1]
#Get the second table from all the tables in the html file

listOfHeadings = []
rows = table.findAll('tr')
for tr in rows:
    cols = tr.findAll('th')
    for th in cols:
        listOfHeadings.append(th.find(text=True).lower())
listOfHeadings = listOfHeadings[:6]
listOfHeadings[0] = "Game number"
listOfHeadings[1] ="year"
#Getting the required headings of the 2nd table
#The headings in the HTML file are Game and Date. These are to be changed to match the required output.

listOfRomanNumbers = []
listOfLists=[]
rows = table.findAll('tr')
for tr in rows:
    cols = tr.findAll('td')
    a_list = []
    for td in cols:
        a_list.append(td.find(text=True).strip(' !'))
    for a in tr.findAll('a'):
        if a.has_attr("title") and a['title'].startswith('Super Bowl '):
            listOfRomanNumbers.append(a.text)
       
    listOfLists.append(a_list)   
#Getting the required data out of 2nd table 

listOfLists.remove([])
listOfLists.pop()
listOfLists.pop()
#We require only 50 items from the table

indextToListOfRomanNumbers = 0
for simpleList in listOfLists:
    simpleList[0] = listOfRomanNumbers[indextToListOfRomanNumbers]
    simpleList[1] = simpleList[1][8:12]
    simpleList[3] = simpleList[3][:2] + '-' + simpleList[3][2:]
    
    del simpleList[6:]
    indextToListOfRomanNumbers = indextToListOfRomanNumbers + 1
#Change the retrieved data according to the requirements

listOfLists.insert(0, listOfHeadings)

   
with open('result.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(listOfLists)
#Code to write the result to a csv file
