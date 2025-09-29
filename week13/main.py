import sys, os
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem

DB_PATH = os.path.join(os.path.dirname(__file__), "DB.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        cur.execute(
            """
                    CREATE TABLE IF NOT EXISTS profile(
                    id_student BLOB PRIMARY KEY NOT NULL,
                    f_name BLOB ,
                    l_name BLOB ,
                    major BLOB)"""
        )
        conn.commit()
    finally:
        conn.close()

class StudentForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("student_form.ui", self)

        init_db()     

        self.loadData()
        self.btn_save.clicked.connect(self.saveData)
        self.btn_save.clicked.connect(self.loadData)

        self.btn_delete.clicked.connect(self.delelte_record)
        self.btn_delete.clicked.connect(self.loadData)

        self.btn_update.clicked.connect(self.update_record)
        self.btn_update.clicked.connect(self.loadData)

        self.tableWidget.cellClicked.connect(self.fill_form_table)

    def saveData(self):
        id_student = self.id_student.text()
        f_name = self.f_name.text()
        l_name = self.l_name.text()
        major = self.major.text()

        ###### INSERT TO DATABASE ######
        if not all([id_student, f_name, l_name, major]):
            QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO profile (id_student, f_name, l_name, major) VALUES(?,?,?,?) ",
                (id_student, f_name, l_name, major),
            )
            conn.commit()
        except Exception as e:
            QMessageBox.critical(self, "บันทึกข้อมูลล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลสำเร็จ")

        QMessageBox.information(
            self,
            "ข้อมูลนักศึกษา",
            f"รหัสนักศึกษา : {id_student}\n"
            f"ชื่อ : {f_name}\n"
            f"นามสกุล : {l_name}\n"
            f"สาขาวิชา : {major}\n",
        )
        self.id_student.setText("")
        self.f_name.setText("")
        self.l_name.setText("")
        self.major.setText("")
        self.lineCode.setText("")

        

    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "โหลดข้อมูลล้มเหลว", f"เกิดความผิดพลาด\n {e}")
            return
        finally:
            conn.close()
        # กำหนดแถว
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(4)

        self.tableWidget.setHorizontalHeaderLabels(["รหัส", "ชื่อ", "นามสกุล", "สาขาวิชา"])

        # โหลดข้อมูลทีละแถว
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()

    def delelte_record(self):
        code = self.lineCode.text().strip()
        if not code :
            return self.msg("ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน", QMessageBox.warning)
        
        confirm = QMessageBox.question(self, "ยืนยันการลบ", f"ต้องการลบข้อมูลหรือไม่ '{code}' ใช่หรือไม่",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm != QMessageBox.Yes:
            return
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM profile WHERE id_student = ?", (code,))
        conn.commit()

        self.id_student.setText("")
        self.f_name.setText("")
        self.l_name.setText("")
        self.major.setText("")
        self.lineCode.setText("")


    def update_record(self):
        code = self.lineCode.text().strip()
        id_student = self.id_student.text().strip()
        f_name = self.f_name.text().strip()
        l_name = self.l_name.text().strip()
        major = self.major.text().strip()

        if not code :
            return self.msg("ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน", QMessageBox.warning)
        if not (id_student and f_name and l_name and major) :
            return self.msg("ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลใหม่", QMessageBox.warning)
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "UPDATE profile SET id_student = ?, f_name = ?, l_name = ?, major = ? WHERE id_student = ?",
            (id_student, f_name, l_name, major, code)
        )

        conn.commit()
        
        comfirm = QMessageBox.question(self, "ยืนยันการลบ", f"ต้องการลบข้อมูลหรือไม่ '{code}' ใช่หรือไม่",
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        self.id_student.setText("")
        self.f_name.setText("")
        self.l_name.setText("")
        self.major.setText("")
        self.lineCode.setText("")


    def fill_form_table(self, row, column):
        # ดึงค่าจากแถวที่เลือก
        id_student = self.tableWidget.item(row, 0).text()
        f_name = self.tableWidget.item(row, 1).text()
        l_name = self.tableWidget.item(row, 2).text()
        major = self.tableWidget.item(row, 3).text()

        # ใส่ค่าลงในช่องกรอก
        self.id_student.setText(id_student)
        self.f_name.setText(f_name)
        self.l_name.setText(l_name)
        self.major.setText(major)

        # เก็บค่าไว้ใน lineCode (ใช้ตอน update/delete)
        self.lineCode.setText(id_student)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())