import pandas as pd
dataF1 = pd.read_csv("base de dados\curso(2019-2022).csv")
dataF2 = pd.read_csv("base de dados\evento(2019-2022).csv")
dataF3 = pd.read_csv("base de dados\produto(2019-2022).csv")
dataF4 = pd.read_csv("base de dados\programa(2019-2022).csv")
dataF5 = pd.read_csv("base de dados\projetos(2019-2022).csv")
dataF6 = pd.read_csv("cursos(2023).csv")
dataF7 = pd.read_csv("evento(2023).csv")
dataF8 = pd.read_csv("produto(2023).csv")
dataF9 = pd.read_csv("programa(2023).csv")
dataF10 = pd.read_csv("projetos(2023).csv")

dataframe = pd.concat([dataF1,dataF6,dataF2,dataF7,dataF3,dataF8,dataF4,dataF9,dataF5,dataF10], ignore_index=True)

dataframe["funçao"] = dataframe.apply(lambda row: "DISCENTE TESTE" if "discente teste" in row["funçao"] else row["funçao"], axis=1)
dataframe["funçao"] = dataframe.apply(lambda row: "ALUNO(A) VOLUNTARIO(A)" if "VOLUNTÁRIO" in row["funçao"] else row["funçao"], axis=1)
dataframe["funçao"] = dataframe.apply(lambda row: "ALUNO(A) EM ATIVIDADE CURRICULAR" if "ATIVIDADE CURRICULAR" in row["funçao"] else row["funçao"], axis=1)
dataframe["funçao"] = dataframe.apply(lambda row: "ALUNO(A) BOLSISTA COVID-19" if "COVID" in row["funçao"] else row["funçao"], axis=1)
dataframe["funçao"] = dataframe.apply(lambda row: "ALUNO(A) BOLSISTA" if "BOLSISTA" in row["funçao"] and "COVID" not in row["funçao"] else row["funçao"], axis=1)
dfparticipantes = dataframe.drop_duplicates(subset={"codigo", "nome"}, keep="first", ignore_index=True)

dfparticipantes = dfparticipantes.loc[:,["codigo", "nome", "categoria", "funçao"]]
# print(dfparticipantes)

dfsoma = pd.DataFrame()
dfparcial = pd.DataFrame()

for id in dfparticipantes["codigo"].unique().tolist():
    df1 = dfparticipantes[dfparticipantes["codigo"] == id]
    dfsoma["codigo"] = [id]

    for categoria in sorted(dfparticipantes["categoria"].unique().tolist()):
        df2 = df1[df1["categoria"] == categoria]
        dfsoma[f"{categoria}"] = [len(df2)]

    for funçao in sorted(dfparticipantes["funçao"].unique().tolist()):
        df2 = df1[df1["funçao"] == funçao]
        dfsoma[f"{funçao}"] = [len(df2)]

        if funçao == "COORDENADOR(A)" and len(df2) != 0:
            dfsoma["NOME COORDENADOR(A)"] = df2["nome"].tolist()[0]
        elif funçao == "COORDENADOR(A)" and len(df2) == 0:
            dfsoma["NOME COORDENADOR(A)"] = "S/COORDENADOR(A)"

    dfparcial = pd.concat([dfparcial,dfsoma], ignore_index=True)
    print(dfparcial)

dataframeprojetos = dataframe.loc[:,['codigo', 'titulo', 'tipo da açao', 'ano', 'centro/departamento', 'area tematica', 'edital', 'situaçao', 'bolsa solicitada', 'bolsa consedida']]
dataframeprojetos = dataframe.drop_duplicates(subset={"codigo"}, ignore_index=True)

dffinal = dataframeprojetos.merge(dfparcial, on="codigo")
print(dffinal)
dffinal.to_excel("EXTENSÃO.xlsx", index=False)
print(dffinal)