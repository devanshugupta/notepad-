import NotepadModel


class Controller:
    def __init__(self):
        self.model = NotepadModel.Model()

    def save_file(self, msz, url):
        self.model.save_file(msz, url)

    def save_as(self, msz, url):
        self.model.save_as(msz, url)

    def read_file(self, path):
        file_content, file = self.model.read_file(path)
        return file_content, file

    def saysomeThing(self):
        self.takeAudio = self.model.takeQuery()
        return self.takeAudio

##c = Controller()
##c.saysomeThing()