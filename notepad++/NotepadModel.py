from os import path as p
import speech_recognition as s

class Model:
    def __init__(self):
        self.key = "abcdefghijklmnopqrstuvwxvzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.offset = 5

    def encrypt(self, plaintext):
        result = ''
        for ch in plaintext:
            try:
                i = (self.key.index(ch) + self.offset) % 62
                result += self.key[i]
            except ValueError:
                result += ch
        return result

    def decrypt(self, cipher_text):
        result = ''
        for ch in cipher_text:
            try:
                i = (self.key.index(ch) - self.offset) % 62
                result += self.key[i]
            except ValueError:
                result += ch
        return result

    def save_file(self, msz, url):
        print("Url is",url)
        if type(url) is not str:
            file = url.name
        else:
            file = url
        base = p.splitext(file)
        file_name, extension = base
        #print("File name is",file_name,"and extension is",extension)
        if extension in '.ntxt':
            msz = self.encrypt(msz)
        with open(file, "w") as f:
            f.write(msz)
            print("File saved successfully")

    def save_as(self, msz, url):
        if type(url) is not str:
            file = url.name
        else:
            file = url
        with open(file, "w") as f:
            f.write(self.encrypt(msz))
            print("File saved successfully")

    def read_file(self, path):
        base = p.basename(path) # not required. Simply we can concatenate file_name and extension
        file_name, extension = p.splitext(base)
        with open(path, "r") as f:
            file_content = f.read()
        if extension in '.ntxt':
            file_content = self.decrypt(file_content)
        return file_content,base

    def takeQuery(self):
        sr = s.Recognizer()
        sr.pause_threshold = 1

        with s.Microphone() as m:
            print("Say something:")
            sr.adjust_for_ambient_noise(m)
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            print(query)
            return query
