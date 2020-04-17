import sys
import re
import requests
from bs4 import BeautifulSoup

class Extractor:
    def __init__(self):
        self.headers = {
            "User-Agent": "MHLW-COVID-Info-Extractor/0.0.1",
        }

    def extract_list(self, verbose):
        summary_page = 'https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00086.html'
        res = requests.get(summary_page, headers = self.headers)
        res.raise_for_status()
        if verbose:
            print(res.request.headers, file=sys.stderr)
            print(res.status_code, file=sys.stderr)
        soup = BeautifulSoup(res.content, "html5lib")
        list = (soup
                .find_all("div", class_="m-grid__col1")[1]
                .find_all(href=re.compile(r"html$"), string=re.compile(r"^新型コロナ"))
                # .find_parent("a")
        )
        return list

    def extract_table(self, url, num):
        res = requests.get(url, headers = self.headers)
        res.raise_for_status()
        
        soup = BeautifulSoup(res.content, "html5lib")
        print(soup.find_all)

        title = soup.find('title').string
        date = re.findall('\d+月\d+日', title)[0]
        print(f'{date}')
        head = soup.find_all("thead")
        for h in head:
            header = []
            for th in h.find_all("th"):
                header.append(th.text)
            print('\t'.join(header))

        tables = soup.find_all("tbody")
        for t in tables:
            self.print_table(t, num)

    def print_table(self, t, num):
        rows = t.find_all("tr")
        n_rows = len(rows)
        # Do not print short notes, but only long tables
        if n_rows <= 5:
            return
        first_line_cols = rows[0].find_all("td")
        n_cols = len(first_line_cols)
        # Only country table (2 or 3 cols) and prefecture table (5 cols)
        if n_cols >= 8:
            return
        # print(n_cols, 'cols', 'x', n_rows, 'rows')
        # print(first_line_cols[0].text)
        max = len(rows)
        if num is not None:
            max = num
        for i in range(max):
            data = []
            cols = rows[i].find_all("td")
            for j in range(len(cols)):
                data.append(self.get_str(cols[j]))
            print('\t'.join(data), flush=True)

    def get_str(self, elem):
        # if elem.string:
        #     return(elem.string)
        # else:
        return(re.sub('\n\s*', '', elem.text))



# def str2int(x):

#     x = x.replace(",", "")
#     x = x.strip()
#     x = jaconv.z2h(x, digit=True)

#     return int(x)



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
