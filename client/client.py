import requests
import pwd
import os
from fabric import Connection
from patchwork.files import exists

USERNAME = pwd.getpwuid(os.getuid())[0]

MASTER_ADDRESS = 'http://127.0.0.1:5000'
KEY_LOCATION = f"/home/{USERNAME}/new_key.pem"
LOCAL_STORAGE = os.getcwd() + "/storage"
SERVER_STORAGE = '/home/ubuntu/storage'
CURRENT_DIR = ""


def init():
    datanode = requests.get(f"{MASTER_ADDRESS}/dirdel").text
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    con.run(f"rm -rf {SERVER_STORAGE}")
    con.run(f"mkdir {SERVER_STORAGE}")


def create(name):
    datanode = requests.get(f"{MASTER_ADDRESS}/create/{name}").text
    print("Datanode:", datanode)
    temp_file = open(f"{LOCAL_STORAGE}/{name}", "w")
    print(os.listdir(LOCAL_STORAGE))
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    path = os.path.join(SERVER_STORAGE, CURRENT_DIR)
    con.put(f"{LOCAL_STORAGE}/{name}", path)
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
    path = os.path.join(SERVER_STORAGE, CURRENT_DIR)
    con.put(f"{LOCAL_STORAGE}/{name}", path)


def read(name):
    datanode = requests.get(f"{MASTER_ADDRESS}/read/{name}").text
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
    con.get(f"{SERVER_STORAGE}/{name}", path)


def delete(name):
    datanode = requests.get(f"{MASTER_ADDRESS}/delete/{name}").text
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)

    # if exists(con, path):
    #     if exists(con, path):
    #         print(f"No such file {name}")
    #     else:
    #         con.run(f"rm {path}")
    # else:
    #     print(f"No such file {name}")

    if exists(con, path):
        con.run(f"rm {path}")
    else:
        print(f"No such file {name}")


def info(name):
    datanode = requests.get(f"{MASTER_ADDRESS}/info/{name}").text
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    # if exists(con, f"{SERVER_STORAGE}/{name}"):
    #     if exists(con, f"{SERVER_STORAGE}/{name}/"):
    #         print(f"No such file {name}")
    #     else:
    #         con.run(f"stat {SERVER_STORAGE}/{name}")
    # else:
    #     print(f"No such file {name}")
    path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
    if exists(con, path):
        con.run(f"stat {path}")
    else:
        print(f"No such file {name}")


def copy(name, new_loc):
    root = False
    if new_loc[0] == "~":
        root = True
        new_loc = new_loc[2::]
    global CURRENT_DIR
    datanode = requests.get(f"{MASTER_ADDRESS}/copy/{name}").text
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    path_file = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
    if root:
        path_loc = os.path.join(SERVER_STORAGE, new_loc)
        if exists(con, path_file):
            if exists(con, path_loc):
                con.run(f"cp -b {path_file} {path_loc}")
            else:
                print(f"No such directory {path_loc}")
        else:
            print(f"No such file {path_file}")
    else:
        path_loc = os.path.join(SERVER_STORAGE, CURRENT_DIR, new_loc)
        if exists(con, path_file):
            if exists(con, path_loc):
                con.run(f"cp -b {path_file} {path_loc}")
            else:
                print(f"No such directory {path_loc}")
        else:
            print(f"No such file {path_file}")

    # if exists(con, f"{SERVER_STORAGE}/{name}"):
    #     if exists(con, f"{SERVER_STORAGE}/{name}/"):
    #         print(f"No such file {name}")
    #     else:
    #         con.run(f"cp -b {SERVER_STORAGE}/{name} {SERVER_STORAGE}/{new_loc}/")
    # else:
    #     print(f"No such file {name}")


def move(name, new_loc):
    root = False
    if new_loc[0] == "~":
        root = True
        new_loc = new_loc[2::]
    global CURRENT_DIR
    datanode = requests.get(f"{MASTER_ADDRESS}/move/{name}").text
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    path_file = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
    if root:
        path_loc = os.path.join(SERVER_STORAGE, new_loc)
        if exists(con, path_file):
            if exists(con, path_loc):
                con.run(f"mv  {path_file} {path_loc}")
            else:
                print(f"No such directory {path_loc}")
        else:
            print(f"No such file {path_file}")
    else:
        path_loc = os.path.join(SERVER_STORAGE, CURRENT_DIR, new_loc)
        if exists(con, path_file):
            if exists(con, path_loc):
                con.run(f"mv {path_file} {path_loc}")
            else:
                print(f"No such directory {path_loc}")
        else:
            print(f"No such file {path_file}")

    # if exists(con, f"{SERVER_STORAGE}/{name}"):
    #     if exists(con, f"{SERVER_STORAGE}/{name}/"):
    #         print(f"No such file {name}")
    #     if exists(con, f"{SERVER_STORAGE}/{new_loc}/"):
    #         con.run(f"mv {SERVER_STORAGE}/{name} {SERVER_STORAGE}/{new_loc}/")
    #     else:
    #         print(f"No such directory {new_loc}")
    # else:
    #     print(f"No such file {name}")


def diropen(name):
    root = False
    if name[0] == "~":
        root = True
        name = name[2::]
    datanode = requests.get(f"{MASTER_ADDRESS}/diropen").text
    global CURRENT_DIR
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    if name == "back":
        cut = 0
        for i in range(len(CURRENT_DIR)):
            if CURRENT_DIR[i] == "/":
                cut = i
        # if CURRENT_DIR[cut + 1::] == "":
        #     print("Already in root directory!")
        # else:
            # before_c = CURRENT_DIR[:cut]
            # print(before_c)
        CURRENT_DIR = CURRENT_DIR[:cut]
        path = os.path.join(SERVER_STORAGE, CURRENT_DIR)
        print(f"Current directory: {path}")
        return
    # full path written (~/path)
    if root:
        path = os.path.join(SERVER_STORAGE, name)
        if exists(con, path):
            con.run(f"cd {path}")
            CURRENT_DIR = name
            print(f"Current directory: {path}")

        else:
            print(f"No such directory {path}")
    # new directory from current one (path or name of dir)
    else:
        path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
        if exists(con, path):
            # if CURRENT_DIR == "":
            #     CURRENT_DIR = f"{name}"
            # else:
            #     CURRENT_DIR = f"{CURRENT_DIR}/{name}"
            CURRENT_DIR = os.path.join(CURRENT_DIR, name)
            con.run(f"cd {path}")
            print(f"Current directory: {path}")
        else:
            print(f"No such directory {path}")


def dirread(name):
    root = False
    if name != "" and name[0] == "~":
        root = True
        name = name[2::]
    datanode = requests.get(f"{MASTER_ADDRESS}/dirread").text
    global CURRENT_DIR
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    if root:
        path = os.path.join(SERVER_STORAGE, name)
        if exists(con, f"{path}/"):
            con.run(f"ls {path}")
        else:
            print(f"No such directory {path}")
    else:
        path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
        print(path)
        if exists(con, str(path[:-1])):
            con.run(f"ls {path}")
        else:
            print(f"No such directory {path}")


def dirmake(name):
    root = False
    if name[0] == "~":
        root = True
        name = name[2::]
    datanode = requests.get(f"{MASTER_ADDRESS}/dirmake").text
    global CURRENT_DIR
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    if root:
        path = os.path.join(SERVER_STORAGE, name)
        if exists(con, path):
            print("Such directory already exists!")
        else:
            con.run(f"mkdir {path}")
    else:
        path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
        if exists(con, path):
            print("Such directory already exists!")
        else:
            con.run(f"mkdir {path}")


def dirdel(name):
    root = False
    if name != "" and name[0] == "~":
        root = True
        name = name[2::]
    datanode = requests.get(f"{MASTER_ADDRESS}/dirdel").text
    global CURRENT_DIR
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    if root:
        path = os.path.join(SERVER_STORAGE, name)
        if exists(con, path):
            # con.run(f"find {SERVER_STORAGE}/{CURRENT_DIR}/{name} -type f -exec echo Not empty \;")
            con.run(f"rm -rf {path}")
        else:
            print(f"No such directory {path}")
    else:
        path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
        if exists(con, path):
            # con.run(f"find {SERVER_STORAGE}/{CURRENT_DIR}/{name} -type f -exec echo Not empty \;")
            con.run(f"rm -rf {path}")
        else:
            print(f"No such directory {path}")


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
            "init": (init, ()),
            "create": (create, (name, )),
            "read": (read, (name, )),
            "write": (write, (name, )),
            "delete": (delete, (name, )),
            "info": (info, (name, )),
            "copy": (copy, (name, new_loc)),
            "move": (move, (name, new_loc)),
            "diropen": (diropen, (name, )),
            "dirread": (dirread, (name, )),
            "dirmake": (dirmake, (name, )),
            "dirdel": (dirdel, (name, ))
        }

        if command == "q":
            print("Quiting")
            return
        elif command not in functions:
            print("Command not found. Try again")
        else:
            func, args = functions[command]
            func(*args)
        print(f"DONE: `{' '.join(s)}`\n")


main()
