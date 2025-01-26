import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CarScraper:
    def __init__(self, headless=True):
        self.options = uc.ChromeOptions()
        if headless:
            self.options.add_argument('--headless')  
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.driver = uc.Chrome(options=self.options)
        
    def open_page(self, url):
        """Ouvre une page et attend que le contenu soit chargé."""
        self.driver.get(url)
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "ListItem_wrapper__TxHWu"))
        )
    
    def extract_car_links(self, page_number):
        """Extrait les liens des voitures d'une page donnée."""
        website = f"https://www.autoscout24.be/fr/lst?atype=C&cy=B&desc=0&page={page_number}&search_id=a5i2bcp2m1&sort=standard&source=listpage_pagination&ustate=N%2CU"
        self.open_page(website)
        cars_sections = self.driver.find_elements(By.CLASS_NAME, "ListItem_wrapper__TxHWu")
        links = []
        for car in cars_sections:
            try:
                link_car = WebDriverWait(car, 30).until(
                    EC.presence_of_element_located((By.XPATH, './/a'))
                )
                car_url = link_car.get_attribute('href')
                links.append(car_url)
            except Exception as e:
                print(f"Erreur lors de la récupération du lien de la voiture : {e}")
        return links
    
    def extract_car_details(self, car_url):
        """Extrait les détails d'une voiture donnée."""
        self.driver.get(car_url)

        #CarNAME
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "StageTitle_boldClassifiedInfo__sQb0l"))
        )
        CarName = self.driver.find_element(By.CLASS_NAME, "StageTitle_boldClassifiedInfo__sQb0l")

        #CarModele
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]/span[2]'))
        )
        CarModele = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[1]/div[2]/h1/div[1]/span[2]')

        #CarPrice
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'PriceInfo_price__XU0aF'))
        )
        CarPrice = self.driver.find_element(By.CLASS_NAME, 'PriceInfo_price__XU0aF')
        #CareEtat
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[3]/div[2]/div/div'))
        )
        CarEtat = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[2]/div[3]/div[2]/div/div')
        #Options
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'StageTitle_modelVersion__Yof2Z'))
        )
        CarOptions = self.driver.find_element(By.CLASS_NAME, 'StageTitle_modelVersion__Yof2Z')
        #Miliage
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[1]/div[4]'))
        )
        CarMil = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[1]/div[4]')
        #Transmission
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[2]/div[4]'))
        )
        CarTra = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[2]/div[4]')
        #Annee
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[3]/div[4]'))
        )
        CarAnnee = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[3]/div[4]')
        #Carbu
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[4]/div[4]'))
        )
        CarCarbu = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[4]/div[4]')
        #Puissance
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[5]/div[4]'))
        )
        CarPui = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[5]/div[4]')
        #Vendeuer
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[6]/div[4]'))
        )
        CarV = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div[3]/div[3]/div/div[6]/div[4]')


        return CarName.text, CarModele.text, CarPrice.text, CarEtat.text, CarOptions.text, CarMil.text, CarTra.text, CarAnnee.text, CarCarbu.text, CarPui.text, CarV.text

    
    def close(self):
        """Ferme le navigateur."""
        self.driver.quit()

def main():
    scraper = CarScraper()

    try:
        i = 1
        while True:
            car_links = scraper.extract_car_links(i)
            print(f"Nombre de voitures sur la page {i} : {len(car_links)}")
            
            for car_url in car_links:
                try:
                    print(f"Accès à la page de la voiture : {car_url}")
                    car_name, carModele, CarPrice , Etat, Options, Milieage , Tran, Annee, CarCar, CarPui, CarVen= scraper.extract_car_details(car_url)
                    print(f"Nom de la voiture : {car_name}")
                    print(f"Modele de la voiture : {carModele}")
                    print(f"Price de la voiture : {CarPrice}")
                    print(f"Etat de la voiture : {Etat}")
                    print(f"Options de la voiture : {Options}")
                    print(f"Miliage de la voiture : {Milieage}")
                    print(f"Transmission de la voiture : {Tran}")
                    print(f"Annee de la voiture : {Annee}")
                    print(f"Carburant de la voiture : {CarCar}")
                    print(f"Puissance de la voiture : {CarPui}")
                    print(f"Vendeur de la voiture : {CarVen}")
                except Exception as e:
                    print(f"Erreur lors de la récupération des informations de la voiture : {e}")
            i += 1

    except Exception as e:
        print(f"Erreur générale : {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()
