import sys, os
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

DB_PATH = os.path.join(os.path.dirname(__file__), "AssetDB.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_code TEXT NOT NULL UNIQUE,
            name TEXT,
            detail TEXT,
            room TEXT,
            building TEXT,
            latitude REAL,
            longitude REAL);"""
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
        self.id.clear()
        self.asset_code.clear()
        self.name.clear()
        self.detail.clear()
        self.room.clear()
        self.building.clear()
        self.latitude.clear()
        self.longitude.clear()
        self.loadData()

    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM assets;")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "โหลดข้อมูลล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(["รหัส", "รหัสครุภัณฑ์", "ชื่อครุภัณฑ์", "รายละเอียด", "ห้อง", "อาคาร", "ละติจูด", "ลองจิจูด"])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()

    def fillTable (self, row, column):
        id = self.tableWidget.item(row, 0).text()
        asset_code = self.tableWidget.item(row, 1).text()
        name = self.tableWidget.item(row, 2).text()
        detail = self.tableWidget.item(row, 3).text()
        room = self.tableWidget.item(row, 4).text()
        building = self.tableWidget.item(row, 5).text()
        latitude = self.tableWidget.item(row, 6).text()
        longitude = self.tableWidget.item(row, 7).text()

        self.id.setText(id)
        self.asset_code.setText(asset_code)
        self.name.setText(name)
        self.detail.setText(detail)
        self.room.setText(room)
        self.building.setText(building)
        self.latitude.setText(latitude)
        self.longitude.setText(longitude)

    def saveData(self):
        asset_code = self.asset_code.text().strip()
        name = self.name.text().strip()
        detail = self.detail.text().strip()
        room = self.room.text().strip()
        building = self.building.text().strip()
        latitude = self.latitude.text().strip()
        longitude = self.longitude.text().strip()

        if not all([asset_code, name, detail, room, building, latitude, longitude]):
            return QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO assets (asset_code, name, detail, room, building, latitude, longitude) VALUES(?,?,?,?,?,?,?) ",
                (asset_code, name, detail, room, building, latitude, longitude)
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
        id = self.id.text().strip()
        asset_code = self.asset_code.text().strip()
        name = self.name.text().strip()
        detail = self.detail.text().strip()
        room = self.room.text().strip()
        building = self.building.text().strip()
        latitude = self.latitude.text().strip()
        longitude = self.longitude.text().strip()

        if not id:
            return QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
        if not (asset_code and name and detail and room and building and latitude and longitude):
            return QMessageBox.warning(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลใหม่")
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
                "UPDATE assets SET asset_code = ?, name = ?, detail = ?, room = ?, building = ?, latitude = ?, longitude = ? WHERE id = ?",
                (asset_code, name, detail, room, building, latitude, longitude, id)
            )
        conn.commit()
        if cur.rowcount == 0:
            QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสที่ต้องการอัปเดต")
        conn.close()
        self.clear()
        self.loadData()

    def deleteRecord(self):
        id = self.id.text().strip()
        if not id:
            return QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
        
        confirm = QMessageBox.question(
            self, "ยืนยันการลบ" , f"ต้องการลบข้อมูลรหัส : {id} ใช่หรือไม่",
            QMessageBox.Yes | QMessageBox.No , QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM assets WHERE id = ?",(id,))
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