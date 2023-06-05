from collections import deque

archivo = open('input2.txt')

def verificar(aviones, aeropuerto, eventos):

    if '==' not in aeropuerto: return 0
    if len(aeropuerto) < 2: return 0

    contador_de_eventos = 0
    contador_de_aviones = 0
    máximos_aviones = 0

    for evento in eventos:
        
        if evento > 0: contador_de_aviones += 1
        else: contador_de_aviones -= 1
        if contador_de_aviones > aviones or contador_de_aviones > len(aeropuerto)-1: return 0
        
        if contador_de_aviones > máximos_aviones: máximos_aviones = contador_de_aviones

        contador_de_eventos += evento
        if contador_de_eventos < 0: return 0
    
    return máximos_aviones

def crear_aeropuerto(filas, columnas):

    matriz_input = []
    por_evaluar = deque()

    for i in range(filas):
        fila = archivo.readline().strip().split()

        for j in range(columnas):
            if fila[j] == '==': por_evaluar.append((i, j))
            elif fila[j] not in ['..', '##']: fila[j] = int(fila[j])
        
        matriz_input.append(fila)
    
    aeropuerto = {}
    coordenadas = [-1, 0, 0, 1, 1, 0, 0, -1]
    
    while por_evaluar:

        plaza_actual = por_evaluar.pop()
        aledaños_a_la_plaza = set()
        visitados_temporales = [plaza_actual]
        
        i = 0        
        while i < len(visitados_temporales):
            plaza_temporal = visitados_temporales[i]
           
            for j in range(0, 8, 2):

                x = plaza_temporal[0] + coordenadas[j]
                y = plaza_temporal[1] + coordenadas[j+1]
            
                if 0 <= x < len(matriz_input) and 0 <= y < len(matriz_input[0]):
                    if type(matriz_input[x][y]) == int and matriz_input[x][y] != matriz_input[plaza_actual[0]][plaza_actual[1]]:
                        aledaños_a_la_plaza.add(matriz_input[x][y])
                        if matriz_input[x][y] not in aeropuerto:
                            por_evaluar.append((x,y))
                    elif matriz_input[x][y] == '..' and (x,y) not in visitados_temporales: visitados_temporales.append((x, y))

            i += 1
        
        if matriz_input[plaza_actual[0]][plaza_actual[1]] in aeropuerto: aeropuerto[matriz_input[plaza_actual[0]][plaza_actual[1]]][2] = aeropuerto[matriz_input[plaza_actual[0]][plaza_actual[1]]][2] | aledaños_a_la_plaza
        else: aeropuerto[matriz_input[plaza_actual[0]][plaza_actual[1]]] = [0, 0, aledaños_a_la_plaza]

    return aeropuerto


def crear_historial(events):

    pila_historial = []
    for i in events: pila_historial.append([i, 0, 0])
    return pila_historial


def bloquear(aeropuerto, parqueadero, avión):

    # bloquea el parqueadero que se solicitó
    aeropuerto[parqueadero][0] = 1
    aeropuerto[parqueadero][1] = avión

    # busca los alcanzables, parqueaderos a los que se puede llegar sin pasar por el parqueadero que se va a tapar
    alcanzables = deque()
    alcanzables.append('==')
    i = 0
    while i < len(alcanzables):
        for adyacente in aeropuerto[alcanzables[i]][2]:
            if adyacente != parqueadero and adyacente not in alcanzables and aeropuerto[adyacente][0] == 0:
                alcanzables.append(adyacente)
        i += 1

    alcanzables.popleft()
    # si todos los aledaños son alcanzables, se para la ejecución de la función
    if aeropuerto[parqueadero][2] <= set(alcanzables): return
    # como no hay alcanzables, se bloquean todos los parqueaderos del aeropuerto y se para la ejecución
    elif len(alcanzables) == 0:
        for i in aeropuerto:
            if i != '==' and aeropuerto[i][0] != 1: aeropuerto[i][0] = 1
        return

    # como no todos están disponibles y no todos se pueden bloquear, se buscan aquellos que se pueden bloquear
    bloqueables = deque()
    bloqueables.append(parqueadero)
    i = 0
    while i < len(bloqueables):
        for adyacente in aeropuerto[bloqueables[i]][2]:
            if adyacente not in alcanzables and adyacente not in bloqueables and aeropuerto[adyacente][0] == 0:
                bloqueables.append(adyacente)
        i += 1
    
    for i in bloqueables: aeropuerto[i][0] = 1


def desbloquear(aeropuerto, parqueadero):

    desbloqueables = list(aeropuerto[parqueadero][2])
    i = 0

    # sacar los desocupados
    while i < len(desbloqueables) and desbloqueables:
        if aeropuerto[desbloqueables[i]][0] == 0: desbloqueables.pop(i)
        else: i += 1

    # si todos sus adyacentes estaban disponibles, se desocupa el espacio y ya
    if len(desbloqueables) == 0:
        aeropuerto[parqueadero][0] = 0
        aeropuerto[parqueadero][1] = 0
        return True
    
    # si todos sus adyacentes están ocupados, no se puede desocupar el espacio
    elif len(desbloqueables) == len(aeropuerto[parqueadero][2]) and parqueadero not in aeropuerto['=='][2]: return False

    # los que tengan un avión no se pueden desocupar, entonces se sacan de la pila
    i = 0
    while i < len(desbloqueables) and desbloqueables:
        if aeropuerto[desbloqueables[i]][1] != 0: desbloqueables.pop(i)
        else: i += 1

    # aquí mete todos los que está tapando el parqueadero que se quiere desocupar
    i = 0
    while i < len(desbloqueables):
        for adjacent in aeropuerto[desbloqueables[i]][2]:
            if adjacent != parqueadero and adjacent not in desbloqueables and aeropuerto[adjacent][0] == 1 and aeropuerto[adjacent][1] == 0:
                desbloqueables.append(adjacent)
        i += 1

    aeropuerto[parqueadero][0] = 0
    aeropuerto[parqueadero][1] = 0
    for j in desbloqueables: aeropuerto[j][0] = 0
    return True
    

def backtracking(aeropuerto, pila_historial, máximo_aviones): 

    puntero = 0

    while 0 <= puntero < len(pila_historial) and pila_historial[0][1] < len(aeropuerto):

        evento = pila_historial[puntero][0]
        encontrado = False

        if evento > 0:
            máximo_aviones -= 1
            for intento, parqueadero in enumerate(aeropuerto.keys()):
                if parqueadero != '==' and aeropuerto[parqueadero][0] == 0 and intento > pila_historial[puntero][1]:
                    bloquear(aeropuerto, parqueadero, evento)
                    encontrado = True
                    pila_historial[puntero][2] = parqueadero
                    pila_historial[puntero][1] = intento
                    break
                if intento > pila_historial[puntero][1]: pila_historial[puntero][1] = intento

            parqueaderos_disponibles = 0
            for j in aeropuerto.keys():
                if aeropuerto[j][0] == 0 and j != '==': parqueaderos_disponibles += 1
            if parqueaderos_disponibles < máximo_aviones and pila_historial[puntero][1] != len(aeropuerto)-1:
                desbloquear(aeropuerto, pila_historial[puntero][2])
                pila_historial[puntero][2] = 0
                máximo_aviones += 1
                continue
        

        else:

            máximo_aviones += 1

            for j in range(len(pila_historial)):
                if pila_historial[j][0]== abs(evento):
                    if desbloquear(aeropuerto, pila_historial[j][2]):
                        pila_historial[puntero][2] = pila_historial[j][2]
                        encontrado = True
                    break

            pila_historial[puntero][1] = len(aeropuerto) - 1
        

        if encontrado:
            puntero += 1
            continue 


        while pila_historial[puntero][1] == len(aeropuerto)-1:
            if pila_historial[puntero][0] > 0 and pila_historial[puntero][2] != 0:
                máximo_aviones += 1
                desbloquear(aeropuerto, pila_historial[puntero][2])
            elif pila_historial[puntero][0] < 0 and pila_historial[puntero][2] != 0:
                máximo_aviones -= 1
                bloquear(aeropuerto, pila_historial[puntero][2], abs(pila_historial[puntero][0]))
            pila_historial[puntero][1] = 0
            pila_historial[puntero][2] = 0
            puntero -= 1

        if puntero < 0: return []
        else:
            desbloquear(aeropuerto, pila_historial[puntero][2])
            pila_historial[puntero][2] = 0

    output = {pila_historial[j][0]: pila_historial[j][1] for j in range(len(pila_historial)) if pila_historial[j][0] > 0}
    return output


def main():

    contador_de_casos = 1
    while True:
    
        primera_línea = archivo.readline().strip()
        if primera_línea[0] == '0': break
        aviones, filas, columnas = map(int, primera_línea.split())

        aeropuerto = crear_aeropuerto(filas, columnas)

        eventos = deque(map(int, archivo.readline().strip().split()))
        máximos_aviones = verificar(aviones, aeropuerto, eventos)

        if máximos_aviones == 0:
            print(f'Case {contador_de_casos}: No\n')
        
        else:

            pila_historial = crear_historial(eventos)
            output = backtracking(aeropuerto, pila_historial, máximos_aviones)

            if len(output) > 0:

                print(f'Case {contador_de_casos}: Yes')
                
                for i in output:
                    parqueadero_asignado = str(output[i])
                    if len(parqueadero_asignado) == 1:
                        parqueadero_asignado = '0'+parqueadero_asignado
                    print(parqueadero_asignado, end=' ')
                print('\n')
            
            else: 
                print(f'Case {contador_de_casos}: No', '\n')

        contador_de_casos += 1


import time

start = time.time()
if __name__ == '__main__': main()
end = time.time()
print(end - start)

archivo.close()
