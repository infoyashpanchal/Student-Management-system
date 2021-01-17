from sqlite3 import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import re
import bs4
import requests


# ================================= Button functions =======================================================
#
# ========================================= ADD window ======================================
def openadd():
    root.withdraw()
    add.deiconify()

def saveadd():
    con = None
    try:
        rno = add_entRNO.get()
        name = add_entNAME.get()
        alpha = re.compile("^[a-zA-Z ]+$")
        marks = add_entMARKS.get()
        if (rno == '') or (name == '') or (marks == ''):
            showerror("Error", "Some fields are Empty!")
        else:
            rno = int(rno)
            marks = int(marks)
            if rno < 0:
                showerror("Error", "Roll number cannot be negative!")
            elif not alpha.match(name):
                showerror(
                    "Error", "Name must be a string!\n(no special characters)")
            elif len(name) < 2:
                showerror("Error", "Please enter a valid Name")
            elif marks < 0 or marks > 100:
                showerror("Error", "Marks should be in range of 0-100")
            else:
                con = connect("SMS.db")
                cursor = con.cursor()
                sql = "INSERT INTO student values('%d', '%s', '%d');"
                cursor.execute(sql % (rno, name, marks))
                con.commit()
                showinfo("Success", "Student Entery added Successfully!")
    except ValueError:
        showerror("Error", "Roll number and Marks\nshould be a number")
        con.rollback()
    except IntegrityError:
        showerror("Error", "Roll number already exists")
        con.rollback()
    except Exception as e:
        showerror("Error", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
            add_entRNO.delete(0, END)
            add_entNAME.delete(0, END)
            add_entMARKS.delete(0, END)
            add_entRNO.focus()

def closeadd():
    add.withdraw()
    root.deiconify()

# ==================================== VIEW window ======================================
def openview():
    root.withdraw()
    view.deiconify()
    view_DISPLAY.delete(1.0, END)
    con = None
    try:
        con = connect("SMS.db")
        cursor = con.cursor()
        sql = "SELECT * FROM student;"
        cursor.execute(sql)
        con.commit()
        data = cursor.fetchall()
        info = "ROLL NO.\t\tNAME\t\tMARKS "
        for d in data:
            info += "\n>  {}\t\t{}\t\t{}".format(d[0], d[1], d[2])
        view_DISPLAY.insert(INSERT, info)
    except Exception as e:
        showerror("Error", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()

def closeview():
    view.withdraw()
    root.deiconify()

# ======================================= UPDATE window ================================
def openupdate():
    root.withdraw()
    update.deiconify()

def saveupdate():
    con = None
    con1 = None
    try:
        # ============ getting existing roll numbers =====================
        con1 = connect("SMS.db")
        cursor1 = con1.cursor()
        sql = "SELECT rno FROM student;"
        cursor1.execute(sql)
        con1.commit()
        data = cursor1.fetchall()
        rno_list = []
        for x in data:
            rno_list.append(x[0])
        if con1 is not None:
            con1.close()

    # ============= Validation of the data ===========================
        rno = update_entRNO.get()
        name = update_entNAME.get()
        # variable alpha is the required set of "alphabests" and "space" that a name can contain
        alpha = re.compile("^[a-zA-Z ]+$")
        marks = update_entMARKS.get()

        if (rno == '') or (name == '') or (marks == ''):
            showerror("Error", "Some fields are Empty!")
        else:
            rno = int(rno)
            marks = int(marks)
            if rno < 0:
                showerror("Error", "Roll number cannot be negative!")
            elif not alpha.match(name):
                showerror(
                    "Error", "Name must be a string!\n(no special characters)")
            elif rno not in rno_list:
                showerror("Error", "Roll number does not exists!")
            elif len(name) < 2:
                showerror("Error", "Please enter a valid Name")
            elif marks < 0 or marks > 100:
                showerror("Error", "Marks should be in range of 0-100")
            else:
                con = connect("SMS.db")
                cursor = con.cursor()
                sql = """UPDATE student
                    SET name = '%s', marks = '%d'
                    WHERE rno = '%d';"""
                cursor.execute(sql % (name, marks, rno))
                con.commit()
                showinfo("Success", "Student Entery added Successfully!")
    except ValueError:
        showerror("Error", "Roll number and Marks\nshould be a number")
        con.rollback()
    except Exception as e:
        showerror("Error", e)
        con.rollback()
    finally:
        if con is not None:
            con.close()
            update_entRNO.delete(0, END)
            update_entNAME.delete(0, END)
            update_entMARKS.delete(0, END)
            update_entRNO.focus()

def closeupdate():
    update.withdraw()
    root.deiconify()

# ================== DELETE window ======================
def opendelete():
    root.withdraw()
    delete.deiconify()

def deletedata():
    con = None
    con1 = None
    try:
        # ======= Getting already existing roll number ===========
        con1 = connect("SMS.db")
        cursor1 = con1.cursor()
        sql = "SELECT rno FROM student;"
        cursor1.execute(sql)
        con1.commit()
        data = cursor1.fetchall()
        rno_list = []
        for x in data:
            rno_list.append(x[0])
        # print(rno_list)
        # print(data)
        if con1 is not None:
            con1.close()
    # ====== validation of data ===========================
        rno = delete_entRNO.get()
        if rno == '':
            showerror("Error", "Please enter a Roll number!")
        else:
            rno = int(rno)
            if rno not in rno_list:
                showerror("Error", "Roll number does not exists!")
            else:
                con = connect("SMS.db")
                cursor = con.cursor()
                sql = "DELETE FROM student WHERE rno = '%d';"
                cursor.execute(sql % (rno))
                con.commit()
                showinfo("Success", "Student Deleted Successfully!")
    except ValueError:
        showerror("Error", "Roll number must be a positive integer")
        con.rollback()
    finally:
        if con is not None:
            con.close()
            delete_entRNO.delete(0, END)
            delete_entRNO.focus()

def closedelete():
    delete.withdraw()
    root.deiconify()

import matplotlib.pyplot as plt
# ================= Chart ====================================
import pandas as pd


def chart():
    NAME = []
    MARKS = []
    con2 = connect("SMS.db")
    cursor_name = con2.cursor()
    cursor_marks = con2.cursor()
    sql_name = "SELECT name from student;"
    sql_marks = "SELECT marks from student;"
    cursor_name.execute(sql_name)
    cursor_marks.execute(sql_marks)
    con2.commit()
    data_name = cursor_name.fetchall()
    for x in data_name:
        NAME.append(x[0])        
    data_marks = cursor_marks.fetchall()
    for x in data_marks:
        MARKS.append(x[0])
    NAME_list = [a.split(" ")[0] for a in NAME]
    plt.figure(figsize = (6,6))
    plt.bar(NAME_list, MARKS,  color = ['red', 'green', 'brown', 'blue'])
    plt.xlabel('Students')
    plt.xticks(rotation = 20)
    plt.ylabel('Score')
    plt.title('Bactch Information')
    plt.show()

# ================ Location and Temp and Quote ==============================
def getloc():
    city = str
    try:
        web_add = "https://ipinfo.io/"
        res1 = requests.get(web_add)
        data1 = res1.json()

        city = data1['city']
    except Exception as e:
        print("Issue", e)
    finally:
        return city

def gettemp():
    temperature = str
    city = getloc()
    try:
        a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
        a2 = "&q=" + city
        a3 = "&appid=c6e315d09197cec231495138183954bd"
        web_add = a1 + a2 + a3
        res2 = requests.get(web_add)
        data2 = res2.json()
        
        main = data2['main']
        temperature = main['feels_like']
    except Exception as e:
        print("Issue",e)
    finally:
        return temperature

def getquote():
    try:
        web = "https://www.brainyquote.com/quote_of_the_day"
        res = requests.get(web)
        data = bs4.BeautifulSoup(res.text, "html.parser")
        
        info = data.find('img', {'class': 'p-qotd'})
        quote = info['alt']
    except Exception as e:
        print(e)
    finally:
        return quote


CITY = getloc()
TEMP = gettemp()    
QUOTE = getquote()

# ================= DataBase Creation ========================
def createtable():
    con = None
    try:
        con = connect("SMS.db")
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS student(rno int primary key, name var(30), marks int(3));")
        cursor.commit()
    except Exception:
        con.rollback()
    finally:
        if con is not None:
            con.close()

createtable()

# ================= GUI Creation ===============================
# ================= Main window ================================
root = Tk()
root.title("Student Managemnet System")
root.geometry("680x400+300+200")
root['background']='#086A87'

btnADD = Button(root, text = "Add", width = 10, font = ('times new roman', 18, 'bold'), bg="#01A9DB", fg="#01DF74", command = openadd)
btnVIEW = Button(root, text = "View", width = 10, font = ('times new roman', 18, 'bold'), bg="#01A9DB", fg="#01DF74", command = openview)
btnUPDATE = Button(root, text = "Update", width = 10, font = ('times new roman', 18, 'bold'), bg="#01A9DB", fg="#01DF74", command = openupdate)
btnDELETE = Button(root, text = "Delete", width = 10, font = ('times new roman', 18, 'bold'), bg="#01A9DB", fg="#01DF74", command = opendelete)
btnChart = Button(root, text = "Charts", width = 10, font=('times new roman', 18, 'bold'), bg="#01A9DB", fg="#01DF74", command = chart)
btnADD.pack(pady = 5)
btnVIEW.pack(pady = 5)
btnUPDATE.pack(pady = 5)
btnDELETE.pack(pady = 5)
btnChart.pack(pady = 5)

lblLOCTEMP = Label(root, text = "Location: {}\t\tTemperature: {}\u00B0C".format(CITY, TEMP), fg="black", bg="#01DF74", pady = 5, justify = LEFT, font = ('comic sans ms', 20, 'bold'), borderwidth=2, relief="groove")
lblQUOTE = Label(root, text = "QOTD: {}".format(QUOTE), fg="black", bg="#01DF74", wraplength=650, pady = 5, justify = LEFT, font = ('comic sans ms', 18, 'bold italic'), borderwidth=2, relief="groove")
lblLOCTEMP.pack(padx = 10, pady = 10, fill = X)
lblQUOTE.pack(padx = 10, fill = X)


# ================== Add window ===============================
add = Toplevel(root)
add.geometry("500x450+300+200")
add.title("Add Student")
add['background'] = '#AEB404'

add_lblRNO = Label(add, text = "Enter Roll No.:", font = ('arial black', 18, 'bold'), bg = '#AEB404', fg="black")
add_entRNO = Entry(add, bd = 3, font = ('arial', 18, 'bold italic'), bg = '#FFBF00')
add_lblNAME = Label(add, text = "Enter Name:", font = ('arial black', 18, 'bold'), bg = '#AEB404', fg="black")
add_entNAME = Entry(add, bd = 3, font = ("arial", 18, 'bold italic'), bg = '#FFBF00')
add_lblMARKS = Label(add, text = "Enter Marks:", font = ("arial black", 18, "bold"), bg = '#AEB404', fg="black")
add_entMARKS = Entry(add, bd = 3, font = ("arial", 18, "bold italic"), bg = '#FFBF00')
add_btnADD = Button(add, text = "ADD", width = 10, font = ('arial', 18, 'bold'), fg="white", bg="#FF8000", command = saveadd)
add_btnBACK = Button(add, text = "BACK", width = 10, font = ('arial', 18, 'bold'), fg="white", bg="#FF8000", command = closeadd)

add_lblRNO.pack(pady = 10)
add_entRNO.pack(pady = 10)
add_lblNAME.pack(pady = 10)
add_entNAME.pack(pady = 10)
add_lblMARKS.pack(pady = 10)
add_entMARKS.pack(pady = 10)
add_btnADD.pack(pady = 10)
add_btnBACK.pack(pady = 10)

add.withdraw()
# ================== View window ===============================
view = Toplevel(root)
view.geometry("650x400+300+200")
view.title("View Student")
view['background'] = '#4B088A'

view_DISPLAY = ScrolledText(view, height = 15, width = 40, font = ("times new roman", 15, "bold"), bg = '#FE2EF7')
view_btnBACK = Button(view, text = "BACK", width=10, font = ("arial", 18, "bold"), fg = 'white', bg = '#A901DB', command = closeview)

view_DISPLAY.pack(pady = 10)
view_btnBACK.pack(pady = 10)

view.withdraw()
# ================== Update window ===============================
update = Toplevel(root)
update.geometry("500x450+300+200")
update.title("Update Student")
update['background'] = '#4E387E' #dark

update_lblRNO = Label(update, text = "Enter Roll No.:", font = ('arial', 18, 'bold'), bg = '#4E387E', fg="#3EA99F")
update_entRNO = Entry(update, bd = 3, font = ('arial', 18, 'bold italic'), bg = '#93FFE8')
update_lblNAME = Label(update, text = "Enter Name:", font = ('arial', 18, 'bold'), bg = '#4E387E', fg="#3EA99F")
update_entNAME = Entry(update, bd = 3, font = ("arial", 18, 'bold italic'), bg = '#93FFE8')
update_lblMARKS = Label(update, text = "Enter Marks:", font = ("arial", 18, "bold"), bg = '#4E387E', fg="#3EA99F")
update_entMARKS = Entry(update, bd = 3, font = ("arial", 18, 'bold italic'), bg = '#93FFE8')
update_btnSAVE = Button(update, text = "SAVE", width = 10, font = ('arial', 18, 'bold'), fg="white", bg="#7F525D", command = saveupdate)
update_btnBACK = Button(update, text = "BACK", width = 10, font = ('arial', 18, 'bold'), fg="white", bg="#7F525D", command = closeupdate)

update_lblRNO.pack(pady = 10)
update_entRNO.pack(pady = 10)
update_lblNAME.pack(pady = 10)
update_entNAME.pack(pady = 10)
update_lblMARKS.pack(pady = 10)
update_entMARKS.pack(pady = 10)
update_btnSAVE.pack(pady = 10)
update_btnBACK.pack(pady = 10)

update.withdraw()
# ================== Delete window ===============================
delete = Toplevel(root)
delete.geometry("400x230+300+200")
delete.title("Update Student")
delete['background'] = '#610B0B'

delete_lblRNO = Label(delete, text = "Enter Roll No.:", font = ('arial', 18, 'bold'), bg = '#610B0B', fg = '#DF013A')
delete_entRNO = Entry(delete, bd = 3, font = ('arial', 18, 'bold'), bg = '#FA5858')
delete_btnDELETE = Button(delete, text = "DELETE", width = 10, font = ('arial', 18, 'bold'), fg = 'white', bg = '#DF013A', command = deletedata)
delete_btnBACK = Button(delete, text = "BACK", width = 10, font = ('arial', 18, 'bold'), fg = 'white', bg = '#DF013A', command = closedelete)

delete_lblRNO.pack(pady = 10)
delete_entRNO.pack(pady = 10)
delete_btnDELETE.pack(pady = 10)
delete_btnBACK.pack(pady = 10)

delete.withdraw()
root.mainloop()
