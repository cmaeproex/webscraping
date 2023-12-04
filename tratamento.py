import pandas as pd
dataF1 = pd.read_csv("base de dados\curso(2019-2022).csv")
dataF2 = pd.read_csv("base de dados\evento(2019-2022).csv")
dataF3 = pd.read_csv("base de dados\produto(2019-2022).csv")
dataF4 = pd.read_csv("base de dados\programa(2019-2022).csv")
dataF5 = pd.read_csv("base de dados\projetos(2019-2022).csv")

dataframe = pd.concat([dataF1,dataF2,dataF3,dataF4,dataF5], ignore_index=True)
# print(dataframe["situaçao"].unique())

# print(dataframe["categoria"].unique())
dataframe["funçao"] = dataframe.apply(lambda row: "DISCENTE TESTE" if "discente teste" in row["funçao"] else row["funçao"], axis=1)
dataframe["funçao"] = dataframe.apply(lambda row: "ALUNO(A) VOLUNTARIO(A)" if "VOLUNTÁRIO" in row["funçao"] else row["funçao"], axis=1)
dataframe["funçao"] = dataframe.apply(lambda row: "ALUNO(A) EM ATIVIDADE CURRICULAR" if "ATIVIDADE CURRICULAR" in row["funçao"] else row["funçao"], axis=1)
dataframe["funçao"] = dataframe.apply(lambda row: "ALUNO(A) BOLSISTA COVID-19" if "COVID" in row["funçao"] else row["funçao"], axis=1)
dataframe["funçao"] = dataframe.apply(lambda row: "ALUNO(A) BOLSISTA" if "BOLSISTA" in row["funçao"] and "COVID" not in row["funçao"] else row["funçao"], axis=1)
# # print(dataframe["funçao"].unique())
# # print(len(dataframe))
dfparticipantes = dataframe.drop_duplicates(subset={"codigo", "nome"}, keep="first", ignore_index=True)
# print(len(dfparticipantes))

dfparticipantes = dfparticipantes.loc[:,["codigo", "nome", "categoria", "funçao"]]
print(dfparticipantes)

dfsoma = pd.DataFrame()
dfparcial = pd.DataFrame()
# print(dfparticipantes["codigo"].unique().tolist())

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