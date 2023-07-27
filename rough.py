visited = [] # List for visited nodes.
queue = []     #Initialize a queue

def bfs(node): #function for BFS
    print(node)
    visited.append(node)
    queue.append(node)
    print('visited', visited)
    while len(queue) != 0:     # Creating loop to visit each node
        m =  queue.pop(0) 

        print(m)

        if(m[0]>1):
            # print('hello')
            n = [m[0]-1, m[1]]
            # print(n)
        
        if n not in visited:
            # print("hello", visited)
            visited.append(n)
            queue.append(n)

        if(m[0]<9):
            n = [m[0]+1, m[1]]
        
        if n not in visited:
            visited.append(n)
            queue.append(n)

        if(m[1]>1):
            n = [m[0], m[1]-1]
        
        if n not in visited:
            visited.append(n)
            queue.append(n)

        if(m[1]<9):
            n = [m[0], m[1]+1]
        
        if n not in visited:
            visited.append(n)
            queue.append(n)

    



node  = [5,5]


# Driver Code
print("Following is the Breadth-First Search")
bfs(node)    # function calling