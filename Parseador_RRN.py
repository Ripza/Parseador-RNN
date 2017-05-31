import psycopg2
import sys

lista_puntos = []
lista_recorridos = []
bRecorridoV = False
lista_puntosV = []
lista_puntosI = []
Last_Recorrido = "0"
Cont_Recorrido = 0
Cont_Recorrido_Total = 0

# Conexión a base de datos
def conect():
    conn_string ="host='127.0.0.1' port='5432' dbname='admingeso' user='postgres' password='root'"

    print ("Conectando a: \n =>%s" % (conn_string) )
    conn = psycopg2.connect(conn_string)
    print ("Conectado!")
    return conn

# Parseamos la hora del día , los minutos y los segundos, luego se aplica una modulacion entre 0 y 1
def parser_time(dato):
    #print ("dato entrada" + str(dato[2]))
    spliter = dato[2].split(' ')
    splitFecha = spliter[0].split('/')
    splitHora = spliter[1].split(':')
    dia = int(splitFecha[0])/31
    mes = int(splitFecha[1])/12
    horaStand = (int(splitHora[0])*3600+int(splitHora[1])*60+int(splitHora[2]))/(23*3600+59*60+59)
    datoStand = [dia,mes,horaStand]
    #print ("dato salida :" +str(datoStand))
    return datoStand

# Parseamos la fecha del registro
def parser_date(dato):
    print ("hola")

def agregar_recorrido():
    celda_recorrido = []
    puntos_r = lista_puntos[:]
    celda_recorrido.append(Last_Recorrido)

    if(bRecorridoV == True):    
        celda_recorrido.append("V")
    else:
        celda_recorrido.append("I")
                
    celda_recorrido.append(Cont_Recorrido)
    celda_recorrido.append(puntos_r)
    
    lista_recorridos.append(celda_recorrido)
    
    #print (puntos_r)
    
    del lista_puntos[:]
    
    #print(lista_recorridos[len(lista_recorridos)-1][3])
    
def main():
    global Last_Recorrido
    global Cont_Recorrido
    global Cont_Recorrido_Total
    global bRecorridoV
    global lista_puntosV
    global lista_puntosI
    global lista_puntos
    lista_puntosV = []
    
    
    conn = conect()
    cursor = conn.cursor()
    cont_print = 0
    query = "SELECT * FROM datos"
    #query = "SELECT * FROM datos LIMIT 200"
    cursor.execute(query)
    records = cursor.fetchall()
    for record in records:
        
    #Lista_recorridos[ Numero de patente, I/V , Num_Recorrido , Lista_Puntos[ Lista_Fecha,Lista_Hora,LatLong ]
        if(Last_Recorrido == "0"):
            if(record[4] == "V"):
                bRecorridoV = True
            else:
                bRecorridoV = False
            Last_Recorrido = record[1]
        
        #Cambio de recorrido
        
        if(Last_Recorrido != record[1]):
                
            #Agregamos el recorrido anterior a la lista de recorridos
            agregar_recorrido()
            
            #Inicializamos la ruta en funcion de la nueva
            
            if(record[4] == "V"):
                bRecorridoV = True
            else:
                bRecorridoV = False
            Last_Recorrido = record[1]
            Cont_Recorrido = 0
            Cont_Recorrido_Total += 1
        
            print ("\n\n\n\n\n\n\n\n\n\n\n\n\n")
            print ("---- Cambio de patente detectado. Procediendo a reiniciar contadores ----")
            print ("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        
        #Recreamos el cambio de ruta
        if(record[4] == "V" and bRecorridoV == False):
            bRecorridoV = True
            Cont_Recorrido += 1
            Cont_Recorrido_Total += 1
            print ("Cambio de recorrido detectado, Recorrido en V")
            agregar_recorrido()
            print("Cantidad de recorridos de la patente "+ str(Cont_Recorrido))
            print("Cantidad de recorridos totales "+ str(Cont_Recorrido_Total))
            
        
        elif(record[4] == "I" and bRecorridoV == True):
            bRecorridoV = False
            Cont_Recorrido += 1
            Cont_Recorrido_Total += 1
            print ("Cambio de recorrido detectado, Recorrido en I")
            agregar_recorrido()
            print("Cantidad de recorridos de la patente "+ str(Cont_Recorrido))
            print("Cantidad de recorridos totales "+ str(Cont_Recorrido_Total))
        
        celda = []
        cont_print += 1
        #celda.append(parser_date(record))
        
        tiempo = parser_time(record)
        celda.append(tiempo[0])
        celda.append(tiempo[1])
        celda.append(tiempo[2])
        celda.append(float(record[5].replace(",", ".")))
        celda.append(float(record[6].replace(",", ".")))
        #celda.append(Cont_Recorrido_Total)
        
        if(cont_print % 40 == 0):
            print (celda)
            
        lista_puntos.append(celda)
        
        if(bRecorridoV == True):
            lista_puntosV.append(celda)
        else:
            lista_puntosI.append(celda)

            
    #Hacer la ultima operacion para la ultima ruta
    Cont_Recorrido += 1
    Cont_Recorrido_Total += 1
    agregar_recorrido()
    print("Cantidad de recorridos de la patente "+ str(Cont_Recorrido))
    print("Cantidad de recorridos totales "+ str(Cont_Recorrido_Total))
            
    conn.close()
    print ("Conexion Cerrada")
if __name__ == "__main__":
    main()
    print (len(lista_puntos))
    print (Cont_Recorrido_Total)
    print ("Tamaño de lista puntos en V : "+str(len(lista_puntosV)))
    print ("Tamaño de lista puntos en I : "+str(len(lista_puntosI)))
    print (len(lista_recorridos))