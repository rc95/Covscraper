import requests
from bs4 import BeautifulSoup

parsed_cdc = BeautifulSoup(requests.get("https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html").content, "html.parser")
parsed_cdc_cases = parsed_cdc.find("div", {"class": "2019coronavirus-summary"}).findChildren("li")

for i in range(len(parsed_cdc_cases)):
	print(parsed_cdc_cases[i].get_text())

