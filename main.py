from bs4 import BeautifulSoup as bfs
import requests
import sys
import time

site = input("site:")

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

all_pages = []
numbers_pages = 0


def getting_html(site, headers):
    try:
        session = requests.Session()
        request = session.get(site, headers=headers)
        status = request.status_code
        page_html = bfs(request.text, "lxml")
        if status == 200:

            return getting_url(page_html)

    except Exception as name_error:
        print("Error!", name_error)
        print(sys.exc_info()[1])


def getting_url(page_html):
    all_links = page_html.find_all('a', href=True)
    url_list = []
    meta_title = page_html.find('title')
    meta_keywords = page_html.find('meta', attrs={'name': 'keywords'})
    meta_description = page_html.find('meta', attrs={'name': 'description'})
    print(meta_title)
    print(meta_keywords)
    print(meta_description)
    for link in all_links:
        url = (link.get('href'))
        if (url != '/') and (url != ''):
            url_list.append(url)

    return finding_url_pages(url_list)



def host_name(site):
    w = "www."
    b = "://"
    if w in site:
        url_names = site.split(w)
        host = (url_names[0] + w)
        name = url_names[1]

        return host, name

    elif b and (w not in site):
        url_names = site.split(b)
        host = (url_names[0] + b)
        name = url_names[1]

        return host, name


def finding_url_pages(url_list):
    list_0 = set(url_list)
    list_1 = list(list_0)
    list_bad = ["tel:", "mailto:", "#", "javascript:", ".jpg", ".png", "./", ".rar", ".pdf", ".PDF", ".jpeg"]
    item = 0

    while item < (len(list_1) + 1):
        for n in list_1:
            for list_1_f in range(len(list_bad)):
                find_str = list_bad[list_1_f]
                # print(find_str)
                if find_str in n:
                    i = list_1.index(n)
                    list_1.pop(i)
        item += 1

    return filtering_pages(list_1)


def filtering_pages(list_1):
    host, domain = host_name(site)
    filtered_pages = []
    for item in range(0, len(list_1)):
        if host and domain in list_1[item]:
            filtered_pages.append(list_1[item])

        elif "/" == (list_1[item][0]):
            if domain[-1] == "/":
                filtered_pages.append(host + domain[:-1] + list_1[item])
            else:
                filtered_pages.append(host + domain + list_1[item])
        # elif "/" and host not in list_1[item]:
        #     if domain[-1] == "/":
        #         filtered_pages.append(host + domain[:-1] + list_1[item])
        #     else:
        #         filtered_pages.append(host + domain + list_1[item])

    return collecting_page(filtered_pages)


def collecting_page(filtered_pages):
    for i in filtered_pages:
        if i not in all_pages:
            all_pages.append(i)


getting_html(site, headers)

#item = 0

while numbers_pages != len(all_pages):
    time.sleep(3)
    numbers_pages += 1
    getting_html(all_pages[numbers_pages], headers)

    print(all_pages[numbers_pages])
    print(numbers_pages)
    print(len(all_pages))

print("End!")

