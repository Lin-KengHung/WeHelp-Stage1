from bs4 import BeautifulSoup
import urllib.request as req
def getData(url, file):

    request = req.Request(url, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "cookie" : "over18=1"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = BeautifulSoup(data, "html.parser")
    titles = root.find_all("div", class_="title")
    for title in titles:
        line = []
        if title.a != None:
            line.append(title.a.string)
            href = "https://www.ptt.cc" + title.find("a")["href"]
            

            request2 = req.Request(href, headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "cookie" : "over18=1"
            })
            with req.urlopen(request2) as response:
                data2 = response.read().decode("utf-8")
           
            root2 = BeautifulSoup(data2, "html.parser")

            # 計算推噓總數
            like = root2.find_all("span", class_="hl push-tag", string="推 ")
            dislike = root2.find_all("span", class_="f1 hl push-tag", string="噓 ")
            count = len(like) + len(dislike)
            line.append(str(count))
            
            # 抓時間
            if (root2.find("span", string="時間") != None and root2.find("span", string="時間").find_next("span") != None):
                time =  root2.find("span", string="時間").find_next("span").string
                line.append(time)
            
        else:
            continue
     
        file.write(",".join(line) + "\n")



    nextLink = root.find("a", string="‹ 上頁")
    return nextLink["href"]

# pageURL = "https://www.ptt.cc/bbs/Lottery/index.html"
# getData(pageURL)

with open("article.csv", mode="w", encoding="utf-8") as file:
    count = 0
    pageURL = "https://www.ptt.cc/bbs/Lottery/index.html"
    while count < 3:
        pageURL = "https://www.ptt.cc" + getData(pageURL, file)
        count += 1
