import sys, os
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

DB_PATH = os.path.join(os.path.dirname(__file__), "ProductDB.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            product_name TEXT,
            product_type TEXT,
            product_price REAL,
            product_detail TEXT);"""
        )
    finally:
        conn.close()

class display(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("display.ui", self)

        init_db()
        self.loadData()


        self.btn_clear.clicked.connect(self.clear)
        self.btn_save.clicked.connect(self.saveData)
        self.btn_update.clicked.connect(self.updateData)
        self.btn_delete.clicked.connect(self.deleteRecord)

        self.tableWidget.cellClicked.connect(self.fillTable)

    def clear(self):
        self.product_id.clear()
        self.product_name.clear()
        self.product_type.clear()
        self.product_price.clear()
        self.product_detail.clear()
        self.loadData()

    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM product;")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "โหลดข้อมูลล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["รหัสสินค้า", "ชื่อสินค้า", "ประเภทสินค้า", "ราคา", "รายละเอียด"])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()

    def fillTable (self, row, column):
        product_id = self.tableWidget.item(row, 0).text()
        product_name = self.tableWidget.item(row, 1).text()
        product_type = self.tableWidget.item(row, 2).text()
        product_price = self.tableWidget.item(row, 3).text()
        product_detail = self.tableWidget.item(row, 4).text()

        self.product_id.setText(product_id)
        self.product_name.setText(product_name)
        self.product_type.setText(product_type)
        self.product_price.setText(product_price)
        self.product_detail.setText(product_detail)

    def saveData(self):
        product_name = self.product_name.text().strip()
        product_type = self.product_type.text().strip()
        product_price = self.product_price.text().strip()
        product_detail = self.product_detail.text().strip()

        if not all([product_name, product_type, product_price]):
            return QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO product (product_name, product_type, product_price, product_detail) VALUES(?,?,?,?) ",
                (product_name, product_type, product_price, product_detail),
            )
            conn.commit()
        except Exception as e:
            QMessageBox.critical(self, "บันทึกล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close

        QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลสำเร็จ")
        self.clear()
        self.loadData()

    def updateData(self):
        product_id = self.product_id.text().strip()
        product_name = self.product_name.text().strip()
        product_type = self.product_type.text().strip()
        product_price = self.product_price.text().strip()
        product_detail = self.product_detail.text().strip()

        if not product_id:
            return QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
        if not (product_name and product_type and product_price ):
            return QMessageBox.warning(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลใหม่")
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
                "UPDATE product SET product_name = ?, product_type = ?, product_price = ?, product_detail = ? WHERE product_id = ?",
                (product_name, product_type, product_price, product_detail, product_id)
            )
        conn.commit()
        if cur.rowcount == 0:
            QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสที่ต้องการอัปเดต")
        conn.close()
        self.clear()
        self.loadData()

    def deleteRecord(self):
        product_id = self.product_id.text().strip()
        if not product_id:
            return QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
        
        confirm = QMessageBox.question(
            self, "ยืนยันการลบ" , f"ต้องการลบข้อมูลรหัส : {product_id} ใช่หรือไม่",
            QMessageBox.Yes | QMessageBox.No , QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM product WHERE product_id = ?",(product_id,))
        conn.commit()
        if cur.rowcount == 0:
            QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสที่ต้องการลบ")
        conn.close()
        self.clear()
        self.loadData()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = display()
    window.show()
    sys.exit(app.exec_())