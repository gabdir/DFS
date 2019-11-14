import requests
import pwd
import os
from fabric import Connection

USERNAME = pwd.getpwuid(os.getuid())[0]

MASTER_ADDRESS = 'http://127.0.0.1:5000'
KEY_LOCATION = f"/home/{USERNAME}/new_key.pem"
LOCAL_STORAGE = os.getcwd() + "/storage"
SERVER_STORAGE = '/home/ubuntu'


def init():
    print("This is mock function")


def create(name):
    datanode = requests.get(f"{MASTER_ADDRESS}/create/{name}").text
    print("Datanode:", datanode)
    temp_file = open(f"{LOCAL_STORAGE}/{name}", "w")
    print(os.listdir(LOCAL_STORAGE))
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )

    con.put(f"{LOCAL_STORAGE}/{name}", SERVER_STORAGE)
    os.remove(f"{LOCAL_STORAGE}/{name}")


def write(name):
    if name not in os.listdir(LOCAL_STORAGE):
        print(f"No such file `{name}`")
        return

    datanode = requests.get(f"{MASTER_ADDRESS}/write/{name}").text
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    con.put(f"{LOCAL_STORAGE}/{name}", SERVER_STORAGE)


def read(name):
    datanode = requests.get(f"{MASTER_ADDRESS}/read/{name}").text
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    con.get(f"{SERVER_STORAGE}/{name}", f"{LOCAL_STORAGE}/{name}")


def delete(name):
    print("This is mock function")


def info(name):
    print("This is mock function")


def copy(name, new_loc):
    print("This is mock function")


def move(name, new_loc):
    print("This is mock function")


def diropen(name):
    print("This is mock function")


def dirread(name):
    print("This is mock function")


def dirmake(name):
    print("This is mock function")


def dirdel(name):
    print("This is mock function")


def main():
    """
        ● Initialize​ (). Initialize the client storage on a new system, should remove any
          existing file in the dfs root directory and return available size.
        ● File create (file).​ Should allow to create a new empty file.
        ● File read​ (file). Should allow to read any file from DFS (download a file from the DFS to the Client side).
        ● File write​ (file). Should allow to put any file to DFS (upload a file from the Client side to the DFS)
        ● File delete​ (file). Should allow to delete any file from DFS
        ● File info​ (file). Should provide information about the file (any useful information - size, node id, etc.)
        ● File copy​ (file, new_loc). Should allow to create a copy of file.
        ● File move​ (file, new_loc). Should allow to move a file to the specified path.
        ● Open directory​ (dir). Should allow to change directory
        ● Read directory​ (dir). Should return list of files, which are stored in the directory.
        ● Make directory​ (dir). Should allow to create a new directory.
        ● Delete directory​ (dir). Should allow to delete directory. If the directory contains files
          the system should ask for confirmation from the user before deletion.
    """
    while True:
        s = input().split()
        command = s[0]
        name = "" if len(s) <= 1 else s[1]
        new_loc = "" if len(s) <= 2 else s[2]

        functions = {
            "init": (init,),
            "create": (create, (name)),
            "read": (read, (name)),
            "write": (write, (name)),
            "delete": (delete, (name)),
            "info": (info, (name)),
            "copy": (copy, (name, new_loc)),
            "move": (move, (name, new_loc)),
            "diropen": (diropen, (name)),
            "dirread": (dirread, (name)),
            "dirmake": (dirmake, (name)),
            "dirdel": (dirdel, (name))
        }

        if command == "q":
            print("Qiting")
            return
        elif command not in functions:
            print("Command not found. Try again")
        else:
            func, args = functions[command]
            func(args)
        print(f"DONE: `{' '.join(s)}`\n")


main()
