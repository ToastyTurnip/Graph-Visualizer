import Graph

file = open("minimax.txt")
lines = file.read()
graph = Graph.CreateGraph("mygraph", lines)    
#graph.printALL()

states = list()

def minimaxpruning(node, depth, alpha, beta, isMaximizing):
    if len(node.GetChildren()) == 0:
        return int(node.params['value'])

    if isMaximizing:
        maxEval = -9999
        for child in node.GetChildren():
            evalu = minimaxpruning(child, None, alpha, beta, False)
            maxEval = max(maxEval, evalu)
            alpha = max(alpha, evalu)
            node.params['alpha'] = alpha
            if beta <= alpha:
                print("Prune!")
                break
        node.params['value'] = maxEval
        states.append(graph.CaptureState())
        return maxEval

    else:
        minEval = 9999
        for child in node.GetChildren():
            evalu = minimaxpruning(child, None, alpha, beta, True)
            minEval = min(minEval, evalu)
            beta = min(beta, evalu)
            node.params['beta'] = beta
            if beta <= alpha:
                print("Prune!")
                break
        node.params['value'] = minEval
        states.append(graph.CaptureState())
        return minEval
    
RESULT = minimaxpruning(graph.nodes[0], None, -9999, 9999, True)
