import csv
from parsel import Selector
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

writer = csv.writer(open('output.csv', 'w+', encoding='utf-8-sig', newline=''))
writer.writerow(['Name', 'Position', 'Company', 'Education', 'Location', 'URL']) #dados da pessoa

driver = webdriver.Chrome("chromedriver.exe")#driver do navegador
driver.get('https://www.linkedin.com/')

html_Search = "input[class*='input__field input__field--with-label'][name='session_key']" #busca botão de log

username = driver.find_element_by_css_selector(html_Search)
ActionChains(driver).move_to_element(username).click(username).perform()
username.send_keys('seu Login')
sleep(0.5)

password = driver.find_element_by_name('session_password')
password.send_keys('Sua Senha')
sleep(0.5)

sign_in_button = driver.find_element_by_class_name('sign-in-form__submit-btn')
sign_in_button.click()
sleep(2)

driver.get('https://www.google.com/')
search_query = driver.find_element_by_name('q')
search_query.send_keys('site:linkedin.com/in AND "Laravel" AND "catalão"') #alterar pesquisa para profissão e regiao desejada
search_query.send_keys(Keys.RETURN)
sleep(0.5)
print(Keys.RETURN)


urls = driver.find_elements_by_xpath('//*[@class = "r"]/a[@href]')
urls = [url.get_attribute('href') for url in urls]
sleep(0.5)

for url in urls: #monta os dados de acordo com a pagina
    driver.get(url)
    sleep(2)

    sel = Selector(text=driver.page_source)

    name = sel.xpath('//*[@class = "inline t-24 t-black t-normal break-words"]/text()').extract_first().split()
    name = ' '.join(name)

    position = sel.xpath('//*[@class = "mt1 t-18 t-black t-normal"]/text()').extract_first().split()
    position = ' '.join(position)

    experience = sel.xpath('//*[@class = "pv-top-card-v3--experience-list"]')
    company = experience.xpath('./li[@data-control-name = "position_see_more"]//span/text()').extract_first()
    company = ''.join(company.split()) if company else None
    education = experience.xpath('.//li[@data-control-name = "education_see_more"]//span/text()').extract_first()
    education = ' '.join(education.split()) if education else None

    location = ' '.join(sel.xpath('//*[@class = "t-16 t-black t-normal inline-block"]/text()').extract_first().split())

    url = driver.current_url

    print('\n')
    print('Name: ', name)
    print('Position: ', position)
    print('Company: ', company)
    print('Education: ', education)
    print('Location: ', location)
    print('URL: ', url)
    print('\n')

    writer.writerow([name,
                     position,
                     company,
                     education,
                     location,
                     url])

driver.quit()
