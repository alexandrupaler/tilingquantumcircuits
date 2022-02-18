import cirq

class ctrl_add:

    def __init__(self, ctrl, A, B):
        self.size = len(B) - 2
        self.ctrl = ctrl
        self.A = A
        self.B = B

    def construct_circuit(self):
        circuit = cirq.Circuit()
        cnotcount = 0
        toffcount = 0

        # step 1
        for i in range(1, self.size):
            circuit.append(cirq.CNOT(self.A[i], self.B[i]))
            cnotcount += 1

        # step 2:
        circuit.append(cirq.decompose(cirq.TOFFOLI(self.ctrl, self.A[self.size - 1], self.B[self.size])))
        toffcount += 1
        for i in range(self.size - 2, 0, -1):
            circuit.append(cirq.CNOT(self.A[i], self.A[i + 1]))
            cnotcount += 1

        # step 3:
        for i in range(0, self.size - 1):
            circuit.append(cirq.decompose(cirq.TOFFOLI(self.A[i], self.B[i], self.A[i + 1])))
            toffcount += 1

        # step 4:
        circuit.append(cirq.decompose(cirq.TOFFOLI(self.A[self.size - 1], self.B[self.size - 1], self.B[self.size+1])))
        circuit.append(cirq.decompose(cirq.TOFFOLI(self.ctrl, self.B[self.size+1], self.B[self.size])))
        circuit.append(cirq.decompose(cirq.TOFFOLI(self.A[self.size - 1], self.B[self.size - 1], self.B[self.size+1])))
        circuit.append(cirq.decompose(cirq.TOFFOLI(self.ctrl, self.A[self.size - 1], self.B[self.size - 1])))
        toffcount += 4

        # step 5:
        for i in range(self.size - 2, -1, -1):
            circuit.append(cirq.decompose(cirq.TOFFOLI(self.A[i], self.B[i], self.A[i + 1])))
            circuit.append(cirq.decompose(cirq.TOFFOLI(self.ctrl, self.A[i], self.B[i])))
            toffcount += 2

        # step 6:
        for i in range(1, self.size - 1):
            circuit.append(cirq.CNOT(self.A[i], self.A[i + 1]))
            cnotcount += 1

        # step 7:
        for i in range(1, self.size):
            circuit.append(cirq.CNOT(self.A[i], self.B[i]))
            cnotcount += 1

        print("toffoli count in adder")
        print(toffcount)
        print("cnot count in adder")
        print(cnotcount)

        return circuit

    # Toff: n + 4 + 2(n-1)
    # CNOT: