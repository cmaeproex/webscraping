from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

servico = Service(GeckoDriverManager().install())
anos = [2023]

for yaer in anos:
    for j in range(2,10):
        robo = webdriver.Firefox(service=servico)
        robo.get("https://sigaa.ufpb.br/sigaa/logon.jsf")
        usuario = WebDriverWait(robo,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form:login"]')))
        usuario.clear()
        usuario.send_keys("adriell18a")
        senha = WebDriverWait(robo,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form:senha"]')))
        senha.clear()
        senha.send_keys("Aap180402")
        WebDriverWait(robo,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="form:entrar"]'))).click()

        robo.find_element(By.XPATH, "//*[@id='main-menu']/li[3]/a").click()
        robo.find_element(By.XPATH, '//*[@id="j_id_jsp_552244886_1:consultarAcoesExtensao"]').click()

        ano = WebDriverWait(robo,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="formBuscaAtividade:buscaAno"]')))
        ano.clear()
        ano.send_keys(f"{yaer}")

        
        robo.find_element(By.XPATH, f'//*[@id="formBuscaAtividade:buscaTipoAcao"]/option[1]').click()

        robo.find_element(By.XPATH, f'//*[@id="formBuscaAtividade:buscaAreaTematica"]/option[{j}]').click()
        WebDriverWait(robo, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="formBuscaAtividade:btBuscar"]'))).click()

        projetos = robo.find_elements(By.XPATH, '//*[@title="Visualizar Ação"]')
        print(len(projetos))
        n = 0 
        planilha = []
        while n < len(projetos):
            try:
                projetos[n].click()

                equipe = robo.find_elements(By.XPATH, '//*[@id="tbEquipe"]/tbody/tr')
                for i in range(0,len(equipe)):
                    element_equipe = [
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[2]/td',#codigo//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[2]/td
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[3]/td',#titulo//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[3]/td
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[4]/td[1]',#tipo da açao//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[4]/td[1]
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[5]/td[1]',#ano//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[5]/td[1]
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[6]/td',#unidade//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[6]/td
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[9]/td[2]',#area tematica//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[9]/td[2]
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[16]/td[1]',#edital//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[16]/td[1]
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[23]/td',#situaçao//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[23]/td
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[10]/td[1]',#bolsa solicitada//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[10]/td[1]
                        '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[10]/td[2]',#bolsa consedida
                        f'//*[@id="tbEquipe"]/tbody/tr[{i+1}]/td[1]',#nome//*[@id="tbEquipe"]/tbody/tr[1]/td[1]
                        f'//*[@id="tbEquipe"]/tbody/tr[{i+1}]/td[3]',#funçao
                        f'//*[@id="tbEquipe"]/tbody/tr[{i+1}]/td[2]',#categoria
                    ]

                    for e in element_equipe:
                        planilha.append(robo.find_element(By.XPATH, e).text.replace('\n',''))

                complano = robo.find_elements(By.XPATH, '//*[@id="tbDis"]/tbody/tr')
                if len(complano) != 0:
                    for i in range(0,len(complano)):
                        element_complano = [
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[2]/td',#codigo//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[2]/td
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[3]/td',#titulo//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[3]/td
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[4]/td[1]',#tipo da açao//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[4]/td[1]
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[5]/td[1]',#ano//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[5]/td[1]
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[6]/td',#unidade//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[6]/td
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[9]/td[2]',#area tematica//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[9]/td[2]
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[16]/td[1]',#edital//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[16]/td[1]
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[23]/td',#situaçao//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[23]/td
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[10]/td[1]',#bolsa solicitada//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[10]/td[1]
                            '//*[@id="j_id_jsp_188201070_4"]/table/tbody/tr[10]/td[2]',#bolsa consedida
                            f'//*[@id="tbDis"]/tbody/tr[{i+1}]/td[1]',#nome
                            f'//*[@id="tbDis"]/tbody/tr[{i+1}]/td[2]',#funçao
                        ]

                    
                        for e in element_complano:
                            if e != element_complano[10]:
                                planilha.append(robo.find_element(By.XPATH, e).text.replace('\n',''))
                            else:
                                planilha.append(robo.find_element(By.XPATH, e).text.replace('\n','').split(' - ')[1])
                        planilha.append("DISCENTE")

                print(n)
                n+=1
                robo.get('https://sigaa.ufpb.br/sigaa/extensao/Atividade/lista.jsf')
                projetos = robo.find_elements(By.XPATH, '//*[@title="Visualizar Ação"]')

            except:
                print(n, "erro")

        colunas = ['codigo', 'titulo', 'tipo da açao', 'ano', 'centro/departamento', 'area tematica', 'edital', 'situaçao', 'bolsa solicitada', 'bolsa consedida', 'nome', 'funçao', 'categoria']
        dividindo = np.array(planilha).reshape(int(len(planilha)/13), 13)
        dataframe = pd.DataFrame(data=dividindo, columns=colunas)

        dfparcial = pd.read_csv('curso(2023).csv')
        dffinal = pd.concat([dfparcial,dataframe], ignore_index=True) 

        dffinal.to_csv('curso(2023).csv', index=False)
        robo.close()