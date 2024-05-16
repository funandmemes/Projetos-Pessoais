#!/usr/bin/env python3

from tkinter import *
class main:
    def __init__(self, display):
        self.display = display
        self.line = Label(self.display, text='')
        self.line.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.b1 = Button(self.display, text='1', command=lambda: self.num_but('1'))
        self.b1.grid(row=1, column=0, sticky='nsew')
        self.b2 = Button(self.display, text='2', command=lambda: self.num_but('2'))
        self.b2.grid(row=1, column=1, sticky='nsew')
        self.b3 = Button(self.display, text='3', command=lambda: self.num_but('3'))
        self.b3.grid(row=1, column=2, sticky='nsew')
        self.b4 = Button(self.display, text='4', command=lambda: self.num_but('4'))
        self.b4.grid(row=2, column=0, sticky='nsew')
        self.b5 = Button(self.display, text='5', command=lambda: self.num_but('5'))
        self.b5.grid(row=2, column=1, sticky='nsew')
        self.b6 = Button(self.display, text='6', command=lambda: self.num_but('6'))
        self.b6.grid(row=2, column=2, sticky='nsew')
        self.b7 = Button(self.display, text='7', command=lambda: self.num_but('7'))
        self.b7.grid(row=3, column=0, sticky='nsew')
        self.b8 = Button(self.display, text='8', command=lambda: self.num_but('8'))
        self.b8.grid(row=3, column=1, sticky='nsew')
        self.b9 = Button(self.display, text='9', command=lambda: self.num_but('9'))
        self.b9.grid(row=3, column=2, sticky='nsew')
        self.b0 = Button(self.display, text='0', command=lambda: self.num_but('0'))
        self.b0.grid(row=4, column=1, sticky='nsew')
        self.op_sum = Button(self.display, text='+', bg='#f0ddaa',
        command=lambda: self.op_but('+'))
        self.op_sum.grid(row=1, column=3, sticky='nsew')
        self.op_sub = Button(self.display, text='-', bg='#f0ddaa',
        command=lambda: self.op_but('-'))
        self.op_sub.grid(row=2, column=3, sticky='nsew')
        self.op_mul = Button(self.display, text='*', bg='#f0ddaa',
        command=lambda: self.op_but('*'))
        self.op_mul.grid(row=3, column=3, sticky='nsew')
        self.op_div = Button(self.display, text='/', bg='#f0ddaa',
        command=lambda: self.op_but('/'))
        self.op_div.grid(row=4, column=3, sticky='nsew')
        self.eq = Button(self.display, text='=',bg='#e47c5d', command=self.equals)
        self.eq.grid(row=4, column=2, sticky='nsew')
        self.cl = Button(self.display, text='C', bg='#59b390', command=self.clear)
        self.cl.grid(row=4, column=0, sticky='nsew')
    def num_but(self, num):
        old_text = self.line.cget('text')
        if type(old_text) == int or type(old_text) == float:
            self.clear
            self.line.config(text=num)
        else:
            new_text = old_text + num
            self.line.config(text=new_text)

    def op_but(self, op):
        old_text = self.line.cget('text')
        if type(old_text) == int or type(old_text) == float:
            old_text = str(old_text)
        elif len(old_text) < 1:
            return
        new_text = old_text + op
        self.line.config(text=new_text)

    def equals(self):
        old_text = self.line.cget('text')
        result = eval(old_text)
        self.line.config(text=result)
        
    def clear(self):
        self.line.config(text='')
        
display = Tk()
display.title('Calculadora')
app = main(display)
display.mainloop()
