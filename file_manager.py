# coding: utf-8
import os
import subprocess

class File_manager:
    def __init__(self, file_name = '', prefixe = '', extension = '.txt'):
        self.file_name = file_name
        if self.file_name != '':
            print('[FM] Using custom file '+file_name)
            if self.check(return_value = True):
                print('[FM] File found')
            else:
                print('[FM] File not found')
        self.prefixe = prefixe
        self.extension = extension

    def new_file(self, prefixe = ''):
        if self.file_name == '':
            n, i = self.find_last_file()
            i += 1
            self.file_name = self.gen_name(i)
        print('[FM] Creating a new file with name '+self.file_name)
        try:
            subprocess.call(['touch', self.file_name])
        except TypeError:
            raise ValueError('[FM] Problem with the command')

        if not os.path.isfile(self.file_name):
            raise ValueError('[FM] Problem creating the file')
        print('[FM] Created a new file : '+self.file_name)


    def last_simulation(self):
        n, i =  self.find_last_file()
        if i == -1:
            raise ValueError('[FM] No simulations yet')
        else:
            self.file_name = n
            print('[FM] Opening last simulation : '+self.file_name)

    def find_last_file(self):
        i = 0
        name = self.gen_name(i)
        while os.path.isfile(name):
            i += 1
            name = self.gen_name(i)
        i -= 1
        name = self.gen_name(i)

        return name, i

    def check(self, return_value = False):
        if not os.path.isfile(self.file_name):
            if not return_value:
                self.new_file(self.prefixe)
            else:
                return False
        elif not return_value:
            return True

    def read(self):
        self.check()

        raw = open(self.file_name, 'r')
        return_value = raw.read()
        raw.close()
        return return_value

    def readlines(self):
        self.check()

        raw = open(self.file_name, 'r')
        return_value = raw.readlines()
        raw.close()
        return return_value

    def write(self, content=''):
        self.check()

        self.file = open(self.file_name, 'a')
        self.file.write(content)
        self.file.close()

    def new_line(self, number = 1):
        self.check()

        self.write('\n'*number)

    def reset_file(self):
        if not os.path.isfile(self.file_name):
            self.new_file()
        with open(self.file_name, 'w'):
            pass
        print('[FM] File '+self.file_name+' has been resetted')

    def gen_name(self, argument = ''):
        return str(self.prefixe)+str(argument)+str(self.extension)
