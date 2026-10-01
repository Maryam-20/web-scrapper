import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import random
import urllib3
from bs4 import BeautifulSoup
import time


class BookScrapper:
    def __init__(self, base_url, no_of_pages_to_scrape):
        os.environ["PATH"] +=  r"C:\\Users\\Hp\Downloads\\chromedriver-win64"
        self.driver = webdriver.Chrome()
        self.base_url = base_url
        
        self.no_of_pages_to_scrape = no_of_pages_to_scrape

        book_info = {}
        self.book_info = book_info
        
        product_info = {}
        self.product_info = product_info
        
        pages_info = {}
        self.pages_info = pages_info
        
        self.nextPage_count = 1
        
        # Scrapping the current page loaded
    def current_page(self):  
        page_no_element = self.driver.find_element(By.CSS_SELECTOR, "li.current") 
        page_no = page_no_element.text
        print("Scraping ",page_no)
        
        container_element = self.driver.find_element(By.CSS_SELECTOR, "ol.row")
        list_items = container_element.find_elements(By.TAG_NAME, "li")
        
        for index in range(len(list_items)):
            current_list = list_items[index]
            image_link = current_list.find_element(By.CSS_SELECTOR, "div.image_container a")
            if image_link:
                image_link.click()
                wait = WebDriverWait(self.driver, 120)
                ul_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.breadcrumb")))
                li_element = ul_element.find_elements(By.TAG_NAME, "li")
                if len(li_element) >= 3:
                    book_category = li_element[2].text
                    
                book_title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product_main h1")))
                book_title = book_title_element.text
                
                book_price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product_main p.price_color")))
                book_price = book_price_element.text
                
                book_stockStatus_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product_main p.instock.availability")))
                book_stockStatus  = book_stockStatus_element.text
                
                book_productDescription_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "article.product_page p ")))
                book_productDescription = book_productDescription_element.text
                
                product_info_rows =  wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tr")))
                for product_info_row in product_info_rows:
                    column_th = product_info_row.find_element(By.TAG_NAME, "th").text
                    column_td = product_info_row.find_element(By.TAG_NAME, "td").text
                    self.product_info.update({column_th:column_td})
                    
                self.book_info.update({index + 1: {"Book Name": book_title, "Price":book_price, "Stock Status": book_stockStatus, "Description":book_productDescription, "Product Infomation": self.product_info, "Category": book_category}})
                self.pages_info.update({page_no:self.book_info})
                print(f"Scraped Data for item {index + 1} on  {page_no[:6]} ") #: Dtype of page_no = {type(page_no)}

            self.driver.back()
        
        self.nextPage_count += 1
        if self.nextPage_count <= 5:
            self.nextPage(nextPage_count = 1 + self.nextPage_count)
        else:
            print("Done Scrapping the five pages")
            self.stop_driver()
            
    def nextPage(self, nextPage_count ):
        nextPage_count = self.nextPage_count
        try:
            wait = WebDriverWait(self.driver, 420)
            format_url = self.base_url.format(nextPage_count)
            url = self.driver.get(format_url)
            
            self.current_page()
            
        except Exception as e:
            print("No more Next Page to scrape or an error occured", e)
        
        # Scrapping initiation
    def start_scrapping(self, num):
        format_url = self.base_url.format(num)
        url = self.driver.get(format_url)
        self.current_page()
        
        # Stop Driver after all pages have been scraped
    def stop_driver(self):
        
        self.driver.quit()
        print(self.pages_info)
                
# Scrapping 10 distinct quote(Different quote scrapped from different Pages)                
class QuoteScrapper:
    def __init__(self, base_url):
        os.environ["PATH"] +=  r"C:\\Users\\Hp\Downloads\\chromedriver-win64"
        
        self.base_url = base_url
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 120)
        self.quote_info = []
        self.details = {}
       
        
    def scrapping_cuurent_div(self):
        quote_element = current_div_to_scrape.find_element(By.CSS_SELECTOR, "div.quote span.text")
        quote = quote_element.text
        
        name_element = current_div_to_scrape.find_element(By.CSS_SELECTOR, "div.quote small.author")
        name = name_element.text
        
        about_element = current_div_to_scrape.find_element(By.CSS_SELECTOR, "div.quote a")
        about = about_element.text
        
        if about_element:
            about_element.click()
            wait = WebDriverWait(self.driver, 120)
            
            dob_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.author-details span.author-born-date")))
            dob  = dob_element.text 
            
            nationality_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.author-details span.author-born-location")))
            nationality = nationality_element.text
            
            description_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.author-description")))
            description = description_element.text 
            self.details.update({"name":name, "quote": quote, "Date of Birth": dob, "Nationality": nationality, "Description":description[:20]})
            print(self.details)
        self.quote_info.append({f"page{random_no}":self.details})
                    
        
    def start_scrapping(self):
        generated_numbers = set()
        i = 1
        while len(self.quote_info) <= 10:
            if len(self.quote_info) == 10:
                break
            else:
                global random_no
                random_no = random.randint(1, 10)
                if random_no in generated_numbers:
                    print(f"Number {random_no} is already in the set!  Skipping iteration: ", i)
                    continue
                generated_numbers.add(random_no)
                try:
                    print("Going for the iteration", i)
                    
                    print("Scrapping from page", random_no)
                    format_url = self.base_url.format(random_no)
                    url = self.driver.get(format_url)
                    container = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "col-md-8")))
                    container_items = self.driver.find_elements(By.CSS_SELECTOR, "div.quote")
                    
                    print(f"Found {len(container_items)} quotes.")
                    container_items_no = random.randint(1, len(container_items))
                    print(container_items_no)
                    
                    
                    global current_div_to_scrape
                    current_div_to_scrape = container_items [container_items_no]
                   
                    if current_div_to_scrape:
                        try:
                            self.scrapping_cuurent_div()
                        except Exception as e:
                            print("EEEEOORR", e)
                    i +=1
                except Exception as err:
                   print("errororrnvmn", err)
        
        print(self.quote_info) 
    
    
    
# Scrapping Random Page on Wikipedia  Based on the random generated word        
class RandomScrapper():
    def __init__(self, url):
        pass
        self.driver = webdriver.Chrome()
        self.url = url
        
    def wait_for_page_load(self, timeout=30):
        try:
            # Wait for the presence of an element that indicates the page has loaded
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            print("Page loaded successfully!")
        except TimeoutError:
            print("Page load timed out!")
            
    def get_random_word(self):
        try:
            word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
            open_word_site = urllib3.request("GET", word_site)
            response_status  = open_word_site.status
            if response_status == 200:
                response_data = open_word_site.data
                decoded_data = response_data.decode("utf-8")
                word_list =  decoded_data.split("\n")
                random_word = random.choice(word_list)
                return random_word
            else:
                print("Failed to fetch word. Status Code:", response_status)
        except Exception as e:
            print("Error occured while fetching word:", e)
            
    def scrape_page(self):
        page_source = self.driver.page_source  
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Extracting all text in the page
        all_text = soup.get_text(strip=True)
        print("All infomation about ", random_word,  ":", "\n",  all_text) 
        
        
    def scrape(self):
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 20)
        try:
            global random_word
            random_word = self.get_random_word()
            print("Random word to search: ", random_word )
            search_bar = wait.until(EC.presence_of_element_located((By.ID, "searchInput")))
            search_bar.send_keys(random_word)
            search_bar.send_keys(Keys.RETURN)
            self.wait_for_page_load()
            
            self.scrape_page()
            
        except Exception as e:
            print("Error occured during scrapping", e)
        finally:
            self.driver.quit()
            

if __name__ == "__main__":
    action = input("What do you want to scrape: Book or Quote or Random?: \n")
    if action == "book".lower():
        scrapper = BookScrapper(base_url= "http://books.toscrape.com/catalogue/page-{}.html" , no_of_pages_to_scrape= 5)
        scrapper.start_scrapping(num=1)
        
    elif action.lower() == "quote":
        quote_scrappper = QuoteScrapper(base_url= "https://quotes.toscrape.com/page/{}/")
        quote_scrappper.start_scrapping()
        input("Press Enter to close the browser...")
        
    elif action.lower() == "random":
        random_scrapper = RandomScrapper(url= "https://www.wikipedia.org/")
        random_scrapper.scrape()
        
    else:
        print("Operation Error")

# input("Press Enter to close the browser...")