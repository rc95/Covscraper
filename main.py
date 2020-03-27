import requests, re
from bs4 import BeautifulSoup

# cdc testing
def get_cdc():
	parsed_cdc = BeautifulSoup(requests.get("https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html").content, "html.parser")
	parsed_cdc_cases = parsed_cdc.find("div", {"class": "2019coronavirus-summary"}).findChildren("li")
	numResults = []
	blacklist = ['Jurisdictions', 'reporting', 'states', 'district']

	for i in range(len(parsed_cdc_cases)):
		canAppend = True
		s = parsed_cdc_cases[i].get_text()

		for i2 in range(len(blacklist)):
			if s.find(blacklist[i]) != -1:
				canAppend = False
				break

		if canAppend:
			numResults.append(int(''.join(re.findall("\d+", s))))

	numResults.sort(reverse=True)

	return {'cases': numResults[0], 'deaths': numResults[1]}

print(get_cdc())

# folkhälsomyndigheten testing
#https://experience.arcgis.com/experience/09f821667ce64bf7be6f9f87457ed9aa
parsed_fhm = BeautifulSoup(requests.get("https://fohm.maps.arcgis.com/apps/opsdashboard/index.html").content, "html.parser")
print(parsed_fhm.find("iframe-widget_1"))
parsed_fhm_cases = parsed_fhm.find("full-container", {"class": "layout-reference"}).findChildren("text")
numResults = []
blacklist = ['Intensivvårdade']

for i in range(len(parsed_fhm_cases)):
	canAppend = True
	s = parsed_fhm_cases[i].get_text()

	for i2 in range(len(blacklist)):
		if s.find(blacklist[i]) != -1:
			canAppend = False
			break

	if canAppend:
		numResults.append(int(''.join(re.findall("\d+", s))))

numResults.sort()
print(numResults)


# typical structure should follow:
# 1. request with a GET
# 2. parse with BeautifulSoup 4 using the html.parser
# 3. find the appropriate div with relevant class (if possible)
# 4. loop through the list and add text to a list
# 5. parse the list for cases and deaths and add to two separate self vars