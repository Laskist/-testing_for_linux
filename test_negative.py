from checkout import checkout, FOLDER_TST, FOLDER_OUT, FOLDER_folder1

def test_step1():
    assert checkout(f'cd {FOLDER_OUT}; 7z e bad.7z -o{FOLDER_folder1} -y', 'Can not open the file as [7z] archive'), 'test1 fail'

def test_step2():
    assert checkout(f'cd {FOLDER_OUT}; 7z t bad.7z', 'Can not open the file as [7z] archive'), 'test2 fail'