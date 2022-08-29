# Importando modulos
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import sqlite3
# *********APIS**********
# Apis de texto aleatoreo
url_random_text = 'http://metaphorpsum.com/paragraphs/1/1'
response = requests.get(url_random_text)


# ******INSERTANDO CONTENIDO DEL API EN UN DICCIONARIO******
# Inersion de texto random
if response.status_code == 200:
    random_text = response.content.decode('UTF-8')

# ******CONSTANTS******
running = False
minutes, seconds, milliseconds = 0, 0, 0

# ******CREACION DE VENTANA******
class typing_program:

    db_name = 'database.db'

    def __init__(self):
        
        self.root = tk.Tk()
        self.root.geometry('485x220')
        self.root.title('Typing Game')
        self.root.config(background="#373733")

        # Title
        self.stopwatch_label = tk.Label(text='Typing Game', font=('Roboto mono', 70), fg='#ffffff', bg='#373733')
        self.stopwatch_label.pack()

        # label to display time
        self.stopwatch_label = tk.Label(text='00:00:00', font=('Roboto mono', 70), fg='#ffffff', bg='#373733')
        self.stopwatch_label.pack()
        self.letters_label = tk.Label( 
            width = 90, 
            #relief="flat", 
            text=random_text, 
            font=('Roboto mono', 15), 
            fg='#ffffff', 
            bg='#373733',
            wraplength=990
            )
        self.letters_label.pack(padx=1, pady=1)
        
        self.entry_text = Entry(font = ("Calibri 20"))
        self.entry_text.focus()
        self.entry_text.pack(pady=50)

        frame = LabelFrame(text = "Record", bg='#373733',relief="flat", font=('Roboto mono', 20), fg='#ffffff')
        frame.pack()

        #Table
        columns = ('Time','Text','Total',)
        self.tree = ttk.Treeview(frame, height = 14, columns=columns, show='headings')
        self.tree.grid(row = 0, column = 0, columnspan = 4, padx = 5, pady = 1) 
        # define headings
        self.tree.heading('Time', text='Time')
        self.tree.heading('Text', text='Text')
        self.tree.heading('Total', text='Total Words')
        

        # Keybind binds
        #Pause
        self.root.bind("<Return>", self.pause)
        #Start
        self.root.bind("<Key>", self.start)

        # MAINLOOP
        # RUN APP
        self.get_products()
        self.root.mainloop()


    def start(self, event):
        global running
        if not running and event.char == random_text[0]:
            self.update()
            running = True


    def pause(self, event):
        # if event.char == "Key.Enter":
        global hours, minutes, seconds
        global running
        if running:
            # cancel updating of time using after_cancel()
            self.stopwatch_label.after_cancel(update_time)
            running = False
            self.get_user_text()
            self.add_record()

    # update stopwatch function
    def update(self):
        # update seconds with (addition) compound assignment operator
        global minutes, seconds, milliseconds
        milliseconds += 1
        if milliseconds == 60:
            seconds += 1
            milliseconds = 0
        if seconds == 60:
            minutes += 1
            seconds = 0
        # format time to include leading zeros
        minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
        seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
        milliseconds_string = f'{milliseconds}' if milliseconds > 9 else f'0{milliseconds}'
        # update timer label after 1000 ms (1 second)
        self.stopwatch_label.config(text=minutes_string + ':' + seconds_string + ':' + milliseconds_string)
        # after each second (1000 milliseconds), call update function
        # use update_time variable to cancel or pause the time using after_cancel

        global update_time
        update_time = self.stopwatch_label.after(10, self.update)
    
    def get_user_text(self):
        self.user_text = self.entry_text.get()
        self.chequear_si_son_iguales()

    def check_if_are_same(self):
        spliting_random_text = random_text.split()
        spliting_user_text = self.user_text.split()
        self.number_words = len(spliting_user_text)
        
        self.difference_1 = set(spliting_user_text).difference(set(spliting_random_text))
        

        if self.user_text == random_text:
            self.status = 'Son iguales bien hecho'
        else:
            self.status = 'No son iguales'

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def get_products(self):
        #Cleanin table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #quering data
        query = 'SELECT * FROM historioc'
        db_rows = self.run_query(query)
        #Filling data
        for row in db_rows:
            self.tree.insert('',tk.END,values=row)

    """def validation(self):
        return len(self.entry_text.get()) != 0"""

    def add_record(self):
        time = (str(minutes)+':'+str(seconds)+':'+str(milliseconds))
        query = 'INSERT INTO historioc VALUES(?,?,?)'
        parameters = (time,self.status,self.number_words)
        self.run_query(query, parameters)
        print('Datos requeridos')
        print(time)
        self.get_products()


        print(parameters)

if __name__ == '__main__':
    application = typing_program()
    application.mainloop()