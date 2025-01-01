# InstaMart and Amazon Scraper
This project is a Python-based web scraper designed to scrape product details from Amazon and Instamart using **Selenium** and **BeautifulSoup**.

### Features
- Scrapes product names, prices, images, and URLs from Amazon and Instamart.
- Uses Selenium for navigating and scraping dynamically generated content.

### Requirements
Make sure you have the following installed:
- Python 3.x
- Selenium
- ChromeDriver (or another WebDriver depending on your browser)
    - Download ChromeDriver (or any WebDriver for the browser you use) and ensure it's in your system's `PATH`.
    - For example, you can move it to `/usr/local/bin` on macOS or add it to your environment variables in Windows.
- AWS CLI (if using DynamoDB for storing data)
- Required Python libraries:
    - `selenium`
    - `bs4` (BeautifulSoup)
    - `requests`

### Installing Requirements
1. Install required libraries:
`pip install selenium requests beautifulsoup4 boto3`

2. Download ChromeDriver for your version of Chrome:
- Go to ChromeDriver Downloads and download the version matching your browser.
- Extract the file and move it to your system path: `mv chromedriver /usr/local/bin`
- Alternatively, you can set the path in your code like: 
`driver = webdriver.Chrome(executable_path='/path/to/chromedriver')`

### Setting Up AWS Keys (For DynamoDB)
1. Install the AWS CLI (if not installed): `pip install awscli`
2. Configure your AWS credentials: `aws configure`
Enter your `AWS Access Key ID`, `AWS Secret Access Key`, region (`eu-north-1`), and output format (`json`).



### Running the Scraper
1. Edit the code to include the URL of the Amazon or Instamart page you want to scrape:
- `url = "https://www.amazon.in/s?k=sofas"  # Example for Amazon`
2. Run the scraper:
```
python3 amazon-scraper.py
python3 indiamart-scraper.py
```



