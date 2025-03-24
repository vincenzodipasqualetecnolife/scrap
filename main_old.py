import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import json



class EurostatScraper:
    
    def set_up_chrome_options(self):
        options = ChromeOptions()
        options.add_argument('--no-sandbox')  # Disable sandbox to avoid issues with ChromeDriver
        options.add_argument('--disable-gpu')  # Disable GPU to avoid issues with ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
    def search_url_mef(self, driver):
        driver.get("https://ec.europa.eu/eurostat/web/main/data/database")
        time.sleep(2)
        try:
    # Attendere che il popup dei cookie sia visibile
            cookie_button = driver.find_element(By.XPATH, '//a[contains(text(), "Accept all cookies")]')
            cookie_button.click()
            print("Cookie accettati!")
        except Exception as e:
            print("Nessun popup per i cookie trovato:", e)
        # Attendere fino a quando il primo div è visibile
        try:
            shadow_host = driver.find_element(By.TAG_NAME, "navigation-full-tree")
            
            shadow_root = shadow_host.shadow_root
            tree = shadow_root.find_element(By.CLASS_NAME, "tree")
        except Exception as e:
            print(f"Errore nel trovare il div iniziale: {e}")
            return

        children_open = tree.find_element(By.CSS_SELECTOR, "div.children.open")
        print("Trovato il div principale",children_open)

        time.sleep(1)

        self.open_folder(children_open)
    

    def open_folder(self, children_open):
        navigations = children_open.find_elements(By.XPATH, "./*")

        # structure = {}

        for navigation in navigations:
            nav_buttons = navigation.find_elements(By.CSS_SELECTOR, 'a[role="button"][aria-expanded="false"]')
            # nav_name = navigation.find_element(By.TAG_NAME, 'span').text

            # hello = []
            # for i in range(len(nav_buttons)):
            #     hello.append("ciao")

            # structure[f"{nav_name}_button"] = hello

            self.expand_all_categories(driver, nav_buttons)
        
        # #Sceivi questa structurei n un file txt
        # with open("structure.json", "w", encoding="utf-8") as json_file:
        #     # Convertiamo il dizionario in JSON e lo scriviamo nel file
        #     json.dump(structure, json_file, ensure_ascii=False, indent=4)


    def expand_all_categories(self, driver, buttons):
        
        for button in buttons:            
            current_button = button
            
            # Trova il testo all'interno di 'span'
            try:
                span = current_button.find_element(By.TAG_NAME, 'span').text
                print(f"Categoria: {span}")
            except Exception as e:
                print(f"Errore nell'estrarre il testo dal 'span': {e}")
                continue
            
                
            # Fai clic sul bottone
            try:
                # driver.execute_script("arguments[0].scrollIntoView();", current_element)  # Scrolla fino al bottone
                driver.execute_script("arguments[0].click();", current_button)  # Clicca sul bottone
            except Exception as e:
                print(f"Errore nel cliccare sul bottone: {e}")
                continue
            
            shadow_host = driver.find_element(By.TAG_NAME, "navigation-full-tree")
            shadow_root = shadow_host.shadow_root
            tree = shadow_root.find_element(By.CLASS_NAME, "tree")
            children_open = tree.find_element(By.CSS_SELECTOR, "div.children.open")

            time.sleep(0.25)

            self.open_folder(children_open)              
        return
        


            
if __name__ == "__main__":
    mef = EurostatScraper()
    driver = mef.set_up_chrome_options()
    mef.search_url_mef(driver)
    input("Ciao")
   