import sqlite3

#DB_CONN=sqlite3.connect('dbshoppro')
#connect database

class DB_SESSION:
    def __init__(self,conn):#,conn=None):
        self.conn=conn
        self.cur=self.conn.cursor()

    def _query(self,q="""SELECT * from invoices"""):
        self.cur.execute(q)
        return self.cur.fetchall()
    def _find_products(self,val):
        print (val)
        self.cur.execute("select * from products where name like '%"+val+"%'")
        return self.cur.fetchall()
    def _delete_invoice(self,i_d):
        t=(i_d,)
        self.cur.execute('DELETE FROM invoices WHERE id=?',t)
        self.cur.execute('DELETE FROM invoiceitems WHERE invoiceid=?',t)
        self.conn.commit()
    

    def _add_product(self,items):
        # users is a list of (id, name, description, salesprice)
        self.cur.execute('select MAX(id) from products')
        i_d=self.cur.fetchone()[0] + 1
        items=(i_d,)+items
        self.cur.execute('INSERT INTO products VALUES (?,?,?,?)',items)
        self.conn.commit()

    def _add_invoice(self,inv,items):
        #items is a list of (id, invoiceid, productid, quantity)
        #inv is a tuple like (id,customer, date, amount)
        self.cur.execute('INSERT INTO invoices VALUES (?,?,?,?)',inv)
        for t in items:
            self.cur.execute('INSERT INTO invoiceitems VALUES (?,?,?,?)',t)
        self.conn.commit()
        
    def _add_product_cmd(self):
        self.cur.execute('select MAX(id) from products')
        i_d=self.cur.fetchone()[0] + 1
        items=[]
        while True:
            name=input('Product Name: ')
            if name =='': break
            desc=input('Product Description: ')
            price=input('Price: ')
            t=(i_d,name,desc,int(price))
            self.cur.execute('insert into products values (?,?,?,?)', t)
            i_d+=1

        self.conn.commit()
        
    def _show_invoice(self,i_d):
        t=(i_d,)
        self.cur.execute('''select invoiceitems.id,name,quantity,description,price,price*quantity
        from invoiceitems,products
        where invoiceitems.productid=products.id
        and invoiceitems.invoiceid=?''', t)
        return self.cur.fetchall()

    def _delete_product(self,i_d):
        t=(i_d,)
        self.cur.execute('DELETE FROM products WHERE id=?',t)
        self.conn.commit()
        
    def close(self):
        self.conn.close()

    def _next_invoiceid(self):
        self.cur.execute('select MAX(id) from invoices')
        i_d=self.cur.fetchone()[0] + 1
        return i_d


'''    
    def _add_invoice(self):
        query="INSERT INTO invoices VALUES (0,'',0,0)"
        c=self.conn.cursor()
        c.execute(query)
        self.conn.commit()
        print (self._last_rowid())
        
                
    def _add_invoice_items(self):
        pass
    
    def _update(self):
        query='UPDATE invoices SET invoiceid=4 WHERE id = "Smith"';
        
    def _last_rowid(self):
        return int(self.c.lastrowid)
'''

session=DB_SESSION(sqlite3.connect('dbshoppro'))
