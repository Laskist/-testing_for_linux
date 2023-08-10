from checkout import checkout, getout
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)
class TestPositive:

    def test_step1(self, make_folders, clear_folders, make_files):
        res1 = checkout('cd {}; 7z a {}/arx -t{}'.format(data['FOLDER_TST'], data['FOLDER_OUT'], data['file_extension']), 'Everything is Ok')
        res2 = checkout('ls {}'.format(data['FOLDER_OUT']), 'arx.{}'.format(data['file_extension']))
        assert res1 and res2, 'test1 fail'


    def test_step2(self, clear_folders, make_files):
        res = []
        res.append(checkout('cd {}; 7z a {}/arx -t{}'.format(data['FOLDER_TST'], data['FOLDER_OUT'], data['file_extension']), 'Everything is Ok'))
        res.append(checkout('cd {}; 7z e arx.{} -o{} -y'.format(data['FOLDER_OUT'], data['file_extension'], data['FOLDER_folder1']), 'Everything is Ok'))
        for item in make_files:
            print(item)
            res.append(checkout('ls {}'.format(data['FOLDER_folder1']), item))
        assert all(res), 'test2 fail'


    def test_step3(self):
        assert checkout('cd {}; 7z t arx.{}'.format(data['FOLDER_OUT'], data['file_extension']), 'Everything is Ok'), 'test3 fail'


    def test_step4(self):
        assert checkout('cd {}; 7z u arx.{}'.format(data['FOLDER_OUT'], data['file_extension']), 'Everything is Ok'), 'test4 fail'


    def test_step5(self, clear_folders, make_files):
        res = []
        res.append(checkout('cd {}; 7z a {}/arx -t{}'.format(data['FOLDER_TST'], data['FOLDER_OUT'], data['file_extension']), 'Everything is Ok'))
        for item in make_files:
            print(item)
            print(make_files)
            res.append(checkout('cd {}; 7z l arx.{}'.format(data['FOLDER_OUT'], data['file_extension']), item))
            print(res)
        assert all(res), 'test5 fail'


    def test_step6(self, clear_folders, make_files, make_subfolder):
        res = []
        res.append(checkout('cd {}; 7z a {}/arx -t{}'.format(data['FOLDER_TST'], data['FOLDER_OUT'], data['file_extension']), 'Everything is Ok'))
        res.append(checkout('cd {}; 7z x arx.{} -o{} -y'.format(data['FOLDER_OUT'], data['file_extension'], data['FOLDER_folder1']), 'Everything is Ok'))
        for item in make_files:
            res.append(checkout('ls {}'.format(data['FOLDER_folder1']), item))
        res.append(checkout('ls {}'.format(data['FOLDER_folder1']), make_subfolder[0]))
        res.append(checkout('ls {}/{}'.format(data['FOLDER_folder1'], make_subfolder[0]), make_subfolder[1]))
        assert all(res), 'test6 fail'


    def test_step7(self):
        assert checkout('cd {}; 7z d arx.{}'.format(data['FOLDER_OUT'], data['file_extension']), 'Everything is Ok'), 'test4 fail'


    def test_step8(self, clear_folders, make_files):
        res = []
        for item in make_files:
            res.append(checkout('cd {}; 7z h {}'.format(data['FOLDER_TST'], item), "Everything is Ok"))
            hash = getout('cd {}; crc32 {}'.format(data['FOLDER_TST'], item)).upper()
            res.append(checkout('cd {}; 7z h {}'.format(data['FOLDER_TST'], item), hash))
        assert all(res), 'test 8 fail'