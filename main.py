import cirq

# testing qubit setup
# circuit.append(cirq.H(q) for q in qubitsA)
# circuit.append(cirq.Z(q) for q in qubitsB)
# circuit.append(cirq.X(q) for q in qubitsOut)

# def the following as ctrl_add with ctrl as the ctrl, qubitsSumnA as the bits of one summand, and qubitsSumnB as the
# bits of the other, with the result stored in qubitsSumnB. qubitsSumnA[n] is ancillary, qubitsSumnB[n] = s[4] dot ctrl
def ctrl_add (circuit, ctrl, qubitsSumnA, qubitsSumnB):      # circuit is possibly unnecessary, n is definitely unnecessary
    n = len(qubitsSumnB) - 1

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
    circuit.append(cirq.TOFFOLI(qubitsSumnA[n - 1], qubitsSumnB[n - 1], qubitsSumnA[n]))
    circuit.append(cirq.TOFFOLI(ctrl, qubitsSumnA[n], qubitsSumnB[n]))
    circuit.append(cirq.TOFFOLI(qubitsSumnA[n - 1], qubitsSumnB[n - 1], qubitsSumnA[n]))
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

def main():
    length = 4

    # set up qubits (for an n-bit multiplication, there are n 'a' qubits, n 'b' qubits, 2n output qubits, 1 ancillary qubit)
    # qubitsA, qubitsB, qubitsOut = [(cirq.GridQubit(0, i) for i in range(n)), (cirq.GridQubit(1, i) for i in range(n)),
    #   ^^ this is wrong for some reason        (cirq.GridQubit(2, j) for j in range(2 * n + 1))]
    qubitsA = [cirq.GridQubit(0, i) for i in range(length+1)]       # right now the +1 on a creates a convenient ancillary qubit
    qubitsB = [cirq.GridQubit(1, i) for i in range(length)]         # that in reality belongs as the +1 on qubitsOut
    qubitsOut = [cirq.GridQubit(2, i) for i in range(2 * length + 1)]
    # ^^ sets up a qubits as [0][n] and b qubits as [1][n], outputqubits as [2][n]
    circuit = cirq.Circuit()

    ctrl_add(circuit, qubitsB[0], qubitsA, qubitsOut[1:6])

    print(qubitsA)
    print(qubitsB)
    print(qubitsOut)
    print(circuit)

if __name__ == '__main__':
    main()

