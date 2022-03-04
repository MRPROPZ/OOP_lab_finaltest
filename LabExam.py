"""
@Author         : ???????? ?????????
@Number_student : ???????????
@Facultry       : Information and technology
"""

# Import library
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from bmi import *

# No class

# Run app
app = QtWidgets.QApplication(sys.argv)

# Load data
window  = uic.loadUi("bmi.ui")
sqluser = SqliteBMI("bmi.db")

# Method function
def loadData():
    userall = sqluser.select("SELECT * FROM tb_bmi ")
    # เอาข้อมูลจาก database ลงในฟอร์ม user interface qt designer

    # ดึงข้อมูลใน database สร้างตาราง
    for row_num, user in enumerate(userall):
        # window.ชื่อตารางใน qt designer ทำการแทรกข้อมูลที่ดึงมาลงไป
        window.tableWidget.insertRow(row_num)
        for col_num, data in enumerate(user):
            cell = QtWidgets.QTableWidgetItem(str(data))
            window.tableWidget.setItem(row_num, col_num, cell)

# Add_button do
def addUser():
    # window.ชื่อช่องช่องกรอกข้อมูลถัดจาก name.แสดงข้อความ
    name = window.lineEdit_name.text()
    # window.ชื่อช่องกรอกข้อมูลถัดจาก year.แสดงข้อความ
    weight = window.lineEdit_kg.text()
    #
    height = window.lineEdit_cm.text()
    # window.ชื่อช่องติีกถูก admin.ดูว่าเช็คหรือไม่
    male = window.radioButton_male.isChecked()
    female = window.radioButton_female.isChecked()


    gender = 0
    if male:
        gender = 1
    if name.strip("")!="" and weight.strip("")!="" and height.strip("") != "":
        try:
            # name:str year:int เลยแปลงเป็น integer a:ค่าหลังเช็คว่าถ้าติ๊กจะให้ = 1 ไม่ติ๊ก = 0
            user = (name, float(weight), int(height), gender)
            sqluser.insert("INSERT INTO tb_bmi(name, wei, hei, sex) VALUES(?,?,?,?)", user)
            clearData()
            loadData()
        except ValueError:
            QMessageBox.warning(None, "คำเตือน", "กรุณากรอกตัวเลข")
    else:
        QMessageBox.information(None, "คำเตือน","คุณกรอกข้อมูลยังไม่ครบ")

# Click table
def getSelectionRowId():
    return window.tableWidget.currentRow()

# Select table do
def selectionChanged():
    select_row = getSelectionRowId()
    name = window.tableWidget.item(select_row, 1).text()
    wei = window.tableWidget.item(select_row, 2).text()
    hei = window.tableWidget.item(select_row, 3).text()
    sex = window.tableWidget.item(select_row, 4).text()
    window.lineEdit_name.setText(name)
    window.lineEdit_kg.setText(wei)
    window.lineEdit_cm.setText(hei)

    if sex =='0':
        window.radioButton_female.setChecked(True)
    if sex == '1':
        window.radioButton_male.setChecked(True)

# Select id do
def getSelectionUserId():
    select_row = getSelectionRowId()
    return window.tableWidget.item(select_row, 0).text()

# Update_button do
def updateUser():
    id_update = getSelectionUserId()
    name = window.lineEdit_name.text()
    weight = window.lineEdit_kg.text()
    height = window.lineEdit_cm.text()
    male = window.radioButton_male.isChecked()
    female = window.radioButton_female.isChecked()

    gender = 0
    if male:
        gender = 1
    if name.strip("") != "" and weight.strip("") != "" and height.strip("") != "":
        try:
            # name:str year:int เลยแปลงเป็น integer a:ค่าหลังเช็คว่าถ้าติ๊กจะให้ = 1 ไม่ติ๊ก = 0
            user = (name, float(weight), int(height), gender)
            sqluser.edit("UPDATE tb_bmi SET name=?, wei=?, hei=?, sex=? WHERE id =" + id_update, user)
            QMessageBox.information(None, "แจ้งเตือน", "อัพเดตสำเร็จ")
            clearData()
            loadData()
        except ValueError:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("กรุณากรอกตัวเลข")
            msgBox.setWindowTitle("คำเตือน")
            QMessageBox.warning(None, "คำเตือน", "กรุณากรอกตัวเลข")
    else:
        QMessageBox.warning(None, "คำเตือน", "กรุณาเลือกข้อมูลที่จะอัพเดตด้วยครับ")

    clearData()
    loadData()

# Delete_Button do
def deleteUser():
    id_del = getSelectionUserId()
    name = window.lineEdit_name.text()
    weight = window.lineEdit_cm.text()
    height = window.lineEdit_kg.text()
    male = window.radioButton_male.isChecked()
    female = window.radioButton_female.isChecked()

    if name.strip("") != "" and weight.strip("") != "" and height.strip("") != "":
        try:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Confirm clear table?")
            msgBox.setWindowTitle("Alert!!!")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                sqluser.delete("DELETE FROM tb_bmi WHERE id=" + id_del)
            clearData()
            loadData()
        except ValueError:
            QMessageBox.information(None, "คำเตือน", "กรุณากรอกตัวเลข")
    else:
        QMessageBox.information(None, "คำเตือน", "กรุณาเลือกข้อมูลที่จะลบด้วยครับ")

    clearData()
    loadData()

# Clear data do
def clearData():
    window.tableWidget.clearSelection()
    while window.tableWidget.rowCount()>0:
        window.tableWidget.removeRow(0)
        window.tableWidget.clearSelection()
    window.lineEdit_name.setText("")
    window.lineEdit_kg.setText("")
    window.lineEdit_cm.setText("")
    window.radioButton_male.setChecked(False)
    window.radioButton_female.setChecked(False)

# Clear user do
def clearUser():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("Confirm clear table?")
    msgBox.setWindowTitle("Alert!!!")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        sqluser.delete("DELETE FROM tb_bmi")
    clearData()
    loadData()

# Exit program do
def exitprogram():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText("You sure?")
    msgBox.setWindowTitle("Alert!!!")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    returnValue = msgBox.exec()
    if returnValue == QMessageBox.Ok:
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Good bye ")
        msgBox.setWindowTitle("Notice!!!")
        returnValue = msgBox.exec()
        sys.exit(app.exec_())

# Bmi calculate
def bmi():
    id_del = getSelectionUserId()
    name = window.lineEdit_name.text()
    height = window.lineEdit_cm.text()
    weight = window.lineEdit_kg.text()
    male = window.radioButton_male.isChecked()
    female = window.radioButton_female.isChecked()

    gender = 0
    if male:
        gender = 1

    if name.strip("") != "" and weight.strip("") != "" and height.strip("") != "":
        bmi = BMI(name,gender ,float(weight),int(height))

        info = "คุณ%s\nBMI = %s\n%s"%(bmi.getName(),bmi.getBMI(),bmi.getBMImeaning())
        QMessageBox.information(None, "Your BMI", info)
    else:
        QMessageBox.information(None, "คำเตือน", "กรุณาเลือกข้อมูลที่จะคำนวณด้วยครับ")

# การทำงานของปุ่ม
# window.ชื่อปุ่ม ใน Qt designer
window.pushButton_add.clicked.connect(addUser)
window.tableWidget.itemSelectionChanged.connect(selectionChanged)
window.pushButton_update.clicked.connect(updateUser)
window.pushButton_del.clicked.connect(deleteUser)
window.pushButton_clear.clicked.connect(clearUser)
window.pushButton_bmi.clicked.connect(bmi)
window.actionExit.triggered.connect(exitprogram)

loadData()
window.show()
app.exec()
