import requests
from bs4 import BeautifulSoup
import re
import csv
toCSV = []

base="https://aa.stanford.edu"
link = base+"/people/faculty"
f = requests.get(link)
print(link)

dep="Aeronautics & Astronautics"
uni="Stanford"


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

all_rows=BeautifulSoup(f.text, "lxml").find_all(attrs={"class": "views-row"})

all_people=[]
for row in all_rows:
    all_people_a=row.find_all('a')
    for a in all_people_a:
        all_people.append(a['href'])


all_people=all_people[1:]
for plink in all_people:
    print(base+plink)
    read_single = requests.get(base + plink)

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "su-person-name"})
        name = cleanhtml(str(sp[0].find('h1')))
        print(name)
        if len(name.split(" "))==2:
            first_name=name.split(" ")[0]
            last_name=name.split(" ")[1]
            middle_name = ""
        if len(name.split(" "))==3:
            first_name=name.split(" ")[0]
            middle_name=name.split(" ")[1]
            last_name = name.split(" ")[2]
    except Exception as e:
        first_name=last_name=name=""
        print(str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "su-person-email"})
        email = cleanhtml(str(sp[0].find('a')))
        print(email)
    except Exception as e:
        email=""
        print(str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "su-person-links"})
        #print(sp[0].find('a').split('"')[1])
        site = cleanhtml(str(sp[0].find('a')).split('"')[1])
        print(site)
    except Exception as e:
        site=""
        print(str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "node-stanford-person-su-person-full-title"})
        position=cleanhtml(str(sp[0]))
        position=position.split("of")[0]
        of_str=position.split("of")[1]
        print(position.split("of"))
    except Exception as e:
        position=""
        of_str=""
        print(str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field-block node-stanford-person-su-person-mobile-phone block-layout-builder"})
        phone=cleanhtml(str(sp[0]))
        print(phone)
    except Exception as e:
        phone=""
        print(str(e))

    try:
        sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "su-person-education"})
        edu=cleanhtml(str(sp[0]))
        print(edu)
    except Exception as e:
        edu=""
        print(str(e))

    toCSV.append({ "FullName":name.strip() ,"FirstName":first_name.strip() ,"MiddleName":middle_name ,"LastName":last_name.strip()
                     ,"Position":position.strip(),"Of":of_str ,"Phone":phone.strip() , "Email":email.strip()
                     , "Email":email.strip() ,
                   "Site":site.strip(),"Department":dep,"University":uni,"Education":edu.strip(),"profile_src":base+plink })
keys = toCSV[0].keys()
with open(dep+'.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(toCSV)