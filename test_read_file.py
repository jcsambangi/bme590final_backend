from read_file import read_file_data
import datetime


def test_read_file():
    with open("./test.txt", "w") as f:
        f.write("HELLO WORLD")
    assert read_file_data("./test.txt", 9307,
                          datetime.datetime.now()) == 1
    assert read_file_data("./test.txt", 9307,
                          datetime.datetime.now()) == 0
    with open("./test.txt", "w") as f:
        f.write("HI HUMANS")
        assert read_file_data("./test.txt", 9307,
                              datetime.datetime.now()) == 1


