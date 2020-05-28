import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import shutil
import requests
import os

"""
Scraping du site : https://identify.plantnet.org/explo/salad/

On s'intéresse aux espèces stockées dans la variable FLOWER_URL. Le script
va prendre chacune de ces URL et va stocker toutes les images de prévisualisation
dans le dossier correspondant.

Note: on peut toujours utiliser du multiprocessing pour chaque URL avec concurrent.futures
"""

FLOWER_URL = {
    'Campanula persicifolia L.': 'https://identify.plantnet.org/species/salad/Campanula%20persicifolia%20L.',
	'Cichorium intybus L.': 'https://identify.plantnet.org/species/salad/Cichorium%20intybus%20L.' ,
    'Lepidium draba L.' :'https://identify.plantnet.org/species/salad/Lepidium%20draba%20L.',
    'Leucanthemum vulgare (Vaill.) Lam.' : 'https://identify.plantnet.org/species/salad/Leucanthemum%20vulgare%20(Vaill.)%20Lam.',
    'Malva sylvestris L.': 'https://identify.plantnet.org/species/salad/Malva%20sylvestris%20L.'
}

#Télécharge les images dans le dossier
def download_image(links):
    for i, link in enumerate(links):
        response = requests.get(link, stream=True)
        with open(f'{dirname}/img_{i}.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

# Navigue sur la page URL et récupère les images dessus
def navigate_to_images(url):
    browser.get(url)
    #Marque une pause pour que l'élément en forme d'icône de fleur soit visible
    pause = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/ul/li[2]/a/img")))
    #Clique sur l'icône fleur pour afficher les images en forme de fleur
    flower_icon = browser.find_element_by_xpath('/html/body/div/div/div/div[2]/ul/li[2]/a/img')
    flower_icon.click()

    #Marque une pause de 1:15 maximum pour que toutes les images soient disponibles
    pause = WebDriverWait(browser, 75).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR , "img.img.img-responsive.img-thumbnail")))
    
    #Capture tous les éléments web ayant une prévisualisation d'image et prend les liens
    flowers = browser.find_elements_by_css_selector("img.img.img-responsive.img-thumbnail")
    return [flower.get_attribute("src") for flower in flowers]

# Définit le navigateur sur Firefox par défaut
browser = webdriver.Firefox()

#Itère sur chacun des noms et des liens
for name, url in FLOWER_URL.items():

    #Crée un nouveau répertoire pour stocker les images si il n'existe pas
    dirname = "../training_data/raw/" + name.replace(" ", "_").replace(".","")
    if not os.path.exists(dirname):
        os.makedirs(dirname)

        img_links = navigate_to_images(url)

        download_image(img_links)
    else:
        img_links = navigate_to_images(url)
        #Vérifie si toutes les images sont là, sinon itère sur le reste
        if len(os.listdir(dirname)) < len(img_links):
            img_links = img_links[len(os.listdir(dirname)):]
            download_image(img_links)

# ferme le navigateur
browser.close()