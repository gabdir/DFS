import requests
import os
from fabric import Connection
from patchwork.files import exists

MASTER_ADDRESS = 'http://127.0.0.2:5000'
KEY_LOCATION = "my_key.pem"
LOCAL_STORAGE = os.getcwd() + "/storage"
SERVER_STORAGE = '/home/ubuntu/storage'
CURRENT_DIR = ""


def init():
    response = requests.get(f"{MASTER_ADDRESS}/init")
    datanodes = response.json()['datanodes']
    for datanode in datanodes:
        print("Datanode:", datanode)
        con = Connection(host=datanode,
                         user="ubuntu",
                         connect_kwargs={"key_filename": KEY_LOCATION}
                         )
        con.run(f"rm -rf {SERVER_STORAGE}")
        con.run(f"mkdir {SERVER_STORAGE}")


def write(name, creation=False):
    if not creation:
        if name not in os.listdir(LOCAL_STORAGE):
            print(f"No such local file `{name}`")
            return
        size = os.path.getsize(os.path.join(LOCAL_STORAGE, name))
    else:
        open(f"{LOCAL_STORAGE}/{name}", "w")
        size = 0
    headers = {'size': str(size), 'dir_path': CURRENT_DIR}
    response = requests.get(f"{MASTER_ADDRESS}/write/{name}", headers=headers)
    status = response.status_code

    if status == 400:
        print("Such file already exists!")
        return
    datanodes = response.json()['datanodes']
    for datanode in datanodes:
        print("Datanode:", datanode)
        con = Connection(host=datanode,
                         user="ubuntu",
                         connect_kwargs={"key_filename": KEY_LOCATION}
                         )
        path = os.path.join(SERVER_STORAGE, CURRENT_DIR)
        con.put(f"{LOCAL_STORAGE}/{name}", path)
    if creation:
        os.remove(f"{LOCAL_STORAGE}/{name}")


def create(name):
    write(name, creation=True)


def read(name):
    headers = {"dir_path": CURRENT_DIR}
    response = requests.get(f"{MASTER_ADDRESS}/read/{name}", headers=headers)
    datanode = response.json()['datanode']
    status = response.status_code
    if status == 400:
        print(f"No such file {name}")
        return
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
    con.get(path, f"{LOCAL_STORAGE}/{name}")


def delete(name):
    response = requests.get(f"{MASTER_ADDRESS}/delete/{name}")
    status = response.status_code

    if status == 400:
        print(response.json()['message'])
        return
    else:
        datanodes = response.json()['datanodes']
        for datanode in datanodes:
            print("Datanode:", datanode)
            con = Connection(host=datanode,
                             user="ubuntu",
                             connect_kwargs={"key_filename": KEY_LOCATION}
                             )
            path = os.path.join(SERVER_STORAGE, CURRENT_DIR, name)
            con.run(f"rm {path}")


def info(name):
    response = requests.get(f"{MASTER_ADDRESS}/info/{name}")
    print(response.json()["message"])


def copy(name, new_loc):
    move(name, new_loc, copy=True)


def move(name, new_loc, copy=False):
    dir_to_move = get_dir(new_loc)
    temp_dir = get_dir_for_file(name)
    headers = {"dir_from_move": temp_dir, "dir_to_move": dir_to_move}
    if copy:
        response = requests.get(f"{MASTER_ADDRESS}/copy/{name}", headers=headers)
    else:
        response = requests.get(f"{MASTER_ADDRESS}/move/{name}", headers=headers)
    datanodes = response.json()['datanodes']
    message = response.json()['message']
    status = response.status_code
    if status == 400:
        print(message)
        return
    for datanode in datanodes:
        print("Datanode:", datanode)
        con = Connection(host=datanode,
                         user="ubuntu",
                         connect_kwargs={"key_filename": KEY_LOCATION}
                         )
        path_file = os.path.join(SERVER_STORAGE, temp_dir)
        file = os.path.join(path_file, name)
        if exists(con, path_file):
            path_loc = os.path.join(SERVER_STORAGE, dir_to_move)
            if exists(con, path_loc):
                if copy:
                    con.run(f"cp -b {file} {path_loc}")
                else:
                    con.run(f"mv {file} {path_loc}")
            else:
                print(f"No such directory {path_loc}")
        else:
            print(f"No such file {path_file}")


def get_dir_for_file(name):
    root = False
    if name != "" and name[0] == "~":
        root = True
        name = name[2::]
    if root:
        cut = 0
        for i in range(len(name)):
            if name[i] == "/":
                cut = i
        temp_dir = name[:cut]
    else:
        cut = 0
        for i in range(len(name)):
            if name[i] == "/":
                cut = i
        temp_to_cur = name[:cut]
        temp_dir = os.path.join(CURRENT_DIR, temp_to_cur)
        if cut == 0:
            temp_dir = temp_dir[:-1]
    return temp_dir


def get_dir(name):
    root = False
    if name != "" and name[0] == "~":
        root = True
        name = name[2::]

    if root:
        temp_dir = name
    else:
        if name == "":
            temp_dir = CURRENT_DIR
        else:
            temp_dir = os.path.join(CURRENT_DIR, name)

    return temp_dir


def diropen(name):
    global CURRENT_DIR

    if name == "back":
        cut = 0
        for i in range(len(CURRENT_DIR)):
            if CURRENT_DIR[i] == "/":
                cut = i

        CURRENT_DIR = CURRENT_DIR[:cut]
        path = os.path.join(SERVER_STORAGE, CURRENT_DIR)
        print(f"Current directory: {path}")
        return

    temp_dir = get_dir(name)
    headers = {"dir_path": temp_dir}
    response = requests.get(f"{MASTER_ADDRESS}/diropen", headers=headers)
    datanode = response.json()['datanode']
    status = response.status_code
    if status == 400:
        print(f"No such directory {temp_dir}")
        return
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )

    path = os.path.join(SERVER_STORAGE, temp_dir)
    if exists(con, path):
        con.run(f"cd {path}")
        CURRENT_DIR = temp_dir
        print(f"Current directory: {path}")
    else:
        print(f"No such directory {path}")


def dirread(name):
    global CURRENT_DIR
    temp_dir = get_dir(name)
    headers = {"dir_path": temp_dir}
    response = requests.get(f"{MASTER_ADDRESS}/dirread", headers=headers)
    datanode = response.json()['datanode']
    status = response.status_code
    if status == 400:
        print(f"No such directory {temp_dir}")
        return
    print("Datanode:", datanode)
    con = Connection(host=datanode,
                     user="ubuntu",
                     connect_kwargs={"key_filename": KEY_LOCATION}
                     )
    path = os.path.join(SERVER_STORAGE, temp_dir)
    if exists(con, path):
        print(f"Directory: {path}")
        print(f"List of files and directories:")
        con.run(f"ls {path}")
    else:
        print(f"No such directory {path}")


def dirmake(name):
    path_without = get_dir_for_file(name)
    path_with_current = get_dir(name)
    cut = 0
    for i in range(len(name)):
        if name[i] == "/":
            cut = i
    only_name = name[(cut + 1):]
    headers = {"dir_path": path_without, "dir_with_current": path_with_current}
    response = requests.get(f"{MASTER_ADDRESS}/dirmake/{only_name}", headers=headers)
    status = response.status_code
    message = response.json()["message"]
    if status == 400:
        print(message)
        return
    datanodes = response.json()['datanodes']
    for datanode in datanodes:
        print("Datanode:", datanode)
        con = Connection(host=datanode,
                         user="ubuntu",
                         connect_kwargs={"key_filename": KEY_LOCATION}
                         )
        full_with_current = os.path.join(SERVER_STORAGE, path_with_current)
        full_without = os.path.join(SERVER_STORAGE, path_without)
        if exists(con, full_without):
            if exists(con, full_with_current):
                print("Such directory already exists!")
            else:
                con.run(f"mkdir {full_with_current}")
        else:
            print(f"No such directory {full_without}")


def dirdel(name):
    global CURRENT_DIR
    dir_path = get_dir(name)
    headers = {'dir_path': dir_path}
    response = requests.get(f"{MASTER_ADDRESS}/dirdel", headers=headers)
    datanodes = response.json()['datanodes']
    status = response.status_code
    message = response.json()['message']
    if status == 400:
        print(message)
        return
    for datanode in datanodes:
        print("Datanode:", datanode)
        con = Connection(host=datanode,
                         user="ubuntu",
                         connect_kwargs={"key_filename": KEY_LOCATION}
                         )
        path = os.path.join(SERVER_STORAGE, dir_path)
        if exists(con, path):
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
    global MASTER_ADDRESS
    MASTER_ADDRESS = input('datanode ip:').strip()
    while True:
        s = input().split()
        command = s[0]
        name = "" if len(s) <= 1 else s[1]
        new_loc = "" if len(s) <= 2 else s[2]

        functions = {
            "init": (init, ()),
            "create": (create, (name,)),
            "read": (read, (name,)),
            "write": (write, (name,)),
            "delete": (delete, (name,)),
            "info": (info, (name,)),
            "copy": (copy, (name, new_loc)),
            "move": (move, (name, new_loc)),
            "diropen": (diropen, (name,)),
            "dirread": (dirread, (name,)),
            "dirmake": (dirmake, (name,)),
            "dirdel": (dirdel, (name,))
        }

        if command == "q":
            print("Quiting")
            return
        elif command not in functions:
            print("Command not found. Try again")
        else:
            func, args = functions[command]
            func(*args)
        print(f"Executed: `{' '.join(s)}`\n")


if __name__ == "__main__":
    main()
