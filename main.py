
import cirq
from cirq import ops
from cirq_pasqal import ThreeDQubit, TwoDQubit, PasqalVirtualDevice, PasqalNoiseModel
import cirq.contrib.routing as ccr
from cirq.contrib.routing.greedy import route_circuit_greedily
from Multiplier import multiplier
from Control_add import ctrl_add
import networkx as nx
import itertools
from typing import Iterable
import sys

from multiprocessing import Process

""" Mirror contrib.routing.greedy_test.py"""

def main():
    circuit = cirq.Circuit()

    """ASSUMES AN EXISTING FILE OF THE NAME cirq_test_out.txt !!!!!!"""
    f = open("cirq_test_out.txt", "a")
    exTestMultiply(circuit, 11, 12)
    """choice = int(input("1. Add two numbers\n2. Multiply two numbers\n3. Multiply the first n numbers together"))
    if(choice == 1):
        testAdd(circuit)
    if(choice == 2):
        testMultiply(circuit)
    if(choice == 3):
        exampleMultiply()"""

    simulator = cirq.Simulator()
    result = simulator.run(circuit)

    #print(circuit)
    #f.write(str(circuit))
    #print(result)
    circdep = 0
    for moment in circuit:
        circdep+=1
    #print(circdep)
    #print("Now running tests: ")
    if(int(sys.argv[1]) == 3):
        width = int(sys.argv[2])
        height = int(sys.argv[3])
        depth = int(sys.argv[4])
        p_qubits = [ThreeDQubit(row, col, lay)
                    for row in range(width)
                    for col in range(height)
                    for lay in range(depth)]
        device_graph = nx.Graph(
            pair for pair in itertools.combinations(p_qubits, 2) if _my_manhattan_distance(*pair) == 1
        )
    if(int(sys.argv[1]) == 2):
       device_graph = ccr.get_grid_device_graph(int(sys.argv[2]), int(sys.argv[3]))

    sn = ccr.greedy.route_circuit_greedily(circuit, device_graph, max_search_radius=3, random_state=1) # This random seed is the reason for variation
    #print(str(sn))

    swapcount = 0
    swapdepth = 0
    for moment in sn.circuit:
        temp = swapcount
        for op in moment:
            if len(op.qubits) == 2:
                #print(op.gate)
                if op.gate == cirq.contrib.acquaintance.SwapPermutationGate():
                    swapcount += 1
        if temp != swapcount:
            swapdepth += 1
    if(int(sys.argv[1]) == 2):
        outputdimdata = [sys.argv[2], " by ", sys.argv[3], "\n"]
    if(int(sys.argv[1]) == 3):
        outputdimdata = [sys.argv[2], " by ", sys.argv[3], " by ", sys.argv[4], "\n"]
    testoutput = ["SWAP count: ", str(swapcount), "\nSWAP depth: ", str(swapdepth), "\n"]
    f.writelines(outputdimdata)
    f.writelines(testoutput)
    """for moment:
            for gate:
                    is swap?"""

    f.close()

def _my_manhattan_distance(qubit1: ThreeDQubit, qubit2: ThreeDQubit) -> int: # mirrors ccr._manhattan_distance()
    return abs(qubit1.distance(qubit2))

def testAdd(circuit): # does not work for two ints using diff number of bits e.g. 7+8 does not work
    num1 = int(input("Enter the first summand"))
    num2 = int(input("Enter the second summand"))
    size = (len(bin(max(num1, num2))))
    size -= 2
    qubitsTestA = [cirq.GridQubit(0, i) for i in range(size)]
    qubitsTestB = [cirq.GridQubit(1, i) for i in range(size + 2)]
    ctrl = cirq.GridQubit(2,0)
    circuit.append(cirq.X.on(ctrl))
    i = size-1
    for bit in (bin(num1)[2:]):
        if bit == '1':
            circuit.append(cirq.X.on(qubitsTestA[i]))
        i -= 1
    i = size-1
    for bit in (bin(num2)[2:]):
        print("bit " + str(i) + " = " + bit)
        if bit == '1':
            circuit.append(cirq.X.on(qubitsTestB[i]))
        i -= 1
    circuit += ctrl_add(ctrl, qubitsTestA, qubitsTestB).construct_circuit()
    circuit.append(cirq.measure(qubitsTestB[i]) for i in range(size+2))
    #TODO: this is wrong, returns the largest of the two summands rather than the actual sum, likely due to the above line.
    return;

def testMultiply(circuit):
    num1 = int(input("Enter the first number to be multiplied"))
    num2 = int(input("Enter the second number to be multiplied"))
    size = (len(bin(max(num1, num2))))
    size -= 2

    qubitsTestA = [cirq.GridQubit(0, i) for i in range(size)]
    qubitsTestB = [cirq.GridQubit(1, i) for i in range(size)]

    i = 0

    for bit in reversed((bin(num1)[2:])):
        # print("num1 bit " + str(i) + " = " + bit)
        if bit == '1':
            circuit.append(cirq.X.on(qubitsTestA[i]))
        i += 1
    i = 0
    for bit in reversed((bin(num2)[2:])):
        # print("num2 bit " + str(i) + " = " + bit)
        if bit == '1':
            circuit.append(cirq.X.on(qubitsTestB[i]))
        i += 1
    qubitsTestOut = [cirq.GridQubit(2, i) for i in range(2*size + 1)]
    circuit += multiplier(qubitsTestA, qubitsTestB, qubitsTestOut).multiply()
    circuit.append(cirq.measure(qubitsTestOut[i]) for i in range(2*size + 1))
    return;

def exTestMultiply(circuit, num1, num2):  #overloaded for the purposes of exampleMultiply
    size = (len(bin(max(num1, num2))))
    size -= 2

    qubitsTestA = [cirq.GridQubit(0, i) for i in range(size)]
    qubitsTestB = [cirq.GridQubit(1, i) for i in range(size)]

    i = 0

    for bit in reversed((bin(num1)[2:])):
        # print("num1 bit " + str(i) + " = " + bit)
        if bit == '1':
            circuit.append(cirq.X.on(qubitsTestA[i]))
        i += 1
    i = 0
    for bit in reversed((bin(num2)[2:])):
        # print("num2 bit " + str(i) + " = " + bit)
        if bit == '1':
            circuit.append(cirq.X.on(qubitsTestB[i]))
        i += 1
    qubitsTestOut = [cirq.GridQubit(2, i) for i in range(2*size + 1)]
    circuit += multiplier(qubitsTestA, qubitsTestB, qubitsTestOut).multiply()
    circuit.append(cirq.measure(qubitsTestOut[i]) for i in range(2*size + 1))
    return;

def exampleMultiply():
    num = int(input("The program will multiply every number between 1 and the number you enter inclusive. Enter the range: "))
    for i in range(1,num+1):
        for j in range(1, num+1):
            circuit = cirq.Circuit()
            exTestMultiply(circuit, i, j)
            simulator = cirq.Simulator()
            result = simulator.run(circuit)

            # print(circuit)
            print(i, "*", j, "=")
            print(result)
    return;


if __name__ == '__main__':
    main()
