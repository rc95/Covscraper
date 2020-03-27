import requests, PyPDF2, io
from bs4 import BeautifulSoup

parsed = BeautifulSoup(requests.get("https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports").content, "html.parser")
parsed_cases = parsed.find("div", {"id": "PageContent_C006_Col01"}).findChildren("p")

pdf_urls = []

for i in range(len(parsed_cases)):
	pdf_urls.append("https://www.who.int" + parsed_cases[i].findChildren("a")[0].get('href'))

	response = requests.get(pdf_urls[i])

	pdf = PyPDF2.PdfFileReader(io.BytesIO(response.content))
	text = pdf.getPage(0).extractText()
	text = text.split()

	data = []

	for i2 in range(len(text)):
		if text[i2] == "Globally":
			cases = ""
			deaths = ""

			i2 += 1

			while text[i2].isdigit():
				cases += text[i2]
				i2 += 1

			i2 += 1

			while not text[i2].isdigit():
				i2 += 1

			while text[i2].isdigit():
				deaths += text[i2]
				i2 += 1

			# more robust process would be:
			# 1. find confirmed
			# 2. while loop backwards till
			# you find Globally again
			# 3. while looping add to the array
			# 4. repeat for deaths

			data.append({'global_cases': cases, 'global_deaths': deaths})

	print(data)

	# wont parse well beyond 10-ish due to WHO pdf format changing
	if i >= 6:
		break