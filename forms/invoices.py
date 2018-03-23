from tkinter import *
from tkinter.ttk import *
from modules.tklistview import MultiListbox
from modules.tktoolbar import _init_toolbar
from datetime import datetime

from models import Inventory_Product as Product
from models import Inventory_Invoice as Invoice
from models import Inventory_InvoiceItem as InvoiceItem

def label_entry(frmlblent,txtlbl,txtlbl2=None):
    label=Label(frmlblent,text=txtlbl)
    label.pack(side=LEFT)
    frmlblent._entry=Entry(frmlblent)
    frmlblent._entry.pack(side=LEFT)
    if txtlbl2:
        label2=Label(frmlblent,text=txtlbl2)
        label2.pack(side=LEFT)
        frmlblent._entry2=Entry(frmlblent)
        frmlblent._entry2.pack(side=LEFT)
    
        
class FormInvoices:
    def __init__(self):
        self.frame=Toplevel()
        _init_toolbar(self)
        self._init_gridbox()
        self.frm_addinvoice=None
        self.addinvoiceflag=False
        self.editinvoiceflag=False
        
    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',5),('Customer', 25), ('Date', 15), ('Grand Total', 15)))
        # tbproducts=sql.session._query("select * from inventory_invoice")
        self.update_mlb(Invoice.select())
        self.mlb.pack(expand=YES,fill=BOTH)
        

    def update_mlb(self,tb):
        self.mlb.delete(0,END)
        for i in tb:
            self.mlb.insert(END, (i.id,i.customer,i.date,i.amount))
        self.mlb.selection_set(0) #set first row selected
    
    def btn_add_click(self):
        print ('check addwindow exist or not. If not exist cmd will display not exist')
        if self.addinvoiceflag: return 0
        print ('not exist')
        self.addinvoiceflag=True
        self.frm_addinvoice=FormAddInvoice()
        self.frame.wait_window(self.frm_addinvoice.master)
        print ('form addinvoice doesnot exist. Add button will work')
        self.addinvoiceflag=False
        
    def btn_edit_click(self):
        if self.editinvoiceflag: return 0
        self.editinvoiceflag=True
        self.frm_editinvoice=FormEditInvoice()
        self.frm_editinvoice.init_entryboxes(self.mlb.item_selected[1:])#(id,customer,date,amount)
        #tbinvitems=sql.session._show_invoice(self.mlb.item_selected[1])
        items = InvoiceItem.select().where(InvoiceItem.invoice == int(self.mlb.item_selected[1]))
        self.frm_editinvoice.update_mlbitems(items)
        self.frame.wait_window(self.frm_editinvoice.master)
        self.editinvoiceflag=False
    

    def btn_del_click(self):
        if self.mlb.item_selected==None: return 'please select first'
        print (self.mlb.item_selected[1])
        #sql.session._delete_invoice(int(self.mlb.item_selected[1]))
        item = Invoice.get(Invoice.id == self.mlb.item_selected[1])
        item.delete_instance(recursive=True)
        
        self.mlb.delete(self.mlb.item_selected[0])
        self.mlb.item_selected=None
    def btn_find_click(self):
        print ('find')


class FormAddInvoice:
    '''Add New product three labels and three textboxes and an OK button'''
    def __init__(self):
        
        self.master=Toplevel()
        self.master.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()
        
        
    def _init_widgets(self):
        self.frame0=Frame(self.master)
        label_entry(self.frame0,'Invoice# :')
        self.frame0._entry.insert(END,'xx')
        self.frame0._entry['state']=DISABLED
        self.frame0.pack(side=TOP)
        #frame1- lblcustomer, lbl_date, btn_date
        self.frame1=Frame(self.master)
        label_entry(self.frame1,'Customer:')
        self.lbl_date=Label(self.frame1,text='Date:'+str(datetime.today())[:10])
        self.lbl_date.pack(side=LEFT,padx=10)
        self.btn_date=Button(self.frame1,text="PickDate",width=8,
                             command=self.btn_date_click)
        self.btn_date.pack(side=LEFT)
        self.frame1.pack(side=TOP,anchor=W,pady=10)

        #frame2- lookuplist
        self.frame2=LookupList(self.master)
        self.frame2.ent.focus() #set_focus to entry product
        self.frame2.ent.bind("<KeyRelease>",self.txtchange)#<Key>",self.keypressed)
        
        #frame3- quantity, ent_qty, btn_additem
        self.frame3=Frame(self.master)
        self.lbl3_1=Label(self.frame3,text="Quantity")
        self.lbl3_1.pack(side=LEFT)
        self.ent_qty=Entry(self.frame3)
        self.ent_qty.pack(side=LEFT)
        self.btn_additem=Button(self.frame3,text="AddItem",width=8,
                                command=self.btn_additem_click)
        self.btn_additem.pack(side=LEFT)
        self.frame3.pack(side=TOP,anchor=E)

        #frame4- mlbitems 
        self.frame4=Frame(self.master)
        self.mlbitems=MultiListbox(self.frame4, (('LN#',4),('ID#',6),
                ('Product', 15), ('Quantity',5),('Description', 20),
                ('UnitPrice', 10),('Total',10)))
        self.mlbitems.not_focus() #don't take_focus
        self.mlbitems.pack(expand=YES,fill=BOTH,side=TOP)
        self.frame4.pack(side=TOP,pady=10)

        #frame5-netamount-stringvar, paid, balance
        self.frame5=Frame(self.master)
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
        self.ent_paid.bind("<KeyRelease>",self.ent_paid_change)
        self.balanceamount=StringVar()
        self.lbl5_4=Label(self.frame5,text="Balance: ").pack(side=LEFT)
        #self.balanceamount.set('balance:')
        self.lblbal=Label(self.frame5,textvariable=self.balanceamount,
                          foreground='red',font=("Helvetica", 22)).pack(side=LEFT)
        
        self.frame5.pack(side=TOP,anchor=E)

        self.btn_ok=Button(self.master,text="OK",width=15,command=self.btnok_click)
        self.btn_ok.pack(side=TOP)
        
    def txtchange(self,event):
        #print (event.keycode)
        if event.keycode == 36:
            print ('Enter key')
            
    def add_item(self):
        qty=self.ent_qty.get()
        if qty=='':
            print ('no quantity set')
            return 0
        qty=int(qty)
        LN=self.mlbitems.size()+1
        r,i_d,prdct,desc,price=self.frame2.mlb.item_selected
        self.mlbitems.insert(END, (LN,i_d,prdct,qty,desc,price,price*qty))
        net_amt=int(self.netamount.get())+(price*qty)
        self.netamount.set(str(net_amt))# stringvar: change liked to label
        self.frame2.ent.delete(0,END) #clear entry product
        self.ent_qty.delete(0,END)#clear entry quantity
        self.frame2.ent.focus()  #set_focus to entry product
        
    def btn_date_click(self):
        print('date')

    def ent_paid_change(self,event):
        paid=self.ent_paid.get()
        if paid=='':
            return 0
        bal=int(paid)-int(self.netamount.get())
        self.balanceamount.set(str(bal))
        
    def btn_additem_click(self):        
        self.add_item()
        
        #self.itemcounter+=1
        #LN=itemconter,product, qty, description,unitprice,total
        #print(self.frame2.mlb.item_selected)
        #print('add item')'''
        
    def btnok_click(self):
        no_of_items=self.mlbitems.size()
        if no_of_items==0:
            print('please select some products first')
            return '0'        
        #i_d=int(self.frame0._entry.get())#invoiceid
        items=[]
        for item in range(no_of_items):
            temp1=self.mlbitems.get(item)
            items.append((temp1[1],temp1[3],)) # product_id, qty
        # (customer, date, amount)

        cur_inv = Invoice.create(
            customer=self.frame1._entry.get(),
            date=str(datetime.today()),
            amount=self.netamount.get()
        )
        for i in items:
            InvoiceItem.insert(
                invoice=cur_inv,product=i[0],quantity=i[1]).execute()

        # sql.session._add_invoice(tbinv,tbinv_items)
        self._okbtn_clicked=1
        print ('user exits the screen by clicking ok butn')
        self.master.destroy()
        
    def callback(self):        
        self._okbtn_clicked=0
        print ('user exits the screen')
        self.master.destroy()

# LookupList class
# a mlb and a entry box for FormAddInvoice class
class LookupList:
    def __init__(self,master):
        self.frame=Frame(master)#,width=100,height=200)
        self.le_frame=Frame(self.frame)
        #self.tblookup=sql.session
        lbl=Label(self.le_frame,text="Product: ").pack(side=LEFT)
        self.ent=Entry(self.le_frame)
        self.ent.pack(side=LEFT)
        #self.ent.bind("<KeyRelease>",self.txtchange)#<Key>",self.keypressed)
        self.le_frame.pack(side=TOP,anchor=W)
        self._init_gridbox()
        self.frame.pack(side=TOP,expand=NO)

    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',5),('Product', 20), ('Description', 32), ('UnitPrice', 15)))
        self.update_mlb('')
        self.mlb.not_focus()
        self.mlb.pack(expand=YES,fill=BOTH,side=TOP)
        
    def txtchange(self,event):
        #print (event.keycode)
        if event.keycode == 36:
            print ('Enter key')
            #self.ent_qty.set_text('1')
        txtent=self.ent.get()
        self.update_mlb(txtent)
                
    def update_mlb(self,val):
        # x = self.tblookup._query("select * from inventory_product where name like '%"+val+"%' order by name")
        items = Product.select().where(Product.name.contains(val)).order_by(Product.name)
        self.mlb.delete(0,END)
        for p in items:
            self.mlb.insert(END, (p.id,p.name,p.description,p.price))
        self.mlb.selection_set(0) #set first row selected
        
class FormEditInvoice:
    def __init__(self):
        self.master=Toplevel()
        self.frame1=Frame(self.master)#,width=100,height=200)
        label_entry(self.frame1,'Invoice#:')
        self.frame1.pack(side=TOP)

        self.frame2=Frame(self.master)#,width=100,height=200)
        label_entry(self.frame2,'Customer:','Date:')
        self.frame2.pack(side=TOP)

        lblprod=Label(self.master,text='Items').pack(side=TOP)
        self.frame3=Frame(self.master)
        self.mlbitems=MultiListbox(self.frame3, (('LN#',5),
                ('Product', 15), ('Quantity',5),('Description', 20),
                ('UnitPrice', 10),('Total',10)))
        self.mlbitems.not_focus() #don't take_focus
        self.mlbitems.pack(expand=YES,fill=BOTH,side=TOP)
        self.frame3.pack(side=TOP)

        self.frame4=Frame(self.master)#,width=100,height=200)
        label_entry(self.frame4,'GrandTotal:')
        self.frame4.pack(side=TOP)

    def init_entryboxes(self,val):
        #val=(id,customer,date,amount)
        self.frame1._entry.insert(END,val[0])
        self.frame1._entry['state']=DISABLED
        
        self.frame2._entry.insert(END,val[1])
        self.frame2._entry2.insert(END,val[2])
        self.frame2._entry['state']=DISABLED
        self.frame2._entry2['state']=DISABLED
        
        self.frame4._entry.insert(END,val[3])
        self.frame4._entry['state']=DISABLED        
        
    def update_mlbitems(self,items):
        self.mlbitems.delete(0,END)
        for i in items:
            qty,price = (i.quantity,i.product.price)
            self.mlbitems.insert(END,(
                i.id,
                i.product.name,
                qty,
                i.product.description,
                price,
                price * qty)
            )
        self.mlbitems.selection_set(0) #set first row selected
