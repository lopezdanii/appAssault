     
#-*- coding:UTF-8 -*-
'''
@author: Raul Izquierdo y Daniel Lopez

'''
import sys
import math
from idlelib.ReplaceDialog import replace
def main():
    try :
        opcion = pantallainicio()
        seleccion(opcion)
    except ValueError:
        print "ERROR"
        main()
    return None
    
def pantallainicio():
    print "--------------------ASALTO--------------------"
    print "-Practica de Paradigmas de Programacion 2018-19"
    print '-'*46
    print ' '
    print "\t1. NUEVA PARTIDA\t"
    print "\t2. CARGAR PARTIDA\t"
    print "\t3. SALVAR PARTIDA\t"
    print "\t4. CONTROL OFICIALES: [HUMANO] AZAR"
    print "\t5. CONTROL REBELDES: [HUMANO] AZAR BASICO"
    print "\t6. SALIR\n"
    opcion = int(raw_input("Indique opcion: "))
    while comprobar(opcion) == False:
        opcion = int(raw_input("Indique opcion entre 1 y 6: ")) 
    return opcion

def comprobar(opcion):
    if opcion >6 or opcion<1:
        return False
    else:
        return True
    
def seleccion(opcion):
    if opcion == 1:
        jugadas_guardadas=nueva_partida()
    elif opcion == 2:
        cargar_partida()
    elif opcion == 3:
        salvar_partida(jugadas_guardadas)
    elif opcion == 4:
        x=int(raw_input("1 para HUMANOS; 2 para AZAR"))
        control_oficiales(x)
        
    elif opcion == 5:
        x=int(raw_input("1 para HUMANOS; 2 para AZAR; 3 para BASICO"))
        control_rebeldes(x)
    elif opcion == 6:
        salir()
def nueva_partida():
    tablero, numero_rebeldes = construir_columnas()
    actualizar_tablero(tablero)
    contador = 0
    jugadas_guardadas = jugar(contador,tablero,numero_rebeldes)
    return jugadas_guardadas

def control_humano():
    return None

def control_azar():
    return None

def control_basico():
    return None 

def construir_columnas():
    puntos_coincidentes = []
    numero_rebeldes = 0
    tablero_operaciones = [[' ']* 7 for x in range(7)]
    for i in range(0,7): 
        for j in range(2,5):
            puntos_coincidentes.append((i,j))
            tablero_operaciones[i][j]= 0
            numero_rebeldes=numero_rebeldes+1    
    for i in range(2,5):
        for j in range(0,7):
            if (i,j) not in puntos_coincidentes:
                tablero_operaciones[i][j] = 0
                numero_rebeldes=numero_rebeldes+1
    for i in range(0,3):
        for j in range (2,5):
            tablero_operaciones[i][j] = -1
            tablero_operaciones[1][2]= 1
            tablero_operaciones[1][4]= 1
            numero_rebeldes=numero_rebeldes-1
    return tablero_operaciones, numero_rebeldes

def cargar_partida():
    guardado = raw_input("Introduce el nombre de la partida que desea cargar:")
    open(guardado.txt,"+")
    return None

def salvar_partida(jugadas_guardadas):
    guardado = raw_input("Introduce del fichero en el que desea guardar la partida:")
    f=open(guardado.txt,"w")
    f.write(jugadas_guardadas)
    f.flush()
    f.close()
    return None

def control_oficiales(x):
    control={1:"HUMANO",2:"AZAR"}
    print control.get(x,"Invalido")
    return None

def control_rebeldes(x):
    control={1:"HUMANO",2:"AZAR",3:"BASICO"}
    print control.get(x,"Invalido")
    return None

def salir():
    return None

def jugar(contador,tablero,numero_rebeldes):
    finjuego=False
    jugadas_guardadas = []
    print "Turno:",
    if contador%2 == 0:
        print "OFICIALES"
        print "Jugadas posibles:",
        lista_definitiva_o, lista_captura, lista_capturado=jugadas_oficiales(tablero)
        if lista_captura:
            print " ".join(lista_captura),
        else:
            print " ".join(lista_definitiva_o),
        jugadaoficiales = raw_input("\nIntroduce jugada o FIN:")
        jugadas_guardadas.append(jugadaoficiales)
        if jugadaoficiales == "FIN":
            main()
        else:
            numero_rebeldes = realizar_jugada_o(jugadaoficiales,tablero,lista_definitiva_o, lista_captura, lista_capturado, numero_rebeldes)
            actualizar_tablero(tablero)
            
        if numero_rebeldes<=9:
            finjuego=True
            ganan_oficiales=True
            ganan_rebeldes=False
            
        if bloqueo(lista_definitiva_o)==True:
            finjuego=True
            ganan_rebeldes=True
            ganan_oficiales=False    
        
    else:
        print "REBELDES"
        print "Quedan ",numero_rebeldes
        print "Jugadas posibles:",
        lista_definitiva_r=jugadas_rebeldes(tablero)
        print " ".join(lista_definitiva_r),
        jugadarebeldes = raw_input("\nIntroduce jugada o FIN:")
        jugadas_guardadas.append(jugadarebeldes)
        if jugadarebeldes == "FIN":
            main()
        else:
            realizar_jugada_r(jugadarebeldes,tablero,lista_definitiva_r)
            actualizar_tablero(tablero)

        if recorrer_castillo(tablero)==True:
            finjuego=True
            ganan_rebeldes=True
            ganan_oficiales=False
        
    contador += 1
    
    if finjuego==False:
        jugar(contador, tablero,numero_rebeldes)
    else:
        if ganan_oficiales == True:
            print "LOS OFICIALES HAN GANADO"
        elif ganan_rebeldes == True:
            print "LOS REBELDES HAN GANADO"
    return jugadas_guardadas

def jugadas_oficiales(tablero):
    lista_definitiva = []
    lista_captura = []
    lista_captura_definitiva = []
    lista_capturado = []
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j]==1:
                punto = (i,j)
                pto_valido(punto)
                for (x,y) in vecinos((i,j)):
                    if (en_tablero((x,y))==True):
                        lista, lista_captura, lista_capturado = posiciones_libres_o((i,j),(x,y),tablero, lista_captura, lista_capturado)
                        traducir_numeros_letras(lista_definitiva, lista, (i,j))
                traducir_numeros_letras(lista_captura_definitiva, lista_captura, (i,j))
    return lista_definitiva, lista_captura_definitiva, lista_capturado

def jugadas_rebeldes(tablero):
    lista_definitiva = []
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            if tablero[i][j]==0:
                dist1=dist_castillo((i,j))
                punto=(i,j)
                pto_valido((i,j))
                for (x,y) in vecinos(punto):
                    if (en_tablero((x,y))==True):
                        lista = posiciones_libres_r((x,y),tablero)
                        traducir_numeros_letras(lista_definitiva, lista,(i,j))
    return lista_definitiva

def traducir_numeros_letras(lista_definitiva, lista,(i,j)):
    for x in range(len(lista)):
        posx = chr(lista[x][0]+97)
        posy = chr(lista[x][1]+97)
        posx_actual = chr(i+97)
        posy_actual = chr(j+97)
        posicion_definitiva = posx_actual.upper()+posy_actual+"-"+posx.upper()+posy 
        lista_definitiva.append(posicion_definitiva)
    return lista_definitiva

def traducir_letras_numeros(jugada):
    posx=ord(jugada[0].lower()) - ord('a')
    posy=ord(jugada[1]) - ord('a')
    return (posx,posy)

def vecinos ((x,y)):
    DVEC = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
    for (dx,dy) in DVEC:
        if not pto_valido((x+dx, y+dy)):
            continue
        if dy == 0 or dx == 0:
            yield (x+dx, y+dy)
        elif (abs(x-y) % 2 == 0 and
              pto_valido((x+dx, y)) and pto_valido((x, y+dy))):
            yield (x+dx, y+dy)

def pto_valido((x,y)):
    return (0 <= x < 7 and
            0 <= y < 7 and
            max(min(x, 6-x), min(y, 6-y)) > 1
            )

def en_tablero(pto):
    contador = 0
    for i in range(0,7): 
        for j in range(2,5):
            punto = (i,j)
            if pto == punto:
                return True
            else:
                contador += 1
                    
    for i in range(0,7):
        for j in range(0,7):
            punto = (i,j)
            if pto == punto:
                return True
            else:
                contador += 1
    
    if contador == 42:
        return False            
    return None

def posiciones_libres_o((a,b),(x,y),tablero,lista_captura, lista_capturado):
    lista = []
    if tablero[x][y]==-1:
        lista.append((x,y))
    elif  tablero [x][y]==0:
        for (i,j) in vecinos((x,y)):
            if pto_captura((a,b),(x,y)) == (i,j) and tablero[i][j]==-1:
                lista.append((i,j))
                lista_captura.append((i,j))
                lista_capturado.append((x,y))   
    return lista, lista_captura, lista_capturado

def posiciones_libres_r((x,y),tablero):
    lista = []
    if tablero[x][y]==-1:
        lista.append((x,y))
    return lista

def realizar_jugada_o(jugadaoficiales, tablero, lista_definitiva, lista_captura, lista_capturado, numero_rebeldes):
    (x,y)=traducir_letras_numeros(jugadaoficiales[3:5])
    (i,j)=traducir_letras_numeros(jugadaoficiales[:2])
    if jugadaoficiales in lista_captura:
        tablero[i][j]=-1
        tablero[x][y]=1
        tablero[lista_capturado[0][0]][lista_capturado[0][1]]=-1
        numero_rebeldes = numero_rebeldes-1    
    elif jugadaoficiales in lista_definitiva:
        if tablero[i][j] == 1:
            tablero[i][j]=-1
            tablero[x][y]=1
        elif tablero[i][j] == 0:
            tablero[i][j]=-1
            tablero[x][y]=0
    else:
        print "Posicion introducida incorrecta"
        jugadaoficiales = raw_input("Introduce una nueva posicion:")
        realizar_jugada_o(jugadaoficiales, tablero, lista_definitiva, lista_captura, lista_capturado, numero_rebeldes)
    return numero_rebeldes

def realizar_jugada_r(jugadaoficiales, tablero, lista_definitiva):
    (x,y)=traducir_letras_numeros(jugadaoficiales[3:5])
    (i,j)=traducir_letras_numeros(jugadaoficiales[:2])        
    if jugadaoficiales in lista_definitiva:
        if tablero[i][j] == 1:
            tablero[i][j]=-1
            tablero[x][y]=1
        elif tablero[i][j] == 0:
            tablero[i][j]=-1
            tablero[x][y]=0    
    else:
        print "Posicion introducida incorrecta"
        jugadaoficiales = raw_input("Introduce una nueva posicion:")
        realizar_jugada_r(jugadaoficiales, tablero, lista_definitiva)
    return None

def actualizar_tablero(tablero):
    primera_fila = ['a','b','c','d','e','f','g']
    print " ", 
    for i in range(len(primera_fila)): 
        print primera_fila[i],
        print " ",
    print
    for i in range(len(tablero)):
        print primera_fila[i].upper(),
        for j in range(len(tablero[i])):
            if tablero[i][j] == 0:
                print str(tablero[i][j]).replace("0","R"),
            elif tablero[i][j] == -1:
                print str(tablero[i][j]).replace("-1","."),
            elif tablero[i][j] == 1:
                print str(tablero[i][j]).replace("1","O"),
            else:
                print tablero[i][j],
            if pto_valido((i,j))and pto_valido((i,j+1)):
                print "-",
            else:
                print " ",
        if i in range(2,4):
            print "\n ",
        else:
            print "\n   ",
        for j in range(len(tablero[i])):
            if pto_valido((i,j))and pto_valido((i+1,j)):
                print "|",
                if pto_valido((i, j+1)):
                    if (i+j)%2==0:
                        print "\\",
                    else:
                        print "/",
            else:
                print "  ",        
        print

def dist_castillo((x,y)):
    return max(0, max(abs(x-3), abs(y-1))-1)

def pto_captura((x_ofi,y_ofi), (x_reb,y_reb)):
    return (2*x_reb - x_ofi, 2*y_reb - y_ofi)

def pto_castillo((x,y)):
    return 2 <= x < 5 and 0 <= y < 3

def bloqueo(lista_jugadas_o):    
    if lista_jugadas_o:
        return False
    else:
        return True

def recorrer_castillo(tablero):
    contador=0
    for i in range(0,3):
        for j in range(2,5):
            if tablero[i][j]==0:
                contador+=1
    if contador==9:
        return True
    else: 
        return False

if __name__ == "__main__":
    main()
