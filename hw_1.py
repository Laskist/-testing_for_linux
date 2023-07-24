import subprocess
import string


def func_all(command: str, text: str):
    """search of all matches"""
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if res.returncode == 0:
        if text in res.stdout:
            return True
        else:
            return False
    else:
        return False


def func_str(command: str, text: str):
    """string match search"""
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    my_list = res.stdout.split('\n')
    if res.returncode == 0:
        if text in my_list:
            return True
        else:
            return False
    else:
        return False


def func_word(command: str, text: str):
    """word matching search"""
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    my_list = res.stdout.translate(string.punctuation)
    if res.returncode == 0:
        if text in my_list:
            return True
        else:
            return False
    else:
        return False


if __name__ == '__main__':
    print(func_all('cat /etc/os-release', 'jammy'))
    print(func_str('cat /etc/os-release', 'VERSION_CODENAME=jammy'))
    print(func_str('cat /etc/os-release', 'VERSION_CODENAME='))
    print(func_word('cat /etc/os-release', 'PRETY'))
    print(func_word('cat /etc/os-release', 'PRETTY'))