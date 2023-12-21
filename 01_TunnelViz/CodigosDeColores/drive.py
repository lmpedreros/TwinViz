import gspread
from oauth2client.service_account import ServiceAccountCredentials

def listaDePernosQueNecesito(values_list):
    lista_final = [[], [], []]
    index_que_me_importan = [[2, 3, 4], [17, 18, 19], [33, 34, 35]]
    for i in range(0, len(values_list)-1):
        for cuadrante in range(0,3):
            if i in index_que_me_importan[cuadrante]:
                lista_a_unir = values_list[i]
                lista_a_unir.append("I"+str(i+1))
                lista_a_unir.pop(0)
                lista_final[cuadrante].append(lista_a_unir)
    return lista_final

myscope = ['https://spreadsheets.google.com/feeds', 
            'https://www.googleapis.com/auth/drive']
credenciales = ServiceAccountCredentials.from_json_keyfile_name('my-project-twinviz-d279dede6608.json',myscope)
client = gspread.authorize(credenciales)

excel = client.open("BD_Prototipo").sheet1
#mysheet = client.open("planchuelas").sheet1
#mysheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1yf6cTbf500VQvxi0sO6_0vYtO6Uc_5ycarysJo47QV4/edit#gid=0').sheet1

valoresFilaDos = excel.row_values(2)
excelEnLista = excel.get_all_values()
print(valoresFilaDos)
print(excelEnLista[1])
print('-----------------------------------------------')
pernos = listaDePernosQueNecesito(excelEnLista)

#print(pernos[3])

for cuadrante in pernos:
    for perno in cuadrante:
        perno[7] = "MALO"
        print(perno)
        #excel.update(range_name=perno[8], values='BUENO')




# list_of_row = excel.get_all_records()

# row1 = excel.row_values(1)
# print("List of countries:")
# print(list_of_row)
# print("The first country:")
# print(row1)

#excel.update('A1', [[1, 2], [3, 4]])
