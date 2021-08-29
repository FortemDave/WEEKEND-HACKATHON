
from bgconvert import bgconvert
import datetime

#TEMPORARY POWER FOR DEBUGGING
import sqlite3
db_handle = sqlite3.connect('citybloodorg.db')
command = db_handle.cursor()
#############################-

def bldsmpldetails():
    #THE BLOOD SAMPLE QUANTITIES ARE LOGGED AT EVERY DONATION ACTION
    #THIS IS TO PRINT THE VALUES OF THE LATEST DAY .i.e TODAY
    print(f"The transactions done on {datetime.date.today()} are: ")

    command.execute("""SELECT blood_bank.name,bank_log.user_id,user.name,user.blood_group
                        FROM bank_log
                        INNER JOIN blood_bank
                        ON bank_log.bank_id = blood_bank.bank_id
                        INNER JOIN user
                        ON bank_log.user_id = user.user_id
                        WHERE bank_log.date = (?); """,(datetime.date.today(),))

    print("BANK_NAME | USER_ID  |  USER_NAME  | BLOOD TYPE")
    [print(f"{a}   {b}    {c}    {d}") for (a,b,c,d) in command.fetchall()]

def rarebldgrps():
    #THESE ARE ALSO STORED IN THE TABLES OF THE DATABASE FILE
    #THIS FUNCTION PRINTS OUT THE RARE BLOOD GROUP OF EACH BANK IN L
    #WE CONSIDER AB- B- and AB+ as rare groups

    command.execute("""SELECT bank_quantity.bank_id,blood_bank.name,bank_quantity.ABm,bank_quantity.Bm,bank_quantity.ABp
                       FROM bank_quantity
                       INNER JOIN blood_bank
                       ON bank_quantity.bank_id = blood_bank.bank_id ORDER BY bank_quantity.bank_id; """)

    print("BANK_ID     | BANK_NAME     | AB- Quantity (L) | B- Quantity (L) | AB+ Quantity (L)")
    [print(f"{a}   {b}    {c}    {d}  {e}") for (a,b,c,d,e) in command.fetchall()]

def donorDat():
    print("Enter 1 For User ID Input, Enter 2 for User NAME Input")
    choice = int(input("Choice-- "))

    if choice == 1:
        user_id = int(input("User-Id -- "))

        command.execute("SELECT * FROM user WHERE user_id = (?);",(user_id,))
        [print(i) for i in command.fetchone()]

    elif choice == 2:
        user_name = input("User Name(spelling sensitive) --").strip().upper()

        command.execute("SELECT * from user WHERE name like (?);",(user_name,))
        [print(i) for i in command.fetchone()]

    else:
        print("INVALID INPUT.TRY AGAIN")

def rarBgSpecificDat():
    value = input("Enter The Blood Type: ")
    value = bgconvert(value)

    print("Press 1 to print Donor Specific Data. Press 2 to print Blood Bank Data.")
    choice = int(input("Choice-- "))

    if choice == 1:
        command.execute("SELECT name,user_id,locality FROM user WHERE blood_group = (?);",(value,))
        print("NAME      |   USER_ID     | LOCALITY")
        [print(i) for i in command.fetchall()]

    elif choice == 2:
        if len(value) == 2:
            len_val = value[0] + value[1].lower()
        else:
            len_val = value[0] + value[1] + value[2].lower()
        command.execute(f"""SELECT blood_bank.name,bank_quantity.{len_val}
                            FROM blood_bank
                            INNER JOIN bank_quantity
                            ON blood_bank.bank_id = bank_quantity.bank_id""")

        [print(i) for i in command.fetchall()]

def branchDat():
    print("Enter 1 For Branch ID Input, Enter 2 for Branch NAME Input")
    choice = int(input("Choice-- "))

    if choice == 1:
        branch_id = int(input("User-Id -- "))

        command.execute("SELECT * FROM blood_bank WHERE bank_id = (?);",(branch_id,))

        if command.fetchone() == None:
            print("No data Exists for This User.\n")
            return
        [print(i) for i in command.fetchone()]

    elif choice == 2:
        branch_name = input("Branch/Bank Name(spelling sensitive) --").strip().upper()

        command.execute("SELECT * from blood_bank WHERE name like (?);",(branch_name,))
        [print(i) for i in command.fetchone()]

    else:
        print("INVALID INPUT.TRY AGAIN")

def dateWise():
    command.execute("SELECT * FROM bank_log WHERE date = (?)",(datetime.date.today(),))
    print("USER_ID | DATE | Quantity_transfused | Bank_ID")
    [print(i) for i in command.fetchall()]