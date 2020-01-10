import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import math

driver = webdriver.Chrome(executable_path='c:/chromedriver')

# dataframe
df = pd.read_excel('')

# login
u = ''
p = ''

driver.get('https://www.scopus.com')
driver.find_element_by_xpath('//*[@id="signin_link_move"]').click()
driver.find_element_by_xpath('//*[@id="bdd-email"]').send_keys(u)
driver.find_element_by_xpath('//*[@id="bdd-elsPrimaryBtn"]').click()
driver.find_element_by_xpath('//*[@id="bdd-password"]').send_keys(p)
driver.find_element_by_xpath('//*[@id="bdd-elsPrimaryBtn"]').click()

for index, row in df.iterrows():
    row = row.copy()

    try:
        scopus_ids = str(row['Scopus ID']).split('; ')
        links = ['http://www.scopus.com/authid/detail.url?authorId=%s' %
                 scopus_id for scopus_id in scopus_ids]

        NUM_PUBS = 0
        CITES = 0
        HINDEX = 0
        CITES_5 = 0
        HINDEX_SELF = 0

        for i in range(0, len(links)):
            link = links[i]
            scopus_id = scopus_ids[i]

            driver.get(link)
            sleep(5)

            # check id
            try:
                info = driver.find_element_by_class_name('authId')
                info = info.text.strip().split('\n')[0].split(': ')[1]
            except:
                pass

            # 01 get pubs (ok)
            try:
                num_pubs = int(driver.find_element_by_id(
                    'authorDetailsDocumentsByAuthor').find_element_by_class_name('panel-body').text.split('\n')[0])
            except:
                num_pubs = 0
                pass

            # 02 get citations (ok)
            try:
                cites = int(driver.find_element_by_id('totalCiteCount').text)
            except:
                cites = 0
                pass

            # 03 hindex (ok)
            try:

                hindex = driver.find_element_by_id('authorDetailsHindex')
                hindex = int(hindex.text.strip().split('\n')[2])

                if hindex > HINDEX:
                    HINDEX = hindex

            except:
                hindex = 0
                pass

            # 05 getting h-index w/o self citation
            try:
                hindex_self = driver.find_element_by_xpath(
                    '//*[@id="authorDetailsHindex"]/div[2]/button').click()
                hindex_self = driver.find_element_by_xpath(
                    '//*[@id="hindexCheckboxes"]/div[1]/label').click()
                hindex_self = driver.find_element_by_xpath(
                    '//*[@id="updateGraphButton_submit1"]').click()
                sleep(6)
                hindex_self = int(driver.find_element_by_xpath(
                    '//*[@id="analyzeSourceTitle"]/span[2]').text)

                if hindex_self > HINDEX_SELF:
                    HINDEX_SELF = hindex_self

            except:
                hindex_self = 0
                pass

            if scopus_id != info:
                print('[WARN] SCOPUS_ID_REDIRECT: %s' % scopus_id)

            else:
                NUM_PUBS += num_pubs
                CITES += cites

            df.loc[index, 'Num Pub'] = NUM_PUBS
            df.loc[index, 'Citations'] = CITES
            df.loc[index, 'h-index'] = HINDEX
            df.loc[index, '5-Years-Citations'] = CITES_5
            df.loc[index, 'h-index_self'] = HINDEX_SELF

    except:
        pass

driver.close()
driver.quit()

out_file = 'out.xlsx'
writer = pd.ExcelWriter(out_file)
df.to_excel(writer, sheet_name='out')
writer.save()
