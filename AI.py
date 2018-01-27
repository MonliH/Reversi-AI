from reversi import *
import random
import numpy as np
import math
from copy import deepcopy

invalidMove = (-1, -1)
structure = [n * n, 2 * n * n, 2 * n * n, n * n]
population = 50
bestNetworksPopulation = 5
previousGeneration = 1271
mutationAmount = 0.05

# sigmoid function
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

# negative function
def negative(x):
  return -x

# evaluate the neural network
def evaluate(board, structure, weights, turn):
    layer = np.array(sum(board, [])) # first layer
    negativeForArray = np.vectorize(negative)
    if turn == w: # flip board ID for white
        layer = negativeForArray(layer)
    for i in range(1, len(structure)):
        layer = np.append(layer, 1) # add bias
        layer = np.dot(weights[i - 1], layer) # get next layer
        sigmoidForArray = np.vectorize(sigmoid)
        layer = sigmoidForArray(layer) # apply sigmoid function
    return layer

# choose the best move
def chooseMove(board, sturcture, weights, turn):
    results = evaluate(board, structure, weights, turn) # results of the nerual network
    validMoves = generateValidMovesList(board, turn) # list of value moves
    bestMove = invalidMove
    highestValue = -1
    for coordinates in validMoves: # choose best move
        valueOfCoordinates = results[n * coordinates[0] + coordinates[1]]
        if valueOfCoordinates > highestValue:
            highestValue = valueOfCoordinates
            bestMove = coordinates
    return bestMove

# generate random neural network
def generateNetwork(structure):    
    weights = []
    for i in range(len(structure) - 1):
        weights.append(np.array([[random.uniform(-1, 1) for _ in range(structure[i] + 1)] for _ in range(structure[i + 1])]))
    return weights

 # function for loading neural networks
def loadNetworks(structure, previousGeneration):
    with open("gen" + str(previousGeneration), "r") as file:
        lines = file.read().splitlines()
        for i in range(len(lines) - 1, -1, -1): # removing fitness information
            if lines[i][0] == "F":
                lines.pop(i)
           
        weightsList = sum([line.split("\t") for line in lines], [])

        weightsListIndex = 0
        networks = []

        while len(networks) < bestNetworksPopulation:
            weights = []
            for i in range(len(structure) - 1):
                layer = [[0 for _ in range(structure[i] + 1)] for _ in range(structure[i + 1])]
                for j in range(structure[i + 1]):
                    for k in range(structure[i] + 1):
                        layer[j][k] = float(weightsList[weightsListIndex])
                        weightsListIndex += 1
                weights.append(np.array(layer))
            networks.append(weights)

        return networks      

# function for saving neural networks
def saveNetworks(networks, sortedNetworksTuples, previousGeneration):
    file = open("gen" + str(previousGeneration), "w")
    for networkTuple in sortedNetworksTuples:
        fitness = networkTuple[0]
        file.write("Fitness:" + str(fitness) + "\n")
        networkIndex = networkTuple[1]
        for p in range(len(networks[networkIndex])):
            for q in range(len(networks[networkIndex][p])):
                file.write(str(networks[networkIndex][p][q][0]))
                for r in range(1, len(networks[networkIndex][p][q])):
                    file.write("\t" + str(networks[networkIndex][p][q][r]))
                file.write("\n")
    file.close()


if __name__ == "__main__":
    # create new set of neura networks if there is no previous generations
    if previousGeneration < 0:
        networks = [generateNetwork(structure) for _ in range(population)]
        
    while previousGeneration < 10000000:
        # repopulate
        if previousGeneration >= 0:
            # read networks from file if there is some previous generations
            networks = loadNetworks(structure, previousGeneration)
            bestNetworkPoplation = len(networks)

            # mutation
            for i in range(bestNetworkPoplation):
                for _ in range(5): # do 5 mutations for each neural network
                    newNetwork = deepcopy(networks[i])
                    for p in range(len(newNetwork)):
                        for q in range(len(newNetwork[p])):
                            for r in range(len(newNetwork[p][q])):
                                newNetwork[p][q][r] += random.uniform(-mutationAmount, mutationAmount)
                    networks.append(newNetwork)

            # crossover
            for i in range(bestNetworkPoplation):
                for j in range(bestNetworkPoplation):
                    if i != j:
                        for _ in range(2): # do 2 crossovers for each neural network
                            newNetwork = deepcopy(networks[i])
                            useNetworkJWeight = True if random.randrange(0, 1) < 0.5 else False
                            for p in range(len(newNetwork)):
                                for q in range(len(newNetwork[p])):
                                    for r in range(len(newNetwork[p][q])):
                                        useNetworkJWeight = not useNetworkJWeight \
                                        if random.randrange(0, 1) < 30/(8*n*n*n*n) else useNetworkJWeight
                                        if useNetworkJWeight:
                                            newNetwork[p][q][r] = networks[j][p][q][r]
                            networks.append(newNetwork)
      
        # play against each other
        previousGeneration += 1
        fitnesses = [0 for _ in range(population)]
        for i in range(population): # black
            for j in range(population): # white
                if i != j:
                    turn = b
                    board = generateBoard()
                    whiteCanPlay = True # if white is not stuck
                    blackCanPlay = True # if black is not stuck
                    while whiteCanPlay or blackCanPlay:
                        move = chooseMove(board, structure, networks[i if turn == b else j], turn)
                        if move == invalidMove:
                            if turn == w:
                                whiteCanPlay = False
                            if turn == b:
                                blackCanPlay = False
                        else :
                            if turn == w:
                                whiteCanPlay = True
                            if turn == b:
                                blackCanPlay = True
                            board = makeMove(board, move[0], move[1], turn)
                        # switching players
                        turn = opposite(turn)
                    # add to fitnesses
                    print("Generation " + str(previousGeneration) + ": network " + str(i), black, str(countChess(board, b)),"vs.", \
                          str(countChess(board, w)), white + " network " + str(j))
                    fitnesses[i] += countChess(board, b)
                    fitnesses[j] += countChess(board, w)
        fitnesses = [score /((population - 1) * 2) for score in fitnesses]
        print("Generation", previousGeneration, "Fitness: ", fitnesses)

        # sort networks according to fitnesses
        networksIndices = [i for i in range(len(networks))]
        sortedNetworksTuples = [(networksIndex, fitness) for networksIndex, fitness in reversed(sorted(zip(fitnesses, networksIndices)))]

        # eliminate
        sortedNetworksTuples = sortedNetworksTuples[ : bestNetworksPopulation]

        # save best networks in the population to file
        saveNetworks(networks, sortedNetworksTuples, previousGeneration)
