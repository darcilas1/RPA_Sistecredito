from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.action_chains import ActionChains 
from dotenv import load_dotenv
import time
import pandas as pd 
import os


def login(driver, username, password):
    driver.get(os.environ.get("URL_VG"))
    driver.maximize_window()
    time.sleep(2) # Wait for the page to load

    # Enter the email
    email=driver.find_element(By.XPATH, '//*[@id="signInName"]')
    email.send_keys(username)

    # Enter the password
    password_field=driver.find_element(By.XPATH, '//*[@id="password"]')
    password_field.send_keys(password)
 
    # Click the login button
    driver.find_element(By.XPATH, '//*[@id="next"]').click() 
    time.sleep(2)

def client_management(driver, cedula):
    time.sleep(3)
    # Search for the client by cedula
    cedula_input = driver.find_element(By.XPATH, "/html/body/app-root/div/app-sc-template-commitment/app-home/app-header/div/form/div/div[1]/div[2]/app-sc-control/div/input")
    acciones = ActionChains(driver)
    #double click on the input field
    acciones.double_click(cedula_input).perform()
    time.sleep(2) 
    cedula_input.send_keys(cedula)
    time.sleep(2) 
    cedula_input.send_keys(Keys.ENTER)
    # Click the search button
    time.sleep(3) 

    # Copy the P.total value
    elements = driver.find_element(By.XPATH, "/html/body/app-root/div/app-sc-template-commitment/app-home/div/div[1]/app-table-credits/div[1]/div[1]/div/div[2]/div[2]")
    texto = elements.text.strip()

    # Clean the p.total value
    texto = texto.replace('$', '').replace(' ', '').replace('.', '') # Remove special character
    return texto



if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Get the username and password from environment variables
    username = os.environ.get("USERNAME_VG")
    password = os.environ.get("PASSWORD_VG")

    options = Options()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)


    login(driver, username, password)

    csv_path = r"C:\Users\57318\Cedulas_prueba.csv"
    df = pd.read_csv(csv_path, sep=";")

    resultados = []

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        cedula = str(row["NIT"]).strip()

        try:
            valor=client_management(driver, cedula)
        except Exception as e:
            valor=None
        resultados.append(valor)
    
    # Add the results to the DataFrame
    df["P.total"] = resultados 
    df.to_csv(csv_path, sep=";", index=False)
    print("Proceso terminado")
    driver.quit()
    