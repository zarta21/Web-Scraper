from requests_html import HTMLSession
import pandas as pd


# url = 'https://negyvaseteris.lt/visos-prekes/' # url of the page from where we want get data

s = HTMLSession() 
itemsList = [] 

def request(url):
    r = s.get(url)
    r.html.render(sleep = 1) 

    return r.html.xpath('//*[@id="products-container"]/div/div/ul', first = True) 


def parse(products):

    for item in products.absolute_links:
        r = s.get(item) 

        try:
            title = r.html.find('h1.product_title', first = True).text 
        except:
            title = "no title"
        try:
            material = r.html.find('div.elementor-element.elementor-element-ad63ff6.elementor-widget.elementor-widget-woocommerce-product-content > div > p:nth-child(1)', first = True).text
        except:
            material = "no material"

        price = r.html.find('span.woocommerce-Price-amount.amount', first = True).text
        
        product = {
            "Title": title,
            "Price": price,
            "Material": material,
        }
        
        itemsList.append(product) 

def output():
    df = pd.DataFrame(itemsList)  
    df.to_csv('negyvasEteris.csv') 
    print("Saved to CSV file") 



# data = request(url)
# parse(data)

#if url has more than one page, comment out the last two lines (data = request(url) and parse(data)) and uncomment code below

i = 1

while True:
    try:
        data = request(f'https://negyvaseteris.lt/visos-prekes/page/{i}')
        print(f'Getting items from page {i}')
        parse(data)
        print("Total: ", len(itemsList))

        i = i + 1 
    except:
        print('No more products found!')
        break

output()
