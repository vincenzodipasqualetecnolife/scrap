queue = [root_element]  # Inizializza la coda con l'elemento principale

            while queue:
                current_element = queue.pop(0)  # Prendi il primo elemento dalla coda
                
                # Trova il testo all'interno di 'span'
                try:
                    span = current_element.find_element(By.TAG_NAME, 'span').text
                    print(f"Categoria: {span}")
                except Exception as e:
                    print(f"Errore nell'estrarre il testo dal 'span': {e}")
                    continue
                
                    
                # Fai clic sul bottone
                try:
                    # driver.execute_script("arguments[0].scrollIntoView();", current_element)  # Scrolla fino al bottone
                    driver.execute_script("arguments[0].click();", current_element)  # Clicca sul bottone
                except Exception as e:
                    print(f"Errore nel cliccare sul bottone: {e}")
                    continue
                    

                time.sleep(0.25)