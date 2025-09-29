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
        self.btn_delete.clicked.connect(self.delete_record)
        self.btn_update.clicked.connect(self.update_record)
        self.btn_clear.clicked.connect(self.clear_form)

        self.tableWidget.cellClicked.connect(self.fill_form_table)

    def clear_form(self):
        self.id_student.clear()
        self.f_name.clear()
        self.l_name.clear()
        self.major.clear()
        self.lineCode.clear()

    def saveData(self):
        id_student = self.id_student.text().strip()
        f_name = self.f_name.text().strip()
        l_name = self.l_name.text().strip()
        major = self.major.text().strip()

        if not all([id_student, f_name, l_name, major]):
            return QMessageBox.warning(self, "ข้อมูลไม่ครบถ้วน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO profile (id_student, f_name, l_name, major) VALUES(?,?,?,?) ",
                (id_student, f_name, l_name, major),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "รหัสซ้ำ", f"รหัสนักศึกษา {id_student} มีอยู่แล้ว")
            return
        except Exception as e:
            QMessageBox.critical(self, "บันทึกล้มเหลว", f"เกิดข้อผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        QMessageBox.information(self, "สำเร็จ", "บันทึกข้อมูลสำเร็จ")
        self.clear_form()
        self.loadData()

    def loadData(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile")
            rows = cur.fetchall()
        except Exception as e:
            QMessageBox.critical(self, "โหลดข้อมูลล้มเหลว", f"เกิดความผิดพลาด\n{e}")
            return
        finally:
            conn.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["รหัส", "ชื่อ", "นามสกุล", "สาขาวิชา"])

        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                self.tableWidget.setItem(r, c, QTableWidgetItem(str(val)))

        self.tableWidget.resizeColumnsToContents()

    def delete_record(self):
        code = self.lineCode.text().strip()
        if not code:
            return QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")

        confirm = QMessageBox.question(
            self, "ยืนยันการลบ", f"ต้องการลบข้อมูลรหัส {code} ใช่หรือไม่?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM profile WHERE id_student = ?", (code,))
        conn.commit()
        if cur.rowcount == 0:
            QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสที่ต้องการลบ")

        conn.close()
        self.clear_form()
        self.loadData()

    def update_record(self):
        code = self.lineCode.text().strip()
        id_student = self.id_student.text().strip()
        f_name = self.f_name.text().strip()
        l_name = self.l_name.text().strip()
        major = self.major.text().strip()

        if not code:
            return QMessageBox.warning(self, "ไม่พบรหัส", "กรุณาเลือกรายการจากตารางก่อน")
        if not (id_student and f_name and l_name and major):
            return QMessageBox.warning(self, "ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลใหม่")

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            "UPDATE profile SET id_student = ?, f_name = ?, l_name = ?, major = ? WHERE id_student = ?",
            (id_student,f_name, l_name, major, code)
        )
        conn.commit()
        if cur.rowcount == 0:
            QMessageBox.warning(self, "ไม่พบข้อมูล", "ไม่พบรหัสที่ต้องการอัปเดต")

        conn.close()
        self.clear_form()
        self.loadData()

    def fill_form_table(self, row, column):
        id_student = self.tableWidget.item(row, 0).text()
        f_name = self.tableWidget.item(row, 1).text()
        l_name = self.tableWidget.item(row, 2).text()
        major = self.tableWidget.item(row, 3).text()

        self.id_student.setText(id_student)
        self.f_name.setText(f_name)
        self.l_name.setText(l_name)
        self.major.setText(major)
        self.lineCode.setText(id_student)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = StudentForm()
    window.show()
    sys.exit(app.exec_())
