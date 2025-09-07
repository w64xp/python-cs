import os

class TXT:
    filepath = r"C:\Users\Byt3sp1\student.txt"
    
    def Create():
        text_data = """New file create"""
        with open(TXT.filepath, "w", encoding="utf-8") as file:
            try:
                file.write(text_data)
                print("New file created")
            except:
                print("can't Save")

    def Reader():
        with open(TXT.filepath, "r", encoding="utf-8") as file:
            try:
                print(file.read())
            except:
                print("can't read")

    def Updated(data_update):
        with open(TXT.filepath, "w", encoding="utf-8") as file:
            try:
                file.write(data_update)
                print("update")
            except:
                print("can't update")

    def Del():
        if os.path.exists(TXT.filepath):
            os.remove(TXT.filepath)
            print("Deleted")
        else:
            print(f"Not found : {TXT.filepath}")


#----------------------------
while True:
    print("<--------------------------------------------------Menu-------------------------------------------------->")
    print("Q = Quit, C = Create, R = Read, U = Update, D = Delete")
    print("<--------------------------------------------------Menu-------------------------------------------------->")
    status = input("Select : ")
    if(status.lower()=="q"):
        break
    elif(status.lower()=="c"):
        TXT.Create()
    elif(status.lower()=="r"):
        TXT.Reader()
    elif(status.lower()=="u"):
        inp = input("Data_input: ")
        TXT.Updated(inp)
    elif(status.lower()=="d"):
        TXT.Del()
