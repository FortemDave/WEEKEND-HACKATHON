#PROGRAM TO CONVERT BLOOD TYPE FROM ALPHANUMERIC TO ALPHA ONLY AND VICE VERSA
#FOR STORAGE AND VISUAL AID

def bgconvert(input_val):
    if input_val == "A+":
        return "AP"
    elif input_val == "A-":
        return "AM"
    elif input_val == "B+":
        return "BP"
    elif input_val == "B-":
        return "BM"
    elif input_val == "O+":
        return "OP"
    elif input_val == "O-":
        return "OM"
    elif input_val == "AB+":
        return "ABP"
    elif input_val == "AB-":
        return "ABM"

    elif input_val == "AP":
        return "A+"
    elif input_val == "AM":
        return "A-"
    elif input_val == "BP":
        return "B+"
    elif input_val == "BM":
        return "B-"
    elif input_val == "OP":
        return "O+"
    elif input_val == "OM":
        return "O-"
    elif input_val == "ABP":
        return "AB+"
    elif input_val == "ABM":
        return "AB-"
    else:
        print(f"INVALID input_val {input_val}-bgconvert")
        return None

