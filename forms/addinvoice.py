from tkinter import *
from tkinter.ttk import *
from modules.tklistview import MultiListbox
from datetime import datetime
from forms import invoices
from models import Inventory_Product as Product
from models import Inventory_Invoice as Invoice
from models import Inventory_InvoiceItem as InvoiceItem

class FormAddInvoice:
    '''Add New product three labels and three textboxes and an OK button'''
    def __init__(self):        
        self.frame=Toplevel()
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()        
        
    def _init_widgets(self):
        self.frame1=Frame(self.frame)
        invoices.label_entry(self.frame1,'Customer:')
        self.lbl_date=Label(self.frame1,text='Date:'+str(datetime.today())[:10])
        self.lbl_date.pack(side=LEFT,padx=10)
        self.frame1.pack(side=TOP,anchor=W,pady=10)

        #frame2- lookuplist
        self.frame2=LookupList(self.frame)
        self.frame2.ent.focus() #set_focus to entry product
        self.frame2.ent.bind("<KeyRelease>",self.txtproduct_change)#<Key>",self.keypressed)
        self.frame2.ent.bind("<Return>", lambda e: self.add_item())
        self.frame2.ent.bind("<Escape>", lambda e: self.ent_paid.focus())#print(e.keycode))#self.ent_qty.focus())

        #frame3- quantity, ent_qty, btn_additem
        self.frame3=Frame(self.frame)
        self.lbl3_1=Label(self.frame3,text="Quantity")
        self.lbl3_1.pack(side=LEFT)
        self.ent_qty=Entry(self.frame3)
        self.ent_qty.pack(side=LEFT)
        # keyboard events
        self.ent_qty.bind("<Return>", lambda e: self.add_item())

        self.btn_additem=Button(self.frame3,text="Add Item",width=8,
                                command=self.btn_additem_click)
        self.btn_additem.pack(side=LEFT)
        self.frame3.pack(side=TOP,anchor=E)

        #frame4- mlbitems 
        self.frame4=Frame(self.frame)
        self.mlbitems=MultiListbox(self.frame4, (('LN#',4),('ID#',6),
                ('Product', 15), ('Quantity',5),('Description', 20),
                ('UnitPrice', 10),('Total',10)))
        self.mlbitems.not_focus() #don't take_focus
        self.mlbitems.pack(expand=YES,fill=BOTH,side=TOP)
        self.frame4.pack(side=TOP,pady=10)

        #frame5-netamount-stringvar, paid, balance
        self.frame5=Frame(self.frame)
        self.lbl5_1=Label(self.frame5,text="Net:")
        self.lbl5_1.pack(side=LEFT)
        self.netamount=StringVar()
        self.netamount.set('0')
        self.lbl5_2=Label(self.frame5,textvariable=self.netamount, font=("Helvetica", 16))
        self.lbl5_2.pack(side=LEFT)
        self.lbl5_3=Label(self.frame5,text="paid:")
        self.lbl5_3.pack(side=LEFT)
        self.ent_paid=Entry(self.frame5)
        self.ent_paid.pack(side=LEFT)
        self.ent_paid.bind("<KeyPress>",self.ent_paid_change)
        self.ent_paid.bind("<KeyRelease>",self.ent_paid_keyrelease)
        self.balanceamount=StringVar()
        self.lbl5_4=Label(self.frame5,text="Balance: ").pack(side=LEFT)
        self.lblbal=Label(self.frame5,textvariable=self.balanceamount,
                          foreground='red',font=("Helvetica", 22)).pack(side=LEFT)
        
        lbl_ent_paid_help=Label(self.frame5,text="""
            Press <Enter> to create invoice.
            Press <Escape> to close.""")
        lbl_ent_paid_help.pack(side=LEFT)
        self.frame5.pack(side=TOP,anchor=E)

        self.btn_ok=Button(self.frame,text="Add Invoice",width=15,command=self.btnok_click)
        self.btn_ok.pack(side=TOP)

        
    def txtproduct_change(self,event):
        if event.keycode == 114:
            # -> <right arrow key>
            self.ent_qty.focus()
            return
        txtent=self.frame2.ent.get()
        self.frame2.update_mlb(txtent)
    
    def add_item(self):
        qty=self.ent_qty.get()
        if qty=='':qty=2
        qty=int(qty)
        LN=self.mlbitems.size()+1
        r,i_d,prdct,desc,price=self.frame2.mlb.item_selected
        self.mlbitems.insert(END, (LN,i_d,prdct,qty,desc,price,price*qty))
        net_amt=int(self.netamount.get())+(price*qty)
        self.netamount.set(str(net_amt))# stringvar: change liked to label
        self.frame2.ent.delete(0,END) #clear entry product
        self.ent_qty.delete(0,END)#clear entry quantity
        self.frame2.ent.focus()  #set_focus to entry product
        self.frame2.update_mlb('')    

    def ent_paid_change(self,event):
        if event.keycode == 36: # <Enter>
            self.btnok_click()
        elif event.keycode == 9: # <Esc>
            self.frame.destroy()
            
    def ent_paid_keyrelease(self,event):
        paid=self.ent_paid.get()
        if paid=='':paid = 0
        bal=int(paid)-int(self.netamount.get())
        self.balanceamount.set(str(bal))
        
    def btn_additem_click(self):        
        self.add_item()
        
    def btnok_click(self):
        no_of_items=self.mlbitems.size()
        if no_of_items==0:
            print('please select some products first')
            return '0'        
        items=[]
        for item in range(no_of_items):
            temp1=self.mlbitems.get(item)
            items.append((temp1[1],temp1[3],)) # product_id, qty
        
        cur_inv = Invoice.create(
            customer=self.frame1._entry.get(),
            date=str(datetime.today()),
            amount=self.netamount.get()
        )
        for i in items:
            InvoiceItem.insert(
                invoice=cur_inv,product=i[0],quantity=i[1]).execute()

        self._okbtn_clicked=1
        self.frame.destroy()
        
    def callback(self):        
        self._okbtn_clicked=0
        self.frame.destroy()

# LookupList class
# a mlb and a entry box for FormAddInvoice class
class LookupList:
    def __init__(self,master):
        self.frame=Frame(master)#,width=100,height=200)
        self.le_frame=Frame(self.frame)
        lbl=Label(self.le_frame,text="Product: ").pack(side=LEFT)
        self.ent=Entry(self.le_frame)
        self.ent.pack(side=LEFT)
        lbl_produt_help=Label(self.le_frame,text="""
            Press <Enter> to add product with 1 quantity.
            Press <Right Arrow> to get focus to text quantity.
            Press <Escape> to get focus to text paid.""")
        lbl_produt_help.pack(side=LEFT)

        self.le_frame.pack(side=TOP,anchor=W)
        self._init_gridbox()
        self.frame.pack(side=TOP,expand=NO)

    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',5),('Product', 20), ('Description', 32), ('UnitPrice', 15)))
        self.update_mlb('')
        self.mlb.not_focus()
        self.mlb.pack(expand=YES,fill=BOTH,side=TOP)    
                
    def update_mlb(self,val):
        items = Product.select().where(Product.name.contains(val)).order_by(Product.name)
        self.mlb.delete(0,END)
        for p in items:
            self.mlb.insert(END, (p.id,p.name,p.description,p.price))
        self.mlb.selection_set(0) #set first row selected
        
