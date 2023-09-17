import random
import datetime 
import mysql.connector
from prettytable import from_db_cursor, PrettyTable
import sys

str1 = "Enter the alphabet and space only!!!\n"
str2 = "PRESS\n1. TO JUMP TO VIEW RECORDS OPTION\nELSE ANY KEY TO EXIT THIS OPTION\n"
str3 = "NO SUCH RECORDS ARE PRESENT !!\n"
str4 = "Kindly choose from available serial numbers\n"

print("WELCOME TO LIBRARY MANAGEMENT".center(100), end = '\n\n')

#Preparing Database
mydb=mysql.connector.connect(host='localhost',user='root',passwd='1010',buffered=True)
cursor=mydb.cursor()
cursor1=mydb.cursor()
dbname="library_management"
cursor.execute(f'Create database if not exists {dbname}')
mydb.commit()
cursor.execute(f'Use {dbname}')
cursor.execute("Create table if not exists reader_info (reader_id int(7),reader_name varchar(50),contact_no varchar(12),address varchar(70))") 
cursor.execute("Create table if not exists book_info (book_id int(7),book_name varchar(50),nameofauthor varchar(30),price int,genre varchar(20),qty int)")  
cursor.execute("Create table if not exists issue_table (book_id int ,reader_id int,qty int,dob date,due_date date,amount_of_fine int,dos date)")
mydb.commit()
                   
# Functions used in Project are defined below
def due_date():
    return datetime.date.today()+datetime.timedelta(15)

def qty_i(b_id):
    while True:
        QTY=input("\nEnter the copies you want to issue : ")
        if (not(QTY.isdigit())):
            print('\nKindly Enter digits only\n')
        elif (int(QTY)<=0):
            print('\nKindly enter a valid quantity\n')
        else:
            QTY = int(QTY)
            break
    cursor.execute("Select qty from book_info where book_id=%s",[b_id])
    for i in cursor:
        qty=i[0]
    if qty>=QTY:
        cursor.execute("Update book_info set qty = %s  where book_id = %s",[qty-QTY,b_id])
        return QTY
    print("\nSorry that much is not in stock\n")
    return 0
    


def qty_r(b_id, c_id):
    cursor.execute("select qty from issue_table where reader_id = %s", [c_id])
    for i in cursor:
        qty = int(i[0])
    QTY=int(input("\nEnter the copies you want to return : "))
    if(qty<QTY):
        print("\nThat much number of books were not issued\n")
    cursor.execute("Select qty from book_info where book_id=%s",[b_id])
    for i in cursor:
        qty=i[0]
    fq=qty+QTY
    cursor.execute("Update book_info set qty = %s  where book_id = %s",[fq,b_id])
    if(qty!=QTY):
        cursor.execute("Update issue_table set qty = %s where book_id = %s",[qty-QTY])
    else:
        cursor.execute("Delete from book_info where book_id = %s and reader_id = %s", [b_id, c_id])
    return QTY


def aof(c_id,b_id):
    cursor.execute("select due_date from issue_table where reader_id=%s and book_id=%s and dos is null",[c_id,b_id])
    for i in cursor:
        d=i[0]    
    d0=datetime.date.today()
    if d0>=d:
        f=(d0-d).days
        fine=f*2
        print("amount of fine: ",fine)
    else:
        print("no fine")
        fine=0
    return fine

# Project execution code starts from here
while(True):
    options = ["1 ADD BOOK       ", "2 ADD READER     ", "3 VIEW RECORDS   ", "4 DELETE RECORDS ", "5 ISSUE A BOOK   ", "6 SUBMIT A BOOK  ", "LEFT KEYS TO EXIT"]
    for i in options:
        print(i.center(100), end = '\n\n')
    l,l1,l2 = [],[],[]
    option=input("\nENTER THE CHOICE\n")
    if(option not in "123456" or option == str()):
        sys.exit()
    option = int(option)

    if (option==1):                               #OPTION1 FOR ADDING NEW BOOK RECORDS
        while(True):
            while(True):
                book_name=input("Enter book name\n")
                if(book_name == str() or book_name.isspace()):
                    print("Kindly Enter a correct name\n")
                else:
                    for i in book_name:
                        if(i.isalpha()):
                            break
                    break
            while True:
                nameofauthor=input("Enter author name\n")
                for i in nameofauthor:
                    if not(i.isalpha() or i.isspace):
                        print(str1)
                        break
                if(nameofauthor.isspace()):
                    print("Kindly Enter Aplhabets in name\n")
                else:
                    nameofauthor = (nameofauthor.rstrip()).lstrip()
                    break
            while True:
                price=input("Enter the price\n")
                if(not(price.isdigit())):
                    print("Kindly Enter Price in Digits\n")
                elif(int(price)<0):
                    print("Kindly Enter a valid Book Price\n")
                else:
                    price = int(price)
                    break
            while(True):
                genre=input("Enter the genre of book\n")
                for i in genre:
                    if not(i.isalpha() or i.isspace):
                        print(str1)
                        break
                if(genre.isspace()):
                    print("Kindly Enter Aplhabets in Genre\n")
                else:
                    genre = (genre.rstrip()).lstrip()
                    break
            while(True):
                qty=input("Enter the qty\n")
                if(not(qty.isdigit())):
                    print("Kindly Enter Quantity in Digits\n")
                elif(int(qty)<0):
                    print("Kindly Enter a valid Quantity\n")
                else:
                    qty = int(qty)
                    break
            while True:
                book_id=random.randrange(10**6,10**7-1)
                cursor.execute("select book_id from book_info")
                for i in cursor:
                    if i[0] == book_id:
                        break
                else:
                    print("BOOK ID IS : ",book_id, end = '\n\n')
                    break
            cursor.execute("insert into book_info values(%s,%s,%s,%s,%s,%s)",(book_id,book_name,nameofauthor,price,genre,qty))
            mydb.commit()
            op=input("Press\n1 TO CONTINUE ADDING BOOK \nELSE ANY KEY TO EXIT\n")
            if not(op=='1'):
                break

    elif (option==2):                      # OPTION 2  FOR ADDING NEW CUSTOMER RECORDS
        while True:
            while True:
                reader_name=input("\nEnter your name\n")
                if(reader_name.isspace()):
                    print("Kindly Enter Aplhabets in the name\n")
                    continue
                for i in reader_name:
                    if not(i.isalpha() or i.isspace):
                        print("Enter alphabets and/or spaces only!!!\n")
                        break
                else:
                    reader_name = (reader_name.rstrip()).lstrip()
                    break
            while True:
                contact_no=input("Enter reader's phone number\n")
                if len(contact_no)==10 and contact_no.isdigit():
                    break
                print("Enter 10 'DIGITS' only!!!\n")
            while True:
                address=input("Enter address of reader\n")
                if not(address.isspace()):
                    break
                print("Kindly Enter reader's Address\n")
            while True:
                reader_id=random.randrange(10**6,10**7-1)
                cursor.execute("select reader_id from reader_info")
                for i in cursor:
                    if i[0] == reader_id:
                        break
                else:
                    print("\nYOUR READER ID IS : ",reader_id)
                    break
            cursor.execute("insert into reader_info values (%s,%s,%s,%s)",(reader_id,reader_name,contact_no,address))
            mydb.commit()
            op=input("PRESS\n1 TO CONTINUE ADDING READER INFO\nELSE ANY KEY TO EXIT\n")
            if not(op=='1'):
                break
     
    elif (option==3):                      #OPTION 3 FOR VIEWING ANY RECORDS
        while True:
            print("1. VIEW ALL BOOKS \n2. VIEW A BOOK BY NAME  \n3. VIEW ALL READER \n4. VIEW A READER BY NAME \n5. VIEW THE BOOK ISSUED \n6.VIEW THE BOOK SUMBIT\nELSE ANY KEY TO EXIT THE BOOK VIEWING\n")
            ch=input("\nEnter your choice: \n")
            if(ch not in "1 2 3 4 5 6"):
                break
            ch = int(ch)
            if ch==1:
                view="select * from book_info"
                cursor.execute(view)
                if cursor.rowcount == 0:
                    print("\nBooks aren't available yet\n")
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    print(from_db_cursor(cursor))
                    a = input(str2)
                    if(a != '1'):
                        break
            elif ch == 2:
                bn=input("\nEnter book name: \n")
                db = "select * from book_info WHERE book_name LIKE %s"
                cursor.execute(db,['%'+bn+'%'])
                if(cursor.rowcount == 0 or cursor.rowcount == -1):
                    print(f"Books with name {bn} not found\n")
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    print("LIST OF BOOK(S) IS HERE".center(100), end = '\n\n')
                    print(from_db_cursor(cursor))
                    a = input(str2)
                    if(a != '1'):
                        break
            elif ch==3:
                vw='select * from reader_info'
                cursor.execute(vw)
                if(cursor.rowcount == 0):
                    print("There aren't any reader yet\n")
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    cursor.execute(vw)
                    print(from_db_cursor(cursor))
                    a = input(str2)
                    if(a != '1'):
                        break
            elif ch==4:
                cn=input("Enter reader's name: \n")
                db = "select * FROM reader_info as Reader WHERE reader_name LIKE %s limit 20" 
                cursor.execute(db,(f"%{cn}%",))
                if(cursor.rowcount == 0):
                    print(f"There aren't any reader with name like {cn}\n")
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    cursor.execute(db,(f"%{cn}%",))
                    print((f"THE LIST OF READERS WITH NAME LIKE {cn} IS HERE").center(100), end = '\n\n')
                    print(from_db_cursor(cursor))

            elif ch==5:
                view="select book_id,reader_id,qty,dob,due_date from issue_table"
                cursor.execute(view)
                if(cursor.rowcount == 0):
                    print("\nCurrently there are no issued book(s)\n")
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    cursor.execute(view)
                    print(from_db_cursor(cursor))
                    a = input(str2)
                    if(a != '1'):
                        break
            else:
                view="select book_id,reader_id,dos,amount_of_fine from issue_table"
                cursor.execute(view)
                if(cursor.rowcount == 0):
                    print("\nCurrently there are no issued book(s)\n")
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    cursor.execute(view)
                    print(from_db_cursor(cursor))
                    a = input(str2)
                    if(a != '1'):
                        break

    elif (option==4):                      #OPTION 4 FOR DELETING ANY RECORDS
        while(True):
            print("1. DELETE BOOK \n2. DELETE READER'S INFORMATION\n3. DELETE ISSUE INFORMATIOM\nELSE ANY KEY TO EXIT\n")
            choice=input("Enter any of these options : ")
            if choice not in "123":
                break
            elif choice=='1':
                d=input("Enter book id\n")
                db = "select book_name,book_id FROM book_info WHERE book_id LIKE %s limit 20" 
                cursor.execute(db,(f"%{d}%",))
                a = 0
                l1,l = [],[]
                for i in cursor:
                    l.append([a+1,i[1]])
                    l1.append(i[1])
                    a+=1
                if(a==0):
                    print(str3)
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    table = PrettyTable()
                    table.field_names = ['Serial No.', 'book id']
                    table.add_rows(l)
                    print(table)
                    print()
                    while(True):
                        ch=input("Enter your choice: ")
                        if(not(ch.isdigit())):
                            print("Enter Digits Only\n")
                        elif(int(ch)>a+1):
                            print(str4)
                        else:
                            cursor.execute("delete from book_info where book_id='%s'",(l1[int(ch)-1],))
                            print("Sucessfully Deleted Book Details\n")
                            mydb.commit()
                            break
            elif(choice=='2'):
                d=input("\nEnter Reader's id: ")
                db = "select reader_id FROM reader_info WHERE reader_id LIKE %s limit 20" 
                cursor.execute(db,(f"%{d}%",))
                l2=[]
                if(cursor.rowcount == 0):
                    print(str3)
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    table = PrettyTable()
                    table.field_names = ['Serial No.', 'Readers id']
                    b = 0
                    for i in cursor:
                        l2.append([b+1,i[0]])
                        b+=1
                    if(b == 0):
                        print(str3)
                    else:
                        table.add_rows(l2)
                        print(table)
                        print()
                        while(True):
                            ch=input("\nEnter Serial Number: ")
                            if(not(ch.isdigit())):
                                print("Enter digits only\n")
                            elif(int(ch)>b+1):
                                print(str4)
                            else:
                                cursor.execute("delete from reader_info where reader_id='%s'",(l2[int(ch)-1][1],))
                                mydb.commit()
                                print("Sucessfully Deleted Reader's Information\n")
                                break
            elif(choice=='3'):
                d=input("\nEnter Your Reader Id: ")
                db = "select reader_id from issue_table where reader_id LIKE %s limit 20" 
                cursor.execute(db,(f"%{d}%",))
                l2=[]
                if(cursor.rowcount == 0):
                    print(str3)
                    a = input(str2)
                    if(a != '1'):
                        break
                else:
                    table = PrettyTable()
                    table.field_names = ['Serial No.', "Reader id"]
                    c = 0
                    for i in cursor:
                        l2.append([c+1,i])
                        c+=1
                    if(c == 0):
                        print(str3)
                    else:
                        table.add_rows(l2)
                        print(table)
                        print()
                        while(True):
                            ch=input("\nEnter Serial Number: ")
                            if(not(ch.isdigit())):
                                print("Enter digits only\n")
                            elif(int(ch)>c+1):
                                print(str4)
                            else:
                                cursor.execute("delete from issue_table where reader_id='%s'",(l2[int(ch)-1][1][0],))
                                print("Sucessfully Deleted Issued Iformation\n")
                                mydb.commit()
                                break
                            a = input("PRESS\n1. TO JUMP TO DELETE RECORDS AGAIN\n ELSE ANY KEY TO EXIT\n")
                            if(a != '1'):
                                break
            

    elif(option==5):                       #Option 5 for Issuing a Book
        while(True):
            view="select * from book_info"
            cursor.execute(view)
            if(cursor.rowcount == 0):
                print("No books are available yet\n")
                a = input("PRESS\n1. TO JUMP 'TO ISSUE A BOOK' AGAIN\nELSE ANY KEY TO EXIT\n")
                if(a != '1'):
                    break
            else:
                cursor.execute(view)
                print(from_db_cursor(cursor))
            while True :
                while True:
                    book_id=(input("\nEnter book id of the book: "))
                    if book_id.isdigit():
                        break
                    book_id = int(book_id)
                    print("Enter a valid book id\n")
                cursor.execute("select book_id from book_info where book_id = %s",[book_id])
                if(cursor.rowcount == 0):
                    print("Wrong book_id\n")
                else:
                    break

            while True :
                while True:
                    c_id=(input("\nEnter your reader_id : "))
                    if c_id.isdigit() :
                        break
                    print("Enter a valid reader_id")
                cursor.execute("select reader_id from reader_info where reader_id = %s", [c_id])
                if(cursor.rowcount == 0):
                    print("\nWrong reader_id\n")
                else:
                    break
            cursor.execute("select i.book_id book_id,b.book_name book_name,i.qty Quantity,i.amount_of_fine fine from issue_table i , book_info b where b.book_id=i.book_id and reader_id=%s group by book_name ",[c_id])
            q=qty_i(book_id)
            dob=datetime.date.today()
            dd=due_date()
            if(q == 0):
                print("\nBook not issued due to unavailability in stock\n")
            else:
                cursor.execute("insert into issue_table(book_id,reader_id,qty,dob,due_date) values (%s,%s,%s,%s,%s)",(book_id,c_id,q,dob,dd))
                mydb.commit()
                print("\nYour due date to submit the book(s) is: ",dd)
                a = input("PRESS\n1. TO ISSUE ANOTHER BOOK\nELSE ANY KEY TO EXIT THIS OPTION")
                if(a!='1'):
                    break    
    
    else:                                  #Option 6 to Submit a Book
        while True :
            while True:
                b_id=(input("\nEnter book id of the book: "))
                if b_id.isdigit():
                    break
                b_id = int(b_id)
                print("Enter a valid book id\n")
            cursor.execute("select book_id from book_info where book_id = %s",[b_id])
            if(cursor.rowcount == 0):
                print("Wrong book_id\n")
            else:
                break
        while True :
            while True:
                c_id=(input("\nEnter your reader_id : "))
                if c_id.isdigit() :
                    break
                print("Enter a valid reader_id")
            cursor.execute("select reader_id from reader_info where reader_id = %s", [c_id])
            if(cursor.rowcount == 0):
                print("\nWrong Reader_id\n")
            else:
                break
            
        amount_of_fine = aof(c_id,b_id)
        if amount_of_fine==0:
            break
        print(f"Kindly pay {amount_of_fine} Rs")
        ds=datetime.date.today()
        q=qty_r(b_id, c_id)
        cursor.execute("update issue_table set amount_of_fine=%s where reader_id=%s and book_id = %s",[0,c_id, b_id])
        cursor.execute("update issue_table set qty=%s where reader_id=%s and book_id = %s",[q,c_id, b_id])
        cursor.execute("update issue_table set dos=%s where reader_id=%s and book_id = %s",[ds,c_id, b_id])
        mydb.commit()
