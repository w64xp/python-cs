import os
class TXT:
    def Create():
        text_data = """New file create"""
        with open("student.txt", "w", encoding="utf-8") as file:
            try:
                file.write(text_data)
                print("New file create")
            except:
                print("can't Save")
    def Reader():
        with open("student.txt", "r", encoding="utf-8") as file:
            try:
                print(file.read())
            except:
                print("can't read")
    def Updated(data_update):
        with open("student.txt", "w", encoding="utf-8") as file:
            try:
                file.write(data_update)
                print("update")
            except:
                print("can't update")
    def Del(fileName):
        file = fileName
        if(os.path.exists(file)):
            os.remove(file)
        else:
            print(f"Not found : {file}")

#----------------------------
while True:
    print("<--------------------------------------------------Menu-------------------------------------------------->")
    print("Q = Quit,C = Create,R = Read, Fetch, Quary, Select (index),U = Update,D = Delete (index)")
    print("<--------------------------------------------------Menu-------------------------------------------------->")
    status = input("Select : ")
    if(status.lower()=="q"):
        break
    elif(status.lower()=="c"):
        TXT.Create()
    elif(status.lower()=="r"):
        TXT.Reader()
    elif(status.lower()=="u"):
        inp = input("Data_input:")
        TXT.Updated(inp)
    elif(status.lower()=="d"):
        TXT.Del("student.txt")