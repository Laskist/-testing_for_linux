from checkout import getout
from ssh_checkout import ssh_checkout_negative
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


def save_log(start_time, name):
    with open(name, "w", encoding="utf-8") as f:
        f.write(getout(f"journalctl --since '{start_time}'"))


class TestNegative:

    def test_step1(self, make_bad_arx, start_time):
        save_log(start_time, "log_negative_step1")
        assert ssh_checkout_negative(data["host"], data["user"], data["passwd"], 'cd {}; 7z e arxbad.{} -o{} -y'.format(data["FOLDER_OUT"], data['file_extension'], data["FOLDER_folder1"]), 'Can not open the file as [zip] archive'), 'test1 negative fail'

    def test_step2(self, make_bad_arx, start_time):
        save_log(start_time, "log_negative_step2")
        assert ssh_checkout_negative(data["host"], data["user"], data["passwd"], 'cd {}; 7z t arxbad.{}'.format(data["FOLDER_OUT"], data["file_extension"]), 'Can not open the file as [zip] archive'), 'test2 negative fail'

