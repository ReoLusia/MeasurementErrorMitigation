#!/usr/bin/env python
# coding: utf-8

# In[12]:


from qiskit import QuantumCircuit, QuantumRegister, Aer, transpile
from qiskit.visualization import plot_distribution
import copy
import math

class MeasurementErrorMitigation:
    def __init__(self, 
                 quantum_circuit: QuantumCircuit
                ) -> None:
        self.quantum_circuit = quantum_circuit
        self.num_qubits = self.quantum_circuit.num_qubits
        self.backend = Aer.get_backend('qasm_simulator')
    
    """ Check variable 'quantum_circuit' """
    @property
    def quantum_circuit(self) -> QuantumCircuit:
        return self.__quantum_circuit
    
    @quantum_circuit.setter
    def quantum_circuit(self, 
                        quantum_circuit: QuantumCircuit
                       ) -> None:
        
        if type(quantum_circuit) == QuantumCircuit:
            self.__quantum_circuit = quantum_circuit
        else:
            raise ValueError('Invalue variable type: quantum_circuit')
    
    """ Construct quantum circuit with twirling """
    def ConstructQC(self, 
                    unitary_index: int
                   ) -> QuantumCircuit:
        # Construct quantum circuit
        qc = copy.deepcopy(self.quantum_circuit)
        
        # Apply twirling
        qc.append(TwirlingCircuit(unitary_index, self.num_qubits), [i for i in range(self.num_qubits)])

        # Apply measurement
        qc.measure_all()

        return qc
    
    """ Simulate quantum circuit and post-processing """
    def SimulationQC(self, 
                     unitary_index_set=[1,5,9], 
                     eta=0.1) -> None:
        ## Quantum pre-processing
        # Variable setting
        counts = {}

        # Apply 3 unitray indexes to twriling
        for unitary_index in unitary_index_set:
            print('==================================================')
            print('Unitary Index :', unitary_index) # Setting Unitary Index
            print('Name of Backend :', self.backend) # Setting Simulation Backend
            print('Number of Total Shots :', 1000) # Setting Simulation Shot Number

            qc = self.ConstructQC(unitary_index) # construct quantum circuit
            t_qc = transpile(qc, self.backend) # quantum circuit transpile
            results = self.backend.run(t_qc, shots=1000).result() # get result

            # Counts Result
            temp_counts = results.get_counts()
            print('Simulation Result (counts) :', temp_counts)

            counts = SumDictionary(counts, temp_counts)
            print('==================================================\n')
            
        ## Classical post-processing
        # Variable setting
        measurement_counts = []
        counts_pp = {}
        
        # Initialize measurement counts
        for i in range(self.num_qubits):
            measurement_counts.append([0, 0])
        
        # Average count results
        for key in counts: 
            counts[key] = round(counts[key]/3)
            
        # Calculate counts of [x_n | n]
        for i in range(self.num_qubits):
            for key in counts:
                if key[i] == "0":
                    measurement_counts[i][0] += counts[key]
                else:
                    measurement_counts[i][1] += counts[key]
                    
        # Recover counts
        for key in counts:
            counts_pp[key] = counts[key]
            for i in range(self.num_qubits):
                counts_pp[key] = counts_pp[key] * ( (1 - (eta*1000)/(2*measurement_counts[i][int(key[i])])) / (1-eta) )
            counts_pp[key] = round(counts_pp[key])
        counts = counts_pp

        return plot_distribution(counts)


# In[2]:


def SumDictionary(totdic, adddic):
        for key in adddic:
            if key in totdic:
                totdic[key] += adddic[key]
            else:
                totdic[key] = adddic[key]
        return totdic


# In[3]:


def TwirlingCircuit(unitary_index, qubit_num):
    unitary_twirl = {
        1:[0, 0, 0],
        2:[math.pi, 3*math.pi/2, math.pi/2],
        3:[math.pi, 0, math.pi],
        4:[0, math.pi/2, math.pi/2],
        5:[math.pi/2, 0, math.pi/2],
        6:[math.pi/2, math.pi, math.pi/2],
        7:[math.pi/2, math.pi/2, math.pi],
        8:[math.pi/2, math.pi/2, 0],
        9:[math.pi/2, 3*math.pi/2, math.pi],
        10:[math.pi/2, math.pi/2, 0],
        11:[math.pi/2, 0, 3*math.pi/2],
        12:[math.pi/2, math.pi, 3*math.pi/2]} # twirling parameters

    # Create state initialize circuit
    qr = QuantumRegister(qubit_num)
    circ = QuantumCircuit(qr, name='Twirling')

    # Apply U
    theta = (unitary_twirl[unitary_index])[0]
    phi = (unitary_twirl[unitary_index])[1]
    lam = (unitary_twirl[unitary_index])[2]
    circ.u(theta, phi, lam, qr)
    circ.barrier()

    # Apply U^{dag}
    theta = -(unitary_twirl[unitary_index])[0]
    phi = -(unitary_twirl[unitary_index])[2]
    lam = -(unitary_twirl[unitary_index])[1]
    circ.u(theta, phi, lam, qr)

    # Convert to a gate and stick it into an arbitrary place in the bigger circuit
    inst = circ.to_instruction()

    return inst

