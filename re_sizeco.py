import requests
import bs4
import re,config
import product as prd

def get_products(proxies=None):
    """
        'proxies' parameter is a dictionary of http or https proxies
    """
    try:
        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        if config.use_proxies:
            print("[Size Restocks] Fetching Products...")
            sizeco_response = requests.get("https://www.size.co.uk/featured/?facet-size-campaign2=restock&sort=latest",headers=headers,proxies=proxies)
            print("[Size Restocks] Finished Fetching Products")
        else:
            print("[Size Restocks] Fetching Products...")
            sizeco_response = requests.get("https://www.size.co.uk/featured/?facet-size-campaign2=restock&sort=latest",headers=headers,proxies=config.test_proxy)
            print("[Size Restocks] Finished Fetching Products")
        sizeco_document=sizeco_response.text
        return sizeco_document
    except requests.ConnectionError:
        print("\n[Size Restocks] ----------Connection Error\n")
        exit()


def parse_products(product_document):
        sizeco_soup = bs4.BeautifulSoup(product_document,"html.parser")
        products_soup = sizeco_soup.find_all("li",{"class":"productListItem"})
        product_list = []
        for product_soup in products_soup:
            url_data = product_soup.find("a",{"data-e2e":"product-listing-name"})
            image = ((product_soup.find("img",{"class":""})).attrs["src"])
            url = "https://www.size.co.uk"+url_data.attrs["href"]
            title = url_data.get_text()
            price = (product_soup.find("span",{"data-e2e":"product-listing-price"})).get_text().replace("Â","")
            pid = re.match(r".*?/([0-9]+)/.*?",url).group(1)
            product_list.append(prd.Product(title,url,pid,price,image,"size.co.uk"))
        product_list = product_list[:config.ppr]
        return product_list[::-1]
