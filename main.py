import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class EurostatScraper:
    
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
        return navigation.find_elements(By.CSS_SELECTOR, 'a[role="button"][aria-expanded="false"]')

    def expand_category(self, driver, button):
        """
        Espande una categoria facendo clic sul pulsante corrispondente.
        """
    
        stack = [button]

        while stack:
            # Prendi la cartella in cima allo stack (l'ultimo aggiunto)
            current_button = stack.pop()    
            try:

                try:
                    span = current_button.find_element(By.TAG_NAME, 'span').text
                    driver.execute_script("arguments[0].click();", button)
                    print(f"Categoria espansa: {span}")
                except Exception as e:
                    print(f"Errore nel cliccare sulla categoria {span}: {e}")


                shadow_host = driver.find_element(By.TAG_NAME, "navigation-full-tree")
                shadow_root = shadow_host.shadow_root
                tree = shadow_root.find_element(By.CLASS_NAME, "tree")
                children_open = tree.find_element(By.CSS_SELECTOR, "div.children.open")
                navigations = children_open.find_elements(By.XPATH, "./*")


                # Elenco degli elementi nella cartella corrente
                for navigation in navigations:
                    if navigation:  # Se è una cartella, aggiungila allo stack
                        buttons = navigation.find_elements(By.CSS_SELECTOR, 'a[role="button"][aria-expanded="false"]')
                        for button in buttons:
                            stack.append(button)  # Aggiungi la cartella allo stack per esplorarla dopo
                    else:  # Se è un file, lo stampiamo (o lo gestiamo come necessario)
                        print(f" - Navigation category non trovata")
            except PermissionError:
                # Gestire eventuali permessi negati per accedere a certe cartelle
                print(f"Permesso negato per accedere a: {current_button}")

    def handle_navigation(self, driver, tree):
        """
        Gestisce la navigazione attraverso la struttura ad albero delle categorie.
        """
        children_open = tree.find_element(By.CSS_SELECTOR, "div.children.open")
        navigations = children_open.find_elements(By.XPATH, "./*")
        
        for navigation in navigations:
            buttons = self.get_category_buttons(navigation)
            
            for button in buttons:
                self.expand_category(driver, button)

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

        finally:
            # Chiudi il driver dopo l'esecuzione
            driver.quit()

if __name__ == "__main__":
    mef = EurostatScraper()
    mef.run()
