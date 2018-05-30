import random,time,datetime
import discord,footpatrol,jdsports,config,sizeco
import concurrent.futures,os,log
import re_footpatrol,re_sizeco,re_jdsports






RESTOCKED_PRODUCTS_FILES = {
        "footpatrol.com": os.path.join("logs","restock","footpatrol.txt"),
        "size.co.uk": os.path.join("logs","restock","size.txt"),
        "jdsports.co.uk": os.path.join("logs","restock","jdsports.txt"),
    }



NEW_PRODUCTS_FILES = {
        "footpatrol.com": os.path.join("logs","latest","footpatrol.txt"),
        "size.co.uk": os.path.join("logs","latest","size.txt"),
        "jdsports.co.uk": os.path.join("logs","latest","jdsports.txt"),

    }




def main():
    



    #fetch functions for new products
    fetch_funcs_new = [jdsports.get_products,footpatrol.get_products,sizeco.get_products]
    parse_funcs_new = [jdsports.parse_products,footpatrol.parse_products,sizeco.parse_products]

    #fetch functions for restocked products
    fetch_funcs_restock = [re_jdsports.get_products,re_footpatrol.get_products,re_sizeco.get_products]
    parse_funcs_restock = [re_jdsports.parse_products,re_footpatrol.parse_products,re_sizeco.parse_products]

    #threads and futures
    documents_thread_pool_exec = concurrent.futures.ThreadPoolExecutor()
    documents_futures_new = []
    documents_futures_restock = []




    #if bot should use proxies
    #randomly choose proxies
    #add future objects
    if config.use_proxies:
        for fetch_func in fetch_funcs_new:
            documents_futures_new.append(documents_thread_pool_exec.submit(fetch_func,{"https":random.choice(config.proxies)}))
        for fetch_func in fetch_funcs_restock:
            documents_futures_restock.append(documents_thread_pool_exec.submit(fetch_func,{"https":random.choice(config.proxies)}))

    else:
        for fetch_func in fetch_funcs_new:
            documents_futures_new.append(documents_thread_pool_exec.submit(fetch_func))
        for fetch_func in fetch_funcs_restock:
            documents_futures_restock.append(documents_thread_pool_exec.submit(fetch_func))
    


    #documents for new products
    documents_new = []
    for future in documents_futures_new:
        documents_new.append(future.result())
    print("[BOT] All New Products Fetched")



    #documents for restocked products
    documents_restock = []
    for future in documents_futures_restock:
        documents_restock.append(future.result())
    print("[BOT] All Restocked Products Fetched\n\n")




    print("[Parser] Extracting New Products Data...")
    parsed_new_products = []
    for index in range(len(documents_new)):
        parsed_new_products.append(parse_funcs_new[index](documents_new[index]))
    print("[Parser] Done")


    print("[Parser] Extracting Restocked Products Data...")
    parsed_restock_products = []
    for index in range(len(documents_restock)):
        parsed_restock_products.append(parse_funcs_restock[index](documents_restock[index]))
    print("[Parser] Done\n\n")
    
    
    
    verified_new_products = []
    verified_restock_products = []

    


    def match_keywords(to_check):
        is_match = False
        matched=""
        for keyword in config.keywords:
            if keyword.lower() in to_check.lower():
                is_match = True
                matched = keyword.lower()
                break
        return is_match,matched







    def ev_keywords():
        
        
        print("[Logger] •••••• Queuing and Evaluating New Products ••••••")
        
        for retailer_products in parsed_new_products:
            
            for index,product in enumerate(retailer_products):
                is_match,match = match_keywords(product.title)
                if is_match:
                    print("[Logger] Product: ",product.pid," : ",product.title.ljust(45)," From: ",product.retailer," Matches Keyword: ",match)
                    #print(product.retailer)
                    #print(product.title)
                    saved_products = log.get_logged_products(NEW_PRODUCTS_FILES[product.retailer])
                    node = log.compute_node(retailer_products,index)
                    #print(node.pid,":",node.first_n,node.second_n,node.third_n,node.fourth_n)
                    exists,exist_index = log.product_exists(product,saved_products)
                    #print((exists,exist_index))
                    #print()
                    if exists:
                        fn = log.compute_file_nodes(saved_products)
                        #print(fn[exist_index].pid,fn[exist_index].first_n,fn[exist_index].second_n,fn[exist_index].third_n,fn[exist_index].fourth_n)
                        log.record_product(NEW_PRODUCTS_FILES[product.retailer],product.pid)
                        if (log.equal_neighbors(node,fn[exist_index])):
                            print("[Logger] Product: ",product.pid," : ",product.title.ljust(45), " Already Exists")
                        else:
                            #1.3 log.record_product(NEW_PRODUCTS_FILES[product.retailer],product.pid)
                            verified_new_products.append(product)
                            print("[Logger] Product: ",product.pid," is a Restock, Product Queued")
                    else:
                        log.record_product(NEW_PRODUCTS_FILES[product.retailer],product.pid)
                        verified_new_products.append(product)
                        
                        print("[Logger] New Product: ",product.pid," : ",(product.title.ljust(45))," Queued")
                else:
                    log.record_product(NEW_PRODUCTS_FILES[product.retailer],product.pid)
                    print("[Logger] Product: ",product.pid," : ",product.title.ljust(45)," From: ",product.retailer," Does not Match Any Keyword")


        
        
            
                    

        print("[Logger] Done")
        print("[Logger] Found ",str(len(verified_new_products))," New Products (With Keywords)\n\n")


        
        
        
        
        print("[Logger] •••••• Queuing and Evaluating Restocked Products ••••••")
        
        for retailer_products in parsed_restock_products:
            
            for index,product in enumerate(retailer_products):
                is_match,match = match_keywords(product.title)
                if is_match:
                    print("[Logger] Product: ",product.pid," : ",product.title.ljust(45)," From: ",product.retailer," Matches Keyword: ",match)
                    #print(product.retailer)
                    #print(product.title)
                    saved_products = log.get_logged_products(RESTOCKED_PRODUCTS_FILES[product.retailer])
                    node = log.compute_node(retailer_products,index)
                    #print(node.pid,":",node.first_n,node.second_n,node.third_n,node.fourth_n)
                    exists,exist_index = log.product_exists(product,saved_products)
                    #print((exists,exist_index))
                    #print()
                    if exists:
                        fn = log.compute_file_nodes(saved_products)
                        #print(fn[exist_index].pid,fn[exist_index].first_n,fn[exist_index].second_n,fn[exist_index].third_n,fn[exist_index].fourth_n)
                        log.record_product(RESTOCKED_PRODUCTS_FILES[product.retailer],product.pid)
                        if (log.equal_neighbors(node,fn[exist_index])):
                            print("[Logger] Product: ",product.pid," : ",product.title.ljust(45), " Already Exists")
                        else:
                            #1.3 log.record_product(RESTOCKED_PRODUCTS_FILES[product.retailer],product.pid)
                            verified_restock_products.append(product)
                            print("[Logger] Product: ",product.pid," is a Restock, Product Queued")
                    else:
                        log.record_product(RESTOCKED_PRODUCTS_FILES[product.retailer],product.pid)
                        verified_restock_products.append(product)
                        
                        print("[Logger] New Product: ",product.pid," : ",(product.title.ljust(45))," Queued")
                else:
                    log.record_product(RESTOCKED_PRODUCTS_FILES[product.retailer],product.pid)
                    print("[Logger] Product: ",product.pid," : ",product.title.ljust(45)," From: ",product.retailer," Does not Match Any Keyword")
      
        print("[Logger] Done")
        print("[Logger] Found ",str(len(verified_restock_products))," Restocked Products (With Keywords)\n\n")
        

    ev_keywords()
    
    




    if len(verified_new_products) != 0:
        
        products_json = []
        print("[Webhook] Preparing New Products Data For Transfer To Discord...")
        for product in verified_new_products:
            products_json.append(discord.prepare_json(product))
        print("[Webhook] Done\n")
        print("[Webhook] •••••• Sending New Products to Discord ••••••")
        index = 0
        for product_json in products_json:
            index+=1
            print("[Webhook] Sending Product: ["+str(index)+"] to Discord")
            print("[Webhook] Sent")
            discord.post_product(product_json)
        print("[Webhook] All ",index," Products Sent To Discord\n\n")
    else:
        print("[New Products Logger] All New Products Up to Date\n\n")



    if len(verified_restock_products) != 0:
        
        products_json = []
        print("[Webhook] Preparing Restocked Products Data For Transfer To Discord...")
        for product in verified_restock_products:
            products_json.append(discord.prepare_json(product))
        print("[Webhook] Done\n")
        print("[Webhook] •••••• Sending Restocked Products to Discord ••••••")
        index = 0
        for product_json in products_json:
            index+=1
            print("[Webhook] Sending Restocked Product: ["+str(index)+"] to Discord")
            print("[Webhook] Sent")
            discord.post_product(product_json)
        print("[Webhook] All ",index," Restocked Products Sent To Discord\n\n")
    else:
        print("[Restocked Products Logger] All Restocked Products Up to Date\n\n")




    
    

def clean_log():
        for file in NEW_PRODUCTS_FILES:
            with open(NEW_PRODUCTS_FILES[file],"r+") as log:
                logs = log.readlines()
                logs = logs[::-1]
                mod_logs = logs[:config.max_log_products]
                log.close()
                fmod = open(NEW_PRODUCTS_FILES[file],"w")
                fmod.write("")
                fmod.close()
                s = open(NEW_PRODUCTS_FILES[file],"r+")
                for p in mod_logs:
                    p+="\n"
                
                s.writelines(mod_logs[::-1])
                


while True:
    print("[BOT] Starting... Hello!\n")
    print("[BOT] •••••• Initiating Spiders For Crawling ••••••")
    main()
    hours = config.interval["hours"]*60*60
    days = config.interval["days"]*24*60*60*60
    minutes = config.interval["minutes"]*60
    seconds = config.interval["seconds"]
    next_time = days+minutes+hours+seconds
    print("[BOT] Finished, Next Schedule is in: ",next_time/60/60,"hours ->",next_time/60,"minutes ->",next_time,"seconds")
    print("[BOT] Cleaning Up Log Files...")
    clean_log()
    print("[BOT] Sleeping...")
    time.sleep(next_time)
    print("[BOT] Waking Up...")