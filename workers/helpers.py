from bs4 import BeautifulSoup


def extract_company_symbols(html_page):
    soup = BeautifulSoup(html_page, "html.parser")
    table = soup.find(id="constituents")
    for row in table.find_all("tr")[1:]:
        symbol = row.find("td").text.strip("\n")
        yield symbol
