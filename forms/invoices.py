from tkinter import *
from tkinter.ttk import *
from modules.tklistview import MultiListbox
from modules.tktoolbar import _init_toolbar
from forms.addinvoice import FormAddInvoice
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
        self.update_mlb(Invoice.select())
        self.mlb.pack(expand=YES,fill=BOTH)

    def update_mlb(self,tb):
        self.mlb.delete(0,END)
        for i in tb:
            self.mlb.insert(END, (i.id,i.customer,i.date,i.amount))
        self.mlb.selection_set(0) #set first row selected
    
    def btn_add_click(self):
        if self.addinvoiceflag:
            print ('add invoice window exist')
            return 0
        self.addinvoiceflag=True
        self.frm_addinvoice=FormAddInvoice()
        self.frame.wait_window(self.frm_addinvoice.frame)
        self.update_mlb(Invoice.select())
        self.addinvoiceflag=False
        
    def btn_edit_click(self):
        if (self.editinvoiceflag or not self.mlb.item_selected[1]) : return 0
        self.editinvoiceflag=True
        self.frm_editinvoice=FormEditInvoice()
        self.frm_editinvoice.init_entryboxes(self.mlb.item_selected[1:])#(id,customer,date,amount)
        items = InvoiceItem.select().where(InvoiceItem.invoice == int(self.mlb.item_selected[1]))
        self.frm_editinvoice.update_mlbitems(items)
        self.frame.wait_window(self.frm_editinvoice.frame)
        self.editinvoiceflag=False    

    def btn_del_click(self):
        if self.mlb.item_selected==None: return 'please select first'
        print (self.mlb.item_selected[1])
        item = Invoice.get(Invoice.id == self.mlb.item_selected[1])
        item.delete_instance(recursive=True)        
        self.mlb.delete(self.mlb.item_selected[0])
        self.mlb.item_selected=None

    def tb_btnfind_click(self):
        print ('find')

class FormEditInvoice:
    def __init__(self):
        self.frame=Toplevel()
        self.frame1=Frame(self.frame)#,width=100,height=200)
        label_entry(self.frame1,'Invoice#:')
        self.frame1.pack(side=TOP)

        self.frame2=Frame(self.frame)#,width=100,height=200)
        label_entry(self.frame2,'Customer:','Date:')
        self.frame2.pack(side=TOP)

        lblprod=Label(self.frame,text='Items').pack(side=TOP)
        self.frame3=Frame(self.frame)
        self.mlbitems=MultiListbox(self.frame3, (('LN#',5),
                ('Product', 15), ('Quantity',5),('Description', 20),
                ('UnitPrice', 10),('Total',10)))
        self.mlbitems.not_focus() #don't take_focus
        self.mlbitems.pack(expand=YES,fill=BOTH,side=TOP)
        self.frame3.pack(side=TOP)

        self.frame4=Frame(self.frame)#,width=100,height=200)
        label_entry(self.frame4,'GrandTotal:')
        self.frame4.pack(side=TOP)

    def init_entryboxes(self,val):
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