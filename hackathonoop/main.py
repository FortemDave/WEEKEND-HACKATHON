import sqlite3
from user import *
from admin import *
from facilities import *
from bgconvert import *

print("-----------------------PRATHAM HARSHVARDHAN DAVE 20BCS102------------------------")
print("----BLOOD BANK ORGANIZATION SOFTWARE - Done with Python and SQLite3 Library.------")
print("----------------------------------------------------------------------------------")

print("Press to Access Website as a:-")
print("User ----------- 0")
print("Admin ---------- 1")
print("Website Programs 2")
print("___________________")

inp_val = int(input("INPUT -> "))

if inp_val == 0:
    print("==================================")
    print("Press 1 to Register.-------------")
    print("Press 0 to Login with existing ID.")
    choice = int(input("INPUT ->"))

    if choice == 1:
        registerUser()

    # elif choice == 2:
    print("Enter USER ID- \n[usable id- 1723573]")
    user_id_val = int(input("INPUT ->"))

    if idExist(user_id_val):
        DonateReq(user_id_val)
        print("\n")
        print("===========================================================================")
        print("You can request Blood From Blood Banks(for self,or others) should you wish.")
        print("Press 1 to Request Blood of your type")
        print("Press 0 to Cancel Request Procedure.")
        print("---------------------------------------------------------------------------")

        lock = int(input("Choice: "))
        if(lock == 1):
            reqBlood(user_id_val)
        else:
            print("Press X to exit.")

            lock = input("Choice: ").upper()
            if lock == 'X':
                exit
    else:
        print("INVALID ID. TERMINATING.")
        print("________________________")

elif inp_val == 1:
    print("Press 1 to Register.")
    print("Press 0 to Login with existing ID.")
    choice = int(input("INPUT ->"))

    if choice == 1:
        createAdmin()

    print("Enter Admin ID")
    admin_id = int(input("INPUT -> "))

    if adminExist(admin_id):
        print("Please Specify the function you want to perform.")
        print("1--------------Add Hospital To list")
        print("2-------------------View Donor List")
        print("3--------Check Blood Request Status")
        print("4--Issue Emergency Donation Request")

        decision = int(input("INPUT ->"))
        if decision == 1:
            addHospital()
        elif decision == 2:
            viewDonorList()
        elif decision == 3:
            chkBloodReq()
        elif decision == 4:
            displaeUsers()
            emrgncyNotif(admin_id)
        elif decision == 5:
            displaeUsers()
        else:
            print("INVALID INPUT. TERMINATING")
            exit
    
    else:
        print("INVALID ID-MATCH NOT FOUND-TERMINATING.")

elif inp_val == 2:
    print("1------Blood Sample Details---------------")
    print("2------Rare Blood Group Details-----------")
    print("3------Donor Data-------------------------")
    print("4------Rare Blood Group Specific Details.-")
    print("5------Blood Bank Specific Details--------")
    print("6-------Today's Log of Activity-----------")
    
    value = int(input("INPUT -> "))

    if value == 1:
        bldsmpldetails()
    elif value == 2:
        rarebldgrps()

    elif value == 3:
        print("[As the DONOR list is unkown to the new user, here it has been displayed. Not to be implimented in the final function] ")
        displaeUsers()
        print("Following Function is the one to be implimentend in the final one to hid user names from unkown users:-")
        donorDat()

    elif value == 4:
        rarBgSpecificDat()
    elif value == 5:
        branchDat()
    elif value == 6:
        dateWise()