from collections import deque

def solution(bridge_length, weight, truck_weights):
    time = 0
    trucks = deque(truck_weights)
    bridge = deque([0] * bridge_length)
    current_weight = 0
    
    while bridge:
        time += 1
        
        exited_truck = bridge.popleft()
        current_weight -= exited_truck
        
        if trucks:
            if current_weight + trucks[0] <= weight:
                new_truck = trucks.popleft()
                bridge.append(new_truck)
                current_weight += new_truck
            else:
                bridge.append(0)
    
    return time