import cirq

# testing qubit setup
# circuit.append(cirq.H(q) for q in qubitsA)
# circuit.append(cirq.Z(q) for q in qubitsB)
# circuit.append(cirq.X(q) for q in qubitsOut)


"""
Pseudocode for full multiplier:

//step 1: toffolis
for(int i = 0; i < n; i++)
{
    toffoli(qubitsSumnB(0), qubitsSumnA(i), qubitsOut(i);
}

//step 2: ctrladd
for(int i = 0; i < n+1; i++)
{
    ctrladd(qubitsSumnB(1), qubitsSumnA(0:i-1), qubitsOut(0:i))
}

for(int i = 0; i < n+1; i++)
{
    ctrladd(qubitsSumnB(i), qubitsSumnA, qubitsOut(i:i+n+1)) //ctrl on qubitsSumnB[i], sum mapped to qubitsOut[i:i+n-1],
    //the last qubit in qubitsOut(i:i+n) is ancillary. Also it may be n+2 instead of n+1, not sure.
}

"""


# def the following as ctrl_add with ctrl as the ctrl, qubitsSumnA as the bits of one summand, and qubitsSumnB as the
# bits of the other, with the result stored in qubitsSumnB. qubitsSumnA[n] is ancillary, qubitsSumnB[n] = s[4] dot ctrl
# NOTE: The Coreas-Thapliyal paper defines the ancillary bit as A[n+1] and the final sum bit as A[n]. I define them as
# B[n], B[n+1] respectively to stay consistent with the definitions in the multiplier.
def ctrl_add(circuit, ctrl, qubitsSumnA, qubitsSumnB):
    n = len(qubitsSumnB) - 2

    # step 1
    for i in range(1, n):
        circuit.append(cirq.CNOT(qubitsSumnA[i], qubitsSumnB[i]))

    # step 2:
    circuit.append(cirq.TOFFOLI(ctrl, qubitsSumnA[n - 1], qubitsSumnB[n]))
    for i in range(n - 2, 0, -1):
        circuit.append(cirq.CNOT(qubitsSumnA[i], qubitsSumnA[i + 1]))

    # step 3:
    for i in range(0, n - 1):
        circuit.append(cirq.TOFFOLI(qubitsSumnA[i], qubitsSumnB[i], qubitsSumnA[i + 1]))

    # step 4:
    circuit.append(cirq.TOFFOLI(qubitsSumnA[n - 1], qubitsSumnB[n - 1], qubitsSumnB[n+1]))
    circuit.append(cirq.TOFFOLI(ctrl, qubitsSumnB[n+1], qubitsSumnB[n]))
    circuit.append(cirq.TOFFOLI(qubitsSumnA[n - 1], qubitsSumnB[n - 1], qubitsSumnB[n+1]))
    circuit.append(cirq.TOFFOLI(ctrl, qubitsSumnA[n - 1], qubitsSumnB[n - 1]))

    # step 5:
    for i in range(n - 2, -1, -1):
        circuit.append(cirq.TOFFOLI(qubitsSumnA[i], qubitsSumnB[i], qubitsSumnA[i + 1]))
        circuit.append(cirq.TOFFOLI(ctrl, qubitsSumnA[i], qubitsSumnB[i]))

    # step 6:
    for i in range(1, n - 1):
        circuit.append(cirq.CNOT(qubitsSumnA[i], qubitsSumnA[i + 1]))

    # step 7:
    for i in range(1, n):
        circuit.append(cirq.CNOT(qubitsSumnA[i], qubitsSumnB[i]))

    return;


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
    ctrl_add(circuit, ctrl, qubitsTestA, qubitsTestB)
    circuit.append(cirq.measure(qubitsTestB[i]) for i in range(size+2))
    return;

def multiply(circuit, qubitsInA, qubitsInB, qubitsOut): # does not work for two ints using diff number of bits e.g. 7+8 does not work
    n = len(qubitsInA)
    # step 1: toffolis
    for i in range(0,n):
        circuit.append(cirq.TOFFOLI(qubitsInB[0], qubitsInA[i], qubitsOut[i]))
    # step 2 (and 3):
    for i in range(1, n):
        ctrl_add(circuit, qubitsInB[i], qubitsInA, qubitsOut[i:i+n+2])
    return;

def testMultiply(circuit):
    num1 = int(input("Enter the first number to be multiplied"))
    num2 = int(input("Enter the second number to be multiplied"))
    size = (len(bin(max(num1, num2))))
    size -= 2
    qubitsTestA = [cirq.GridQubit(0, i) for i in range(size)]
    qubitsTestB = [cirq.GridQubit(1, i) for i in range(size)]
    i = size - 1
    for bit in (bin(num1)[2:]):
        # print("num1 bit " + str(i) + " = " + bit)
        if bit == '1':
            circuit.append(cirq.X.on(qubitsTestA[i]))
        i -= 1
    i = size - 1
    for bit in (bin(num2)[2:]):
        # print("num2 bit " + str(i) + " = " + bit)
        if bit == '1':
            circuit.append(cirq.X.on(qubitsTestB[i]))
        i -= 1
    qubitsTestOut = [cirq.GridQubit(2, i) for i in range(2*size + 1)]
    multiply(circuit, qubitsTestA, qubitsTestB, qubitsTestOut)
    circuit.append(cirq.measure(qubitsTestOut[i]) for i in range(2*size + 1))
    return;

def main():
    length = 4

    # set up qubits (for an n-bit multiplication, there are n 'a' qubits, n 'b' qubits, 2n output qubits, 1 ancillary qubit)
    # qubitsA, qubitsB, qubitsOut = [(cirq.GridQubit(0, i) for i in range(n)), (cirq.GridQubit(1, i) for i in range(n)),
    #   ^^ this is wrong for some reason        (cirq.GridQubit(2, j) for j in range(2 * n + 1))]

    # qubitsA = [cirq.GridQubit(0, i) for i in range(length)]
    # qubitsB = [cirq.GridQubit(1, i) for i in range(length)]
    # qubitsOut = [cirq.GridQubit(2, i) for i in range(2 * length + 1)]
    # ^^ sets up a qubits as [0][n], b qubits as [1][n], outputqubits as [2][n]

    circuit = cirq.Circuit()

    # ctrl_add(circuit, qubitsB[0], qubitsA, qubitsOut[1:6])
    # multiply(circuit, qubitsA, qubitsB, qubitsOut)

    # testAdd(circuit)
    testMultiply(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit)

    # print(qubitsA)
    # print(qubitsB)
    # print(qubitsOut)
    # print(qubitSumTestctrl)
    # print(qubitsSumTest9)
    # print(qubitsSumTest11)
    print(circuit)
    print(result)

if __name__ == '__main__':
    main()

