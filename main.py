import cirq

n = 4

# set up qubits (for an n-bit multiplication, there are n 'a' qubits, n 'b' qubits, 2n output qubits, 1 ancillary qubit)
qubitsA, qubitsB, qubitsOut = [(cirq.GridQubit(0, i) for i in range(n)), (cirq.GridQubit(1, i) for i in range(n)), (cirq.GridQubit(2, j) for j in range(2*n+1))]
# ^^ sets up a qubits as [0][n] and b qubits as [1][n], outputqubits as [2][n]
circuit = cirq.Circuit()

# testing qubit setup
# circuit.append(cirq.H(q) for q in qubitsA)
# circuit.append(cirq.Z(q) for q in qubitsB)
# circuit.append(cirq.X(q) for q in qubitsOut)

#def the following as ctrl_add with b[1] as the ctrl, a[1:n] as the bits of one summand, and
# stores the sum of a and b in b if ctrl:
#step 1:
for i in range(1, n):
    circuit.append(cirq.CNOT(cirq.GridQubit(0, i), cirq.GridQubit(1, i)))
#step 2:


print(qubitsA)
print(qubitsB)
print(qubitsOut)
print(circuit)