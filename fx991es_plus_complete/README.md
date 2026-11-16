# FX-991ES PLUS-inspired Scientific Calculator

A Python/Tkinter desktop calculator inspired by the workflow and keypad of a scientific calculator. This is an original educational project, not Casio software or an exact hardware/firmware replica.

## Features

- Arithmetic, brackets, powers, modulo and previous answer (`Ans`)
- Trigonometry, inverse trigonometry, hyperbolic functions
- DEG/RAD modes, square/cube roots, logarithms, exponentials, factorials
- pi/e constants, memory add/subtract/recall/clear, decimal-to-fraction, history
- Matrix determinant, inverse, transpose, addition, subtraction and multiplication
- Vector magnitude, dot product, cross product and addition
- Statistics: count, sum, mean, median, mode, variance, standard deviation, min/max
- Polynomial/general equation solver and simultaneous equation solver
- Symbolic derivative, derivative at a point, indefinite and definite integration
- Restricted AST scalar evaluator (does not use Python `eval()`)

## Setup (Windows / VS Code)

Python 3.10+ and Tkinter are required. In a terminal:

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Tkinter is included with most Windows Python installations. On Linux, install your distribution's `python3-tk` package if needed.

## Input examples

- `sin(30)` in DEG mode -> `0.5`
- `sqrt(81)` -> `9`
- `log(1000)` -> `3`
- `factorial(5)` -> `120`
- `2^8` -> `256`
- Matrix A: `[[1,2],[3,4]]`
- Vector A: `[1,2,3]`
- Statistics: `12,15,18,20`
- Equation: `x**2 - 5*x + 6 = 0`
- Simultaneous equations: enter `x + y = 5` and `x - y = 1` on separate lines
- Calculus function: `x**3 + 2*x`

## Project structure

```text
fx991es_plus_complete/
├── main.py
├── calculator_engine.py
├── requirements.txt
├── README.md
└── tests/
    └── test_engine.py
```

## Accuracy and scope

This is a broad portfolio implementation inspired by the fx-991ES PLUS, not a feature-for-feature clone. It does not reproduce every hardware mode, display convention, solver algorithm or internal precision. Check important results independently. Advanced symbolic functions are provided by SymPy.
