import sys
import parsePlanFULL
from pyswip import Prolog
from tkinter import *

def generateMenu(root):
    option1 = Button(root, text='3x3',command = lambda : drawBoard(root)).pack()
    option2 = Button(root, text='Cos innego').pack()

def move():
    pass

def drawBoard(root):
    pass
    '''
    canvas = Canvas(root, width=600, height=600)
    canvas.configure(background='white')
    canvas.pack(side="left")
    canvas.create_rectangle(0,0,200,200)
    canvas.create_rectangle(200,0,400,200)
    canvas.create_rectangle(400,0,600,200)
    canvas.create_rectangle(0,200,200,400)
    canvas.create_rectangle(200,200,400,400)
    canvas.create_rectangle(400,200,600,400)
    canvas.create_rectangle(0,400,200,600)
    canvas.create_rectangle(200,400,400,600)
    canvas.create_rectangle(400,400,600,600)
    button1 = Button(canvas,width=19,height=10,bg='white',text='1',command = move)
    
    button1.place(x=10,y=10)
    button2 = Button(canvas,width=19,height=10,bg='white',text='2',command = move)
    
    button2.place(x=210,y=10)
    button3 = Button(canvas,width=19,height=10,bg='white',text='3',command = move)
    
    button3.place(x=410,y=10)
    button4 = Button(canvas,width=19,height=10,bg='white',text='4',command = move)
    
    button4.place(x=10,y=210)
    button5 = Button(canvas,width=19,height=10,bg='white',text='5',command = move)
    
    button5.place(x=210,y=210)
    button6 = Button(canvas,width=19,height=10,bg='white',text='6',command = move)
    
    button6.place(x=410,y=210)
    button7 = Button(canvas,width=19,height=10,bg='white',text='7',command = move)
    
    button7.place(x=10,y=410)
    button8 = Button(canvas,width=19,height=10,bg='white',text='8',command = move)

    button8.place(x=210,y=410)
    button9 = Button(canvas,width=19,height=10,bg='white',text='',command = move)
    
    button9.place(x=410,y=410)
    canvas2 = Canvas(root,width=600,height=600)
    canvas2.configure(background='white')
    graph = PhotoImage(file='FULL_GRAPHPLAN.gv.png')
    hbar=Scrollbar(root,orient=HORIZONTAL)
    hbar.pack(side=BOTTOM,fill=X)
    hbar.config(command=canvas.xview)
    vbar=Scrollbar(root,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)
    canvas2.create_image(300,300, image=graph)
    label = Label(image=graph) 
    label.image = graph # keep a reference!
    canvas2.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas2.pack(side='right')
    '''


def runGRAPHPLAN():
    graphplan = Prolog()
    graphplan.consult('graphplan.pl')
    graphplan.assertz("state0([na(a,1),pusty(2),pusty(3)])")
    plan = list(graphplan.query('call_plan([na(a,3)],Plan)',maxresult=1))
    g = parsePlanFULL.Graph('outputs/output.txt')
    g.run_all()


def main():
    root = Tk()
    root.title('GRAPHPLAN')
    root.geometry("1200x800")
    generateMenu(root)
    generate = Button(root,bg='white',text='Wygeneruj graf',command = runGRAPHPLAN)
    generate.pack()
    root.mainloop()


if __name__=='__main__':
    main()
    
