import requests
from bs4 import BeautifulSoup
import re
import csv
toCSV = []

base="https://www.royalroads.ca"

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

for i in range(0,34):
    link = base+"/faculty-directory?field_program_area_target_id=All&field_faculty_type_target_id=All&sort_by=field_first_name_value&combine=&page="+str(i)
    f = requests.get(link)
    print("="*8+str(i))

    dep="rru"
    uni="Royal Roads University"




    all_rows=BeautifulSoup(f.text, "lxml").find_all(attrs={"class": "profile-listing-view__content"})
    all_people=[]
    for row in all_rows:
        #print(row)
        all_people_a=row.find_all('a')
        for a in all_people_a:
            all_people.append(a['href'])

    print(len(all_people))
    for plink in all_people:
        print(base+plink)
        read_single = requests.get(base + plink)

        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "page-title"})
            name = cleanhtml(str(sp[0]))
            #print(name)
            first_name=name.split(" ")[0]
            last_name=name.split(" ")[1]
        except Exception as e:
            first_name=last_name=name=""
            #print(str(e))

        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field_testimonial_program"})
            dep = cleanhtml(str(sp[0]))
            #print(dep)

        except Exception as e:
            first_name=last_name=name=""
            #print(str(e))

        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "su-person-email"})
            email = cleanhtml(str(sp[0].find('a')))
            #print(email)
        except Exception as e:
            email=""
            #print(str(e))

        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field_linkedin_link"})
            #print(sp[0].find('a').split('"')[1])
            linkedin = str(sp[0]).split('"')[3]
            #print(linkedin)
        except Exception as e:
            linkedin=""
            #print(str(e))

        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "position-title-wrapper"})
            position=cleanhtml(str(sp[0]))
            #print(position)
        except Exception as e:
            position=""
            #print(str(e))

        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field-block node-stanford-person-su-person-mobile-phone block-layout-builder"})
            phone=cleanhtml(str(sp[0]))
            #print(phone)
        except Exception as e:
            phone=""
            #print(str(e))

        try:
            sp=BeautifulSoup(read_single.text, "lxml").find_all(attrs={"class": "field_education_wrapper"})
            edu=cleanhtml(str(sp[0]))
            #print(edu)
        except Exception as e:
            edu=""
            #print(str(e))

        toCSV.append({ "FullName":name.strip() ,"FirstName":first_name.strip() ,"MiddleName":"" ,"LastName":last_name.strip()
                         ,"Position":position.strip() ,"Phone":phone.strip() , "Email":email.strip()
                         , "Email":email.strip() ,
                       "Linkedin":linkedin.strip(),"Department":dep,"University":uni,"Education":edu.strip(), "Link":base+plink})
keys = toCSV[0].keys()
with open('rru.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(toCSV)