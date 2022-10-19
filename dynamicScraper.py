from requests_html import HTMLSession
import pandas as pd


# You can find more information about requests_html on:
# https://requests.readthedocs.io/projects/requests-html/en/latest/


# url = 'https://negyvaseteris.lt/visos-prekes/' # url of the page from where we want get data

s = HTMLSession() # start sesssion
itemsList = [] # arr for products list

def request(url):
    # This funcion send request to the page and find our element:

    r = s.get(url) # render the page

    r.html.render(sleep = 1) # render page html (sleep is for pause)

    return r.html.xpath('//*[@id="products-container"]/div/div/ul', first = True) # element that contains our data xpath


def parse(products):
    # Grab a list of all links on the page, in absolute form (anchors excluded) and loop for every product in the list:

    for item in products.absolute_links:
        r = s.get(item) #rendering single product page (not list but only one product)

        # Get desired data from the page:
        # In this example, it will be the product title, price, and material
        # In case there is no data, use try & except block to avoid stopping data extraction
        try:
            title = r.html.find('h1.product_title', first = True).text # get product title
        except:
            title = "no title"
        try:
            material = r.html.find('div.elementor-element.elementor-element-ad63ff6.elementor-widget.elementor-widget-woocommerce-product-content > div > p:nth-child(1)', first = True).text # get product material
        except:
            material = "no material"

        price = r.html.find('span.woocommerce-Price-amount.amount', first = True).text # get product price
        
        
        # create object with scraped data:
        product = {
            "Title": title,
            "Price": price,
            "Material": material,
        }
        
        itemsList.append(product) # put the product into the products list


def output():
    # This funcion put our data into Pandas data frame and saved it to CSV file:

    df = pd.DataFrame(itemsList) # put products into Pandas data frame 
    df.to_csv('negyvasEteris.csv') #creating csv file (if index is not needed just add index=False)
    print("Saved to CSV file") #print messagge that work is done



# data = request(url)
# parse(data)

#if url has more than one page, comment out the last two lines (data = request(url) and parse(data)) and uncomment code below

#Pagination:
i = 1 # page number

while True:
    try:
        data = request(f'https://negyvaseteris.lt/visos-prekes/page/{i}')
        print(f'Getting items from page {i}') #messagge to known that is working
        parse(data)
        print("Total: ", len(itemsList))

        i = i + 1 #after every loop, increase the page number by 1
    except:
        #if there is no more pages print out warning messagge and break loop
        print('No more products found!')
        break

output()