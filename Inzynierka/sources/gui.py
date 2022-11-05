import sys
import parsePlanFULL
from tkinter import *
from PIL import ImageTk,Image
from pyswip import Prolog

class GUI:
    def __init__(self):
        self.current_option = -1
        self.pressed_button = ""
        self.buttons = []
        self.cargo_button = ""
        self.cargo_blocks = []
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

    def convert(self,value):
        table = ['a','b','c','d','e','f','g','h']
        return table[int(value)-1]
    
    def runGRAPHPLAN(self):
        graphplan = Prolog()
        graphplan.consult('graphplan.pl')
        command = 'state0(['
        for i,button in enumerate(self.buttons):
            if button['text'] == '':
                command = command + 'pusty({}),'.format(i+1)
            else:
                command = command + 'na({},{}),'.format(self.convert(button['text']),i+1)
        command = command[:len(command)-1]
        command = command+'])'
        graphplan.assertz(command)
        plan = list(graphplan.query('call_plan([na(a,1),na(b,2),na(c,3),na(d,4),na(e,5),na(f,6),na(g,7),na(h,8),pusty(9)],Plan)',maxresult=1))
        g = parsePlanFULL.Graph('outputs/output.txt')
        #graphplan.assertz('state0([na(a,1),pusty(2)])')
        #plan = list(graphplan.query('call_plan([na(a,2)],Plan)',maxresult=1))
        g.run_all()
        plan = g.return_plan()
        print(plan)
        self.printGraph()
    def initMenu(self):
        button1 = Button(self.menu_frame,text='4x4',command = self.drawBoard3x3).pack(side=LEFT)
        button2 = Button(self.menu_frame,text='3x3', command = self.drawBoard3x3).pack(side=LEFT)
        button3 = Button(self.menu_frame,text='Osiem Hetmanow', command = self.drawBoard3x3).pack(side=LEFT)
        button4 = Button(self.menu_frame,text='CargoBot', command = self.cargoBOT).pack(side=LEFT)
        button5 = Button(self.menu_frame,text='Wygeneruj graf', bg='white',command = self.runGRAPHPLAN).pack(side=LEFT)

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
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        canvas_left = Canvas(self.left_panel, width=600, height=600)
        canvas_left.configure(background='white')
        canvas_left.create_rectangle(0,0,200,200)
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
        #for option in options:
        #    popup.add_command(label=option,command = lambda:self.setValue(option,popup,options))
        popup.add_command(label="1",command = lambda:self.setValue('1',popup,options))
        popup.add_command(label="2",command = lambda:self.setValue('2',popup,options))
        popup.add_command(label="3",command = lambda:self.setValue('3',popup,options))
        popup.add_command(label="4",command = lambda:self.setValue('4',popup,options))
        popup.add_command(label="5",command = lambda:self.setValue('5',popup,options))
        popup.add_command(label="6",command = lambda:self.setValue('6',popup,options))
        popup.add_command(label="7",command = lambda:self.setValue('7',popup,options))
        popup.add_command(label="8",command = lambda:self.setValue('8',popup,options))
        popup.add_command(label="",command = lambda:self.setValue('',popup,options))
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

    def assign_table(self,index,popup,button):
        height = 0
        pos = 0
        width = 550/len(self.cargo_blocks)
        for i in range(len(self.cargo_blocks)):
            if(index in self.cargo_blocks[i]):
                pos = i
                height = len(self.cargo_blocks[i])
                self.cargo_blocks[i].append(button['text'])
        print(self.cargo_blocks)
        self.cargo_button.place(x=width*int(pos)+(width/2),y=532-(18*3*height),anchor='nw')


    def chose_table(self,button,canvas):
        table_menu = Menu(canvas, tearoff=0)
        self.cargo_button = button
        for element in self.cargo_blocks:
            table_menu.add_command(label=str(element[0]),command = lambda i=element[0]:self.assign_table(i,table_menu,button))
        try:         
            table_menu.tk_popup(button.winfo_rootx(), button.winfo_rooty(), 0)
        finally:
            table_menu.grab_release()

    def add_block(self,canvas):
        counter=0
        for i in range(len(self.cargo_blocks)):
            counter=counter+len(self.cargo_blocks[i])
        counter=counter-len(self.cargo_blocks)

        button = Button(self.left_panel,width=3,height=3,text=chr(97+counter),bg='orange',command = lambda: self.chose_table(button,canvas))
        button.place(x=0,y=0)
    
    def add_table(self,canvas):
        table_id=-1
        table_id = canvas.create_line(25,550,575,550)
        self.cargo_blocks.append([table_id])
        table_width = 550/len(self.cargo_blocks)
        for i in range(len(self.cargo_blocks)):
            table = self.cargo_blocks[i][0]
            print(table)
            left_side = (table_width * i)+10
            print(left_side)
            right_side = (table_width * (i+1))-10
            print(right_side)
            canvas.coords(table, left_side, 550, right_side, 550)
        print(self.cargo_blocks)

    def cargoBOT(self):
        for widget in self.left_panel.winfo_children():
            widget.destroy()
        for widget in self.right_panel.winfo_children():
            widget.destroy()
        canvas_left = Canvas(self.left_panel, width=600, height=600)
        table_button = Button(self.left_panel,width=10,height=3,text='Dodaj polke',command = lambda: self.add_table(canvas_left))
        block_button = Button(self.left_panel,width=10,height=3,text='Dodaj blok',command= lambda: self.add_block(canvas_left))
        block_button.place(x=350,y=0,anchor='nw')
        table_button.place(x=150,y=0,anchor='nw')
        canvas_left.pack()
        canvas_left.configure(background='white')


    def printGraph(self):
        canvas2 = Canvas(self.right_panel,width=600,height=600) 
        canvas2.pack()  
        self.img = ImageTk.PhotoImage(Image.open("FULL_GRAPHPLAN.gv.png"))  
        canvas2.create_image(300,300, image=self.img)
        


def main():
    gui = GUI()



if __name__=='__main__':
    main()
    
