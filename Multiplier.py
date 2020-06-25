import cirq
from arithmetic.Control_add import ctrl_add
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

class multiplier:

    def __init__(self, A, B, out):
        self.size = len(A)
        self.A = A
        self.B = B
        self.out = out

    def multiply(self):
        circuit = cirq.Circuit()
        # step 1: toffolis
        for i in range(0, self.size):
            circuit.append(cirq.TOFFOLI(self.B[0], self.A[i], self.out[i]))
        # step 2 (and 3):
        for i in range(1, self.size):
            circuit += ctrl_add(self.B[i], self.A, self.out[i:i+self.size+2]).construct_circuit()
        return circuit;
