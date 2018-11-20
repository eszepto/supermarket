
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import *
import sqlite3

class SQLite_database(object):
    def __init__(self,dbpath,table):
        import sqlite3
        self.dbfile = dbpath
        self.table = str(table)
        conn= sqlite3.connect("store.db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS
        `stock` (
        `id`TEXT NOT NULL UNIQUE,
        `name`TEXT NOT NULL UNIQUE,
        `price`DOUB NOT NULL,
        `quantity`INTEGER NOT NULL);""")
        conn.commit()
        conn.close()
    def insert(self,ID,name,price,quantity):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("INSERT INTO " + self.table + " VALUES (?,?,?,?)",(ID,name,price,quantity))
        conn.commit()
        conn.close()
    def edit(self,ID,name,price,quantity):
        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        cur.execute("UPDATE " + self.table + " SET name=? , price=? , quantity=? WHERE id=?",(price,quantity,ID,name))
        conn.commit()
        conn.close()
    def delete(self,name):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("DELETE FROM " + self.table + " WHERE name=?",(name, ))
        conn.commit()
        conn.close()
        
#%% back-end
def add_popup():
    def add_item(event=None):
        try:
            ID = str(id_value.get())
            name = str(name_value.get())
            price = float(price_value.get())
            quantity = int(quantity_value.get())
        except:
            error = Label(entry_frame,text="invalid value",font=("Calibri",10),fg="red",anchor="e")
            error.grid(row=4,column=0)
            return
        if(price >= 0 and quantity >= 0):
            try:
                stock.insert(ID,name,price,quantity)
                refresh()
                popup.destroy()
            except:
                error = Label(entry_frame,text="invalid value",font=("Calibri",10),fg="red",anchor="e")
                error.grid(row=4,column=0)
        else: 
            error = Label(entry_frame,text="invalid",font=("Calibri",10),fg="red",anchor="e")
            error.grid(row=4,column=0)
                
    popup = Toplevel()
    popup.grab_set()
    popup.title('Add')
    
    entry_frame = Frame(popup)
    id_label = Label(entry_frame,text='ID : ',anchor='e',width=20)
    id_value = StringVar()
    id_entry = Entry(entry_frame,textvariable=id_value,font=("Calibri",22,'normal'))
    id_entry.bind('<Return>',add_item)
    name_label = Label(entry_frame,text='Name : ',anchor='e',width=20)
    name_value = StringVar()
    name_entry = Entry(entry_frame,textvariable=name_value,font=("Calibri",22,'normal'))
    name_entry.bind('<Return>',add_item)
    price_label = Label(entry_frame,text='Price : ',anchor='e',width=20)
    price_value = StringVar()
    price_entry = Entry(entry_frame,textvariable=price_value,font=("Calibri",22,'normal'))
    price_entry.bind('<Return>',add_item)
    quantity_label = Label(entry_frame,text='Quantity : ',anchor='e',width=20)
    quantity_value = StringVar()
    quantity_entry = Entry(entry_frame,textvariable=quantity_value,font=("Calibri",22,'normal'))
    quantity_entry.bind('<Return>',add_item)

    menu_frame = Frame(popup)
    add_button = Button(menu_frame,text='Add',command=add_item,font="TkDefaultFont 16")
    cancel_button = Button(menu_frame,text='Cancel',command=lambda:popup.destroy(),font="Helvetica 16")

    entry_frame.grid(row=0,padx=10,pady=10)
    menu_frame.grid(row=1)
    id_label.grid(row=0,column=0)
    id_entry.grid(row=0,column=1)
    name_label.grid(row=1,column=0,pady=10)
    name_entry.grid(row=1,column=1,pady=10)
    price_label.grid(row=2,column=0)
    price_entry.grid(row=2,column=1)
    quantity_label.grid(row=3,column=0,pady=10)
    quantity_entry.grid(row=3,column=1,pady=10)

    add_button.grid(row=0,column=0,padx=15,ipadx=16,pady=25)
    cancel_button.grid(row=0,column=1)

    popup.mainloop()

def edit_popup():
    def edit_item(event=None):
        try:
            ID = str(id_value.get())
            name = str(name_value.get())
            price = float(price_value.get())
            quantity = int(quantity_value.get())
        except:
            error = Label(entry_frame,text="invalid value",font=("Calibri",10),fg="red",anchor="e")
            error.grid(row=4,column=0)
            return
        if(price >= 0 and quantity >= 0):
            try:
                stock.edit(ID,name,price,quantity)
                refresh()
                popup.destroy()
            except:
                error = Label(entry_frame,text="invalid value",font=("Calibri",10),fg="red",anchor="e")
                error.grid(row=4,column=0)
        else: 
            error = Label(entry_frame,text="invalid value",font=("Calibri",10),fg="red",anchor="e")
            error.grid(row=4,column=0)

    #UI Part 1
    popup = Toplevel()
    popup.grab_set()
    popup.title('Edit')

    entry_frame = Frame(popup)
    id_label = Label(entry_frame,text='ID : ',anchor='e',width=20)
    id_value = StringVar()
    id_entry = Entry(entry_frame,textvariable=id_value,font=("Calibri",22,'normal'))
    id_entry.bind('<Return>',edit_item)
    name_label = Label(entry_frame,text='Name : ',anchor='e',width=20)
    name_value = StringVar()
    name_entry = Entry(entry_frame,textvariable=name_value,font=("Calibri",22,'normal'))
    name_entry.bind('<Return>',edit_item)
    price_label = Label(entry_frame,text='Price : ',anchor='e',width=20)
    price_value = StringVar()
    price_entry = Entry(entry_frame,textvariable=price_value,font=("Calibri",22,'normal'))
    price_entry.bind('<Return>',edit_item)
    quantity_label = Label(entry_frame,text='Quantity : ',anchor='e',width=20)
    quantity_value = StringVar()
    quantity_entry = Entry(entry_frame,textvariable=quantity_value,font=("Calibri",22,'normal'))
    quantity_entry.bind('<Return>',edit_item)

    menu_frame = Frame(popup)
    OK_button = Button(menu_frame,text='OK',command=edit_item,font="TkDefaultFont 16")
    cancel_button = Button(menu_frame,text='Cancel',command=lambda:popup.destroy(),font="Helvetica 16")
    
    #UI part 1 - placing
    entry_frame.grid(row=0,padx=10,pady=10)
    menu_frame.grid(row=1)
    id_label.grid(row=0,column=0)
    id_entry.grid(row=0,column=1)
    name_label.grid(row=1,column=0,pady=10)
    name_entry.grid(row=1,column=1,pady=10)
    price_label.grid(row=2,column=0)
    price_entry.grid(row=2,column=1)
    quantity_label.grid(row=3,column=0,pady=10)
    quantity_entry.grid(row=3,column=1,pady=10)

    OK_button.grid(row=0,column=0,padx=15,ipadx=16,pady=25)
    cancel_button.grid(row=0,column=1)
    
    #UI part 2
    value_in_selected = stock_table.item(stock_table.focus())

    ID = value_in_selected['text']    #because ['values'] cannot store '001' ,it will automatically change to '1'
    id_entry.insert(END,ID)
    id_entry.config(state=DISABLED)
    name = value_in_selected['values'][1]
    name_entry.insert(END,name)
    #name_entry.config(state=DISABLED)
    price = value_in_selected['values'][2]
    price_entry.insert(END,price)
    quantity = value_in_selected['values'][3]
    quantity_entry.insert(END,quantity)
            
    popup.mainloop()

def del_popup():
    name = str(stock_table.item(stock_table.focus())['values'][1])
    if messagebox.askyesno("Delete","Delete '" + name +"' ?"):
        stock.delete(name)
        refresh()
    else:
        pass
   
def view():
    conn = sqlite3.connect('store.db')
    cur = conn.cursor()
    cur.execute("select * from stock")
    data = cur.fetchall()
    conn.close()
    return data

def refresh():
    stock_table.delete(*stock_table.get_children())
    for i in view():
        i = tuple(map(str,i))
        stock_table.insert('','end',text=i[0],value=i)  #because value cannot store '001' ,it will automatically change to '1' ,but text can.
    disable_button()

def treeview_sort_column(tv, col, reverse):
    #----------StackOverflow copyright :D --------------------
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
        treeview_sort_column(tv, col, not reverse))

def disable_button(event=None):
    edit_button.config(state=DISABLED)
    del_button.config(state=DISABLED)
def enable_button(event=None):
    edit_button.config(state=NORMAL)
    del_button.config(state=NORMAL)

def on_click(event=None):
    region = stock_table.identify("region", event.x, event.y)
    if(region == 'cell'):
        enable_button()
def on_doubleclick(event=None):
    region = stock_table.identify("region", event.x, event.y)
    if(region == 'cell'):
        #enable_button()
        edit_popup()

#%%    front-end creating components
stock = SQLite_database('store.db','stock')

mainwin = Tk()
mainwin.title('Manager')

Leftframe = Frame(mainwin)
Leftframe.grid(column=0,row=0,sticky="NSEW")
mainwin.grid_columnconfigure(0,weight=1)

Rightframe = Frame(mainwin)
Rightframe.grid(column=1,row=0,sticky="NSEW")
mainwin.grid_columnconfigure(1,weight=0)
mainwin.grid_rowconfigure(0,weight=1)

add_button = Button(Rightframe,text='ADD',command=add_popup,height=2,width=8)
edit_button = Button(Rightframe,text='EDIT',command=edit_popup,height=2,width=8)
del_button = Button(Rightframe,text='DEL',command=del_popup,height=2,width=8)
refresh_button = Button(Rightframe,text='Refresh',width="8",height="1",command=refresh)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Calibri', 14),rowheight=40)
style.configure("Treeview",font=('Calibri',12),rowheight=40)

stock_table = ttk.Treeview(Leftframe,columns=('id','name','price','quantity'),show='headings')
stock_table.bind('<Button-1>',on_click)
stock_table.bind('<Double-Button-1>',on_doubleclick)
vsb = ttk.Scrollbar(Leftframe, orient="vertical", command=stock_table.yview)

stock_table.configure(yscrollcommand=vsb.set)

stock_table.heading('id',text='ID',command=lambda:treeview_sort_column(stock_table, 'id', True))
stock_table.column('id',anchor='center',width=100)
stock_table.heading('name',text='Name',command=lambda:treeview_sort_column(stock_table, 'name', True))
stock_table.column('name',anchor='center',width=250)
stock_table.heading('price',text='Price',command=lambda:treeview_sort_column(stock_table, 'price', True))
stock_table.column('price',anchor='center',width=120)
stock_table.heading('quantity',text='Quantity',command=lambda:treeview_sort_column(stock_table, 'quantity', True))
stock_table.column('quantity',anchor='center',width=75)

#%% layouting
stock_table.grid(row=0,column=0,sticky="NSEW")
Leftframe.grid_columnconfigure(0,weight=1)
vsb.grid(row=0,column=1,sticky="NSEW")
Leftframe.grid_rowconfigure(0,weight=1)
refresh_button.pack(side='top',anchor='e',pady=10,padx=5)
add_button.pack(side='top',pady=5,padx=5)
edit_button.pack(side='top',pady=5,padx=5)
del_button.pack(side='top',pady=5,padx=5)

refresh()
mainwin.mainloop()

# milestone@250 Yeahhhh  :D  :D  :D












# milestone@300 Yeahhhh  :D  :D  :D
