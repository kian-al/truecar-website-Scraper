import mysql.connector
import requests
from bs4 import BeautifulSoup
import re
from colorama import Fore
print(Fore.GREEN+'''Please write the specifications of the machine you want to get the information on, like these examples,
without putting white space at the beginning and end of the sentence. 
for example = |Toyota Camry LE FWD Automatic|BMW X3 xDrive30i|AWD Honda Accord Hybrid Touring CVT'''+Fore.WHITE)
query = input("Enter the car: ")
query = query.lower().strip().split()
url = f"https://www.truecar.com/used-cars-for-sale/listings/{query[0]}/{query[1]}/{query[2]}"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
car_info = soup.find_all("li", class_=["mt-2 flex grow col-md-6 col-xl-4", "mt-3 flex grow col-md-6 col-xl-4"]) 
pattern = r'>[^<]+<'
pattern_price = r'\$\d{1,3}(?:,\d{3})*(?:\.\d+)?'  
pattern_miles = r'\d+k mi'  

div_list = []

for tag in car_info:
    for detail in tag:
        div_list.append(re.findall(pattern, str(detail)))
cnx=mysql.connector.connect(user='kian', password='Kian.py192',host='127.0.0.1', database='car_website')#If you want to use this code, enter your database information in this line
cursor=cnx.cursor()
car_name = query[0]+' '+query[1]
query_insert = "INSERT INTO truecar (car_name, price, miles) VALUES (%s, %s, %s);"

for item in div_list:
    price = None
    miles = None
    for index in item:
        if re.search(pattern_price, index):
            price_match = re.search(pattern_price, index)
            if price_match:
                price = float(re.sub(r'[^\d.]', '', price_match.group()))
        if re.search(pattern_miles, index):
            miles = re.search(pattern_miles, index).group()
    cursor.execute(query_insert, (car_name, price, miles)) 

cnx.commit()

query_result="SELECT * FROM truecar;"
cursor.execute(query_result)
result=cursor.fetchall()
for item in result:
    print(item[0],item[1],item[2])
cursor.close()
cnx.close()




