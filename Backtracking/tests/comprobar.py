# comprobar si los eventos y parqueaderos no se cruzan

from collections import deque

def comprobar():

    eventos = [int(x) for x in input().split()]
    output = [int(x) for x in input().split()]
    print()

    parqueaderos = {}
    puntero = 0
    for evento in eventos:
        if evento > 0:
            parqueaderos[evento] = output[puntero]
            puntero += 1

    aeropuerto = {}
    for i in output:
        if i not in aeropuerto: aeropuerto[i] = 0

    puntero = 0
    for evento in eventos:
        if evento > 0: 
            if aeropuerto[output[puntero]] == 0: aeropuerto[output[puntero]] = evento
            else: print('papi, error porque ya estaba ocupao')
            puntero += 1
        else:
            if aeropuerto[parqueaderos[abs(evento)]] != 0: aeropuerto[parqueaderos[abs(evento)]] = 0
            else: print('papi, error porque estaba desocupado')
        
        for i in aeropuerto:
            if evento > 0 and i == parqueaderos[evento]: print(f'parqueadero {i}:', aeropuerto[i], '--> entró avión')
            elif evento < 0 and i == parqueaderos[abs(evento)]: print(f'parqueadero {i}:', 0, '<-- salió avión', abs(evento))
            else: print(f'parqueadero {i}:' , aeropuerto[i])
        print()

    for i in aeropuerto: print(f'parqueadero {i}:' , aeropuerto[i])
    print()

comprobar()