import product as prd
import bs4,re,requests,config
def get_products(proxies=None):
    """
        'proxies' parameter is a dictionary of http or https proxies
    """
    try:
        headers = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        if config.use_proxies:
            print("[JDSports Restocks] Fetching Products...")
            jdsports_response = requests.get("https://www.jdsports.co.uk/campaign/Re-Stocks/?facet-availability=restock&q=0&sort=latest",headers=headers,proxies=proxies)
            print("[JDSports Restocks] Finished Fetching Products")
        else:
            print("[JDSports Restocks] Fetching Products...")
            jdsports_response = requests.get("https://www.jdsports.co.uk/campaign/Re-Stocks/?facet-availability=restock&q=0&sort=latest",headers=headers,proxies=config.test_proxy)
            print("[JDSports Restocks] Finished Fetching Products")
        jdsports_document=jdsports_response.text
        return jdsports_document
    except requests.ConnectionError:
        print("\n[JDSports Restocks] ----------Connection Error\n")
        exit()
def parse_products(product_document):
        products_list = []
        jdsports_soup = bs4.BeautifulSoup(product_document,"lxml")
        products_soup = jdsports_soup.find_all("li",{"class":"productListItem"})
        for product_soup in products_soup:
            cont = (product_soup.find("a",{"data-e2e":"product-listing-name"}))
            url = cont.attrs["href"]
            image = (product_soup.find("img").attrs["src"])
            price = (product_soup.find("span",{"data-e2e":"product-listing-price"})).get_text().replace("Â","")
            title = cont.get_text()
            pid = re.search("/([0-9]+)/",url).groups()[0]
            url = "https://jdsports.co.uk"+url
            products_list.append(prd.Product(title,url,pid,price,image,"jdsports.co.uk"))
        products_list = products_list[:config.ppr]
        return products_list[::-1]
