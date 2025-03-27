import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup

class EurostatScraper:
    def __init__(self):
        self.aria_getter = 'a[role="button"][aria-expanded="false"]'
        self.structure = {}
    
    def set_up_driver(self):
        """
        Imposta e restituisce un'istanza di Chrome WebDriver con opzioni personalizzate.
        """
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver

    def open_eurostat_page(self, driver):
        """
        Apre la pagina Eurostat e accetta i cookie se il popup appare.
        """
        driver.get("https://ec.europa.eu/eurostat/web/main/data/database")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "Accept all cookies")]'))
        ).click()
        print("Cookies accettati!")

    def get_category_buttons(self, navigation):
        """
        Estrae i pulsanti delle categorie da un elemento di navigazione.
        """
        return navigation.find_elements(By.CSS_SELECTOR, f'{self.aria_getter}')

    def expand_category(self, driver, nav_id, buttons):
        """
        Espande una categoria facendo clic sul pulsante corrispondente.
        """
    
        stack = []
        stacked = set()

        for b in buttons:
            bid = b.get_attribute("id")
            stack.append(b)
            stacked.add(bid)
            self.structure[nav_id][bid] = {}
            
        clicked = set()

        while stack:
            # Prendi la cartella in cima allo stack (l'ultimo aggiunto)
            current_button = stack.pop(0)
            
            span = current_button.find_element(By.TAG_NAME, 'span').text
            button_id = current_button.get_attribute("id")
                

            if button_id in clicked:
                continue
            clicked.add(button_id)

            try:

                try:
                    driver.execute_script("arguments[0].click();", current_button)
                    print(f"Categoria espansa: {span}")
                except Exception as e:
                    print(f"Errore nel cliccare sulla categoria {span}: {e}")

                time.sleep(0.1)

                shadow_host = driver.find_element(By.TAG_NAME, "navigation-full-tree")
                shadow_root = shadow_host.shadow_root
                tree = shadow_root.find_element(By.CLASS_NAME, "tree")
                children_open = tree.find_element(By.CSS_SELECTOR, "div.children.open")

                navigations = children_open.find_elements(By.XPATH, "./*")

                current_navigation = None
                for navigation in navigations:
                    a_nav = navigation.find_element(By.TAG_NAME, "a")
                    id = a_nav.get_attribute("id")

                    if id == nav_id:
                        current_navigation = navigation
                        break


                bs = current_navigation.find_elements(By.CSS_SELECTOR, f'{self.aria_getter}')
                index = 0
                for button in bs:
                        b_id = button.get_attribute("id")
                        if b_id not in stacked and b_id not in clicked:
                            stack.insert(index, button)  # Aggiungi il button all'inizio dello stack
                            index += 1

                            stacked.add(b_id)
                            self.structure[nav_id][button_id] = {b_id : b_id}
            
                print(f"Stack: {len(stack)}")
                self.save_structure_to_json()
                            

            except Exception as e:
                # Gestire eventuali permessi negati per accedere a certe cartelle
                print(f"Errore {e} {current_button}")
        

    def handle_navigation(self, driver, tree):
        """
        Gestisce la navigazione attraverso la struttura ad albero delle categorie.
        """
        children_open = tree.find_element(By.CSS_SELECTOR, "div.children.open")
        navigations = children_open.find_elements(By.XPATH, "./*")
        

        for navigation in navigations:
            a_nav = navigation.find_element(By.TAG_NAME, "a")
            nav_id = a_nav.get_attribute("id")

            self.structure[nav_id] = {}

            buttons = self.get_category_buttons(navigation)
            
            self.expand_category(driver, nav_id, buttons)

            
    # def save_full_html(self, driver):
    #     shadow_host = driver.find_element(By.TAG_NAME, "navigation-full-tree")
    #     shadow_root = shadow_host.shadow_root
    #     tree = shadow_root.find_element(By.CLASS_NAME, "tree")
    #     children_open = tree.find_element(By.CSS_SELECTOR, "div.children.open")
       
    #     html_sotto_span = children_open.get_attribute('outerHTML')

    #     # Ora puoi usare BeautifulSoup per analizzare l'HTML
    #     soup = BeautifulSoup(html_sotto_span, 'html.parser')

    #     with open("output.txt", "w", encoding="utf-8") as file:
    #         file.write(soup.prettify())

    def save_structure_to_json(self, filename="categories_structure.json"):
        """
        Salva la struttura delle categorie (self.structure) in un file JSON.
        """
        try:
            # Scrive il dizionario 'self.structure' in un file JSON
            with open(filename, "w", encoding="utf-8") as json_file:
                json.dump(self.structure, json_file, ensure_ascii=False, indent=4)
            print(f"Struttura salvata correttamente in {filename}")
        except Exception as e:
            print(f"Errore durante il salvataggio della struttura in JSON: {e}")

        
    def run(self):
        """
        Funzione principale che esegue il processo di scraping.
        """
        # Imposta il driver e apri la pagina Eurostat
        driver = self.set_up_driver()
        self.open_eurostat_page(driver)

        try:
            # Accedi alla struttura ad albero nella pagina
            shadow_host = driver.find_element(By.TAG_NAME, "navigation-full-tree")
            shadow_root = shadow_host.shadow_root
            tree = shadow_root.find_element(By.CLASS_NAME, "tree")

            # Gestisci la navigazione e l'espansione delle categorie
            self.handle_navigation(driver, tree)
            # self.save_full_html(driver)


        finally:
            # Chiudi il driver dopo l'esecuzione
            input("ciao")

if __name__ == "__main__":
    mef = EurostatScraper()
    mef.run()
