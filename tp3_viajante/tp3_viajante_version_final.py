#VERSION FINAL
import gmplot  #pip install gmplot
import tkinter as tk  #pip install tk #para linux: sudo apt-get install python3-tk
from random import randint, random, sample
from openpyxl import  load_workbook  #pip install openpyxl
from openpyxl.styles import Font, Color
from openpyxl.chart import Reference, LineChart, Series

#cromosoma: cada gen es una provincia
#poblacion inicial: diferentes combinaciones de las provincias
#las provincias se codifican de 0 a 23 (range(24))

ciclos = 200 #200
cantCromosomas = 50 #poblacion inicial: 50
cantCiudades = 24 #genes: 24
cromosoma = []
poblacion = []
probCross = 0.75
probMutac = 0.05

fitness = [0] * cantCromosomas
mejores_pob = [] #guarda el mejor recorrido/cromosoma de cada poblacion/ciclo
minimos = []
maximos = []
promedios = []

# Creo el mapa:
apikey = 'AIzaSyDEvS6c99Kgzf8pDo7SIA1U6dh5zTQN_d0' #la clave que te da google para que puedas usar el api

#las coordenadas aprox para que muestre argentina, 5 es el zoom del mapa
gmap = gmplot.GoogleMapPlotter(-36.610822172848145, -65.70171587433305, 5, apikey=apikey)

dict_ciudades = {
    0: 'Ciudad de Buenos Aires',
    1: 'Córdoba',
    2: 'Corrientes',
    3: 'Formosa',
    4: 'La Plata',
    5: 'La Rioja',
    6: 'Mendoza',
    7: 'Neuquén',
    8: 'Paraná',
    9: 'Posadas',
    10: 'Rawson',
    11: 'Resistencia',
    12: 'Río Gallegos',
    13: 'San Fernando del Valle de Catamarca',
    14: 'San Miguel de Tucumán',
    15: 'San Salvador de Jujuy',
    16: 'Salta',
    17: 'San Juan',
    18: 'San Luis',
    19: 'Santa Fe',
    20: 'Santa Rosa',
    21: 'Santiago del Estero',
    22: 'Ushuaia',
    23: 'Viedma',
}


ciudades_distancias = (
    (0,646,792,933,53,986,985,989,375,834,1127,794,2082,979,1080,1334,1282,1005,749,393,579,939,2373,799),
    (646,0,677,824,698,340,466,907,348,919,1321,669,2281,362,517,809,745,412,293,330,577,401,2618,1047),
    (792,677,0,157,830,814,1131,1534,500,291,1845,13,2819,691,633,742,719,1039,969,498,1136,535,3131,1527),
    (933,824,157,0,968,927,1269,1690,656,263,1999,161,2974,793,703,750,741,1169,1117,654,1293,629,3284,1681),
    (53,698,830,968,0,1038,1029,1005,427,857,1116,833,2064,1030,1132,1385,1333,1053,795,444,602,991,2350,789),
    (986,340,814,927,1038,0,427,1063,659,1098,1548,802,2473,149,330,600,533,283,435,640,834,311,2821,1311),
    (985,466,1131,1269,1029,427,0,676,790,1384,1201,1121,2081,569,756,1023,957,152,235,775,586,713,2435,1019),
    (989,907,1534,1690,1005,1063,676,0,1053,1709,543,1529,1410,1182,1370,1658,1591,824,643,1049,422,1286,1762,479),
    (375,348,500,656,427,659,790,1053,0,658,1345,498,2320,622,707,959,906,757,574,19,642,566,2635,1030),
    (834,919,291,263,857,1098,1384,1709,658,0,1951,305,2914,980,924,1007,992,1306,1200,664,1293,827,3207,1624),
    (1127,1321,1845,1999,1116,1548,1201,543,1345,1951,0,1843,975,1647,1827,2120,2054,1340,1113,1349,745,1721,1300,327),
    (794,669,13,161,833,802,1121,1529,498,305,1843,0,2818,678,620,729,706,1029,961,495,1132,523,3130,1526),
    (2082,2281,2819,2974,2064,2473,2081,1410,2320,2914,975,2818,0,2587,2773,3063,2997,2231,2046,2325,1712,2677,359,1294),
    (979,362,691,793,1030,149,569,1182,622,980,1647,678,2587,0,189,477,410,430,540,602,915,166,2931,1391),
    (1080,517,633,703,1132,330,756,1370,707,924,1827,620,2773,189,0,293,228,612,727,689,1088,141,3116,1562),
    (1334,809,742,750,1385,600,1023,1658,959,1007,2120,729,3063,477,293,0,67,874,1017,942,1382,414,3408,1855),
    (1282,745,719,741,1333,533,957,1591,906,992,2054,706,2997,410,228,67,0,808,950,889,1316,353,3341,1790),
    (1005,412,1039,1169,1053,283,152,824,757,1306,1340,1029,2231,430,612,874,808,0,284,740,686,583,2585,1141),
    (749,293,969,1117,795,435,235,643,574,1200,1113,961,2046,540,727,1017,950,284,0,560,412,643,2392,882),
    (393,330,498,654,444,640,775,1049,19,664,1349,495,2325,602,689,942,889,740,560,0,641,547,2641,1035),
    (579,577,1136,1293,602,834,586,422,642,1293,745,1132,1712,915,1088,1382,1316,686,412,641,0,977,2044,477),
    (939,401,535,629,991,311,713,1286,566,827,1721,523,2677,166,141,414,353,583,643,547,977,0,3016,1446),
    (2373,2618,3131,3284,2350,2821,2435,1762,2635,3207,1300,3130,359,2931,3116,3408,3341,2585,2392,2641,2044,3016,0,1605),
    (799,1047,1527,1681,789,1311,1019,479,1030,1624,327,1526,1294,1391,1562,1855,1790,1141,882,1035,477,1446,1605,0),
)

#coordenadas de cada ciudad sacadas de google maps (pueden estar mal algunas, hay que verificar)
coordenadas = [
    (-34.595873683601326, -58.38411681579245),
    (-31.416124031214316, -64.18872346409054),
    (-27.469917007385284, -58.835288693322575),
    (-26.18231057314127, -58.17772240012748),
    (-34.921566871153985, -57.957899223252404),
    (-29.409678642062214, -66.85512700267135),
    (-32.88910321839582, -68.84751649859864),
    (-38.9487179910739, -68.06352435203432),
    (-31.74828033680763, -60.51172704633869),
    (-27.38163974111014, -55.91914163844681),
    (-43.30363427656653, -65.10103181452405),
    (-27.448570192640847, -58.98806148893564),
    (-51.62342777695044, -69.22168884446302),
    (-28.46432391156789, -65.78063312478608),
    (-26.815248672062832, -65.22574838585409),
    (-24.187808742841835, -65.29977974284792),
    (-24.789986766887033, -65.4210152712924),
    (-31.53489428847907, -68.53589448728313),
    (-33.29299787840273, -66.32957650402733),
    (-31.61084854671748, -60.70062700984329),
    (-36.628606160588475, -64.29066508177014),
    (-27.79936963438958, -64.27002858643093),
    (-54.80305178234191, -68.3085325838506),
    (-40.81800187375475, -63.0029015193733)
]

#lista donde se irá guardando el recorrido
ciudades_visitadas = []

dist_total = 0

#busca cual es la ciudad más cercana a la última visitada
def buscar_ciudad_cercana(ciudad, matriz):
    ciudad_dist = matriz[ciudad]#lista que contiene las distancias con respecto a la ultima ciudad visitada
    menor_distancia = 99999 #seteo un valor arbitrariamente grande para luego comparar
    prox_ciudad = -1 #seteo un índice inválido pero luego tomará el valor de la próxima ciudad

    for c in range( len(ciudad_dist) ):
        if ( c not in ciudades_visitadas ):#verifico que la próxima ciudad a visitar no haya sido visitada antes
            if ( ciudad_dist[c] < menor_distancia ):#verifico que sea la más cercana con respecto a la última ciudad visitada
                menor_distancia = ciudad_dist[c]
                prox_ciudad = c

    global dist_total
    dist_total += menor_distancia #distancia total recorrida
    ciudades_visitadas.append(prox_ciudad) #agrego la próxima ciudad a visitar al recorrido

    return prox_ciudad

def mostrar_mapa(recorrido):

    latitud_mejor_recorrido = [0] * 24
    longitud_mejor_recorrido = [0] * 24

    # Guarda las coordenadas del mejor recorrido en orden para mostrar en el mapa
    for i in range(0, cantCiudades):
        latitud_mejor_recorrido[i] = coordenadas[recorrido[i]][0]  #guarda latitud de cada ciudad
        longitud_mejor_recorrido[i] = coordenadas[recorrido[i]][1] #guarda longitud de cada ciudad

    for i in range(0, cantCiudades):
        gmap.marker(coordenadas[i][0],coordenadas[i][1],
            title="{}".format(dict_ciudades[i] ), color='red', size=40, marker=True, label=recorrido.index(i)) #marca las ciudades


    #une cada ciudad segun lo almacenado en latitud_mejor_recorrido y longitud_mejor_recorrido
    gmap.polygon(latitud_mejor_recorrido,longitud_mejor_recorrido, color='cornflowerblue', edge_width=5)
    gmap.draw('map.html')  #guarda el mapa en un archivo html

print("-----------------------------------------------------")
print("\t\t>> MENU << \n 1 - Encontrar recorrido mínimo ingresando una ciudad\n 2 - Encontrar recorrido mínimo\n 3 - Encontrar recorrido mínimo utilizando un algoritmo genético")
opc = int(input("\nIngrese opcion: "))

if opc==1:
    ciudades_visitadas.clear()

    for i in dict_ciudades:
        print( "{}.{}".format( i, dict_ciudades[i] ) )

    ciudad_ingresada = int( input("Ingrese el codigo de una ciudad: ") )
    while (ciudad_ingresada < 0 or ciudad_ingresada > 23):
        ciudad_ingresada = int( input("Ingrese el codigo de una ciudad: ") )

    #agrego la ciudad de partida al recorrido
    ciudades_visitadas.append(ciudad_ingresada)

    ultima_ciudad_visitada = ciudad_ingresada

    for i in range(23):
        ultima_ciudad_visitada = buscar_ciudad_cercana(ultima_ciudad_visitada, ciudades_distancias)

    #vuelvo a agregar la ciudad de partida al final del recorrido para el regreso
    ciudades_visitadas.append(ciudad_ingresada)
    dist_total += ciudades_distancias[ultima_ciudad_visitada][ciudad_ingresada]#distancia total recorrida de ida y de vuelta

    rec_completo="" #para almacenar los nombres de las ciudades y poder mostrarlos
    i = 0
    for c in ciudades_visitadas:
        nombre=str(dict_ciudades[c])  #transformo a string el nombre de la ciudad
        rec_completo=rec_completo+nombre  #agrego el nombre de la ciudad
        if i < len(ciudades_visitadas)-1:
            rec_completo=rec_completo+'\n'  #agrego un salto de linea si no es la ultima ciudad
        i+=1

    mostrar_mapa(ciudades_visitadas)

    print('-- FIN DE LA CORRIDA --')

    #creo ventana para que muestre el recorrido y los km
    ventana=tk.Tk()
    ventana.geometry('300x450')   #tamaño de la ventana
    ventana.title("RECORRIDO PARTIENDO DESDE: {}".format(dict_ciudades[ciudad_ingresada]))  #titulo de la ventana
    lbl_titulo=tk.Label(ventana, text="RECORRIDO COMPLETO:\n",font='Helvetica 10 bold') #primer texto (esta separado para poder ponerlo en negrita)
    lbl_titulo.place(x=0, y=0) #posicion del texto
    lbl_texto=tk.Label(ventana, text=rec_completo+"\n")
    lbl_texto.place(x=0,y=0)
    lbl_km=tk.Label(ventana, text="DISTANCIA TOTAL RECORRIDA: {}".format(dist_total) + "km",font='Helvetica 10 bold')
    lbl_km.place(x=0, y=0)
    lbl_titulo.pack()   #.pack agrega el label a la ventana
    lbl_texto.pack()
    lbl_km.pack()
    ventana.mainloop()  #muestra la ventana


if opc==2:
    recorrido_minimo = []#el recorrido mas optimo de todos
    menor_dist_2 = 99999#seteo un valor arbitrariamente grande para luego comparar
    #recorro todas las ciudades para ver desde cual tengo que partir para encontrar el recorrido mas corto
    for k in dict_ciudades:
        ciudades_visitadas.clear()
        dist_total = 0
        ciudades_visitadas.append(k)
        ultima_ciudad_visitada = k
        #calculo todo el recorrido partiendo de la ciudad k
        for i in range(23):
            ultima_ciudad_visitada = buscar_ciudad_cercana(ultima_ciudad_visitada, ciudades_distancias)
        ciudades_visitadas.append(k)
        dist_total += ciudades_distancias[ultima_ciudad_visitada][k]
        #verifico que la distancia total partiendo de la ciudad k sea la mas corta
        if dist_total < menor_dist_2:
            menor_dist_2 = dist_total
            recorrido_minimo = ciudades_visitadas.copy()


    rec_minimo=""  #para almacenar los nombres de las ciudades y mostrarlos
    i = 0
    for c in recorrido_minimo:
        nombre=str(dict_ciudades[c]) #transformo a string el nombre de la ciudad
        rec_minimo=rec_minimo+nombre   #agrego el nombre de la ciudad
        if i < len(recorrido_minimo)-1:
            rec_minimo=rec_minimo+' \n ' #agrego un salto de linea si no es la ultima ciudad
        i+=1

    mostrar_mapa(recorrido_minimo)

    print('-- FIN DE LA CORRIDA --')
    #creo ventana para que muestre el recorrido minimo y los km
    ventana=tk.Tk()   #creo la ventana
    ventana.geometry('500x450')  #tamaño de la ventana
    ventana.title("RECORRIDO MINIMO") #titulo de la ventana
    lbl_titulo=tk.Label(ventana, text="EL RECORRIDO MINIMO ES PARTIENDO DESDE:\n"+" {}".format(dict_ciudades[recorrido_minimo[0]]),font='Helvetica 10 bold')
    lbl_titulo.place(x=0, y=0)
    lbl_texto=tk.Label(ventana, text=rec_minimo+"\n")
    lbl_texto.place(x=0,y=0)
    lbl_km=tk.Label(ventana, text="DISTANCIA TOTAL RECORRIDA: {}".format(menor_dist_2) + "km",font='Helvetica 10 bold')
    lbl_km.place(x=0, y=0)
    lbl_titulo.pack()  #.pack agrega el label a la ventana
    lbl_texto.pack()
    lbl_km.pack()
    ventana.mainloop()   #muestra la ventana


if opc==3:

    def poblacion_inicial():

        for i in range(cantCromosomas):
            cromosoma = sample(range(cantCiudades), cantCiudades)
            cromosoma.append(cromosoma[0]) #agrego la ciudad de partida al final
            poblacion.append(cromosoma)


    #Crossover ciclico
    def crossover(cromo1, cromo2):

        probabilidad = random()
        valoresUsados = []
        valoresUsados.clear()
        hijo = cromo2.copy()
        if probabilidad <= probCross:
            band = True
            hijo[0] = cromo1[0] #DUDA: arranca del 0 o de un random?
            hijo[cantCiudades] = cromo1[cantCiudades] #aseguro que el ultimo lugar sea el mismo que el primero
            indiceAux = 0
            valorAux=cromo1[0]
            valoresUsados.append(cromo1[0])
            while band:
                valorAux = cromo2[indiceAux]
                indiceAux = cromo1.index(valorAux)
                if cromo1[indiceAux] in valoresUsados:
                    band = False
                else:
                    hijo[indiceAux] = cromo1[indiceAux]
                    valoresUsados.append(cromo1[indiceAux])
        return hijo

    #Mutacion (intercambio de 2 genes)
    def mutacion(cromo):
        probabilidad = random()
        if probabilidad <= probMutac: #Verifico que se cumpla la prob de mutacion
            gen1 = randint(1, cantCiudades-1) #posicion del gen a intercambiar. No incluyo ciudad de partida/llegada
            gen2 = randint(1, cantCiudades-1)
            while(gen1 == gen2): #verifico que no sea el mismo gen
                gen2 = randint(1, cantCiudades-1)
            genAux = cromo[gen1]
            cromo[gen1] = cromo[gen2]
            cromo[gen2] = genAux
        return cromo


    def distancia_recorrido(r):
        distancia = 0
        for i in range(cantCiudades-1):
            distancia += ciudades_distancias[r[i]][r[i+1]]
        distancia += ciudades_distancias[r[i+1]][r[0]] #vuelvo al origen

        return distancia

    #Seleccion de padres
    def torneo(fit):
        tam_torneo = randint(2,cantCromosomas)
        participantes = [] #Se llena con fitness de cada cromo participante
        indices_participantes = []
        cant_participantes = 0
        while (cant_participantes < tam_torneo): #Busco participantes hasta llenar el torneo
            indice_fitness_participante = randint(0, cantCromosomas-1) #Referencio dentro del index del arreglo, que arranca en 0 y termina en cantCromo-1
            if indice_fitness_participante not in indices_participantes: #Verifico que no sea participante (elegido antes)
                participantes.append( fit[indice_fitness_participante] )
                indices_participantes.append(indice_fitness_participante)
                cant_participantes = cant_participantes + 1

        #Una vez que tengo todos los participantes busco el ganador del torneo:
        ganador = participantes[0]
        indice_ganador = indices_participantes[0]
        for i in range(tam_torneo-1):
            if participantes[i+1] < ganador: #Comparo segun fitness. El de menor fitness tiene menor distancia de recorrido
                ganador = participantes[i+1]
                indice_ganador = indices_participantes[i+1]

        return indice_ganador #Retorna el indice al cromosoma ganador

    #Menor distancia recorrida en una poblacion
    def elige_mejor(pob):
        mejor = pob[0].copy()
        valorMejor = distancia_recorrido(pob[0]) #asigno el primero para tener un valor para comparar
        for i in range(cantCromosomas):
            if(distancia_recorrido(pob[i]) < valorMejor): #voy calculando la distancia de cada cromo/recorrido
                mejor = pob[i].copy()
                valorMejor = distancia_recorrido(pob[i])

        return mejor


    #Aplicacion de ELITISMO. Devuelve una lsita con el indice de los 10 mejores cromosomas (elites) de la poblacion, segun los valores de fitness del ciclo.
    def elitismo(usados):
        menorFit = 1 #Cualquier fitness sera menor

        for i in range(cantCromosomas):
            if((fitness[i] <= menorFit) and i not in usados):
                menorFit = fitness[i]
                indiceElit = i

        return indiceElit


    def aplicar_AG(pob):
        #calculo la distancia total de esta poblacion
        total_distancia = 0
        for i in range (cantCromosomas):
            total_distancia += distancia_recorrido(pob[i])

        #Calculos para la tabla (max, min, prom)
        mayor = distancia_recorrido(pob[0])
        menor = distancia_recorrido(pob[0])
        for i in range(cantCromosomas):
            if (distancia_recorrido(pob[i])>=mayor):
                mayor = distancia_recorrido(pob[i])
            if (distancia_recorrido(pob[i])<=menor):
                menor = distancia_recorrido(pob[i])

        #Guardo los valores de cada generacion para la tabla
        minimos.append(menor)
        maximos.append(mayor)
        promedios.append(total_distancia/cantCromosomas)


        #calculo de la funcion fitness. A mayor distancia, mayor fitness
        for i in range(cantCromosomas):
            fitness[i] = (distancia_recorrido(pob[i])/total_distancia) #El mejor recorrido es el de menor fitness

        #seleccion de padres mediante torneo
        padres = []
        if elite:
            elitUsados = []
            indicesElit = []
            cantElites = int(20*cantCromosomas/100) #se elige el 20% de la poblacion
            for i in range(cantElites):
                indicesElit.append(elitismo(elitUsados))
                elitUsados.append(indicesElit[i])
            cantPadres = cantCromosomas - cantElites
        else:
            cantPadres = cantCromosomas

        for i in range(cantPadres):
            indice_ganador = torneo(fitness)
            padres.append(pob[indice_ganador])

        #crossover
        nueva_poblacion = []
        if elite:
            ultIndice = cantCromosomas - cantElites - 1
        else:
            ultIndice = cantCromosomas - 1
        for i in range(0, ultIndice, 2):
            nueva_poblacion.append(crossover(padres[i], padres[i+1])) #primer hijo
            nueva_poblacion.append(crossover(padres[i+1], padres[i])) #segundo hijo

        #mutacion
        if elite:
            ultIndice = cantCromosomas - cantElites - 1
        else:
            ultIndice = cantCromosomas - 1
        for i in range(ultIndice):
            nueva_poblacion[i] = mutacion(nueva_poblacion[i])

        #agrego elites
        if elite:
            for i in range(cantElites):
                nueva_poblacion.append(pob[indicesElit[i]])

        #guardo el mejor recorrido de esta poblacion
        mejores_pob.append(elige_mejor(nueva_poblacion))

        return nueva_poblacion


    def tablaExcel(nombreArchivo):
        wb = load_workbook(filename=nombreArchivo) #para arbir uno existente, con los colores preseteados
        tabla = wb.active

        tabla["A1"] = "Minimo recorrido: "
        tabla["C1"] = valorMejor #esto fue calculado en el main
        tabla["D1"] = "KM"
        tabla['A1'].font = Font(bold=True, size=12, color="A72D13") #Estilo visual
        tabla['C1'].font = Font(bold=True, size=12, color="A72D13")
        tabla['D1'].font = Font(bold=True, size=12, color="A72D13")

        tabla.append(["Generacion", "Minimo", "Maximo", "Promedio"]) #titulos
        tabla['A2'].font = Font(bold=True) #Pongo los titulos en negrita. A modo visual
        tabla['B2'].font = Font(bold=True)
        tabla['C2'].font = Font(bold=True)
        tabla['D2'].font = Font(bold=True)
        tabla['E2'].font = Font(bold=True)
        tabla['F2'].font = Font(bold=True)
        for i in range(ciclos): #Datos de la corrida
            tabla.append([i+1, minimos[i], maximos[i], promedios[i]])

        #Generacion de grafico de lineas con minimos, maximos y promedios.
        grafica = LineChart()
        grafica.title = "Grafico"
        grafica.style = 10
        grafica.y_axis.title = "Valores"
        grafica.x_axis.title = "Ciclos"
        grafica.y_axis.scaling.min = 9000 #Limites del eje y
        grafica.y_axis.scaling.max = 25000
        grafica.x_axis.scaling.min = 0 #Limites del eje x
        grafica.x_axis.scaling.max = ciclos
        data = Reference(tabla, min_col=2, min_row=2, max_col=4, max_row=ciclos+2) #Rango que se grafica Maximo, Minimo, Promedio
        grafica.add_data(data, titles_from_data=True)
        tabla.add_chart(grafica, "F2") #agregado y ubicacion del grafico

        wb.save(nombreArchivo)


    #MAIN
    rta = input("ELITISMO? s/n: \n")
    if(rta == 's'):
        elite = True
    elif(rta == 'n'):
        elite= False

    poblacion_inicial()
    poblacion_nueva = aplicar_AG(poblacion)

    for i in range(ciclos-1):
        poblacion_nueva = aplicar_AG(poblacion_nueva)


    #Elegir mejor recorrido entre los mejores de cada ciclo
    for i in mejores_pob:
        mejor_final = mejores_pob[0].copy()
        valorMejor = distancia_recorrido(mejores_pob[0])
        for i in range(ciclos):
            if(distancia_recorrido(mejores_pob[i]) < valorMejor):
                mejor_final = mejores_pob[i].copy()
                valorMejor = distancia_recorrido(mejores_pob[i])


    #Tabla excel corridas
    tablaExcel('tablaAG.xlsx')


    #Mapa
    rec_completo=""  #donde se va a almacenar el recorrido completo

    for i in range(cantCiudades+1):
        rec_completo=rec_completo+str(dict_ciudades[mejor_final[i]])   #agrego el nombre de las ciudades al recorrido
        if i < cantCiudades:   #este if es solamente para ir agregando el salto de linea
                rec_completo=rec_completo+'\n'

    mostrar_mapa(mejor_final)  #poniendo el mostrar_mapa aca hace que el mapa se genere antes de cerrar la ventana

    print('-- FIN DE LA CORRIDA --')
    #creo ventana para que muestre el recorrido y los km
    ventana=tk.Tk()
    ventana.geometry('300x450')   #tamaño de la ventana
    ventana.title("CON GENETICOS")  #titulo de la ventana
    lbl_titulo=tk.Label(ventana, text="RECORRIDO ELEGIDO:\n",font='Helvetica 10 bold') #primer texto (esta separado para poder ponerlo en negrita)
    lbl_titulo.place(x=0, y=0) #posicion del texto
    lbl_texto=tk.Label(ventana, text=rec_completo+"\n")
    lbl_texto.place(x=0,y=0)
    lbl_km=tk.Label(ventana, text="DISTANCIA TOTAL RECORRIDA: {}".format(distancia_recorrido(mejor_final)) + "km",font='Helvetica 10 bold')
    lbl_km.place(x=0, y=0)
    lbl_titulo.pack()   #.pack agrega el label a la ventana
    lbl_texto.pack()
    lbl_km.pack()
    ventana.mainloop()  #muestra la ventana
