import hashlib
import uuid
import time
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ScrapedProducts_IndiaMart')

# Define a function to generate a unique ProductID
def generate_product_id(product_url):
    """Generate a unique ProductID using a hash of the product URL or UUID."""
    if product_url != 'No URL':
        return hashlib.sha256(product_url.encode('utf-8')).hexdigest()
    else:
        return str(uuid.uuid4())  # Generate a UUID if no product URL is found

# Set up Chrome options
options = Options()
options.add_argument('--headless')  # Run in headless mode (no GUI)
options.add_argument('--no-sandbox')  
options.add_argument('--disable-dev-shm-usage')

# Set up the Chrome WebDriver
service = Service('/usr/local/bin/chromedriver')  # Update this path to your ChromeDriver
driver = webdriver.Chrome(service=service, options=options)

# Directly open a specific IndiaMART category page
# url = 'https://dir.indiamart.com/search.mp?ss=sofa&search_type=p&src=adv-srch&q-frame-material=wooden&q-seat-material=cotton&q-primary-color=grey&q-usage-application=living+room&q-cushion-included=yes&cq_src=city-search&cq=gurgaon&biz=40&pr=1&v=4&mcatid=&catid=&ecom_only=true&tags=cq:gurgaon|biz:40|stype:attr=1|qr_nm:gd|res:RC2|com-cf:nl|ptrs:na|ktp:N0|mc:29124|mtp:G|qry_typ:P|lang:en|wc:1|cs:10575'
url = 'https://www.indiamart.com/proddetail/mayfair-grey-2-seater-chesterfield-sofa-2853503288333.html?pos=1&kwd=sofa&tags=BA||Pref||175.18976|Price|product||gurgaon|MDC|rsf:gd-|-cq:gurgaon|biz:40|stype:attr=1|qr_nm:gd|res:RC2|com-cf:nl|ptrs:na|ktp:N0|mc:29124|mtp:G|qry_typ:P|lang:en|wc:1|cs:10575|v=4'
driver.get(url)

# Allow the page to load
time.sleep(5)  # Wait for the page to load; adjust if necessary

# Locate the product cards on the page
try:
    products = driver.find_elements(By.CLASS_NAME, 'ecomCard')  # First attempt with 'ecomCard'
except:
    print("No products found with 'ecomCard'. Trying 'sfirst'...")

if not products:
    try:
        products = driver.find_elements(By.CLASS_NAME, 'sfirst')  # Second attempt with 'sfirst'
    except:
        print("No products found with 'sfirst'. Exiting...")
        driver.quit()

# List to store product details
product_details = []

# Loop through each product and extract details
for product in products:

    # Try to find the product name from various possible locations
    try:
        name_element = product.find_element(By.CLASS_NAME, 'producttitle').find_element(By.TAG_NAME, 'a')
    except:
        try:
            name_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.bo.center-heading")))
        except:
            print("Product name not found")
            continue

    name = name_element.text

    # Try to find the product price from various possible locations
    try:
        price_element = product.find_element(By.CLASS_NAME, 'price')
        price = price_element.text
    except:
        try:
            price_element = WebDriverWait(driver, 10).until( EC.visibility_of_element_located((By.CLASS_NAME, 'price-unit')) )  # New class for <span>
            price = price_element.text
        except:
            print(f"Price not found for {name}")
            price = "N/A"

    # Try to find the product image from various possible locations
    try:
        image_element = product.find_element(By.CLASS_NAME, 'productimg')
        image_url = image_element.get_attribute('src')
    except:
        try:
            image_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//img[contains(@class, 'img-drift-demo-trigger')]")))  # New class for <img>
            image_url = image_element.get_attribute('src')
        except:
            print(f"Image not found for {name}")
            image_url = "N/A"

    # Extract product URL
    product_url = name_element.get_attribute('href')
    if not product_url:  # If href is None or empty, use the current URL
        product_url = url
    
    # Insert each product into DynamoDB
    try:
        table.put_item(
            Item={
                'ProductID': generate_product_id(product_url),  # Generate unique ProductID
                'name': name,
                'price': price,
                'image_url': image_url,
                'product_url': product_url
            }
        )
        print(f"Product {name} inserted into DynamoDB successfully.")
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f"Credentials error: {str(e)}")
    except Exception as e:
        print(f"Error inserting {name} into DynamoDB: {str(e)}")


# Close the driver
driver.quit()
