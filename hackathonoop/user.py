
import random
import datetime
from bgconvert import *
#TEMPORARY POWER FOR DEBUGGING---------------
import sqlite3
from bgconvert import bgconvert
db_handle = sqlite3.connect('citybloodorg.db', timeout=10)
command = db_handle.cursor()
#TEMP----------------------------------------

def registerUser():
    name = input("Full Name: ")
    blood_grp = input("Blood Group: ")
    blood_grp = bgconvert(blood_grp)
    location = input("Home Location: ")

    print("Are you registering as a donor?")
    print("Press 'Y' to agree. Press any other letter to deny.")
    if input().upper() == 'Y':
        is_donor = True
        print("You have been registered as a DONOR !")
    else:
        is_donor = False
        print("You have been registered as an Acceptor/Paitent !")
    
    user_id = random.randrange(100,2000000,1)

    check = command.execute("SELECT EXISTS(SELECT user_id FROM user WHERE user_id = (?) );",(user_id,))

    while command.fetchone() == 1:
        user_id = random.randrange(100,2000000,1)
        check

    with db_handle:
        command.execute("INSERT INTO user (user_id,name,locality,blood_group,is_donor) VALUES (?,?,?,?,?);",
                            (user_id,name.upper().strip(),location.upper().strip(),blood_grp.strip(),is_donor,))
    
    print(f"Your ID on this website is : {user_id}.")

    print("--------------------------------")
    #return user_id
    #MAY BE REQUIRED FOR BETTER AUTOMATION


def reqBlood(user_id_val):
    user_id = user_id_val
    command.execute("SELECT blood_group FROM user WHERE user_id = (?);",(user_id,))
    blood_group = "".join(list(command.fetchone()))
    print(type(blood_group))
    quantity = int(input(f"What quantity of Blood Type : {bgconvert(blood_group)} Would you like to request? : "))

    print("The Following Hospitals have the Required Blood in given Quantity: ")

    command.execute("""SELECT name
                        FROM blood_bank
                        INNER JOIN bank_quantity ON
                        blood_bank.bank_id = bank_quantity.bank_id
                        WHERE bank_quantity.ABM > (?);""",  (quantity,))  

    limst = list(command.fetchall())
    if not limst:
        print("Kindly Submit a Request to an Admin via Mail to get Blood Imported from inter-city Hospitals.")
        print("Access the functions as an ADMIN to create Donor Requests.")
        return 
    else:
        [print(i[0]) for i in limst]

    print("Enter the name of the hospital you would like \n to request the blood to be donated from.")
    hosp_name = input("Hospital Name :")
    hosp_name = hosp_name.upper().strip()

    with db_handle:
        command.execute("""SELECT bank_id FROM blood_bank WHERE name LIKE (?);""",(hosp_name.upper().strip(),))
        bank_id = (command.fetchone())
        bank_id = bank_id[0]


        command.execute(f"""UPDATE bank_quantity SET {blood_group} = {blood_group} - (?) WHERE bank_id = (?)""",
                     (quantity, int(bank_id),))

        command.execute("INSERT INTO bank_log (bank_id,user_id,date,quantity_transfered) VALUES (?,?,?,?)"
                         ,(int(bank_id),int(user_id),datetime.date.today(),int(quantity),))


    print("Congratulations! Your request has been lodged and validated.")
    print("Kindly visit the hospital in working hours to get the transfusion.")

def DonateReq(user_id_val):
    user_id = user_id_val
    command.execute("SELECT quantity FROM request_log WHERE donor_id = (?);",(user_id,))
    sum_valv = [ i for i in command.fetchone()]
    
    sum_val = sum_valv[0]
    
    if sum_val is None:
        print("You Have no Active Donor Requests.")
        return
    
    

    if sum_val >= 1:
        print(f"ALERT! You have been requested to donate {sum_val} amount of your blood for transfusion.")
        print("Would you like to donate your blood and possibly save a life?")
        print("Type 'Y' to agree, anything else to disagree.")
        x = input("Your Answer: ")

        if x.upper() == "Y" or x.upper() == "YES":
            with db_handle:
                command.execute("UPDATE request_log SET has_accepted = (?)",(True,))

            print("Thank you for your service.")
        else:
            with db_handle:
                command.execute("UPDATE request_log SET has_accepted = (?)",(False,))

            print("Your response has been lodged.")

def idExist(user_id_val):
    command.execute("SELECT name FROM user WHERE user_id = (?);",(user_id_val,))
    val =command.fetchone()
    if val == type(None):
        return False
    return True