# import selenium
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
# import time
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# class Mef():
#     def __init__(self):
#         pass

#     def set_up_chrome_options(self):
#         options = ChromeOptions()
#         options.add_argument('--no-sandbox')  # Disable sandbox to avoid issues with ChromeDriver
#         options.add_argument('--disable-gpu')  # Disable GPU to avoid issues with ChromeDriver
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#         return driver
    
#     def search_url_mef(self,driver):
#         driver.get("https://ec.europa.eu/eurostat/web/main/data/database")
#         driver.implicitly_wait(5)  

#         try:
#             time.sleep(5)
            
#             shadow_host = driver.find_element(By.TAG_NAME, "navigation-full-tree")
            
#             shadow_root = shadow_host.shadow_root
#             divisione = shadow_root.find_element(By.CLASS_NAME, "tree")

#             divi = divisione.find_element(By.CSS_SELECTOR, "div.children.open")
#             navigate = divisione.find_elements(By.TAG_NAME, 'navigation-category')
#             for i in navigate:
#                 while navigate_new:
#                     buttons = i.find_elements(By.CSS_SELECTOR, 'a[role="button"][aria-expanded="false"]')
#                     for b in buttons:
#                         b.click()
#                         navigate_new = b.find_elements(By.TAG_NAME, 'navigation-category')
#                         for j in navigate_new:
#                             buttons_new = i.find_elements(By.CSS_SELECTOR, 'a[role="button"][aria-expanded="false"]')
#                             for b in buttons:
#                                 b.click()

#             if not divi:
#                 divi = navigate.find_elements(By.CSS_SELECTOR, "div.children")
#                 print("divi",divi)
            
#             buttons = i.find_elements(By.CSS_SELECTOR, 'a[role="button"][aria-expanded="false"]')


#                 # Esegui il clic su ciascun bottone in sequenza
#                 for button in buttons:
#                     try:
#                         # Fai clic sul bottone
#                         button.click()
#                         divi = i.find_elements(By.TAG_NAME, "div")
#                         print("divi",divi)
#                         buttons = i.find_elements(By.CSS_SELECTOR, 'a[role="button"][aria-expanded="false"]')
#                         # Attendi un momento per permettere l'espansione
#                         time.sleep(2)  # Puoi regolare il tempo di attesa in base alla tua pagina
#                     except Exception as e:
#                         print(f"Errore durante il clic sul bot:",e)

#             title = div_elements.find_element(By.CSS_SELECTOR, "span.tree-title.full-tree-title1").text
#             print(div_elements)
#             print("TITOLO:", title)
#         except Exception as e:
#             print("Errore:", e)

        
# if __name__ == "__main__":
#     mef = Mef()
#     driver = mef.set_up_chrome_options()
#     mef.search_url_mef(driver)
#     driver.quit()

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

class EurostatScraper:
    
    def set_up_chrome_options(self):
        options = ChromeOptions()
        options.add_argument('--no-sandbox')  # Disable sandbox to avoid issues with ChromeDriver
        options.add_argument('--disable-gpu')  # Disable GPU to avoid issues with ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
    def search_url_mef(self, driver):
        driver.get("https://ec.europa.eu/eurostat/web/main/data/database")
        driver.implicitly_wait(5)
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
            divisione = shadow_root.find_element(By.CLASS_NAME, "tree")

            div_principale = divisione.find_element(By.CSS_SELECTOR, "div.children.open")
            print("Trovato il div principale",div_principale)
        except Exception as e:
            print(f"Errore nel trovare il div iniziale: {e}")
            return

        # Trova le categorie di navigazione principali
        navigation_categories = divisione.find_elements(By.TAG_NAME, 'navigation-category')

        # Espandere tutte le categorie
        for category in navigation_categories:
            self.expand_all_categories(driver, category)

    def expand_all_categories(self, driver, root_element):
        queue = [root_element]  # Inizializza la coda con l'elemento principale

        while queue:
            current_element = queue.pop(0)
            span = current_element.find_element(By.TAG_NAME, 'span').text
            print("Elemento 0", span)
            buttons = current_element.find_elements(By.CSS_SELECTOR, 'a[role="button"][aria-expanded="false"]')
            for button in buttons:
                try:
                    spans = button.find_element(By.TAG_NAME, 'span').text

                    print(f"Testo nel bottone: {spans}")

                except Exception as e:
                    print(f"Errore nell'estrarre il testo dal bottone: {e}")
            for button in buttons:
                spans = button.find_element(By.TAG_NAME, 'span').text

                print(f"Testo nel bottone: {spans}")
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", button)  # Scorri fino al bottone
                    try:
                        driver.execute_script("arguments[0].click();", button)

                    except Exception as e:
                        print(f"Errore durante il click sul bottone: {e}")
                    
                    # Attendi fino a quando i nuovi elementi appaiono
                    WebDriverWait(driver, 0.5).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'navigation-category'))
                    )

                    # Dopo il clic, cerchiamo se ci sono nuove categorie visibili
                    new_categories = driver.find_elements(By.TAG_NAME, 'navigation-category')  # Cerca globalmente
                    for new_categorie in new_categories:
                        queue.extend(new_categorie)
                    # Aggiungiamo le nuove categorie alla coda per esplorazione futura
                    
                    print(f"Espanso {len(new_categories)} nuove categorie")

                except Exception as e:
                    print(f"Errore cliccando sul bottone: {e}")

            
if __name__ == "__main__":
    mef = EurostatScraper()
    driver = mef.set_up_chrome_options()
    mef.search_url_mef(driver)
   