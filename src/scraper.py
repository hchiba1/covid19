#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

import re

from urllib.parse import urljoin


def str2int(x):

    x = x.replace(",", "")
    x = x.strip()
    x = jaconv.z2h(x, digit=True)

    return int(x)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
}


def get_link():

    url = "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000121431_00086.html"

    r = requests.get(url, headers=headers)

    r.raise_for_status()

    soup = BeautifulSoup(r.content, "html5lib")

    href = (
        soup.find("div", class_="l-contentMain")
        .find(string=re.compile(r"^新型コロナウイルス感染症の現在の状況と厚生労働省の対応について"))
        .find_parent("a")
    )

    link = urljoin(url, href.get("href"))

    return link


url = get_link()

print(url)

r = requests.get(url, headers=headers)

r.raise_for_status()

soup = BeautifulSoup(r.content, "html5lib")

"""## タイトル表示"""

print(soup.find("h1").get_text(strip=True))

"""## 画像表示"""

img = soup.find("img", src=re.compile("^data:image/png;base64,"))

img_b64 = img.get("src").replace("data:image/png;base64,", "")

import base64

png = base64.b64decode(img_b64)

with open("corona.png", "wb") as fw:
    fw.write(png)

from IPython.display import Image

import jaconv

text = "\n".join([i.strip() for i in soup.get_text().splitlines() if i.strip()])

# 正規表現で抽出
m = re.search(
    r"国内の状況について\n(.+?)月(.+?)日(.+?)：(.+?)現在.+?チャーター便帰国者を除く.+?・患者(.+?)例、無症状病原体保有者(.+?)例\n+?・.+?月.+?日18時時点までに疑似症サーベイランスおよび積極的疫学調査に基づき、計(.+?)件の検査を実施。そのうち(.+?)例が陽性。(.+?)例が陰性、(.+?)例が結果待ち。\n・上記患者のうち入院中または入院予定(.+?)名、退院(.+?)名、死亡(.+?)名。\n・無症状病原体保有者(.+?)名は入院中または入院予定(.+?)名、退院(.+?)名。",
    text,
    re.DOTALL,
)

print(m.group(0))

m.groups()

if m:
    pcr = [str2int(i) for i in m.groups()]

    print([pcr[0], pcr[1], pcr[2], pcr[6], pcr[4] + pcr[5], pcr[4], pcr[11], pcr[12]])

# 00:月
# 01:日
# 02:時
# 03:分
# 04:患者数
# 05:無症状病原体保有者
# 06:検査計
# 07:検査陽性
# 08:検査陰性
# 09:結果待ち
# 10:入院
# 11:退院
# 12:死亡
# 13:無症状計
# 14:無症状入院
# 15:無症状退院

# 画像の表を表示
Image("./corona.png")
