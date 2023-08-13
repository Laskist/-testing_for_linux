# from checkout import checkout
# import pytest
# import yaml
# import random, string
# from datetime import datetime
# from ssh_checkout import ssh_checkout, ssh_getout
#
# with open('config.yaml') as f:
#     data = yaml.safe_load(f)
#
#
#
# @pytest.fixture()
# def clear_folders():
#     return ssh_checkout(data["host"], data["user"], data["passwd"], 'rm -rf {}/* {}/* {}/*'.format(data['FOLDER_TST'], data['FOLDER_OUT'], data['FOLDER_folder1']), '')
#
#
# @pytest.fixture()
# def make_files():
#     list_of_files = []
#     for i in range(data["count"]):
#         filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#         if ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["FOLDER_TST"], filename, data['bs']), ""):
#             list_of_files.append(filename)
#     return list_of_files
#
#
# @pytest.fixture()
# def make_subfolder():
#     test_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#     test_subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
#     if not ssh_checkout(data["host"], data["user"], data["passwd"], 'cd {}; mkdir {}'.format(data['FOLDER_TST'], test_subfolder_name), ''):
#         return None, None
#     if not ssh_checkout(data["host"], data["user"], data["passwd"], 'cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data['FOLDER_TST'], test_subfolder_name, test_file_name), ''):
#         return test_subfolder_name, None
#     else:
#         return test_subfolder_name, test_file_name
#
#
# @pytest.fixture(autouse=True)
# def print_time():
#     print("Start: {}".format(datetime.now().strftime("%H:%M:%S:%F")))
#     yield
#     print("Stop: {}".format(datetime.now().strftime("%H:%M:%S:%F")))
#
# @pytest.fixture()
# def make_bad_arx():
#     ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z a {}/badarx -t{}".format(data["FOLDER_TST"], data["FOLDER_OUT"], data['file_extension']), "Everything is Ok")
#     ssh_checkout(data["host"], data["user"], data["passwd"], "truncate -s 1 {}/badarx.{}".format(data["FOLDER_OUT"], data['file_extension']), "Everything is Ok")
#     yield "badarx"
#     ssh_checkout(data["host"], data["user"], data["passwd"], "rm -rf {}/badarx.{}".format(data["FOLDER_OUT"], data['file_extension']), "")
#
# @pytest.fixture(autouse=True)
# def stat():
#     yield
#     stat = ssh_getout(data["host"], data["user"], data["passwd"],"cat /proc/loadavg")
#     checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().
#                         strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat), "")
#
# @pytest.fixture()
# def start_time():
#     return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


import pytest
from ssh_checkout import ssh_checkout
import random, string
import yaml
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
                        "mkdir {} {} {}".format(data["FOLDER_TST"], data["FOLDER_OUT"], data["FOLDER_folder1"]), "")


@pytest.fixture()
def clear_folders():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
                        "rm -rf {}/* {}/* {}/*".format(data["FOLDER_TST"], data["FOLDER_OUT"], data["FOLDER_folder1"]),
                        "")


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(data["host"], data["user"], data["passwd"],
                        "cd {}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["FOLDER_TST"],
                                                                                               filename), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], data["passwd"],
                        "cd {}; mkdir {}".format(data["FOLDER_TST"], subfoldername), ""):
        return None, None
    if not ssh_checkout(data["host"], data["user"], data["passwd"],
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["FOLDER_TST"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
    ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z a {}/arxbad -t{}".format(data["FOLDER_TST"],
                                                                                                 data["FOLDER_OUT"],
                                                                                                 data[
                                                                                                     "file_extension"]),
                 "Everything is Ok")
    ssh_checkout(data["host"], data["user"], data["passwd"], "truncate -s 1 {}/arxbad.{}".format(data["FOLDER_OUT"],
                                                                                                 data[
                                                                                                     "file_extension"]),
                 "Everything is Ok")
    yield "arxbad"
    ssh_checkout(data["host"], data["user"], data["passwd"],
                 "rm -f {}/arxbad.{}".format(data["FOLDER_OUT"], data["file_extension"]), "")


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield print("Stop: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture()
def start_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
