from tkinter import *
from tkinter.ttk import *
from modules.tklistview import MultiListbox
from modules.tktoolbar import _init_toolbar
from models import Inventory_Product as Product

class FormProducts:
    '''The Products window with toolbar and a datagrid of products'''
    def __init__(self):
        self.frame=Toplevel()
        _init_toolbar(self)
        self._init_gridbox()
        self.frm_addproduct=None
        self.frm_editproduct=None
        self.addproductflag=False # frmaddproduct doesn't exist
        
    def _init_gridbox(self):
        self.mlb = MultiListbox(self.frame, (('id #',3),('Product', 25), ('Description', 25), ('Price', 10)))
        #tbproducts=sql.session._query("select * from inventory_product")
        self.update_mlb(items=Product.select())
        self.mlb.pack(expand=YES,fill=BOTH)
            
    #form product add button clicked()        
    def btn_add_click(self):
        if self.addproductflag: return 0
        print ('not exist')
        self.addproductflag=True
        self.frm_addproduct=FormAddProduct()
        self.frame.wait_window(self.frm_addproduct.frame)
        if self.frm_addproduct._okbtn_clicked==1:
            self.update_mlb(Product.select())
        self.addproductflag=False
            
    def btn_edit_click(self):
        print ('edit')
        
    def btn_del_click(self):
        if self.mlb.item_selected==None: return 'please select first'
        # sql.session._delete_product(int(self.mlb.item_selected[1]))
        item=Product.get(Product.id == self.mlb.item_selected[1])
        item.delete_instance()
        self.mlb.delete(self.mlb.item_selected[0])
        self.mlb.item_selected=None
        
    def tb_btnfind_click(self):
        print('sadfsdadf')
        fnd=self.tb_entryfind.get()
        #sql.session._find_products(fnd)
        self.update_mlb(Product.select().where(Product.name.contains(fnd)))
    def update_mlb(self,items):
        self.mlb.delete(0,END)
        #tbproducts=sql.session._query(q)
        for p in items:    
            self.mlb.insert(END, (p.id,p.name,p.description,p.price))

        self.mlb.selection_set(0) #set first row selected
           
class FormAddProduct:
    '''Add New product three labels and three textboxes and an OK button'''
    def __init__(self):
        
        self.frame=Toplevel()
        self.frame.protocol("WM_DELETE_WINDOW", self.callback) #user quit the screen
        self._init_widgets()
        
    def _init_widgets(self):
        self.label1=Label(self.frame,text="Product #")
        self.label1.grid(row=0,sticky=W)
        self.entry1=Entry(self.frame)
        self.entry1.grid(row=1,column=0)
        self.entry1.focus()
        
        self.label2=Label(self.frame,text="Sales Price")
        self.label2.grid(row=0,column=1,sticky=W)
        self.entry2=Entry(self.frame)
        self.entry2.grid(row=1,column=1)

        self.label3=Label(self.frame,text="Description.")
        self.label3.grid(row=2,sticky=W,columnspan=2)
        self.entry3=Entry(self.frame)
        self.entry3.grid(row=3,sticky=W+E,columnspan=2)
        self.entry3.bind("<Return>", lambda e: self.btnok_click())
        
        self.btn_ok=Button(self.frame,text="Add",width=7,command=self.btnok_click)
        self.btn_ok.grid(row=4,column=1,sticky=E)
        
    def btnok_click(self):
        items=(self.entry1.get(),self.entry3.get(),self.entry2.get())
        if '' in items:
            print ('please fill all boxes')
            return 'break'

        p = Product.create(name=items[0],description=items[1],price=int(items[2]))
        # sql.session._add_product(items)        
        self._okbtn_clicked=1
        print ('user exits the screen by clicking ok butn')
        self.frame.destroy()
        
    def callback(self):        
        self._okbtn_clicked=0
        print ('user exits the screen')
        self.frame.destroy()