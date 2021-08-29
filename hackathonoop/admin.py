from bgconvert import bgconvert
import random

#TEMPORARY POWER FOR DEBUGGING
import sqlite3
db_handle = sqlite3.connect('citybloodorg.db')
command = db_handle.cursor()


def createAdmin():
    name = input("Enter Name: ")
    
    admin_id = random.randrange(100,2000000,1)

    check = command.execute("SELECT EXISTS(SELECT admin_id FROM admin WHERE admin_id = (?) );",(admin_id,))

    while command.fetchone() == 1:
        user_id = random.randrange(100,2000000,1)
        check

    with db_handle:
        command.execute("INSERT INTO admin (admin_id,name) VALUES (?,?);",(admin_id,name,))
    
    print(f"Your Admin-ID on this website is : {admin_id}.")

    print("--------------------------------")
def addHospital():
    name = input("Hospital Name -> ")
    location = input(f"{name}'s Location ->")

    hospital_id = random.randrange(1,2000,1)

    check = command.execute("SELECT EXISTS(SELECT bank_id FROM blood_bank WHERE bank_id = (?) );",(hospital_id,))

    while command.fetchone() == 1:
        hospital_id = random.randrange(1,2000,1)
        check

    with db_handle:
        command.execute("INSERT INTO blood_bank (bank_id,name,location) VALUES (?,?,?)",(hospital_id,name.upper().strip(),location.upper().strip(),))
        command.execute("INSERT INTO bank_quantity (bank_id,Ap,Am,Bp,Bm,Op,Om,ABp,ABm) VALUES (?,?,?,?,?,?,?,?,?)",
                        (hospital_id,random.randrange(0,50,1),random.randrange(0,50,1),random.randrange(0,50,1),random.randrange(0,50,1),
                        random.randrange(0,50,1),random.randrange(0,50,1),random.randrange(0,50,1),random.randrange(0,50,1),))
        
    print(f"HOSPITAL - {name} SUCCESFULLY REGISTERED.")

def viewDonorList():
    blood_type = input("Enter Blood Type : ").upper().strip()
    
    print("Press '1' to view all donors with given Blood Group.")
    print("Press '0' to view donors in a given region")

    choice = int(input("Option -> "))

    if choice == 1:
        command.execute("SELECT name,locality FROM user WHERE blood_group = (?)",(bgconvert(blood_type),))
        [print(f"|{x} >- {y}") for (x,y) in command.fetchall()]
    elif choice == 0:
        locality = input("Enter the Location -> ").upper().strip()
        command.execute("SELECT name FROM user WHERE blood_group = (?) and locality = (?)",(bgconvert(blood_type),locality,))
        view_everything = [i for i in command.fetchall()]
        
        for val in view_everything:
            print(val)
    else:
        print("ERROR: INVALID INPUT.TRY AGAIN.")

def chkBloodReq():
    print("Press 1 to see PENDING requests.")
    print("Press 2 to see    ALL  requests.")

    select = int(input("Your Choice -> "))

    if select == 1:
        command.execute("""SELECT request_log.quantity,request_log.donor_id,user.name 
                        FROM request_log 
                        INNER JOIN user
                        ON request_log.donor_id = user.user_id
                        WHERE has_accepted IS NULL""")
        print("Quantity  | Donor_ID |  Donor_name")
        [print(f"{x} - {y} - {z}") for (x,y,z) in command.fetchall()]
    
    elif select == 2:
        command.execute("""SELECT request_log.quantity,request_log.donor_id,user.name,request_log.has_accepted
                           FROM request_log
                           INNER JOIN user
                           ON request_log.donor_id = user.user_id""")
        print("Quantity  | Donor_ID |  Donor_name | Status")
        [print(f"{x} - {y} - {z} - {a}") for (x,y,z,a) in command.fetchall()]

    else:
        print("ERROR: INVALID INPUT.TRY AGAIN.")

def emrgncyNotif(admin_id):
    # WE ASSUME THAT THE EMERGENCY NOTIFICATION "REQUIREMENTS" 
    #ARE PROVIDED TO THE ADMIN VIA MAIL/IN_PERSON and HENCE
    #WE DIRECTLY INPUT THE VALUES INTO THE REQUEST LOG WITH
    #PERSONALLY INPUT DATA
    admin_id = admin_id;
    reciever_id = input("Enter the reciever's registered ID->")
    blood_type = input("Enter The Blood type requested -> ")
    quantity = input("Enter the quantity (in L) required -> ")
    chemk = int(input("If location is required, press 1. Else, press 0 ->"))
    values = []
    if chemk == 1:
        location = input("Location -> ")

        print("------------------------------------------")
        print("The Following Users are Eligible for donating blood and will be notified for donation immediately.")
        print("USER_ID   |   NAME")

        command.execute("""SELECT user_id,name from user WHERE blood_group = (?) AND location = (?);""",(bgconvert(blood_type),location,))
        for (x,y) in command.fetchall():
            values.append(x)
            print(f"{x} - {y}" )
            with db_handle:
                command.execute("INSERT INTO request_log (admin_id,reciever_id,donor_id,quantity) VALUES (?,?,?,)"
                                ,(admin_id,reciever_id,x,quantity))
    elif chemk == 0:

        
        print("------------------------------------------")
        print("The Following Users are Eligible for donating blood and will be notified for donation immediately.")
        print("USER_ID   |   NAME   | LOCATION")
        command.execute("""SELECT user_id,name,locality from user WHERE blood_group = (?) AND is_donor = TRUE;""",(bgconvert(blood_type),))

        for (x,y,z) in command.fetchall():
            print(f"{x} - {y} - {z}" )
            with db_handle:
                command.execute("INSERT INTO request_log (admin_id,recipient_id,donor_id,quantity) VALUES (?,?,?,?)",(admin_id,reciever_id,x,quantity))


    else:
        print("INVALID INPUT. TRY AGAIN.")  

def adminExist(id_admin):
    command.execute("SELECT admin_id FROM admin WHERE admin_id = (?)",(id_admin,))
    val = command.fetchone()
    if val == type(None):
        return False
    return True

def displaeUsers():
    command.execute("SELECT * FROM user;")
    print("USER-ID  |   NAME   |    LOCALITY |  DONOR  |  BLOOD_GROUP")
    [print(i) for i in command.fetchall()]