from IPython.display import display, HTML
from selenium import webdriver
from pandas import DataFrame
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
from pandas import concat


# noinspection PyTypeChecker
def scanForFacultyInfo(driver: webdriver.Chrome) -> DataFrame:
    frame = DataFrame(columns=['Name', 'Title', 'Email'])
    if 'ucsc.edu' in driver.current_url:
        people = driver.find_element(By.TAG_NAME, 'table').find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME,'tr')
        for person in people:
            info = person.find_elements(By.TAG_NAME, 'td')
            name = info[0].find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'strong').text
            email = info[2].find_element(By.TAG_NAME, 'nobr').find_element(By.TAG_NAME, 'a').get_attribute('title')
            title = info[4].text
            frame.loc[-1] = [name, title, email]
            frame.index = frame.index + 1
            frame = frame.sort_index()
    elif 'ucla.edu' in driver.current_url:
        time.sleep(2)  # allows page to completely load (has a loading animation before providing info)
        people = driver.find_elements(By.XPATH, '//div[@class = "card_description"]')
        print(len(people))
        for person in people:
            name = person.find_element(By.TAG_NAME, 'h4').find_element(By.TAG_NAME, 'a').text
            title = person.find_element(By.TAG_NAME, 'p').find_element(By.TAG_NAME, 'i').text
            email = person.find_element(By.TAG_NAME, 'p').find_element(By.TAG_NAME, 'a').text
            frame.loc[-1] = [name, title, email]
            frame.index = frame.index + 1
            frame = frame.sort_index()
    elif 'ucmerced.edu' in driver.current_url:
        people = driver.find_elements(By.TAG_NAME, 'section')
        for person in people:
            name = person.find_element(By.CLASS_NAME, 'ResultBlock-info-name').text
            if ' / ' in name:
                name = name.split(' / ')[0]
            firstLastNames = name.split(', ')
            name = firstLastNames[1] + ' ' + firstLastNames[0]
            title = person.find_element(By.CLASS_NAME, 'ResultBlock-info-descriptor').find_element(By.CLASS_NAME, 'deptTitle').find_elements(By.TAG_NAME, 'span')[0].text.replace(',', '')

            # Expanding section using Selenium's click()

            expandButton = person.find_element(By.CLASS_NAME, 'ResultBlock-controls').find_element(By.TAG_NAME, 'img')
            expandButton.click()
            time.sleep(1)  # wait for section to completely expand

            email = person.find_element(By.CLASS_NAME, 'ResultBlock-contactTable').find_elements(By.CLASS_NAME, 'TableRow')[0].find_element(By.TAG_NAME, 'a').text

            frame.loc[-1] = [name, title, email]
            frame.index = frame.index + 1
            frame = frame.sort_index()
    elif 'ucdavis.edu' in driver.current_url:
        people = driver.find_elements(By.XPATH, '//article[@class = "node node--type-sf-person vm-teaser--grouped vm-teaser"]')
        for person in people:
            name = person.find_element(By.CLASS_NAME, 'vm-teaser__title').text
            try:
                email = re.findall('(\S+@\S+)', person.text)[0]
            except IndexError:
                print(name + '\'s email not listed on website')
                continue
            title = person.find_element(By.CLASS_NAME, 'vm-teaser__position').find_elements(By.TAG_NAME, 'li')[0].text
            if '|' in title:
                title = title[:title.index('|')]

            frame.loc[-1] = [name, title, email]
            frame.index = frame.index + 1
            frame = frame.sort_index()
    elif 'ucsb.edu' in driver.current_url:
        people = driver.find_elements(By.XPATH, '//span[@class = "field-content"]//div//div[2]')
        for person in people:
            try:
                name = person.find_element(By.TAG_NAME, 'h2').text
            except NoSuchElementException:
                break
            moreInfo = person.find_elements(By.TAG_NAME, 'p')
            title = moreInfo[1].text
            email = moreInfo[4].text

            frame.loc[-1] = [name, title, email]
            frame.index = frame.index + 1
            frame = frame.sort_index()
    elif 'uci.edu' in driver.current_url:
        people = driver.find_elements(By.XPATH, '//div[@class="field field-type-text-long field_body"]')
        for person in people:
            name = person.find_element(By.TAG_NAME, 'h4').text.split(',')[0]
            description = person.find_element(By.TAG_NAME, 'p').text
            title = description[:description.index('Research Interests:')]
            email = description[description.index('Email: ') + 6:description.index('@uci.edu') + 7]

            frame.loc[-1] = [name, title, email]
            frame.index = frame.index + 1
            frame = frame.sort_index()

    elif 'berkeley.edu' in driver.current_url:
        people = driver.find_elements(By.XPATH, '//div[@class="cc-image-list__item__content"]')
        for person in people:
            name = person.find_element(By.TAG_NAME, 'h3').text
            try:
                email = re.findall('(\S+@\S+)', person.find_element(By.TAG_NAME, 'p').text)[0]
            except IndexError:
                print(name + '\'s email not listed on website')
                continue
            title = person.find_element(By.TAG_NAME, 'p').find_elements(By.TAG_NAME, 'strong')[0].text

            frame.loc[-1] = [name, title, email]
            frame.index = frame.index + 1
            frame = frame.sort_index()

    display(frame)
    return frame


def getContacts():
    contactList = list()
    cService = webdriver.ChromeService(executable_path='./chromedriver-win64/chromedriver.exe')
    driver = webdriver.Chrome(service=cService)

    with open('contact_pages.txt') as websites:
        for url in websites:
            print(url)
            driver.get(url)
            extractedContacts = scanForFacultyInfo(driver)
            contactList.append(extractedContacts)

    driver.quit()
    contacts = concat(contactList, ignore_index= False)
    with open('contact_logs.txt', 'w', encoding = 'utf-8') as outputFile:
        outputFile.write(contacts.to_string(header = False, index = False))
    return contacts

if __name__ == '__main__':
    getContacts()