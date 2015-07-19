from selenium import webdriver
import sys

city_code = sys.argv[1]

driver = webdriver.Firefox()
driver.get("http://www.antennesmobiles.fr/index.php?cp=%s&show" %city_code)
data=[]
for tr in driver.find_elements_by_xpath('//table[@id="mytable"]//tr'):
    tds=tr.find_elements_by_tag_name('td')
    if tds:
        data.append([td.text for td in tds])
driver.close()

with open('./data/network-map-%s.txt' %(city_code),'w') as data_file:
    for row in data:
        for elem in row:
            data_file.write('%s; ' % elem.encode('utf-8'))
        data_file.write('\n')