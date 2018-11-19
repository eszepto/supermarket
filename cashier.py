
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import *
import sqlite3
total = 0.0
class store_SQLite_database(object):
    def __init__(self,dbpath,table):
        import sqlite3
        self.dbfile = dbpath
        self.table = str(table)
        
    def insert(self,ID,name,price,quantity):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("INSERT INTO " + self.table + " VALUES (?,?,?,?)",(ID,name,price,quantity))
        conn.commit()
        conn.close()
    def edit(self,ID,name,price,quantity):
        conn = sqlite3.connect('store.db')
        cur = conn.cursor()
        cur.execute("UPDATE " + self.table + " SET price=? , quantity=? WHERE id=? and name=?",(price,quantity,ID,name))
        conn.commit()
        conn.close()
    def plusQtyByidorname(self,id,name,qty):
        conn = sqlite3.connect(self.dbfile,timeout=10)
        cur = conn.cursor()
        cur.execute("update " + self.table + " set quantity=quantity + ? where id = ? or name = ?",(qty,id,name))
        conn.commit()
        conn.close()
    def delete(self,name):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("DELETE FROM " + self.table + " WHERE name=?",(name, ))
        conn.commit()
        conn.close()
    def getByidorname(self,id,name):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("select * from " + self.table + " where id=? or name=?",(id,name))
        data = cur.fetchall()
        return data
    def getall(self):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("select * from " + self.table )
        data = cur.fetchall()
        conn.close()
        return data

class sell_SQLite_database(object):
    def __init__(self,dbpath,table):
        import sqlite3
        self.dbfile = dbpath
        self.table = str(table)
        conn= sqlite3.connect("sell.db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS
        `sell` (
        `item_id`	TEXT NOT NULL UNIQUE,
	    `item_name`	TEXT NOT NULL UNIQUE,
	    `item_price` NUMERIC NOT NULL,
	    `item_qty`	INTEGER NOT NULL,
	    `total_price` NUMERIC NOT NULL);""")
        conn.commit()
        conn.close()
    def insert(self,ID,name,price,quantity,total_price):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("INSERT INTO " + self.table + " VALUES (?,?,?,?,?)",(ID,name,price,quantity,total_price))
        conn.commit()
        conn.close()

    def delete(self,name):
        conn = sqlite3.connect(self.dbfile,timeout=10)
        cur = conn.cursor()
        cur.execute("DELETE FROM " + self.table + " WHERE item_name=?",(name, ))
        conn.commit()
        conn.close()

    def deleteall(self):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("DELETE FROM " + self.table)
        conn.commit()
        conn.close()
        
    def getByidorname(self,item_id,name):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("select * from " + self.table + " where item_id=? or item_name=?",(item_id,name))
        data = cur.fetchall()
        conn.close()
        return data

    def getall(self):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("select * from " + self.table )
        data = cur.fetchall()
        conn.close()
        return data
    
    def getIDandQty(self):
        conn = sqlite3.connect(self.dbfile)
        cur = conn.cursor()
        cur.execute("select item_id,item_qty from " + self.table)
        data = cur.fetchall()
        conn.close()
        return data

    def plusQtyByidorname(self,id,name,qty):
        conn = sqlite3.connect(self.dbfile,timeout=10)
        cur = conn.cursor()
        cur.execute("update " + self.table + " set item_qty=item_qty + ? where item_id = ? or item_name = ?",(qty,id,name))
        conn.commit()
        conn.close()
    
    def sumprice(self):
        conn = sqlite3.connect(self.dbfile,timeout=10)
        cur = conn.cursor()
        cur.execute("select total_price from sell")
        totalprice = cur.fetchall()
        conn.commit()
        conn.close()
        sump=float(0)
        for i in totalprice:
            for j in i:
                sump += j
        return sump
    
def add_item(Event=None):
    try:
        item_id = str(text_id.get())
        item_name = str(text_name.get())
        item_qty = int(text_qty.get())
    except:
        showerror('error','invalid value')
        return

    check_store = store_db.getByidorname(item_id,item_name)
    check_sell = sell_db.getByidorname(item_id,item_name)
    
    if(check_store != []):
        data = check_store
    
        item_id = str(data[0][0])
        item_name = str(data[0][1])
        item_price = float(data[0][2])
        stock_qty = int(data[0][3])
        item_qty = int(item_qty)
        total_price = item_qty * item_price
        
        if(item_qty <= stock_qty):
            if(check_sell == []):
                    sell_db.insert(item_id,item_name,item_price,item_qty,total_price)
                    clear_input()
                    button_pay.config(state=NORMAL)
            elif(check_sell != []):
                incart_qty = int(check_sell[0][3])
                if(item_qty + incart_qty <= stock_qty):
                    sell_db.plusQtyByidorname(item_id,item_name,item_qty)
                    clear_input()
                    button_pay.config(state=NORMAL)
                else:
                    showerror("error"," Store_qty isn't enough!")
        else:
            showerror("error","Store_qty isn't enough!")
    else:
        showerror('error','Not found!')
    
    refresh()
    
def delete(Event=None):
    name = str(sell_table.item(sell_table.focus())['values'][1])
    
    if messagebox.askyesno("Delete","Delete '" + name +"' ?"):
        sell_db.delete(name)
        refresh()
    else:
        pass

def clear(Event=None):
    if(messagebox.askyesno('Clear all','Clear all ?')):
        sell_db.deleteall()
        refresh()

def clear_input(Event=None):
    text_id.set("")
    text_name.set("")
    text_qty.set(1)

def pay(Event=None):
    def success(Event=None):
        def ok_click(Event=None):
            popup2.destroy()
            refresh()

        popup.destroy()
        popup2 = Toplevel()
        popup2.grab_set()
        popup2.resizable(width=False, height=False)
        popup2.title('Success')
        popup2.bind('<Return>',ok_click)
        text = Message(popup2,text="Payment\nSuccess\n",anchor='e',font=(None,20),width=200)
        checky = Message(popup2,text= u'\u2713',fg='green',font=(None,40))
        ok_button = ok_button = Button(popup2,text='OK',width=8,height=2,command=ok_click)
        
        text.grid(column=0,row=0,padx=50)
        checky.grid(column=0,row=1)
        ok_button.grid(column=0,row=2,padx=15,pady=10,ipadx=5,ipady=5)
        
        popup2.mainloop()

    def transaction(Event=None):
        def create_receipt():
            import os, errno
            try:
                os.makedirs('./log/')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            import datetime
            nowtime = datetime.datetime.now()
            timefilename = str(nowtime.strftime('%y%m%d%H%M%S'))
            timestamp = str(nowtime.strftime('%Y-%m-%d %H:%M:%S'))
            log = open('./log/' + 'shop' + timefilename + '.txt','w')
            
            sell_data = sell_db.getall()
            log.write("---------------------------\n")
            log.write("Time : ")
            log.write(timestamp)
            log.write("\n\n")
            log.write("<ShopName>")
            log.write("\n\n")
            for i in sell_data:
                i = list(map(str,i))
                log.write(i[3] + 'x  ' + i[1] + '\t' + i[4] + '\n')
            log.write("\nTotal:  " + str(total) + '\n' )
            log.write("Cash:  " + str(cash) + '\n')
            log.write("Change:  " + str(change) + '\n\n')
            log.write("---------------------------\n")

            log.close()

        cash = float(cash_var.get())
        total = float(total_entry.get("1.0",END))
        change = cash - total

        if(cash >= total):
            cash_entry.config(state=DISABLED)
            sell_id_and_qty = sell_db.getIDandQty()
            
            for i in sell_id_and_qty:
                store_db.plusQtyByidorname(i[0],"",-i[1])
            try:
                create_receipt()
            except:
                pass

            change_entry.config(state=NORMAL)
            change_entry.insert('end',change)
            change_entry.config(state=DISABLED)

            sell_db.deleteall()

            ok_button.config(text='OK',command=success)
            cash_entry.bind('<Return>',success)
            refresh()

        else:
            showerror('error',"Not enough cash")

    popup = Toplevel()
    popup.grab_set()
    popup.resizable(width=False, height=False)
    popup.title('Payment')

    cashframe = Frame(popup)
    buttonframe = Frame(popup)

    total_label = Label(cashframe,text='TOTAL ',font=("Consolas",14,'normal'))
    total_entry = Text(cashframe,height=1,width=15,font=("Consolas",16,'normal'))
    total_entry.insert('end',str(sell_db.sumprice()))
    total_entry.config(state=DISABLED)
    
    cash_label = Label(cashframe,text='CASH ',font=("Consolas",14,'normal'))
    cash_var = StringVar()
    cash_entry = Entry(cashframe,textvariable=cash_var,font=("Consolas",16,'normal'),width=15)
    cash_entry.bind('<Return>',transaction)

    change_label = Label(cashframe,text='CHANGE',font=("Consolas",14,'normal'))
    change_entry = Text(cashframe,height=1,width=15,font=("Consolas",16,'normal'))
    change_entry.config(state=DISABLED)

    ok_button = Button(buttonframe,text='Pay',width=8,height=2,command=transaction)


    cashframe.grid(column=0,row=0)
    buttonframe.grid(column=0,row=1)

    total_label.grid(row=0,column=0,pady=10)
    total_entry.grid(row=0,column=1,pady=10,padx=5)
    cash_label.grid(row=1,column=0,pady=10)
    cash_entry.grid(row=1,column=1,pady=10,padx=5)
    change_label.grid(row=2,column=0,pady=10)
    change_entry.grid(row=2,column=1,pady=10,padx=5)
    ok_button.grid(row=3,column=0,ipadx=5,ipady=5,pady=10)

    popup.mainloop()

def refresh():
    sell_table.delete(*sell_table.get_children())
    sell_db_data = sell_db.getall()
    if(sell_db_data == []):
        button_pay.config(state=DISABLED)
    for i in sell_db_data:
        i = tuple(map(str,i))
        sell_table.insert('','end',text=i[0],value=i)  #because value cannot store '001' ,it will automatically change to '1' ,but text can.              
    label_pricetotal.config(text=str(sell_db.sumprice()) + ' ฿')
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
    button_delete.config(state=DISABLED)
def enable_button(event=None):
    button_delete.config(state=NORMAL)

def on_click(event=None):
    region = sell_table.identify("region", event.x, event.y)
    if(region == 'cell'):
        enable_button()


#%%
from tkinter import *
from tkinter import ttk
import sqlite3

cashier_window = Tk()
cashier_window.resizable(width=False, height=False)
store_db = store_SQLite_database('store.db','stock')
sell_db = sell_SQLite_database('sell.db','sell')

#-------------------------------------------------------------
input_frame = Frame(cashier_window)
##-----------------------------------------------------------
label_id = Label(input_frame, text='ID')
text_id = StringVar()
entry_id = Entry(input_frame, textvariable=text_id)
entry_id.bind('<Return>',add_item)
##-----------------------------------------------------------
label_name = Label(input_frame, text='Name')
text_name = StringVar()
entry_name = Entry(input_frame, textvariable=text_name)
entry_name.bind('<Return>',add_item)
##------------------------------------------------------------
label_qty = Label(input_frame, text='Qty')
text_qty = StringVar()
text_qty.set(1)
entry_qty = Entry(input_frame, textvariable=text_qty)
entry_qty.bind('<Return>',add_item)
##-------------------------------------------------------------
button_add = Button(input_frame, text='ADD', width=8, height=1, command=add_item)
#-------------------------------------------------------------
underframe = Frame(cashier_window)
##-------------------------------------------------------------
Rightframe = Frame(underframe,bg='red')
button_frame = Frame(Rightframe)
button_delete = Button(button_frame, text='DELETE', width=15, height=2,command=delete)
button_clear = Button(button_frame, text='CLEAR ALL', width=15, height=2,command=clear)
blank = Label(button_frame,width=5,height=3)
button_pay = Button(button_frame, text='PAY',height=6,width=16,command=pay)
##-------------------------------------------------------------
Leftframe = Frame(underframe)
table_frame = Frame(Leftframe)
sell_table = ttk.Treeview(table_frame,show='headings')
sell_table.bind('<Button-1>',on_click)
sell_table['columns'] = ('id','item_name','price','quantity','total')
sell_table.heading('id', text='ID', anchor="center",command=lambda:treeview_sort_column(sell_table, 'id', True))
sell_table.column('id', anchor="center", width=150)
sell_table.heading('item_name', text='Item Name',command=lambda:treeview_sort_column(sell_table, 'item_name', True))
sell_table.column('item_name', anchor='center', width=150)
sell_table.heading('quantity', text='Qty',command=lambda:treeview_sort_column(sell_table, 'quantity', True))
sell_table.column('quantity', anchor='center', width=50)
sell_table.heading('price', text='Price',command=lambda:treeview_sort_column(sell_table, 'price', True))
sell_table.column('price', anchor='center', width=100)
sell_table.heading('total', text='Total',command=lambda:treeview_sort_column(sell_table, 'total', True))
sell_table.column('total', anchor='center', width=100)
#---------------------------------------------------------------
summary_frame = Frame(Leftframe)
label_total = Label(summary_frame, text='TOTAL :')
label_pricetotal = Label(summary_frame)
#-------------------------------------------------------------

input_frame.grid(column=0,row=0,sticky="NSEW")
label_id.grid(row=0, column=0,padx=5)
entry_id.grid(row=0, column=1)
label_name.grid(row=0, column=2,padx=5)
entry_name.grid(row=0, column=3)
label_qty.grid(row=0, column=4,padx=5)
entry_qty.grid(row=0, column=5,padx=5)
button_add.grid(row=0, column=6, pady=5,padx=5)


underframe.grid(column=0,row=1,padx=0,pady=0)

Leftframe.grid(column=0,row=0)
table_frame.grid(column=0,row=0)
sell_table.grid(row=0, column=0,padx=10)

Rightframe.grid(column=1,row=0,padx=0,pady=0)
button_frame.grid(column=0,row=0,padx=0,pady=0)
button_delete.pack(side='top',anchor='n',pady=10)
button_clear.pack(side='top',anchor='n',pady=5)
blank.pack(side='top',fill='y')
button_pay.pack(side='bottom', pady=5,padx=10)


summary_frame.grid(column=0,row=3)
label_total.pack(side='left')
label_pricetotal.pack(side='left',anchor='w')


refresh()
cashier_window.mainloop()
#milestone@250 18.24 19/11/18  Yeahh :D :D :D
#milestone@440 2.59 20/11/18  Ahhhhh -0- 