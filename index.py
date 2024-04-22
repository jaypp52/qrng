from flask import Flask, redirect, url_for, request, jsonify
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit,execute, transpile, assemble
from qiskit_aer import Aer
from numpy import pi

app = Flask(__name__)

@app.route('/')
def qrng():
  qreg_q = QuantumRegister(4, 'q')
  creg_c = ClassicalRegister(4, 'c')
  circuit = QuantumCircuit(qreg_q, creg_c)

  circuit.h(qreg_q[0])
  circuit.h(qreg_q[1])
  circuit.h(qreg_q[2])
  circuit.h(qreg_q[3])
  circuit.measure(qreg_q[0], creg_c[0])
  circuit.measure(qreg_q[1], creg_c[1])
  circuit.measure(qreg_q[2], creg_c[2])
  circuit.measure(qreg_q[3], creg_c[3])

  simulator = Aer.get_backend('qasm_simulator')
  compiled_circuit = transpile(circuit, simulator)

  random_number = ""
  for i in range(1,32):
    job = execute(compiled_circuit, simulator, shots=1)
    result = job.result().get_counts()
    random_number = random_number + str(list(result.keys())[0])

  binary_string = random_number

  # Convert binary string to integer
  decimal_value = int(binary_string, 2)

  # Convert integer to hexadecimal string
  random_number = hex(decimal_value)[2:]

  # print(len(random_number))
  # print(random_number)
  return {
        'key': random_number
  }


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')