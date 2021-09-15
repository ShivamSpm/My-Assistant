from pywinauto import application

app1 = application.Application()
class notepadAuto():

    def __init__(self):
        self.app = application.Application()

    def open(self):
        self.app.start("Notepad.exe")


    def write(self,voice_input):
        self.app.Notepad.Edit.type_keys(voice_input,with_spaces=True)


    def close(self):
        self.app.kill()