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
        if airplanes_counter > airplanes or airplanes_counter > len(airport)-1:
            return 0
        
        if airplanes_counter > max_airplanes: max_airplanes = airplanes_counter

        events_counter += event
        if events_counter < 0: return 0
    
    if events_counter > 0: return 0

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
            if adjacent not in visited and airport[adjacent][0] == 0: visited.append(adjacent)
        i += 1

    visited.popleft()
    if len(airport['=='][2] & set(visited)) == 0: 
        for i in visited: airport[i][0] = 1

def unblock(airport, parking):

    visited = [parking]
    i = 0

    while i < len(visited):
        for adjacent in airport[visited[i]][2]:
            if adjacent not in visited and airport[adjacent][0] == 1 and airport[adjacent][1] == 0: visited.append(adjacent)
        i += 1
    
    if airport[parking][2] <= set(visited) and parking not in airport['=='][2]: return False
    else:
        airport[parking][1] = 0
        for i in visited:
            airport[i][0] = 0
            
        return True

def greedy(airport, events, max_airplanes):

    pending = deque()
    events_list = [x for x in events if x > 0]
    output = []

    while events or pending:

        if events: event = events.popleft()
        else: event = pending.popleft()

        if abs(event) in pending:
            pending.append(event)
            continue
        
        found = False

        if event > 0:

            available_parking = 0
            for i in airport.keys():
                if i != '==' and airport[i][0] == 0: available_parking += 1

            if available_parking >= max_airplanes:    
                for i in airport:
                    if i != '==' and airport[i][0] == 0:
                        block(airport, i, event)
                        output.append(i)
                        found = True
                        break

        else:
            for i in airport:
                if airport[i][1] == abs(event):
                    if unblock(airport, i):
                        found = True
                        break

        if not found:
            if event > 0:
                pending.append(event)
            else:
                position = events_list.index(abs(event))
                
                events_list.pop(position)
                events_list.append(abs(event))
                output.pop(position)
                
                pending.append(abs(event))
                pending.append(event)
        
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
        print()

        if max_airplanes == 0:
            print(f'Case {case_counter}: No')
            print()
        else:
            output = greedy(airport, events, max_airplanes)
            print(f'Case {case_counter}: Yes')
            for i in output:
                assigned_parking = str(i)
                if len(assigned_parking) == 1:
                    assigned_parking = '0'+assigned_parking
                print(assigned_parking, end=' ')
            print('\n')
            
        case_counter += 1

if __name__ == '__main__': main()