from checkout import checkout_negative
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


def test_step1(make_bad_arx):
    assert checkout_negative('cd {}; 7z e badarx.{} -o{} -y'.format(data["FOLDER_OUT"], data['file_extension'], data["FOLDER_folder1"]), 'Can not open the file as [zip] archive'), 'test1 fail'

def test_step2(make_bad_arx):
    assert checkout_negative('cd {}; 7z t badarx.{}'.format(data["FOLDER_OUT"], data["file_extension"]), 'Can not open the file as [zip] archive'), 'test2 fail'

