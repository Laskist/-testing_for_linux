import pytest
from checkout import checkout, getout
import yaml
import random, string
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout('mkdir {} {} {}'.format(data['FOLDER_TST'], data['FOLDER_OUT'], data['FOLDER_folder1']), '')


@pytest.fixture()
def clear_folders():
    return checkout('rm -rf {}/* {}/* {}/*'.format(data['FOLDER_TST'], data['FOLDER_OUT'], data['FOLDER_folder1']), '')


@pytest.fixture()
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["FOLDER_TST"], filename, data['bs']), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    test_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    test_subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout('cd {}; mkdir {}'.format(data['FOLDER_TST'], test_subfolder_name), ''):
        return None, None
    if not checkout('cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock'.format(data['FOLDER_TST'], test_subfolder_name, test_file_name), ''):
        return test_subfolder_name, None
    else:
        return test_subfolder_name, test_file_name


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S:%F")))
    yield
    print("Stop: {}".format(datetime.now().strftime("%H:%M:%S:%F")))

@pytest.fixture()
def make_bad_arx():
    checkout("cd {}; 7z a {}/badarx -t{}".format(data["FOLDER_TST"], data["FOLDER_OUT"], data['file_extension']), "Everything is Ok")
    checkout("truncate -s 1 {}/badarx.{}".format(data["FOLDER_OUT"], data['file_extension']), "Everything is Ok")
    yield "badarx"
    checkout("rm -rf {}/badarx.{}".format(data["FOLDER_OUT"], data['file_extension']), "")

@pytest.fixture(autouse=True)
def stat():
    yield
    stat = getout("cat /proc/loadavg")
    checkout("echo 'time: {} count:{} size: {} load: {}'>> stat.txt".format(datetime.now().
                        strftime("%H:%M:%S.%f"), data["count"], data["bs"], stat), "")