"""FX-991ES PLUS-inspired scientific calculator GUI."""
import tkinter as tk
from tkinter import messagebox, simpledialog
from calculator_engine import CalculatorEngine, CalculatorError

class Calculator(tk.Tk):
    BG='#17191d'; SCREEN='#cbd7bd'; GOLD='#d4b46a'; TEXT='#f1f1ed'; KEY='#343b45'; ALT='#4a5360'; FUNC='#66583d'; RED='#884646'
    def __init__(self):
        super().__init__(); self.title('Scientific Calculator | FX-991ES PLUS inspired'); self.geometry('900x790'); self.minsize(680,680); self.configure(bg=self.BG)
        self.engine=CalculatorEngine(); self.expr=tk.StringVar(); self.result=tk.StringVar(value='0'); self.status=tk.StringVar(value='DEG     M: 0'); self.history=[]; self.last=None; self.after_equal=False
        self.build(); self.bind('<Key>',self.keyboard)
    def btn(self,parent,label,cmd,color=None,size=10):
        return tk.Button(parent,text=label,command=cmd,bg=color or self.KEY,fg='#17191d' if color==self.GOLD else self.TEXT,activebackground=self.GOLD,activeforeground='#17191d',relief='flat',bd=0,font=('Arial',size,'bold'),padx=5,pady=9,cursor='hand2')
    def build(self):
        head=tk.Frame(self,bg=self.BG); head.pack(fill='x',padx=18,pady=(14,8)); tk.Label(head,text='SCIENTIFIC CALCULATOR',bg=self.BG,fg=self.GOLD,font=('Arial',13,'bold')).pack(side='left'); tk.Label(head,text='FX-991ES PLUS INSPIRED',bg=self.BG,fg='#aeb4bc').pack(side='right')
        scr=tk.Frame(self,bg=self.SCREEN,bd=4,relief='sunken'); scr.pack(fill='x',padx=18,pady=(0,10)); tk.Label(scr,textvariable=self.status,bg=self.SCREEN,fg='#354032',anchor='w',font=('Consolas',10,'bold')).pack(fill='x',padx=12,pady=(7,0)); self.entry=tk.Entry(scr,textvariable=self.expr,bg=self.SCREEN,fg='#172017',insertbackground='#172017',relief='flat',justify='right',font=('Consolas',19)); self.entry.pack(fill='x',padx=12,pady=5,ipady=5); tk.Label(scr,textvariable=self.result,bg=self.SCREEN,fg='#172017',anchor='e',font=('Consolas',25,'bold')).pack(fill='x',padx=12,pady=(0,8)); self.entry.focus_set()
        bar=tk.Frame(self,bg=self.BG); bar.pack(fill='x',padx=18,pady=(0,8))
        for label,cmd,col in [('DEG/RAD',self.angle,self.FUNC),('S⇔D',self.fraction,self.ALT),('M+',self.memadd,self.ALT),('M−',self.memsub,self.ALT),('MR',self.memrecall,self.ALT),('MC',self.memclear,self.ALT),('HISTORY',self.showhistory,self.ALT)]: self.btn(bar,label,cmd,col,9).pack(side='left',expand=True,fill='x',padx=3)
        grid=tk.Frame(self,bg=self.BG); grid.pack(fill='both',expand=True,padx=18,pady=(0,10)); [grid.columnconfigure(c,weight=1,uniform='c') for c in range(6)]
        rows=[[('sin','sin('),('cos','cos('),('tan','tan('),('sin⁻¹','asin('),('cos⁻¹','acos('),('tan⁻¹','atan(')],[('√','sqrt('),('∛','cbrt('),('x²','**2'),('xʸ','**'),('log','log('),('ln','ln(')],[('(','('),(')',')'),('π','pi'),('e','e'),('n!','factorial('),('⌫','BACK')],[('7','7'),('8','8'),('9','9'),('÷','/'),('AC','AC'),('Ans','Ans')],[('4','4'),('5','5'),('6','6'),('×','*'),('%','%'),('±','NEG')],[('1','1'),('2','2'),('3','3'),('−','-'),('.','.'),('=','EQUAL')],[('0','0'),('sinh','sinh('),('cosh','cosh('),('tanh','tanh('),('exp','exp('),('1/x','1/(')]]
        for r,row in enumerate(rows):
            grid.rowconfigure(r,weight=1,uniform='r')
            for c,(label,value) in enumerate(row):
                col=self.FUNC if r<3 or label in ('sinh','cosh','tanh','exp') else self.KEY
                if label in ('AC','⌫'): col=self.RED
                if label=='=': col=self.GOLD
                self.btn(grid,label,lambda v=value:self.press(v),col).grid(row=r,column=c,sticky='nsew',padx=4,pady=4)
        box=tk.LabelFrame(self,text='ADVANCED MODES',bg=self.BG,fg=self.GOLD,font=('Arial',9,'bold')); box.pack(fill='x',padx=18,pady=(0,14))
        for label,cmd in [('Matrices',self.matrix),('Vectors',self.vector),('Statistics',self.stats),('Equation solver',self.solve),('Simultaneous equations',self.simultaneous),('Calculus',self.calculus)]: self.btn(box,label,cmd,self.ALT,9).pack(side='left',expand=True,fill='x',padx=3,pady=6)
    def insert(self,s):
        old='' if self.after_equal and s not in (')','**','%') else self.expr.get(); self.after_equal=False; self.expr.set(old+s); self.entry.icursor('end'); self.entry.focus_set()
    def press(self,v):
        if v=='AC': self.expr.set(''); self.result.set('0'); self.after_equal=False
        elif v=='BACK': self.expr.set(self.expr.get()[:-1]); self.after_equal=False
        elif v=='EQUAL': self.evaluate()
        elif v=='NEG': self.insert('-')
        else: self.insert(v)
    def evaluate(self):
        try:
            self.last=self.engine.calculate(self.expr.get()); out=self.engine.fmt(self.last); self.result.set(out); self.history.append((self.expr.get(),out)); self.after_equal=True; self.update_status()
        except CalculatorError as e: self.result.set('Math ERROR'); self.status.set(str(e))
    def update_status(self): self.status.set(f'{self.engine.angle_mode}     M: {self.engine.fmt(self.engine.memory)}')
    def angle(self): self.engine.angle_mode='RAD' if self.engine.angle_mode=='DEG' else 'DEG'; self.update_status()
    def fraction(self):
        if self.last is not None:
            try: self.result.set(self.engine.fraction(self.last)+'   ('+self.engine.fmt(self.last)+')')
            except CalculatorError as e: messagebox.showinfo('S⇔D',str(e),parent=self)
    def memadd(self):
        if self.last is not None: self.engine.memory+=self.last; self.update_status()
    def memsub(self):
        if self.last is not None: self.engine.memory-=self.last; self.update_status()
    def memrecall(self): self.insert(str(self.engine.memory))
    def memclear(self): self.engine.memory=0; self.update_status()
    def showhistory(self):
        w=tk.Toplevel(self); w.title('Calculation history'); w.geometry('540x380'); lb=tk.Listbox(w,bg='#252a32',fg=self.TEXT,selectbackground=self.GOLD,font=('Consolas',10)); lb.pack(fill='both',expand=True,padx=12,pady=12)
        for a,b in reversed(self.history[-200:]): lb.insert('end',f'{a} = {b}')
        lb.bind('<Double-Button-1>',lambda e:self.expr.set(lb.get(lb.curselection()[0]).split(' = ')[0]) if lb.curselection() else None)
    def ask(self,title,prompt,initial=''): return simpledialog.askstring(title,prompt,initialvalue=initial,parent=self)
    def output(self,title,fn):
        try: result=fn()
        except CalculatorError as e: messagebox.showerror(title,str(e),parent=self); return
        w=tk.Toplevel(self); w.title(title); w.geometry('600x420'); t=tk.Text(w,wrap='word',bg='#252a32',fg=self.TEXT,font=('Consolas',11),padx=12,pady=12); t.pack(fill='both',expand=True,padx=12,pady=12); t.insert('1.0',str(result)); t.configure(state='disabled')
    def matrix(self):
        a=self.ask('Matrix','Matrix A, e.g. [[1,2],[3,4]]:')
        if a is None:return
        op=self.ask('Operation','determinant, inverse, transpose, A + B, A - B, A × B:','determinant')
        if op is None:return
        b=''
        if op in ('A + B','A - B','A × B'):
            b=self.ask('Matrix B','Matrix B, e.g. [[5,6],[7,8]]:')
            if b is None:return
        self.output('Matrix result',lambda:self.engine.matrix(a,op,b))
    def vector(self):
        a=self.ask('Vector','Vector A, e.g. [1,2,3]:')
        if a is None:return
        op=self.ask('Operation','magnitude, dot product, cross product, A + B:','magnitude')
        if op is None:return
        b=''
        if op!='magnitude':
            b=self.ask('Vector B','Vector B, e.g. [4,5,6]:')
            if b is None:return
        self.output('Vector result',lambda:self.engine.vector(a,op,b))
    def stats(self):
        data=self.ask('Statistics','Enter comma-separated data, e.g. 12,15,18,20:')
        if data is not None:self.output('Statistics',lambda:'\n'.join(f'{k}: {v}' for k,v in self.engine.stats(data).items()))
    def solve(self):
        eq=self.ask('Equation solver','Equation in x, e.g. x**2 - 5*x + 6 = 0:')
        if eq is None:return
        var=self.ask('Variable','Variable name:','x')
        if var is not None:self.output('Solutions',lambda:self.engine.solve(eq,var))
    def simultaneous(self):
        eq=self.ask('Simultaneous equations','One equation per line:\nx + y = 5\nx - y = 1')
        if eq is None:return
        vars=self.ask('Variables','Comma-separated variables:','x,y')
        if vars is not None:self.output('Solutions',lambda:self.engine.simultaneous(eq,vars))
    def calculus(self):
        expr=self.ask('Calculus','Function, e.g. x**3 + 2*x:')
        if expr is None:return
        var=self.ask('Variable','Variable name:','x')
        if var is None:return
        mode=self.ask('Calculus mode','D = derivative + indefinite integral; I = definite integral:','D')
        if mode is None:return
        if mode.upper()=='I':
            lo=self.ask('Lower bound','Lower bound:'); hi=self.ask('Upper bound','Upper bound:')
            if lo is not None and hi is not None:self.output('Integral',lambda:self.engine.calculus(expr,var,lower=lo,upper=hi))
        else:
            p=self.ask('Derivative','Evaluate derivative at:','0')
            if p is not None:self.output('Calculus',lambda:self.engine.calculus(expr,var,point=p))
    def keyboard(self,e):
        if e.keysym=='Return': self.evaluate(); return 'break'
        if e.keysym=='Escape': self.press('AC'); return 'break'
        if e.keysym=='BackSpace': self.press('BACK'); return 'break'
        if e.char=='^': self.insert('**'); return 'break'
        if e.char in '0123456789.+-*/()%': self.insert(e.char); return 'break'

if __name__=='__main__': Calculator().mainloop()
