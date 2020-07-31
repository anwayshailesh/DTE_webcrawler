# importing required modules
import csv
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import matplotlib.pyplot as plt


Result = []       # this list will store final scaraped data

List = ['Amravati', 'Aurangabad', 'Mumbai', 'Nagpur', 'Nashik', 'Pune']
y = [1, 2, 3, 4, 5, 6]

for i in range(0, len(List)):
    url = 'http://dtemaharashtra.gov.in/frmInstituteList.aspx?RegionID={}&RegionName={}'.format(y[i],List[i]) # this is the link given to the url variable and it run multiple times with a specific pattern

    Request = requests.get(url)
    Content = Request.content
    bs = BeautifulSoup(Content, 'html.parser')
    anc = bs.find(class_='DataGrid')
    anc1 = anc.find_all('a')

    n = 10                                    # assign the value to n twice the number user want to scrape because of the website structure.
    for link in anc1[1:n:2]:
        linktext = 'http://dtemaharashtra.gov.in/' + str(link.get('href'))
        r = requests.get(linktext)
        soup = BeautifulSoup(r.content, 'html.parser')
        bo = soup.find(class_='InnerBodyDiv')
        bs1 = bo.find_all('b')

        #this condition will filter out the engneering colleges
        if re.search(' Engineering', bs1[4].get_text())or re.search('Technical', bs1[4].get_text()) or re.search('Technology', bs1[4].get_text()) or re.search('Technological', bs1[4].get_text()) or re.search('Information', bs1[4].get_text()):

            Institute_id = [id for id in bs1[0]]                         # this will store institute id
            Institue_name = [college for college in bs1[4]]              # this will store institute name
            District = [district for district in bs1[5]]                 # this will store district
            Address = [address for address in bs1[7]]                    # this will store address
            if bool(Address)==True:
                pass
            elif bool(Address)==False:
                Address.append('none')
            web_address = [site for site in bs1[13]]                     # this will store website
            if bool(web_address)==True:
                pass
            elif bool(web_address)==False:
                web_address.append('none')
            email_address = [email for email in bs1[14]]                 # this will store email id
            if bool(email_address)==True:
                pass
            elif bool(email_address) == False:
                email_address.append('none')
            official_name = [official for official in bs1[25]]           # this will store institute's authority's name
            if bool(official_name) == True:
                pass
            elif bool(official_name) == False:
                official_name.append('none')
            bs2 = bo.find(id='ctl00_ContentPlaceHolder1_lblPrincipalNameEnglish')
            Principal_name = [principalname for principalname in bs2]       # this will store principal's name
            if bool(Principal_name) == True:
                pass
            elif bool(Principal_name) == False:
                Principal_name.append('none')
            bo1 = bo.find(id='ctl00_ContentPlaceHolder1_lblPersonalPhoneNo')
            if bo1.get_text().split()[0].isdigit:
                Personal_phone_no = bo1.get_text().split()[0]            # this will store principal's phone no
            else:
                Personal_phone_no='none'
            bo2 = bo.find(id='ctl00_ContentPlaceHolder1_lblOfficePhoneNo')
            if bo2.get_text().split()[0].isdigit:
                Office_phone_no = bo2.get_text().split()[0]              # this will store official phone no
            else:
                Office_phone_no = 'none'

            for index in range(0,len(Institute_id)):
                Result.append({
                    'id': Institute_id[index],
                    'Institue_name': Institue_name[index],
                    'District': District[index],
                    'Address': Address[index],
                    'web_address': web_address[index],
                    'email_address': email_address[index],
                    'Principal_name': Principal_name[index],
                    'Personal_Contact_no': Personal_phone_no,
                    'offical_name': official_name[index],
                    'Office_phone_no': Office_phone_no,
                })

# Wait for sometimes to get scraped

collegedata = pd.DataFrame(Result)                                          # this will frame the data and stores in csv file
collegedata.to_csv("collegedata.csv")

print('you have done a scarping')

Amravati = 0                                                            # these are the districts varibles which will be used for visulization
Aurangabad = 0
Mumbai = 0
Nagpur = 0
Nashik = 0
Pune = 0

with open('collegedata.csv') as csv_file:                                   # this will read the saved csv file
    csv_reader = csv.DictReader(csv_file)
    for i in csv_reader:
        if i['District'] == 'Amravati':
            Amravati += 1
        elif i['District'] == 'Aurangabad':
            Aurangabad += 1
        elif i['District'] == 'Mumbai':
            Mumbai += 1
        elif i['District'] == 'Nagpur':
            Nagpur += 1
        elif i['District'] == 'Nashik':
            Nashik += 1
        elif i['District'] == 'Pune':
            Pune += 1


num = [Amravati, Aurangabad, Mumbai, Nagpur, Nashik, Nashik]                       #this part will visulize the data in bar graph and pie chart
DISTRICT = ['Amravati', 'Aurangabad', 'Mumbai', 'Nagpur', 'Nashik', 'Pune']

plt.set_ylabel = num
plt.xlabel = DISTRICT
fig1, ax1 = plt.subplots()
ax1.set_title('Number of engneering colleges per district in the scraped data')
ax1.set_xlabel('districts')
ax1.set_ylabel('numbers of engneering colleges')
ax1.bar(DISTRICT, num, width=0.25)

fig2, ax2 = plt.subplots()

ax2.pie(num, labels=DISTRICT, shadow=True, startangle=90, wedgeprops={'edgecolor': 'black'}, autopct='%1.1f%%')
ax2.set_title('Percentage of engneering colleges in different district in the scraped data')

plt.show()

#End of code


