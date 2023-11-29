from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

servico = Service(GeckoDriverManager().install())
robo = webdriver.Firefox(service=servico)
robo.get("https://sigaa.ufpb.br/sigaa/logon.jsf")
usuario = WebDriverWait(robo,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form:login"]')))
usuario.clear()
usuario.send_keys("adriell18a")
senha = WebDriverWait(robo,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form:senha"]')))
senha.clear()
senha.send_keys("Test1234")
WebDriverWait(robo,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form:entrar"]'))).click()

robo.find_element(By.XPATH, "//*[@id='main-menu']/li[3]/a").click()
robo.find_element(By.XPATH, '//*[@id="j_id_jsp_552244886_1:consultarAcoesExtensao"]').click()

ano = WebDriverWait(robo,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="formBuscaAtividade:buscaAno"]')))
ano.clear()
ano.send_keys("2023")

robo.find_element(By.XPATH, '//*[@id="formBuscaAtividade:buscaTipoAcao"]/option[6]').click()
robo.find_element(By.XPATH, '//*[@id="formBuscaAtividade:buscaCentro"]/option[14]').click()
WebDriverWait(robo, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formBuscaAtividade:btBuscar"]'))).click()

projetos = robo.find_elements(By.XPATH, '//*[@id="listagem"]/tbody/tr')
print(len(projetos))
n = 0 
planilha = []
while n < len(projetos):
    # try:
        element = [
            f'//*[@id="listagem"]/tbody/tr[{n+1}]/td[1]',
            f'//*[@id="listagem"]/tbody/tr[{n+1}]/td[2]',
            f'//*[@id="listagem"]/tbody/tr[{n+1}]/td[2]/i',
            f'//*[@id="listagem"]/tbody/tr[{n+1}]/td[3]',
            f'//*[@id="listagem"]/tbody/tr[{n+1}]/td[4]'
        ]

        for e in element:
            planilha.append(robo.find_element(By.XPATH, e).text.replace('\n',''))

        print(n)
        n+=1
        # robo.get('https://sigaa.ufpb.br/sigaa/extensao/Atividade/lista.jsf')
    # except:
    #     print("erro")

colunas = ['codigo', 'titulo', 'coordenador', 'centro/departamento', 'situaçao']
dividindo = np.array(planilha).reshape(int(len(planilha)/5), 5)
dataframe = pd.DataFrame(data=dividindo, columns=colunas)

dataframe.to_excel('projetos cear.xlsx', index=False)

print(dataframe)
# driver.close()