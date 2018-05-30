import requests,json,config
import product,footpatrol

def prepare_json(product):
    jd = json.dumps({
        "title":product.title,
        "url": product.url,   
    "embeds": [
        {
            "title":product.title,
            "url":product.url,
            "thumbnail": {
                "url":product.image,                
        },  
            "fields": [{
                "name":"Price:",
                "value":product.price,
            },
                {
                "name":"Retailer:",
                "value":product.retailer,
            }
            ],
            "footer": {
                "text": "brought to you by OOTW",
            },
            
            "description": product.pid
        }
    ]
    })
    return jd
      
def post_product(json_product):
    a=requests.post(config.discord_webhook_url,data=json_product,headers={"Content-Type":"application/x-www-form-urlencoded"})
    
#for i_product in footpatrol.parse_products(footpatrol.get_products()):
#    post_product(prepare_json(i_product,"footpatrol.com"))