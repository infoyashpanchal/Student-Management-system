from sqlite3 import *
from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *

# ======= Button functions ===========================
# ================== ADD window ======================
def openadd():
    root.withdraw()
    add.deiconify()

def saveadd():
    con = None
    try:
        con = connect("SMS.db")
        cursor = con.cursor()
        sql = "INSERT INTO student values('%d', '%s', '%d');"
        rno = int(add_entRNO.get())
        name = add_entNAME.get()
        marks = int(add_entMARKS.get())
        cursor.execute(sql % (rno, name, marks))
        con.commit()
        showinfo("Success", "Student Entery added Successfully!")
    except Exception as e:
        showerror("Error",e)
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

# ================== VIEW window ======================
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
        showerror("Error",e)
        con.rollback()
    finally:
        if con is not None:
            con.close()

def closeview():
    view.withdraw()
    root.deiconify()

# ================== UPDATE window ======================
def openupdate():
    root.withdraw()
    update.deiconify()

def closeupdate():
    update.withdraw()
    root.deiconify()

# ================== DELETE window ======================
def opendelete():
    root.withdraw()
    delete.deiconify()

def closedelete():
    delete.withdraw()
    root.deiconify()

# ================= DataBase Creation ========================
def createtable():
    con = None
    try:
        con = connect("SMS.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS student(rno int primary key, name var(30), marks int(3));")
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
root.geometry("800x500+300+200")

btnADD = Button(root, text = "Add", width = 10, font = ('times new roman', 18, 'bold'), command = openadd)
btnVIEW = Button(root, text = "View", width = 10, font = ('times new roman', 18, 'bold'), command = openview)
btnUPDATE = Button(root, text = "Update", width = 10, font = ('times new roman', 18, 'bold'), command = openupdate)
btnDELETE = Button(root, text = "Delete", width = 10, font = ('times new roman', 18, 'bold'), command = opendelete)
btnChart = Button(root, text = "Charts", width = 10, font = ('times new roman', 18, 'bold'))

btnADD.pack(pady = 10)
btnVIEW.pack(pady = 10)
btnUPDATE.pack(pady = 10)
btnDELETE.pack(pady = 10)
btnChart.pack(pady=10)

# ================== Add window ===============================
add = Toplevel(root)
add.geometry("500x450+300+200")
add.title("Add Student")

add_lblRNO = Label(add, text = "Enter Roll No.:", font = ('arial', 18, 'bold'))
add_entRNO = Entry(add, bd = 3, font = ('arial', 18, 'bold'))
add_lblNAME = Label(add, text = "Enter Name:", font = ('arial', 18, 'bold'))
add_entNAME = Entry(add, bd = 3, font = ("arial", 18, 'bold'))
add_lblMARKS = Label(add, text = "Enter Marks:", font = ("arial", 18, "bold"))
add_entMARKS = Entry(add, bd = 3, font = ("arial", 18, "bold"))
add_btnADD = Button(add, text = "ADD", width = 10, font = ('arial', 18, 'bold'), command = saveadd)
add_btnBACK = Button(add, text = "BACK", width = 10, font = ('arial', 18, 'bold'), command = closeadd)

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
view.geometry("800x400+300+200")
view.title("View Student")

view_DISPLAY = ScrolledText(view, height = 15, width = 60, font = ("times new roman", 15, "bold"))
view_btnBACK = Button(view, text = "BACK", width = 10, font = ("arial", 18, "bold"), command = closeview)

view_DISPLAY.pack(pady = 10)
view_btnBACK.pack(pady = 10)

view.withdraw()
# ================== Update window ===============================
update = Toplevel(root)
update.geometry("500x450+300+200")
update.title("Update Student")

update_lblRNO = Label(update, text = "Enter Roll No.:", font = ('arial', 18, 'bold'))
update_entRNO = Entry(update, bd = 3, font = ('arial', 18, 'bold'))
update_lblNAME = Label(update, text = "Enter Name:", font = ('arial', 18, 'bold'))
update_entNAME = Entry(update, bd = 3, font = ("arial", 18, 'bold'))
update_lblMARKS = Label(update, text = "Enter Marks:", font = ("arial", 18, "bold"))
update_entMARKS = Entry(update, bd = 3, font = ("arial", 18, "bold"))
update_btnSAVE = Button(update, text = "SAVE", width = 10, font = ('arial', 18, 'bold'))
update_btnBACK = Button(update, text = "BACK", width = 10, font = ('arial', 18, 'bold'), command = closeupdate)

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

delete_lblRNO = Label(delete, text = "Enter Roll No.:", font = ('arial', 18, 'bold'))
delete_entRNO = Entry(delete, bd = 3, font = ('arial', 18, 'bold'))
delete_btnDELETE = Button(delete, text = "DELETE", width = 10, font = ('arial', 18, 'bold'))
delete_btnBACK = Button(delete, text = "BACK", width = 10, font = ('arial', 18, 'bold'), command = closedelete)

delete_lblRNO.pack(pady = 10)
delete_entRNO.pack(pady = 10)
delete_btnDELETE.pack(pady = 10)
delete_btnBACK.pack(pady = 10)

delete.withdraw()
root.mainloop()