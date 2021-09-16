import cirq
from arithmetic.Multiplier import multiplier
from arithmetic.Control_add import ctrl_add

def main():
    circuit = cirq.Circuit()
    choice = int(input("1. Add two numbers\n2. Multiply two numbers\n3. Multiply the first n numbers together"))
    if(choice == 1):
        testAdd(circuit)
    if(choice == 2):
        testMultiply(circuit)
    if(choice == 3):
        exampleMultiply()

    # simulator = cirq.Simulator()
    # result = simulator.run(circuit)

    # print(circuit)
    # print(result)

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

def testMultiply(circuit, num1, num2):  #overloaded for the purposes of exampleMultiply
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
            testMultiply(circuit, i, j)
            simulator = cirq.Simulator()
            result = simulator.run(circuit)

            # print(circuit)
            print(i, "*", j, "=")
            print(result)
    return;


if __name__ == '__main__':
    main()