import time 
import psutil

def testing(function, words):
  for word in words:
    function(word)
    

def levenshtein_distance(s1, s2):
  # Base cases
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    
    if s1[0] == s2[0]:
        return levenshtein_distance(s1[1:], s2[1:])
    
    # Calculate the cost of different operations
    delete_cost = levenshtein_distance(s1[1:], s2) + 1
    insert_cost = levenshtein_distance(s1, s2[1:]) + 1
    substitute_cost = levenshtein_distance(s1[1:], s2[1:]) + 1
    
    # Return the minimum cost among the operations
    return min(delete_cost, insert_cost, substitute_cost)

process = psutil.Process()
start_time = time.time()
start_cpu = process.cpu_percent()
start_ram = process.memory_info().rss / (1024 * 1024)

print(levenshtein_distance(s1= 'fgtfw', s2 = 'rdgkljjiiogjljsglksjgsklgjslksgjslkjgklsjgskljhj'))


end_time = time.time()
end_cpu = process.cpu_percent()
end_ram = process.memory_info().rss / (1024 * 1024)  # RAM usage in MB
execution_time = (end_time - start_time).__round__(2)
cpu_usage = end_cpu - start_cpu
ram_usage = end_ram - start_ram

print("Execution time:", execution_time, "seconds")
print("CPU usage:", cpu_usage, "%")
print("RAM usage:", ram_usage, "MB")