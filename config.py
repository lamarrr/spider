discord_webhook_url = "https://discordapp.com/api/webhooks/415507905027244043/ORwOCmuvGQ6OZOXwkKoP7kXMANVASpBTAuu8ebsUmMtWDi2_MZZhxmyoTKODc7mno0FJ"
test_proxy = {"https":"http://lum-customer-domdosu-zone-residential-country-us-session-037:dammydosu14@zproxy.luminati.io:22225"}
#list of proxies picked randomly
# i.e: {"https": "http://me:mypassword@myserver:port"}    since they are all https connections
proxies = [
    # goes on and on to your number of proxies
                {"https":""},
                {"https":""},
                {"https":""},
                {"https":""},
                {"https":""},
                {"https":""}
]
use_proxies = False
# ppr - products per request (each -> size.co.uk,foodpatrol,jdsports)
ppr = -1
interval = {
        "days":0,
        "hours": 0,
        "minutes":0,
        "seconds":2,
}


#all in small letters please
#for scraping without keywords add "" to the keywords list
keywords = [
        "nike",
        "adidas",
        "air max",
        "nike air",
        "taylor"
]


max_log_products = 300