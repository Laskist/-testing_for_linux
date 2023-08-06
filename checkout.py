import subprocess

FOLDER_TST = "/home/user/tst"
FOLDER_OUT = "/home/user/out"
FOLDER_folder1 = "/home/user/folder1"

def checkout(cmd, text):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if (text in res.stdout and res.returncode == 0) or text in res.stderr:
        return True
    else:
        return False