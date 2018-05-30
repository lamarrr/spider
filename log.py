import product,time,os


#removed newline file inclusion


class Node:
    def __init__(self,pid,first_n=None,second_n=None,third_n=None,fourth_n=None):
        self.pid,self.first_n,self.second_n,self.third_n,self.fourth_n = pid,first_n,second_n,third_n,fourth_n


def record_product(file_name,product_id):
    with open(file_name,"a+") as record:
        record.write(record.read()+"\n"+product_id)
        record.close()




def get_logged_products(file) -> list:
    logged_products = []
    with open(file) as logfile:
        logged_products = logfile.readlines()
        logfile.close()
    return list(map((lambda x: x.replace("\n","")),logged_products))[::-1]

def product_exists(prd_product,logged_products) -> (bool,int) :
    needle = prd_product.pid
    exists = (needle in logged_products)
    if exists:
        return True, logged_products.index(needle)
    else:
        return False , None




def compute_file_nodes(logged_products) -> list:
    mod_logged_products = logged_products
    length = len(mod_logged_products)
    nodes = []
    for index,prd_id in enumerate(logged_products):
        lrange = (index+1)
        urange = (index)+5
        #lrange = (length-index)
        #urange = (length-index)+4
        product_neighbors = mod_logged_products[lrange:urange]
        node = Node(prd_id,*product_neighbors)
        nodes.append(node)
        index+=1
    return nodes
        





def equal_neighbors(f_node,s_node) -> bool:
    f_neighbors = [f_node.first_n,f_node.second_n,f_node.third_n,f_node.fourth_n]
    s_neighbors = [s_node.first_n,s_node.second_n,s_node.third_n,s_node.fourth_n]
    
    similar = False
    for neigh in f_neighbors:
        if neigh != None:
            n_equal = neigh in s_neighbors
            similar = n_equal or similar
        else:
            n_equal = True
            similar = n_equal or similar
    return similar



def compute_node(product_list,index) -> Node:
    length = len(product_list)
    lrange = -(length-(index-4))
    urange = -(length-index)
    #(index-5)
    #index+1,+5
    product_neighbors = product_list[lrange:urange][::-1]
    product_neighbors = map(lambda x: x.pid,product_neighbors)
    node = Node(product_list[index].pid,*product_neighbors)
    return node




"""demo purposes"""
def list_to_product(product_list) -> list:
    prd_list = list(map((lambda x: product.Product(None,None,x)),product_list))
    return prd_list

def is_loggable(index,parsed_product_list,prev_prds,prev_nodes) -> list:
    prd = parsed_product_list[index]
    t = product_exists(prd,prev_prds)
    if t[0]:
        prev_prd_node = prev_nodes[t[1]]
        new_prd_node = compute_node(parsed_product_list,index)
        #print(new_prd_node.pid,": ",new_prd_node.first_n,new_prd_node.second_n,new_prd_node.third_n,new_prd_node.fourth_n)
        #print(prev_prd_node.pid,": ",prev_prd_node.first_n,prev_prd_node.second_n,prev_prd_node.third_n,prev_prd_node.fourth_n)
        
        if equal_neighbors(prev_prd_node,new_prd_node):
            
            print("[Logger] Same Neighbors, Not Recording  \n")
            return False,"exists"
        else:
            return True,"restock"
    else:
        return True,"neww"



NEW_PRODUCTS_FILES = {
        "footpatrol.com": os.path.join("logs","latest","footpatrol.txt"),
        "size.co.uk": os.path.join("logs","latest","size.txt"),
        "jdsports.co.uk": os.path.join("logs","latest","jdsports.txt"),

    }



#test
#new_prd = ["15","14","13","12","11","10","9","8","7","6","5","4"]
#new_prd = new_prd[::-1]
#new_p = list_to_product(new_prd)

#pprd=(get_logged_products(NEW_PRODUCTS_FILES["size.co.uk"]))
#print(pprd)

#for index,r in enumerate(new_p):
#    s = compute_node(new_p,index)
#    print(s.pid, ": ",s.first_n,s.second_n,s.third_n,s.fourth_n)
