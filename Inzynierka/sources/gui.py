import sys
import parsePlanFULL
import parseplanSIMPLIFIED
from tkinter import *
from PIL import ImageTk,Image
from pyswip import Prolog

class GUI:
    def __init__(self):
        self.chosen_option = -1
        self.pressed_button = ""
        self.buttons = []
        self.cargo_blocks_left = []
        self.cargo_blocks_right = []
        self.cargo_button = ""
        self.image = ""
        self.root = Tk()
        self.root.title('GRAPHPLAN')
        self.root.geometry('1210x800')
        self.menu_frame = Frame(self.root,width=1200,height=100)
        self.left_panel = Frame(self.root,bg='white',width=600,height=700)
        self.right_panel = Frame(self.root,bg='white',width=600,height=700)
        self.initMenu()
        self.menu_frame.pack(side=TOP)
        self.left_panel.pack(side=LEFT)
        self.right_panel.pack(side=RIGHT)
        self.root.mainloop()

    def clear_boards(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        self.pressed_button = ""
        self.buttons = []
        self.cargo_button = ""
        self.cargo_blocks_left = []
        self.cargo_blocks_right = []
        self.image = ""

    #def convert(self,value):
    #    table = ['a','b','c','d','e','f','g','h']
    #    return table[int(value)-1]
    
    def get_graph(self):
        if(self.chosen_option==1):
            self.GRAPHPLAN3x3()
        else:
            self.GRAPHPLANCargo()

    def GRAPHPLAN3x3(self):
        graphplan = Prolog()
        graphplan.consult('graphplan.pl')
        graphplan.assertz('can(zostan(P),[P])')
        graphplan.assertz('can(idz(R,A,B), [na(R,A), pusty(B)]) :- robot(R), adjacent(A,B)')
        graphplan.assertz('effects(zostan(P),[P])')
        graphplan.assertz('effects(idz(R,A,B), [na(R,B),pusty(A),~na(R,A),~pusty(B)])')
        graphplan.assertz('robot(a)')
        graphplan.assertz('robot(b)')
        graphplan.assertz('robot(c)')
        graphplan.assertz('robot(d)')
        graphplan.assertz('robot(e)')
        graphplan.assertz('robot(f)')
        graphplan.assertz('robot(g)')
        graphplan.assertz('robot(h)')
        graphplan.assertz('adjacent(A,B) :- n(A,B) ; n(B,A)')
        graphplan.assertz('n(1,2)')
        graphplan.assertz('n(1,4)')
        graphplan.assertz('n(2,1)')
        graphplan.assertz('n(2,3)')
        graphplan.assertz('n(2,5)')
        graphplan.assertz('n(3,2)')
        graphplan.assertz('n(3,6)')
        graphplan.assertz('n(4,1)')
        graphplan.assertz('n(4,5)')
        graphplan.assertz('n(4,7)')
        graphplan.assertz('n(5,4)')
        graphplan.assertz('n(5,6)')
        graphplan.assertz('n(5,2)')
        graphplan.assertz('n(5,8)')
        graphplan.assertz('n(6,5)')
        graphplan.assertz('n(6,3)')
        graphplan.assertz('n(6,9)')
        graphplan.assertz('n(7,4)')
        graphplan.assertz('n(7,8)')
        graphplan.assertz('n(8,7)')
        graphplan.assertz('n(8,5)')
        graphplan.assertz('n(8,9)')
        graphplan.assertz('n(9,8)')
        graphplan.assertz('n(9,6)')
        graphplan.assertz('incosistent(G,~G)')
        graphplan.assertz('incosistent(~G,G)')
        graphplan.assertz('incosistent(na(R,C1),na(R,C2)) :- C1 \== C2')
        graphplan.assertz('inconsistent(na(_,C),pusty(C))')
        graphplan.assertz('inconsistent(pusty(C),na(_,C))')
        graphplan.assertz('inconsistent(na(R1,C),na(R2,C)) :- R1 \== R2')
        command = 'state0(['
        for i,button in enumerate(self.buttons):
            if button['text'] == '':
                command = command + 'pusty({}),'.format(i+1)
            else:
                command = command + 'na({},{}),'.format(chr(96+int(button['text'])),i+1)
        command = command[:len(command)-1]
        command = command+'])'
        print(command)
        graphplan.assertz(command)
        plan = list(graphplan.query('call_plan([na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),pusty(9)],Plan)',maxresult=1))
        self.printGraph(plan)
        graphplan.retractall('n(_,_)')
        graphplan.retractall('can(_,_)')
        graphplan.retractall('effects(_,_)')
        graphplan.retractall('robot(_)')
        graphplan.retractall('adjacent(_,_)')
        graphplan.retractall('incosistent(_,_)')
        graphplan.retract(command)

    def GRAPHPLANCargo(self):
        graphplan = Prolog()
        graphplan.consult('graphplan.pl')
        inital_state = "state0(["
        goal = "["
        print(self.cargo_blocks_left)
        for tab in self.cargo_blocks_left:
            graphplan.assertz("place({})".format(tab[0]))
            for i in range(len(tab)-1):
                graphplan.assertz("block({})".format(tab[i+1]))
        graphplan.assertz("can(zostan(P),[P])")
        graphplan.assertz("can(idz(Block,From,To), [pusty(Block),pusty(To),na(Block,From)]) :- block(Block), object(To), To \==Block, object(From), From \==To, Block \== From")     
        graphplan.assertz("effects(zostan(P),[P])")
        graphplan.assertz("effects(idz(X,From,To),[na(X,To),pusty(From),~na(X,From),~pusty(To)])")   
        graphplan.assertz("object(X) :- place(X);block(X)")

        for tab in self.cargo_blocks_left:
            inital_state = inital_state + "pusty({}),".format(tab[len(tab)-1])
            for i in range(len(tab)-1):
                inital_state = inital_state + "na({},{}),".format(tab[i+1],tab[i])
        inital_state = inital_state[:len(inital_state)-1]
        inital_state = inital_state+'])'

        for tab in self.cargo_blocks_right:
            goal = goal + "pusty({}),".format(tab[len(tab)-1])
            for i in range(len(tab)-1):
                goal = goal + "na({},{}),".format(tab[i+1],tab[i])
        goal = goal[:len(goal)-1]
        goal = goal+']'

        graphplan.assertz(inital_state)
        plan = list(graphplan.query('call_plan({},Plan)'.format(goal),maxresult=1))
        self.printGraph(plan)

        graphplan.retractall('object(_)')
        graphplan.retractall('can(_,_)')
        graphplan.retractall('effects(_,_)')
        graphplan.retractall('block(_)')
        graphplan.retractall('place(_)')
        graphplan.retract(inital_state)

        
    def initMenu(self):
        button1 = Button(self.menu_frame,text='4x4',command = self.drawBoard3x3).pack(side=LEFT)
        button2 = Button(self.menu_frame,text='3x3', command = self.drawBoard3x3).pack(side=LEFT)
        button3 = Button(self.menu_frame,text='Osiem Hetmanow', command = self.drawBoard3x3).pack(side=LEFT)
        button4 = Button(self.menu_frame,text='CargoBot', command = self.cargoBOT).pack(side=LEFT)
        button5 = Button(self.menu_frame,text='Wygeneruj graf', bg='white',command = self.get_graph).pack(side=LEFT)

    def setValue(self,value,popup,options):
        index = 0
        for i,elem in enumerate(options):
            if value == elem: 
                self.pressed_button['text']=value
                index = options.index(value)
                options.remove(value)
        popup.delete(index)

    def assign(self,button,popup):
        try:         
            self.pressed_button = button
            popup.tk_popup(button.winfo_rootx(), button.winfo_rooty(), 0)
        finally:
            popup.grab_release()
    
    def drawBoard3x3(self):
        self.clear_boards()
        self.chosen_option=1
        canvas_left = Canvas(self.left_panel, width=600, height=600)
        canvas_left.configure(background='white')
        for i in range(3):
            for j in range(3):
                canvas_left.create_rectangle(200*i,200*j,200*(i+1),200*(j+1))
        canvas_left.create_rectangle(200,0,400,200)
        canvas_left.create_rectangle(400,0,600,200)
        canvas_left.create_rectangle(0,200,200,400)
        canvas_left.create_rectangle(200,200,400,400)
        canvas_left.create_rectangle(400,200,600,400)
        canvas_left.create_rectangle(0,400,200,600)
        canvas_left.create_rectangle(200,400,400,600)
        canvas_left.create_rectangle(400,400,600,600)
        options=['1','2','3','4','5','6','7','8','']
        popup = Menu(canvas_left, tearoff=0)
        for option in options:
            popup.add_command(label=option,command = lambda i=option:self.setValue(i,popup,options))
        button1 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button1,popup))
        button1.place(x=10,y=10)

        button2 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button2,popup))
        button2.place(x=210,y=10)

        button3 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button3,popup))
        button3.place(x=410,y=10)

        button4 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button4,popup))
        button4.place(x=10,y=210)

        button5 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button5,popup))
        button5.place(x=210,y=210)

        button6 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button6,popup))
        button6.place(x=410,y=210)


        button7 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button7,popup))
        button7.place(x=10,y=410)

        button8 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button8,popup))
        button8.place(x=210,y=410)

        button9 = Button(canvas_left,width=19,height=10,bg='white',text='',command = lambda:  self.assign(button9,popup))
        button9.place(x=410,y=410)
        canvas_left.pack()
        self.buttons.append(button1)
        self.buttons.append(button2)
        self.buttons.append(button3)
        self.buttons.append(button4)
        self.buttons.append(button5)
        self.buttons.append(button6)
        self.buttons.append(button7)
        self.buttons.append(button8)
        self.buttons.append(button9)

    def assign_table(self,index,popup,button,blocks):
        height = 0
        pos = 0
        block_name = ''
        width = 550/len(blocks)
        for i in range(len(blocks)):
            if(index in blocks[i]):
                pos = i
                height = len(blocks[i])
                blocks[i].append(button['text'])
                block_name = blocks[i][-1]
        for i in range(len(blocks)):
            if(block_name in blocks[i] and i != pos):
                blocks[i].remove(block_name)
        print(blocks)
        self.cargo_button.place(x=width*int(pos)+(width/4),y=532-(18*3*height),anchor='nw')


    def chose_table(self,button,canvas,blocks):
        table_menu = Menu(canvas, tearoff=0)
        self.cargo_button = button
        for element in blocks:
            table_menu.add_command(label=str(element[0]),command = lambda i=element[0]:self.assign_table(i,table_menu,button,blocks))
        try:         
            table_menu.tk_popup(button.winfo_rootx(), button.winfo_rooty(), 0)
        finally:
            table_menu.grab_release()

    def add_block(self,canvas,blocks,panel):
        counter=0
        for i in range(len(blocks)):
            counter=counter+len(blocks[i])
        counter=counter-len(blocks)

        button = Button(panel,width=3,height=3,text=chr(97+counter),bg='orange',command = lambda: self.chose_table(button,canvas,blocks))
        button.place(x=0,y=0)
    
    def add_table(self,canvas,blocks):
        table_id=-1
        table_id = canvas.create_line(25,550,575,550)
        label_id = canvas.create_text(275,580, text=table_id)
        blocks.append([table_id])
        table_width = 550/len(blocks)
        for i in range(len(blocks)):
            table = blocks[i][0]
            left_side = (table_width * i)+10
            right_side = (table_width * (i+1))-10
            canvas.coords(table, left_side, 550, right_side, 550)
            canvas.coords(table+1,right_side - (table_width/2),580)
        #print(blocks)

    def cargoBOT(self):
        self.clear_boards()
        self.chosen_option=3
        canvas_left = Canvas(self.left_panel, width=600, height=600)
        canvas_left.create_text(300,30,text='Stan poczatkowy:')
        table_button = Button(self.left_panel,width=10,height=3,text='Dodaj polke',command = lambda: self.add_table(canvas_left,self.cargo_blocks_left))
        block_button = Button(self.left_panel,width=10,height=3,text='Dodaj blok',command= lambda: self.add_block(canvas_left,self.cargo_blocks_left,self.left_panel))
        block_button.place(x=350,y=50,anchor='nw')
        table_button.place(x=150,y=50,anchor='nw')
        canvas_left.pack()
        canvas_left.configure(background='white')

        canvas_right = Canvas(self.right_panel, width=600, height=600)
        canvas_right.create_text(300,30,text='Stan koncowy: ')
        table_button_right = Button(self.right_panel,width=10,height=3,text='Dodaj polke',command = lambda: self.add_table(canvas_right,self.cargo_blocks_right))
        block_button_right = Button(self.right_panel,width=10,height=3,text='Dodaj blok',command= lambda: self.add_block(canvas_right,self.cargo_blocks_right,self.right_panel))
        block_button_right.place(x=350,y=50,anchor='nw')
        table_button_right.place(x=150,y=50,anchor='nw')
        canvas_right.pack()
        canvas_right.configure(background='white')


    def printGraph(self,plan):
        g = parsePlanFULL.Graph('outputs/output.txt')
        #graphplan.assertz('state0([na(a,1),pusty(2)])')
        #plan = list(graphplan.query('call_plan([na(a,2)],Plan)',maxresult=1))
        g.run_all()
        plan = g.return_plan()

        sg = parseplanSIMPLIFIED.SimplifiedGraph('outputs/output.txt')
        sg.run_all()
        simple_plan = sg.return_plan()
        print(plan)

        print(simple_plan)
        
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        canvas = Canvas(self.right_panel,width=600,height=600)
        canvas.configure(background='white')
        canvas.pack()
        canvas.create_text(300,30,text='Plik z grafami znajduja sie pod nastepujaca nazwa')
        canvas.create_text(300,60,text='FULL_GRAPHPLAN.gv.png')
        canvas.create_text(300,90,text='Wygenerowany plan: ')

        if(self.chosen_option==1):
            for i in range(len(plan)):
                command = plan[i].rstrip(')').split(',')
                command[0] = command[0][4:]
                print(command)
                canvas.create_text(300,120+(30*i),text='Krok {}: Zamien klocek pusty z klockiem {}'.format(i+1,chr(ord(command[0])-48)))
        else:
            for i in range(len(plan)):
                command = plan[i].rstrip(')').split(',')
                command[0] = command[0][4:]
                canvas.create_text(300,120+(30*i),text='Krok {}: Przenies klocek {} z {} na {}'.format(i+1,command[0],command[1],command[2]))
        
        '''
        canvas2 = Canvas(self.right_panel,width=600,height=600) 
        canvas2.pack()  
        self.img = ImageTk.PhotoImage(Image.open("FULL_GRAPHPLAN.gv.png"))  
        canvas2.create_image(300,300, image=self.img)
        '''
        


def main():
    gui = GUI()



if __name__=='__main__':
    main()
    
