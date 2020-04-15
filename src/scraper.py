#!/usr/bin/env python3
import sys
import requests
import argparse
from bs4 import BeautifulSoup

import re

parser = argparse.ArgumentParser(description='MHLW COVID Info Extractor.')
parser.add_argument('-j', '--japan', help='Japanese domestic information')
parser.add_argument('-w', '--world', help='World information')
args = parser.parse_args()

summary_page = 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00086.html'

headers = {
    "User-Agent": "MHLW-COVID-Info-Extractor/0.0.1",
}

res = requests.get(summary_page, headers = headers)
# print(res.request.headers, file=sys.stderr)
# print(res.status_code, file=sys.stderr)
res.raise_for_status()

soup = BeautifulSoup(res.content, "html5lib")

list = (soup
        .find_all("div", class_="m-grid__col1")[1]
        .find_all(href=re.compile(r"html$"), string=re.compile(r"^新型コロナ"))
)
#     .find_parent("a")

def get_str(elem):
    if elem.string:
        return(elem.string)
    else:
        return(re.sub('\n\s*', '', elem.text))

def print_table(t, date):
    rows = t.find_all("tr")
    first_line_cols = rows[0].find_all("td")
    n_cols = len(first_line_cols)
    print(n_cols, 'cols')
    if n_cols >= 8: # only prefecture table and country table
        return
    for i in range(len(rows)):
        data = [date]
        cols = rows[i].find_all("td")
        for j in range(len(cols)):
            data.append(get_str(cols[j]))
        print('\t'.join(data), flush=True)

def extract_table(url, date):
    res = requests.get(url, headers = headers)
    res.raise_for_status()
    
    soup = BeautifulSoup(res.content, "html5lib")
    tables = soup.find_all("tbody")
    for t in tables:
        rows = t.find_all("tr")
        size = len(rows)
        if size > 5:            # print only tables, not notes
            print(size, 'rows')
            print_table(t, date)
            

# extract_table('https://www.mhlw.go.jp/stf/newpage_09571.html', "date")
# extract_table('https://www.mhlw.go.jp/stf/newpage_10636.html')
# sys.exit()

for item in list:
    date = re.findall('令和.*日', item.string)[0]
    link = item.get("href")
    extract_table(link, date)

# link = urljoin(url, href.get("href"))

# print(soup.find("h1").get_text(strip=True))

# text = "\n".join([i.strip() for i in soup.get_text().splitlines() if i.strip()])

# m = re.search(
    # r"国内の状況について\n(.+?)月(.+?)日(.+?)：(.+?)現在.+?チャーター便帰国者を除く.+?・患者(.+?)例、無症状病原体保有者(.+?)例\n+?・.+?月.+?日18時時点までに疑似症サーベイランスおよび積極的疫学調査に基づき、計(.+?)件の検査を実施。そのうち(.+?)例が陽性。(.+?)例が陰性、(.+?)例が結果待ち。\n・上記患者のうち入院中または入院予定(.+?)名、退院(.+?)名、死亡(.+?)名。\n・無症状病原体保有者(.+?)名は入院中または入院予定(.+?)名、退院(.+?)名。",
#     text,
#     re.DOTALL,
# )

# print(m.group(0))

# print(m.groups())

# if m:
#     pcr = [str2int(i) for i in m.groups()]

#     print([pcr[0], pcr[1], pcr[2], pcr[6], pcr[4] + pcr[5], pcr[4], pcr[11], pcr[12]])


# def str2int(x):

#     x = x.replace(",", "")
#     x = x.strip()
#     x = jaconv.z2h(x, digit=True)

#     return int(x)
