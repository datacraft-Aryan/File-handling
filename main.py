from pathlib import Path
import os

def createfile():
    try:
        name= input("please tell your file name:- ")
        path= Path(name)
        if not path.exists(): 
            with open(path,"w") as fs:
                data=input("what you want to write:-")
                fs.write(data)
                print("file created successfully")
        else:
            print("Error File name already exists")   
    except Exception as err:
        print(f"an error occured as{err}")             


def readfile():
    try:
        name= input("Please tell your file name:-")
        path= Path(name)
        if path.exists():
            with open(path,"r") as fs:
                content= fs.read()
                print(f"your file content is\n{content}")
        else:
            print("error no such file exists")  
    except Exception as err:
        print(f"An error occured as {err}")

def updatefile():
    try:
        name= input("Please tell your file name:-")
        path= Path(name)
        if path.exists():
            print("operations")
            print("1. Renaming the file")
            print("2. Appending the content")
            print("3. Overwriting the file")

            choice=int(input("Enter your option:-"))
            if choice==1:
                newname= input("tell your new file name:-")
                new_path= Path(newname)
                if not new_path.exists():
                    path.rename(new_path)
                    print("renamed successfully")
                else:
                    print("file already exists")  
            elif choice== 2:
                with open(path,'a') as fs:
                    data= input("what do you want to append:-")
                    fs.write("\n"+data)  
                print("successfully append")  
            elif choice== 3:  
                with open(path,"w") as fs:  
                    data= input("what do you want to overwrite:-")
                    fs.write("\n"+data)  
                    print("successfully overwritten")
    except Exception as err:    
        print(f"An error occured as {err}")            

    
def deletefile():
    try:
        name= input("please tell your file name:-")
        path=Path(name)
        if path.exists():
            path.unlink()
            print("File deleted successfully")
        else:
            print("Error no suck file exists") 
    except Exception as err:
        print(f"An error occured as {err}")


 

print("press 1 for creating a file") 
print("press 2 for reading a file") 
print("press 3 for updating a file") 
print("press 4 for deleting a file") 

a = int(input("\ntell your response:-"))

if a==1:
    createfile()
if a==2:
    readfile()
if a==3:
    updatefile()
if a==4:
    deletefile()


