import requests
import pwd
import os
from fabric import Connection

USERNAME = pwd.getpwuid(os.getuid())[0]

MASTER_ADDRESS = 'http://127.0.0.1:5000'
KEY_LOCATION = f"/home/{USERNAME}/new_key.pem"
CUR_DIR = os.getcwd()


def init():
    print("This is mock function")


def create(name):
    datanode = requests.get(f"{MASTER_ADDRESS}/create/{name}").text
    print(f"{MASTER_ADDRESS}/create/{name}")
    print(datanode)
    temp_file = open(name, "w")
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    con.put(f"{CUR_DIR}/{name}", "/home/ubuntu")
    os.remove(name)


def read(name):
    print("This is mock function")


def write(name):
    print("This is mock function")


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
            print(func, args)
            func(args)
        print(f"DONE: `{' '.join(s)}`")


main()
