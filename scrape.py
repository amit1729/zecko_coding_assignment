import requests
import json
import csv
# defining the api-endpoint 
COLLECTIONS_API_ENDPOINT = "https://prod.api.sugarcosmetics.com/collections/prod/getCollectionv2"
PRODUCT_API_ENDPOINT = "https://prod.api.sugarcosmetics.com/products/prod/getProductsv2?handle={}"
# your API key here
COLLECTION_HANDLES = ["makeup","blend-trend-makeup-brush", "skin-care-products"]

# data to be sent to api

SCRAPED_DATA = [["Title","Body","Vendor","Price","MRP","Images","Product","URL"]]
PRODUCT_URL = "https://in.sugarcosmetics.com/products/{}"
print("Scraper initiated....")
for handle in COLLECTION_HANDLES:
  data = {
    'collection_handle': handle,
    'count': 1,
    'filter': {},
    'skip': 0,
    'sort': "relevance"
  }
  r = requests.post(url = COLLECTIONS_API_ENDPOINT, data = json.dumps(data))
  no_of_items = r.json()["resbody"]["total_count"][0]
  data['count'] = no_of_items
  resp = requests.post(url = COLLECTIONS_API_ENDPOINT, data = json.dumps(data)).json()
  print(data["collection_handle"])
  print("\n")
  for result in resp["resbody"]["result"]:
    lis = []
    # print(result["handle"], "| ", result["product_price"])
    print(result["handle"])
    handle = result["handle"]
    product_details = requests.get(url = PRODUCT_API_ENDPOINT.format(handle)).json()
    if(product_details["statusId"] == 0):
      continue
    lis.append(product_details["resbody"]["title"])
    lis.append(product_details["resbody"]["body_html"])
    lis.append(product_details["resbody"]["vendor"])
    lis.append(result["product_price"])
    lis.append(result["product_price"])
    image_urls = product_details["resbody"]["image"]["src"]
    for img in product_details["resbody"]["images"]:
      image_urls+= "\n"+ img["src"]
    lis.append(image_urls)
    lis.append(PRODUCT_URL.format(handle))
    SCRAPED_DATA.append(lis)

print("Scraping Completed......")
print("Writing into a csv file....")
with open("scraped_data.csv", "w",encoding='UTF8', newline="") as f:
  writer = csv.writer(f)
  writer.writerows(SCRAPED_DATA)
print("Done....")