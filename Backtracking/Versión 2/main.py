from collections import deque

def verify(airplanes, airport, events):

    if '==' not in airport: return 0
    if len(airport) < 2: return 0

    events_counter = 0
    airplanes_counter = 0
    max_airplanes = 0

    for event in events:
        
        if event > 0: airplanes_counter += 1
        else: airplanes_counter -= 1
        if airplanes_counter > airplanes or airplanes_counter > len(airport)-1: return 0
        
        if airplanes_counter > max_airplanes: max_airplanes = airplanes_counter

        events_counter += event
        if events_counter < 0: return 0
    
    return max_airplanes

def adjacency_list(rows, columns):

    matrix = []
    to_check = deque()

    for i in range(rows):
        row = input().split()

        for j in range(columns):
            if row[j] == '==': to_check.append((i, j))
            elif row[j] not in ['..', '##']: row[j] = int(row[j])
        
        matrix.append(row)
    
    airport = {}
    coordinates = [-1, 0, 0, 1, 1, 0, 0, -1]
    
    while to_check:

        point = to_check.pop()
        point_set = set()
        temporal_visited = [point]
        
        i = 0        
        while i < len(temporal_visited):
            temporal_point = temporal_visited[i]
           
            for j in range(0, 8, 2):

                x = temporal_point[0] + coordinates[j]
                y = temporal_point[1] + coordinates[j+1]
            
                if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
                    if type(matrix[x][y]) == int and matrix[x][y] != matrix[point[0]][point[1]]:
                        point_set.add(matrix[x][y])
                        if matrix[x][y] not in airport:
                            to_check.append((x,y))
                    elif matrix[x][y] == '..' and (x,y) not in temporal_visited: temporal_visited.append((x, y))

            i += 1
        
        if matrix[point[0]][point[1]] in airport: airport[matrix[point[0]][point[1]]][2] = airport[matrix[point[0]][point[1]]][2] | point_set
        else: airport[matrix[point[0]][point[1]]] = [0, 0, point_set]

    return airport

def block(airport, parking, plane):

    airport[parking][0] = 1
    airport[parking][1] = plane
    visited = deque()
    visited.append(parking)
    i = 0

    while i < len(visited):
        for adjacent in airport[visited[i]][2]:
            if adjacent not in visited and airport[adjacent][0] == 0 and adjacent not in airport['=='][2]: visited.append(adjacent)
        i += 1

    visited.popleft()
    
    if len(airport['=='][2] & set(visited)) == 0: 
        for j in visited: airport[j][0] = 1
    
    else:
        accesible = [adjacent for adjacent in airport['=='][2]]
        
        i = 0
        while i < len(accesible):
            for adjacent in airport[accesible[i]][2]:
                if adjacent not in accesible and airport[adjacent][0] == 0 and adjacent != parking: accesible.append(adjacent)
            i += 1

        difference = set(visited) - set(accesible) 
        for j in set(difference): airport[j][0] = 1

def unblock(airport, parking):

    visited = list(airport[parking][2])
    i = 0
    while i < len(visited) and visited:
        if airport[visited[i]][0] == 0: visited.pop(i)
        else: i += 1

    if len(visited) == 0:
        airport[parking][0] = 0
        airport[parking][1] = 0
        return True
    elif len(visited) == len(airport[parking][2]) and parking not in airport['=='][2]: return False

    i = 0
    while i < len(visited) and visited:
        if airport[visited[i]][1] != 0: visited.pop(i)
        else: i += 1

    i = 0
    while i < len(visited):
        for adjacent in airport[visited[i]][2]:
            if adjacent not in visited and airport[adjacent][0] == 1: visited.append(adjacent)
        i += 1

    airport[parking][0] = 0
    airport[parking][1] = 0
    for j in visited: airport[j][0] = 0
    return True
    
def historial(events):

    historial_matrix = []
    for i in events: historial_matrix.append([i, 0, 0])
    return historial_matrix

def backtracking(airport, historial_matrix, max_airplanes): 

    i = 0
    while 0 <= i < len(historial_matrix) and historial_matrix[0][1] < len(airport):
        event = historial_matrix[i][0]
        found = False

        if event > 0:
            max_airplanes -= 1
            for attemp, parking in enumerate(airport.keys()):
                if parking != '==' and airport[parking][0] == 0 and attemp > historial_matrix[i][1]:
                    block(airport, parking, event)
                    found = True
                    historial_matrix[i][2] = parking
                    historial_matrix[i][1] = attemp
                    break
                if attemp > historial_matrix[i][1]: historial_matrix[i][1] = attemp

            parqueaderos_disponibles = 0
            for j in airport.keys():
                if airport[j][0] == 0 and airport[j][0] != '==': parqueaderos_disponibles += 1
            if parqueaderos_disponibles < max_airplanes and historial_matrix[i][1] != len(airport)-1:
                unblock(airport, historial_matrix[i][2])
                max_airplanes += 1
                continue
        
        else:
            max_airplanes += 1
            for j in range(len(historial_matrix)):
                if historial_matrix[j][0]== abs(event):
                    if unblock(airport, historial_matrix[j][2]):
                        historial_matrix[i][2] = historial_matrix[j][2]
                        found = True
                    break
            historial_matrix[i][1] = len(airport) - 1
        
        if found:
            i += 1
            continue 

        while historial_matrix[i][1] == len(airport)-1:
            if historial_matrix[i][0] > 0 and historial_matrix[i][2] != 0:
                max_airplanes += 1
                unblock(airport, historial_matrix[i][2])
            elif historial_matrix[i][0] < 0 and historial_matrix[i][2] != 0:
                max_airplanes -= 1
                block(airport, historial_matrix[i][2], abs(historial_matrix[i][0]))
            historial_matrix[i][1] = 0
            i -= 1

        if i < 0: return []
        else:
            unblock(airport, historial_matrix[i][2])
            historial_matrix[i][2] = 0

    output = {historial_matrix[j][0]: historial_matrix[j][1] for j in range(len(historial_matrix)) if historial_matrix[j][0] > 0}
    return output

def main():

    case_counter = 1
    while True:
    
        first_line = input()
        if first_line[0] == '0': break
        airplanes, rows, columns = map(int, first_line.split())

        airport = adjacency_list(rows, columns)

        events = deque(map(int, input().split()))
        max_airplanes = verify(airplanes, airport, events)

        if max_airplanes == 0:
            print(f'Case {case_counter}: No')
            print()
        
        else:
            historial_matrix = historial(events)
            output = backtracking(airport, historial_matrix, max_airplanes)

            if len(output) > 0:
                print(f'Case {case_counter}: Yes')
                for i in range(len(output)):
                    assigned_parking = str(output[i+1])
                    if len(assigned_parking) == 1:
                        assigned_parking = '0'+assigned_parking
                    print(assigned_parking, end=' ')
                print('\n')
            
            else: 
                print(f'Case {case_counter}: No', '\n')

        case_counter += 1

import time

start = time.time()
if __name__ == '__main__': main()
end = time.time()
print(end - start)
