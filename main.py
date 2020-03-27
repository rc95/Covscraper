import requests, PyPDF2, io
from bs4 import BeautifulSoup


parsed = BeautifulSoup(requests.get("https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports").content, "html.parser")
parsed_cases = parsed.find("div", {"id": "PageContent_C006_Col01"}).findChildren("p")

pdf_urls = []

for i in range(len(parsed_cases)):
	pdf_urls.append("https://www.who.int" + parsed_cases[i].findChildren("a")[0].get('href'))
	break

response = requests.get(pdf_urls[0])

pdf = PyPDF2.PdfFileReader(io.BytesIO(response.content))

print(pdf.getPage(0).extractText())
