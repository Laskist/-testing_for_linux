from checkout import checkout, FOLDER_TST, FOLDER_OUT, FOLDER_folder1

def test_step1():
    res1 = checkout(f'cd {FOLDER_TST}; 7z a ../out/arx2', 'Everything is Ok')
    res2 = checkout(f'ls {FOLDER_OUT}', 'arx2.7z')
    assert res1 and res2, 'test1 fail'

def test_step2():
    res1 = checkout(f'cd {FOLDER_OUT}; 7z x arx2.7z -o{FOLDER_folder1} -y', 'Everything is Ok')
    res2 = checkout(f'ls {FOLDER_folder1}', 'new_test.txt')
    assert res1 and res2,'test2 fail'

def test_step3():
    assert checkout(f'cd {FOLDER_OUT}; 7z t arx2.7z', 'Everything is Ok'), 'test3 fail'

def test_step4():
    assert checkout(f'cd {FOLDER_OUT}; 7z d arx2.7z', 'Everything is Ok'), 'test4 fail'

def test_step5():
    assert checkout(f'cd {FOLDER_OUT}; 7z u arx2.7z', 'Everything is Ok'), 'test5 fail'

def test_step6():
    assert checkout(f'cd {FOLDER_OUT}; 7z l arx2.7z', '2 files'), 'test6 fail'

def test_step7():
    assert checkout(f'cd {FOLDER_OUT}; 7z h bad.7z', 'E427CCEF'), 'test7 fail'

def test_step8():
    assert checkout(f'cd {FOLDER_TST}; 7z h new_test.txt', '693C23DA'), 'test8 fail'