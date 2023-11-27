# MeasurementErrorMitigation

## Index
  - [Overview](#overview) 
  - [Setting](#setting)


## Overview
<!-- Write Overview about this project -->
- A hybrid quantum-classical approach to mitigating measurement errors
- Reference: IEEE Transactions on Computers, vol.70, no.09, pp.1401-1411, 2021


## Features
- The method only requires quantum circuit from qiskit.
- Measurement error mitigation method with fixed unitaries (23.11.27)


### Basic Arguments
```
quantum_circuit: QuantumCircuit
```

```ConstructQC(unitary_index: int)``` 

Create quantum circuit with twirling method

NOTE: The given quantum circuit must exclude barrier and measurement.

```SimulateQC(unitary_index_set=[1,5,9], eta=0.1)``` 

Quantum pre-processing and classical post-processing.

Returns probability distribution graph

### Work in progress
- More manual inputs
- Availablity to real quantum device
