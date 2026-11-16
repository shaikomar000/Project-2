"""Scientific calculator engine. Scalar expressions use a restricted AST, never eval()."""
import ast, math, operator, statistics
from fractions import Fraction
try:
    import sympy as sp
except ImportError:
    sp = None

class CalculatorError(Exception): pass

class CalculatorEngine:
    BIN = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
           ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod}
    UNARY = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    def __init__(self): self.angle_mode, self.ans, self.memory = 'DEG', 0, 0
    def _rad(self, x): return math.radians(x) if self.angle_mode == 'DEG' else x
    def _out_angle(self, x): return math.degrees(x) if self.angle_mode == 'DEG' else x
    @staticmethod
    def _fact(x):
        if int(x) != x or x < 0 or x > 170: raise CalculatorError('Factorial accepts integers from 0 to 170.')
        return math.factorial(int(x))
    def _funcs(self):
        return {'sin':lambda x:math.sin(self._rad(x)), 'cos':lambda x:math.cos(self._rad(x)),
          'tan':lambda x:math.tan(self._rad(x)), 'asin':lambda x:self._out_angle(math.asin(x)),
          'acos':lambda x:self._out_angle(math.acos(x)), 'atan':lambda x:self._out_angle(math.atan(x)),
          'sinh':math.sinh,'cosh':math.cosh,'tanh':math.tanh,'sqrt':math.sqrt,
          'cbrt':lambda x:math.copysign(abs(x)**(1/3),x),'log':math.log10,'ln':math.log,
          'exp':math.exp,'abs':abs,'floor':math.floor,'ceil':math.ceil,'factorial':self._fact}
    def _visit(self, n):
        if isinstance(n, ast.Expression): return self._visit(n.body)
        if isinstance(n, ast.Constant) and type(n.value) in (int,float): return n.value
        if isinstance(n, ast.Name):
            vals={'pi':math.pi,'e':math.e,'Ans':self.ans}
            if n.id in vals: return vals[n.id]
            raise CalculatorError('Unknown name: '+n.id)
        if isinstance(n, ast.BinOp) and type(n.op) in self.BIN:
            a,b=self._visit(n.left),self._visit(n.right)
            if isinstance(n.op,ast.Pow) and abs(b)>10000: raise CalculatorError('Exponent too large.')
            return self.BIN[type(n.op)](a,b)
        if isinstance(n, ast.UnaryOp) and type(n.op) in self.UNARY: return self.UNARY[type(n.op)](self._visit(n.operand))
        if isinstance(n, ast.Call) and isinstance(n.func,ast.Name):
            f=self._funcs().get(n.func.id)
            if f is None or len(n.args)!=1 or n.keywords: raise CalculatorError('Unsupported function or arguments.')
            return f(self._visit(n.args[0]))
        raise CalculatorError('Invalid expression.')
    def calculate(self, text):
        try:
            result=self._visit(ast.parse(text.strip().replace('^','**').replace('×','*').replace('÷','/'),mode='eval'))
            if isinstance(result,complex):
                if not math.isfinite(result.real) or not math.isfinite(result.imag): raise CalculatorError('Result out of range.')
            elif not math.isfinite(float(result)): raise CalculatorError('Result out of range.')
            self.ans=result; return result
        except CalculatorError: raise
        except ZeroDivisionError: raise CalculatorError('Cannot divide by zero.')
        except (ValueError,OverflowError): raise CalculatorError('Math domain or range error.')
        except SyntaxError: raise CalculatorError('Check expression syntax.')
        except Exception as e: raise CalculatorError(str(e))
    @staticmethod
    def fmt(x):
        if isinstance(x,complex): return f'{x.real:.12g}{x.imag:+.12g}i'
        return f'{x:.12g}' if isinstance(x,float) else str(x)
    @staticmethod
    def fraction(x):
        if isinstance(x,complex): raise CalculatorError('Cannot convert a complex result to a simple fraction.')
        return str(Fraction(float(x)).limit_denominator(1000000))
    def _sym(self):
        if sp is None: raise CalculatorError('Advanced tools require SymPy. Run: pip install -r requirements.txt')
        return sp
    def _expr(self,text,local=None):
        s=self._sym(); allowed={'pi':s.pi,'e':s.E,'E':s.E,'sqrt':s.sqrt,'sin':s.sin,'cos':s.cos,'tan':s.tan,'log':s.log,'ln':s.log,'exp':s.exp,'Abs':s.Abs,'abs':s.Abs}
        if local: allowed.update(local)
        try: return s.sympify(text.replace('^','**'),locals=allowed)
        except Exception as e: raise CalculatorError('Expression parse error: '+str(e))
    def matrix(self,a,op,b=''):
        s=self._sym()
        try:
            A=s.Matrix(ast.literal_eval(a))
            if op=='determinant': return str(A.det())
            if op=='inverse': return str(A.inv())
            if op=='transpose': return str(A.T)
            B=s.Matrix(ast.literal_eval(b))
            return str({'A + B':A+B,'A - B':A-B,'A × B':A*B}[op])
        except Exception as e: raise CalculatorError('Matrix error: '+str(e))
    def vector(self,a,op,b=''):
        s=self._sym()
        try:
            A=s.Matrix(ast.literal_eval(a)); A=s.Matrix(list(A))
            if op=='magnitude': return str(s.sqrt(sum(v*v for v in A)))
            B=s.Matrix(list(s.Matrix(ast.literal_eval(b))))
            return str({'dot product':A.dot(B),'cross product':A.cross(B),'A + B':A+B}[op])
        except Exception as e: raise CalculatorError('Vector error: '+str(e))
    def stats(self,text):
        try:
            v=[float(x.strip()) for x in text.replace(';',',').split(',') if x.strip()]
            if not v: raise ValueError('Enter comma-separated numbers.')
            if len(v)>10000: raise ValueError('Maximum 10,000 values.')
            d={'Count':len(v),'Sum':sum(v),'Mean':statistics.mean(v),'Median':statistics.median(v),'Minimum':min(v),'Maximum':max(v),'Population variance':statistics.pvariance(v),'Population standard deviation':statistics.pstdev(v)}
            if len(v)>1: d.update({'Sample variance':statistics.variance(v),'Sample standard deviation':statistics.stdev(v)})
            try: d['Mode']=statistics.mode(v)
            except statistics.StatisticsError: d['Mode']='No unique mode'
            return d
        except Exception as e: raise CalculatorError('Statistics error: '+str(e))
    def solve(self,text,var='x'):
        s=self._sym(); x=s.Symbol(var)
        try:
            if '=' in text:
                a,b=text.split('=',1); expr=self._expr(a,{var:x})-self._expr(b,{var:x})
            else: expr=self._expr(text,{var:x})
            sol=s.solve(expr,x)
            return '\n'.join(f'{var}{i+1} = {v}  ≈  {s.N(v,12)}' for i,v in enumerate(sol)) or 'No solution found.'
        except Exception as e: raise CalculatorError('Equation solver error: '+str(e))
    def simultaneous(self,text,vars='x,y'):
        s=self._sym(); names=[x.strip() for x in vars.split(',') if x.strip()]
        if not names or any(not x.isidentifier() for x in names): raise CalculatorError('Invalid variable list.')
        symbols=s.symbols(' '.join(names)); symbols=(symbols,) if not isinstance(symbols,tuple) else symbols
        local=dict(zip(names,symbols)); lines=[x.strip() for x in text.splitlines() if x.strip()]
        if len(lines)!=len(symbols): raise CalculatorError('Enter one equation per variable.')
        eq=[]
        for line in lines:
            if '=' in line:
                a,b=line.split('=',1); eq.append(self._expr(a,local)-self._expr(b,local))
            else: eq.append(self._expr(line,local))
        try:
            sols=s.solve(eq,symbols,dict=True)
            return '\n'.join(', '.join(f'{k} = {v} ≈ {s.N(v,12)}' for k,v in sol.items()) for sol in sols) or 'No solution found.'
        except Exception as e: raise CalculatorError('Simultaneous solver error: '+str(e))
    def calculus(self,text,var='x',point='0',lower='',upper=''):
        s=self._sym(); x=s.Symbol(var); expr=self._expr(text,{var:x})
        try:
            if lower.strip() and upper.strip():
                val=s.integrate(expr,(x,self._expr(lower),self._expr(upper)))
                return f'Definite integral = {val}\n≈ {s.N(val,14)}'
            p=self._expr(point); deriv=s.diff(expr,x); integ=s.integrate(expr,x)
            return f'Derivative: {deriv}\nAt {var} = {p}: {s.N(deriv.subs(x,p),14)}\n\nIndefinite integral: {integ} + C'
        except Exception as e: raise CalculatorError('Calculus error: '+str(e))
