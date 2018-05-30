


class Product:
    __slot__ = ["name","pid","url","price","image","retailer"]
    def __init__(self,title=None,url=None,pid=None,price=None,image=None,retailer=None):
        self.title,self.pid,self.url,self.price,self.image,self.retailer = title,pid,url,price,image,retailer
