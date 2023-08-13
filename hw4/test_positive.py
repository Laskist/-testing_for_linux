from ssh_checkout import ssh_checkout, ssh_getout
from checkout import getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def save_log(self, start_time, name):
        with open(name, 'w') as f:
            f.write(getout("journalctl --since '{}'".format(start_time)))

    def test_step1(self, make_folders, clear_folders, make_files, start_time):
        res1 = ssh_checkout(data["host"], data["user"], data["passwd"],
                            'cd {}; 7z a {}/arx -t{}'.format(data['FOLDER_TST'], data['FOLDER_OUT'],
                                                             data['file_extension']), 'Everything is Ok')
        res2 = ssh_checkout(data["host"], data["user"], data["passwd"], 'ls {}'.format(data['FOLDER_OUT']),
                            'arx.{}'.format(data['file_extension']))
        self.save_log(start_time, "log_test_step1.txt")
        assert res1 and res2, 'test1 fail'

    def test_step2(self, clear_folders, make_files, start_time):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                'cd {}; 7z a {}/arx -t{}'.format(data['FOLDER_TST'], data['FOLDER_OUT'],
                                                                 data['file_extension']), 'Everything is Ok'))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                'cd {}; 7z e arx.{} -o{} -y'.format(data["FOLDER_OUT"], data["file_extension"],
                                                                    data["FOLDER_folder1"]), "Everything is Ok"))
        for item in make_files:
            res.append(
                ssh_checkout(data["host"], data["user"], data["passwd"], 'ls {}'.format(data['FOLDER_folder1']), item))
        self.save_log(start_time, "log_test_step2.txt")
        assert all(res), 'test2 fail'

    def test_step3(self, start_time):
        self.save_log(start_time, "log_test_step3.txt")
        assert ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z t"
                                                                      " arx.{}".format(data["FOLDER_OUT"], data["file_extension"]),
                            "Everything is Ok"), "test4 FAIL"


    def test_step4(self, start_time):
        self.save_log(start_time, "log_test_step4.txt")
        assert ssh_checkout(data["host"], data["user"], data["passwd"], 'cd {}; 7z u arx.{}'.format(data['FOLDER_OUT'], data['file_extension']),
                            'Everything is Ok'), 'test4 fail'

    def test_step5(self, clear_folders, make_files, start_time):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                'cd {}; 7z a {}/arx -t{}'.format(data['FOLDER_TST'], data['FOLDER_OUT'],
                                                                 data['file_extension']), 'Everything is Ok'))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    'cd {}; 7z l arx.{}'.format(data['FOLDER_OUT'], data['file_extension']), item))
        self.save_log(start_time, "log_test_step5.txt")
        assert all(res), 'test5 fail'

    #
    #
    def test_step6(self, clear_folders, make_files, make_subfolder, start_time):
        res = []
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                'cd {}; 7z a {}/arx2 -t{}'.format(data['FOLDER_TST'], data['FOLDER_OUT'],
                                                                 data['file_extension']), 'Everything is Ok'))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                'cd {}; 7z x arx2.{} -o{} -y'.format(data['FOLDER_OUT'], data['file_extension'],
                                                                    data['FOLDER_folder1']), 'Everything is Ok'))
        for item in make_files:
            res.append(
                ssh_checkout(data["host"], data["user"], data["passwd"], 'ls {}'.format(data['FOLDER_folder1']), item))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], 'ls {}'.format(data['FOLDER_folder1']),
                                make_subfolder[0]))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                'ls {}/{}'.format(data['FOLDER_folder1'], make_subfolder[0]), make_subfolder[1]))
        self.save_log(start_time, "log_test_step6.txt")
        assert all(res), 'test6 fail'


    def test_step7(self, start_time):
        self.save_log(start_time, "log_test_step7.txt")
        assert ssh_checkout(data["host"], data["user"], data["passwd"], "cd {}; 7z d arx.{}".format(data["FOLDER_OUT"], data["file_extension"]),
                            "Everything is Ok"), "test7 FAIL"

    def test_step8(self, clear_folders, make_files, start_time):
        res = []
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    'cd {}; 7z h {}'.format(data['FOLDER_TST'], item), "Everything is Ok"))
            hash = ssh_getout(data["host"], data["user"], data["passwd"],
                              'cd {}; crc32 {}'.format(data['FOLDER_TST'], item)).upper()
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"],
                                    'cd {}; 7z h {}'.format(data['FOLDER_TST'], item), hash))
        self.save_log(start_time, "log_test_step8.txt")
        assert all(res), 'test 8 fail'
