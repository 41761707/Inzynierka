import sys
import parsePlanFULL
import parseplanSIMPLIFIED
from tkinter import *
from tkinter import font as tkFont
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
        self.helv36=tkFont.Font(family='Helvetica', size=36)
        self.menu_font = tkFont.Font(family='Helvetica', size=30)
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

    def convert(self,value):
        table = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,'n':14,'o':15}
        return table[value]
    
    def get_graph(self):
        if(self.chosen_option==1):
            self.GRAPHPLAN3x3()
        elif(self.chosen_option==2):
            self.GRAPHPLAN4x4()
        else:
            self.GRAPHPLANCargo()

    def SquaresENV(self,robots,n,goal):
        graphplan = Prolog()
        graphplan.consult('graphplan.pl')
        graphplan.assertz('preconditions(zostan(P),[P])')
        graphplan.assertz('preconditions(idz(R,A,B), [na(R,A), pusty(B)]) :- robot(R), adjacent(A,B)')
        graphplan.assertz('effects(zostan(P),[P])')
        graphplan.assertz('effects(idz(R,A,B), [na(R,B),pusty(A),~na(R,A),~pusty(B)])')
        #robots = ['a','b','c','d','e','f','g','h']
        for robot in robots:
            graphplan.assertz('robot({})'.format(robot))
        graphplan.assertz('adjacent(A,B) :- n(A,B) ; n(B,A)')
        #n = [[2,4],[1,3,5],[2,6],[1,5,7],[4,6,2,8],[5,3,9],[4,8],[7,5,9],[8,6]]
        for i in range(len(n)):
            for element in n[i]:
                graphplan.assertz('n({},{})'.format(i+1,element))
        graphplan.assertz('inconsistent(G,~G)')
        graphplan.assertz('inconsistent(~G,G)')
        graphplan.assertz('inconsistent(na(R,C1),na(R,C2)) :- C1 \== C2')
        graphplan.assertz('inconsistent(na(_,C),pusty(C))')
        graphplan.assertz('inconsistent(pusty(C),na(_,C))')
        graphplan.assertz('inconsistent(na(R1,C),na(R2,C)) :- R1 \== R2')
        command = 'inital_state(['
        for i,button in enumerate(self.buttons):
            if button['text'] == '':
                command = command + 'pusty({}),'.format(i+1)
            else:
                command = command + 'na({},{}),'.format(chr(96+int(button['text'])),i+1)
        command = command[:len(command)-1]
        command = command+'])'
        print(command)
        graphplan.assertz(command)
        plan = list(graphplan.query('call_plan([{}],Plan)'.format(goal),maxresult=1))
        self.printGraph(plan)
        graphplan.retractall('n(_,_)')
        graphplan.retractall('preconditions(_,_)')
        graphplan.retractall('effects(_,_)')
        graphplan.retractall('robot(_)')
        graphplan.retractall('adjacent(_,_)')
        graphplan.retractall('incosistent(_,_)')
        graphplan.retract(command)

    def GRAPHPLAN3x3(self):
        robots = ['a','b','c','d','e','f','g','h']
        n = [[2,4],[1,3,5],[2,6],[1,5,7],[4,6,2,8],[5,3,9],[4,8],[7,5,9],[8,6]]
        goal = 'na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),pusty(9)'
        self.SquaresENV(robots,n,goal)
    def GRAPHPLAN4x4(self):
        robots = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o']
        n=[[2,5],[1,6,3],[2,7,4],[3,8],[1,6,9],[5,2,7,10],[6,3,8,11],[7,4,12],[5,10,13],[9,6,11,14],[10,7,12,15],[11,8,16],[9,14],[13,10,15],[14,11,16],[15,12]]
        goal='na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),na(i,9),na(j,10),na(k,11),na(l,12),na(m,13),na(n,14),na(o,15),pusty(16)'
        self.SquaresENV(robots,n,goal)

    def GRAPHPLANCargo(self):
        graphplan = Prolog()
        graphplan.consult('graphplan.pl')
        inital_state = "inital_state(["
        goal = "["
        print(self.cargo_blocks_left)
        for tab in self.cargo_blocks_left:
            graphplan.assertz("place({})".format(tab[0]))
            for i in range(len(tab)-1):
                graphplan.assertz("block({})".format(tab[i+1]))
        graphplan.assertz("preconditions(zostan(P),[P])")
        graphplan.assertz("preconditions(idz(Block,From,To), [pusty(Block),pusty(To),na(Block,From)]) :- block(Block), object(To), To \==Block, object(From), From \==To, Block \== From")     
        graphplan.assertz("effects(zostan(P),[P])")
        graphplan.assertz("effects(idz(X,From,To),[na(X,To),pusty(From),~na(X,From),~pusty(To)])")   
        graphplan.assertz("object(X) :- place(X);block(X)")
        graphplan.assertz('incosistent(G,~G)')
        graphplan.assertz('incosistent(~G,G)')
        graphplan.assertz('incosistent(na(R,C1),na(R,C2)) :- C1 \== C2')
        graphplan.assertz('inconsistent(na(_,C),pusty(C))')
        graphplan.assertz('inconsistent(pusty(C),na(_,C))')
        graphplan.assertz('inconsistent(na(R1,C),na(R2,C)) :- R1 \== R2')

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
        print(inital_state)
        print(goal)
        graphplan.assertz(inital_state)
        plan = list(graphplan.query('call_plan({},Plan)'.format(goal),maxresult=1))
        self.printGraph(plan)

        graphplan.retractall('inital_state(_)')
        graphplan.retractall('object(_)')
        graphplan.retractall('preconditions(_,_)')
        graphplan.retractall('effects(_,_)')
        graphplan.retractall('block(_)')
        graphplan.retractall('place(_)')
        graphplan.retractall(inital_state)
        graphplan.retractall(goal)

        
    def initMenu(self):
        button1 = Button(self.menu_frame,text='3x3',font=self.menu_font,command = self.drawBoard3x3).pack(side=LEFT)
        button2 = Button(self.menu_frame,text='4x4',font=self.menu_font, command = self.drawBoard4x4).pack(side=LEFT)
        button3 = Button(self.menu_frame,text='N Hetmanow',font=self.menu_font, command = self.drawBoard3x3).pack(side=LEFT)
        button4 = Button(self.menu_frame,text='CargoBot',font=self.menu_font, command = self.cargoBOT).pack(side=LEFT)
        button5 = Button(self.menu_frame,text='Wygeneruj graf',font=self.menu_font, bg='white',command = self.get_graph).pack(side=LEFT)

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
            self.pressed_button = self.buttons[button]
            popup.tk_popup(self.buttons[button].winfo_rootx(), self.buttons[button].winfo_rooty(), 0)
        finally:
            popup.grab_release()
    
    def drawBoard4x4(self):
        self.clear_boards()
        self.chosen_option=2
        self.helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')
        canvas_left = Canvas(self.left_panel, width=600, height=600)
        canvas_left.configure(background='white')
        options=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','']
        popup = Menu(canvas_left, tearoff=0)
        self.buttons=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        for i in range(4):
            for j in range(4):
                button_number=4*j+i
                self.buttons[button_number]=(Button(canvas_left,width=5,height=3,font=self.helv36,bg='brown',text='',command = lambda x=button_number: self.assign(x,popup)))
                self.buttons[button_number].place(x=(150*i),y=(150*j))
        for option in options:
            popup.add_command(label=option,command = lambda i=option:self.setValue(i,popup,options))
        canvas_left.pack()

    def drawBoard3x3(self):
        self.clear_boards()
        self.chosen_option=1
        self.helv36 = tkFont.Font(family='Helvetica', size=36, weight='bold')
        canvas_left = Canvas(self.left_panel, width=600, height=600)
        canvas_left.configure(background='white')
        options=['1','2','3','4','5','6','7','8','']
        popup = Menu(canvas_left, tearoff=0)
        self.buttons=[1,2,3,4,5,6,7,8,9]
        for i in range(3):
            for j in range(3):
                button_number=3*j+i
                self.buttons[button_number]=(Button(canvas_left,width=7,height=4,bg='brown',font=self.helv36,text='',command = lambda x=button_number: self.assign(x,popup)))
                self.buttons[button_number].place(x=(200*i),y=(200*j))
        for option in options:
            popup.add_command(label=option,command = lambda i=option:self.setValue(i,popup,options))
        canvas_left.pack()

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
        self.cargo_button.place(x=width*int(pos)+(width/4),y=542-(18*3*height),anchor='nw')


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

        button = Button(panel,width=1,height=1,text=chr(97+counter),bg='orange',font=self.helv36,command = lambda: self.chose_table(button,canvas,blocks))
        button.place(x=0,y=0)
    
    def add_table(self,canvas,blocks,font_used):
        table_id=-1
        table_id = canvas.create_line(25,550,575,550)
        label_id = canvas.create_text(275,580, text=table_id, font=font_used)
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
        helv16 = tkFont.Font(family='Helvetica', size=16, weight='bold')
        canvas_left = Canvas(self.left_panel, width=600, height=600)
        canvas_left.create_text(300,30,text='Stan poczatkowy:')
        table_button = Button(self.left_panel,width=10,height=3,text='Dodaj polke',command = lambda: self.add_table(canvas_left,self.cargo_blocks_left,helv16))
        block_button = Button(self.left_panel,width=10,height=3,text='Dodaj blok',command= lambda: self.add_block(canvas_left,self.cargo_blocks_left,self.left_panel))
        block_button.place(x=350,y=50,anchor='nw')
        table_button.place(x=150,y=50,anchor='nw')
        canvas_left.pack()
        canvas_left.configure(background='white')

        canvas_right = Canvas(self.right_panel, width=600, height=600)
        canvas_right.create_text(300,30,text='Stan koncowy: ')
        table_button_right = Button(self.right_panel,width=10,height=3,text='Dodaj polke',command = lambda: self.add_table(canvas_right,self.cargo_blocks_right,helv16))
        block_button_right = Button(self.right_panel,width=10,height=3,text='Dodaj blok',command= lambda: self.add_block(canvas_right,self.cargo_blocks_right,self.right_panel))
        block_button_right.place(x=350,y=50,anchor='nw')
        table_button_right.place(x=150,y=50,anchor='nw')
        canvas_right.pack()
        canvas_right.configure(background='white')


    def printGraph(self,plan):
        g = parsePlanFULL.Graph('outputs/output.txt')
        g.run_all()

        sg = parseplanSIMPLIFIED.SimplifiedGraph('outputs/output.txt')
        simple_plan = sg.run_all()
        
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        canvas = Canvas(self.right_panel,width=600,height=600)
        canvas.configure(background='white')
        canvas.pack()
        canvas.create_text(300,30,text='Plik z grafami znajduja sie pod nastepujaca nazwa')
        canvas.create_text(300,60,text='FULL_GRAPHPLAN.gv.png - graf pelny')
        canvas.create_text(300,90,text='SIMPLE_GRAPHPLAN.gv.png - graf prosty')
        canvas.create_text(300,120,text='Wygenerowany plan: ')

        counter = 0
        if(self.chosen_option in (1,2)):
            for i in range(len(simple_plan)):
                print(simple_plan[i])
                current_plan = re.split(',(?![^(]*\\))',str(simple_plan[i]))
                for action in current_plan:
                    command = action.rstrip(')').split(',')
                    command[0] = command[0][6:]
                    print(command[0])
                    canvas.create_text(300,150+(30*counter),text='Krok {}: Zamien klocek pusty z klockiem {}'.format(i+1,self.convert(command[0])))
                    counter = counter + 1
        else:
            for i in range(len(simple_plan)):
                print(simple_plan[i])
                current_plan = re.split(',(?![^(]*\\))',str(simple_plan[i]))
                for action in current_plan:
                    command = action.rstrip(')').split(',')
                    command[0] = command[0][6:]
                    canvas.create_text(300,150+(30*counter),text='Krok {}: Przenies klocek {} z {} na {}'.format(i+1,command[0],command[1],command[2]))
                    counter = counter + 1
        


def main():
    gui = GUI()



if __name__=='__main__':
    main()
    