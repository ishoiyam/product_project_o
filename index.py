from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import mysql.connector as mdb
import sys
import datetime



MainUi,_ = loadUiType("data/main.ui")

class Main(QMainWindow, MainUi):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Ui_Changes()
        self.DB_Connect()
        self.Handel_Buttons()
        
    def Ui_Changes(self):
        style = open("data/themes/qdark.css", "r")
        style = style.read()
        self.setStyleSheet(style)
        self.tabWidget.tabBar().setVisible(False)
        # table
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        self.name_edit.clear()
        self.quantity_edit.clear()
        self.unit_edit.clear()

        self.name_edit_2.clear()
        self.quantity_edit_2.clear()
        self.unit_edit_2.clear()

    def Change_Theme(self):
        combotext = str(self.cmb_box_themes.currentText())
        if not "---- Themes ----" == combotext:
            if "dark orange".lower() in combotext.lower():
                self.Dark_Orange_Theme()
            elif "dark blue".lower() in combotext.lower():
                self.Dark_Blue_Theme()
            elif "q dark".lower() in combotext.lower():
                self.QDark_Theme()
            elif "dark gray".lower() in combotext.lower():
                self.Dark_Gray_Theme()
            else:
                pass
        else:
            pass

    def Clear_Edit(self):
        self.name_edit.clear()
        self.quantity_edit.clear()
        self.unit_edit.clear()

    def Clear_Edit_2(self):
        self.id_edit.clear()
        self.name_edit_2.clear()
        self.quantity_edit_2.clear()
        self.unit_edit_2.clear()

    def Open_View_Products(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Add_Product(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Edit_Product(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(3)


    def DB_Connect(self):
        self.conn = mdb.connect(host="localhost", user="root", password="toor", database="sql_inventory")
        self.cur = self.conn.cursor()


    def Handel_Buttons(self):
        self.btn_refresh.clicked.connect(self.Get_Data)
        self.btn_add.clicked.connect(self.Add_Product)
        self.btn_delete.clicked.connect(self.Delete_Product)
        self.btn_update.clicked.connect(self.Update_Product)
        self.btn_search.clicked.connect(self.Search_Products)
        self.btn_apply.clicked.connect(self.Change_Theme)
        self.btn_view_all.clicked.connect(self.Open_View_Products)
        self.btn_add_product.clicked.connect(self.Open_Add_Product)
        self.btn_edit_product.clicked.connect(self.Open_Edit_Product)
        self.btn_settings.clicked.connect(self.Open_Settings)




    def Get_Data(self):
        cmd = """ USE sql_inventory  """
        self.cur.execute(cmd)

        cmd = """ SELECT name, quantity_in_stock, unit_price FROM products  """
        self.cur.execute(cmd)

        result = self.cur.fetchall()


        self.table.setRowCount(0)
        header = self.table.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.cur.execute(""" SELECT name FROM products """)
        result = self.cur.fetchall()
        
        self.comboBox.clear()
        self.comboBox.addItem("---- Products ----")
        for r in result:
            self.comboBox.addItem(r[0])



    def Add_Product(self):
        name_val = self.name_edit.text()
        quantity_val = self.quantity_edit.text()
        unit_price_val = self.unit_edit.text()
        
        sql = """ INSERT INTO `products` (name, quantity_in_stock, unit_price) VALUES (%s, %s, %s) """
        val = (name_val, quantity_val, unit_price_val)
        self.cur.execute(sql, val)
        self.conn.commit()

        self.Clear_Edit()
        self.Get_Data()


    def Update_Product(self):
        id_val = self.id_edit.text()
        name_val = self.name_edit_2.text()
        quantity_val = self.quantity_edit_2.text()
        unit_price_val = self.unit_edit_2.text()
        
        sql = """ UPDATE products SET name=%s, quantity_in_stock=%s, unit_price=%s WHERE product_id=%s"""
        row = (name_val, quantity_val, unit_price_val, id_val)
        self.cur.execute(sql, row)
        self.conn.commit()

        self.Clear_Edit_2()
        self.Get_Data()


    def Delete_Product(self):
        id_val = str(self.id_edit.text())
        
        cmd = """ DELETE FROM products WHERE product_id = %s """
        self.cur.execute(cmd, (id_val,))
        self.conn.commit()

        self.Clear_Edit_2()
        self.Get_Data()

    def Search_Products(self):
        try:
            product_val = self.comboBox.currentText()

            sql = """ SELECT product_id, name, quantity_in_stock, unit_price FROM products WHERE name = %s """
            val = (product_val,)
            
            self.cur.execute(sql, val)
            result = self.cur.fetchall()
            
            r1 = result[0][0]
            r2 = result[0][1]
            r3 = result[0][2]
            r4 = result[0][3]

            

            self.id_edit.setText(str(r1))
            self.name_edit_2.setText(str(r2))
            self.quantity_edit_2.setText(str(r3))
            self.unit_edit_2.setText(str(r4))
        except:
            self.Clear_Edit_2()
            pass


    def Dark_Blue_Theme(self):
        style = open('data/themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Gray_Theme(self):
        style = open('data/themes/darkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_Theme(self):
        style = open('data/themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def QDark_Theme(self):
        style = open('data/themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()





