#VersionFinal 
class Objeto:
    def __init__(self, numero, valor, volPeso):
        self.num = numero 
        self.val = valor
        self.med = volPeso #med es la medida que se considere (volumen o peso)
    def __str__(self):
        return "Objeto: {} - Valor: {} - {}: {}".format(self.num, self.val, medida, self.med) 


#FUNCIONES PARA BUSQUEDA EXHAUSTIVA

def comb_de_a_n(lista_obj, n): #Generacion de todas las combinaciones posibles
    if n == 0:
        return [[]]
      
    l =[]
    for i in range(0, len(lista_obj)):
        m = lista_obj[i] #Objeto que se esta combinando con los demas 
        resto = lista_obj[i + 1:] #Los demas objetos posteriores a m 
        for p in comb_de_a_n(resto, n-1):
            l.append([m]+p) #Se agrega la posible solucion a la lista de combinaciones
              
    return l

#Calculo de la suma del peso/volumen de la combinacion de objetos para elegir en la mochila    
def suma_med(combinacion):
    suma = 0
    for i in combinacion:
        suma = suma + (objetos[i-1].med) 
    return suma

#Calculo de la suma del valor de la combinacion de objetos para elegir en la mochila 
def calc_mayor_valor(combinacion):
    suma = 0
    for i in combinacion:
        suma = suma + (objetos[i-1].val)
    return suma


def busqueda_exhaustiva():
    combinaciones = [] #Todas las combinaciones posibles de objetos
    num_obj =[]
    for i in range(1, len(objetos)+1): 
        num_obj.append(i)

    for i in range(1, len(num_obj)): #i indica la cantidad de objetos dentro de una combinacion
        combinaciones.append(comb_de_a_n([x for x in num_obj], i)) 

    suma_mayor = 0
    #Se evalua cada una de las combinaciones o subgrupos (posibles soluciones)
    for i in range(len(combinaciones)): #Se recorren las comninaciones tomadas de a i (1, 2, 3, ... elementos)
        for j in range(len(combinaciones[i])): 
            combinacion = combinaciones[i][j]
            suma_med_comb = suma_med(combinacion)
            if suma_med_comb <= maxMedida: #Evalua si entra en la mochila
                suma_val_comb = calc_mayor_valor(combinacion)
                if suma_val_comb >= suma_mayor: #Busqueda del mejor
                    suma_mayor = suma_val_comb
                    mejor_comb = combinacion
                    mejor_med = suma_med_comb

    print(">> BUSQUEDA EXHAUSTIVA")
    print("\n El {} ocupado es {} y su valor total es ${}\n".format(medida, mejor_med, suma_mayor))
    print("Los objetos elegidos son: {}".format(mejor_comb))
    for i in mejor_comb:
        print(objetos[i-1])



#FUNCIONES PARA HEURISTICA
#Se carga la mochila con los objetos hasta llegar al volumen maximo 
def cargar_mochila(objetos):
    med_ocupada = 0
    mochila = []

    for i in objetos:
        if (med_ocupada + i.med) < maxMedida: 
            mochila.append(i)
            med_ocupada = med_ocupada + i.med
    
    return mochila

#Se ordenan los objetos de mayor a menor segun su proporcion (valor/volumen)
def busqueda_heuristica():
    
    objetos_ord = sorted(objetos, reverse=True, key=lambda obj: obj.val/obj.med)
    mochila = cargar_mochila(objetos_ord)
    
    med_total = 0
    val_total = 0

    for i in mochila:
        med_total = med_total + i.med
        val_total = val_total + i.val
    
    print(">> BUSQUEDA HEURISTICA")
    print("El {} ocupado es {} y su valor total es ${}\n".format(medida, med_total, val_total))
    print("Los objetos elegidos son: ")
    for i in mochila:
        print(i)


#PROGRAMA_PRINCIPAL
print("-----------------------------------------------------")
print("\t\t>> MENU << \n 1 - Seleccionar objetos por VOLUMEN\n 2 - Seleccionar objetos por PESO")
opcMed = int(input("\nIngrese opcion: "))
if(opcMed == 1):
    objetos = [Objeto(1, 20, 150), Objeto(2, 40, 325), Objeto(3, 50, 600), Objeto(4, 36, 805), Objeto(5, 25, 430), Objeto(6, 64, 1200), Objeto(7, 54, 770), Objeto(8, 18, 60), Objeto(9, 46, 930), Objeto(10, 28, 353)]
    maxMedida = 4200
    medida = 'volumen'
elif(opcMed == 2):
    objetos = [Objeto(1, 72, 1800), Objeto(2, 36, 600), Objeto(3, 60, 1200)]
    maxMedida = 3000
    medida = 'peso'
else: 
    print("Opcion invalida")

print("-----------------------------------------------------")
print("1 - Busqueda Exhaustiva \n2 - Busqueda Heuristica")
opcBusq = int(input("\nIngrese opcion: "))
print("-----------------------------------------------------")
if(opcBusq == 1):
    busqueda_exhaustiva()
elif(opcBusq == 2): 
    busqueda_heuristica()
else: 
    print("Opcion invalida")
