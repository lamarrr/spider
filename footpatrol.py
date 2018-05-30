import requests
import bs4
import re,config,random
import product as prd
def get_products(proxies=None):
    """
        'proxies' parameter is a dictionary of http or https proxies
    """
    try:
        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        if config.use_proxies:
            print("[Footpatrol] Fetching Products...")
            footpatrol_response = requests.get("https://www.footpatrol.com/products/ni:view-new-in-items/",headers=headers,proxies=proxies)
            print("[Footpatrol] Finished Fetching Products")
        else:
            print("[Footpatrol] Fetching Products...")
            footpatrol_response = requests.get("https://www.footpatrol.com/products/ni:view-new-in-items/",headers=headers,proxies=config.test_proxy)
            print("[Footpatrol] Finished Fetching Products")
        footpatrol_document=footpatrol_response.text
        return footpatrol_document
    except requests.ConnectionError:
        print("\n[Footpatrol] ----------Connection Error\n")
        exit()

def parse_products(product_document):
        products_list = []
        footpatrol_soup = bs4.BeautifulSoup(product_document,"lxml")
        products_soup = footpatrol_soup.find_all("li",{"class":"fp-column-quarter"})
        for product_soup in products_soup:
            url = (product_soup.find("a").attrs["href"])
            image = (product_soup.find("img").attrs["src"])
            price = (product_soup.find("h4",{"class":"fp-product-thumb-price"}).get_text().replace(" ","").replace("\n",""))
            title = re.sub(r"\s{3,25}","",(product_soup.find("h4",{"class":"fp-product-thumb-title"}).get_text().replace("\n","")))
            pid = re.search("/([0-9]+)",url).groups()[0]
            url = "https://www.footpatrol.com"+url
            products_list.append(prd.Product(title,url,pid,price,image,"footpatrol.com"))
        products_list = products_list[:config.ppr]
        return products_list[::-1]
