import requests
import pandas as pd
import json
from conexionBD import conexionBD


##### requestApi trae la data desde la API y la caga en un DF
def requetApi(url):
    link = url
    data = requests.get(link)

    titulo = []
    episodios = []
    tipo = []
    estado = []
    conn = conexionBD()
    diccionario = {}
    try:
        if data.status_code == 200:
            data = data.json()
            for e in data['data']:
                titulo.append(str(e['title']))
                episodios.append(str(e['episodes']))
                tipo.append(str(e['status']))
                estado.append(str(e['status']))            

            diccionario['Titulo_Anime'] = titulo
            diccionario['Episodios'] = episodios
            diccionario['tipo'] = tipo
            diccionario['estado'] = estado

            data = pd.DataFrame.from_dict(diccionario)
            data.to_csv('listaanime.csv', sep  = ',',header=True, encoding='UTF-8')

            #df = pd.read_csv('listaanime.csv').to_sql('lista_anime', conn, if_exists= 'replace', index= False)
        else:
            data

        return data
    except Exception as e:
        print(e)


##### queryRDS busca, inserta y actualiza los datos de una tabla
def queryRDS(query, tipo):
    response = []
    try:
        conexion = conexionBD()
        cursor = conexion.cursor()

        if tipo == 'select':        
                cursor.execute(query)
                response = cursor.fetchone()
                cursor.close()

        elif tipo == 'insert':
                cursor.execute(query)
                cursor.close()
                response = 'Inserto datos Exitosamente'

        elif tipo == 'update':
                cursor.execute(query)
                cursor.close()
                response = 'Actualizo datos Exitosamente'
        else:
            print('Accion no Valida')

    except Exception as e:
        response = 'Error aca'+ str(e)

    return response


##### insertData inserta o actualiza la data en la base de datos
def insertData(tabla):
    data = tabla
    Q = data['Titulo_Anime'].count()

    for i in range(Q):
        result = ''
        columnas = []
        columnas1 = data.columns.values
        columnas = ','.join(columnas1)
        valores = []
        fila =  list(data.iloc[i])

        for item in fila:
                valores.append("'"+str(item)+"'")

        valores = ','.join(map(str, valores))

        selectData = f'''select Titulo_Anime from public.lista_anime
                        where Titulo_Anime = '{fila[0]}' '''

        ##############################################################
        #### se valida si el dato existe en la tabla, si no existe se inserta en la BD
        if queryRDS(selectData,'select') == None:
            insertData = f''' insert into public.lista_anime({(columnas)})
                                                        values ({(valores)})'''
            result = queryRDS(insertData, 'insert')

        ##############################################################
        #### si el dato existe, se actualiza la base de datos       
        else:
            i = 0
            valores = []
            for campos in columnas1:
                valores.append(f''' {campos} = '{fila[i]}' ''')
                i += 1

            valores = ','.join(map(str, valores))

            updateData = f''' update public.lista_anime set {valores}
                                WHERE titulo_anime = '{fila[0]}' '''
            result = queryRDS(updateData, 'update')

        return result


url = 'https://api.jikan.moe/v4/top/anime'
tabla = requetApi(url)
insertData(tabla)

