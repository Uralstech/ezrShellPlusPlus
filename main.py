from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from subprocess import Popen, PIPE
from os.path import join, isfile
from tempfile import gettempdir
from os import remove, environ
from importlib.util import find_spec
environ['PYTHONUTF8'] = "1"

class Main:
    TEMP_FILE = join(gettempdir(), 'ezrShellv2TempScript.ezr')
    MAX_UNRESPONSIVE_HITS = 100

    def __init__(self):
        if not isfile('data.txt'): self.write_ezr_exe('ezrShell')
        with open('data.txt', 'r') as f: self.ezr_exe = f.read()

    def write_ezr_exe(self, new):
        with open('data.txt', 'w') as f: f.write(new)

    def start(self):
        self.root = Tk()
        self.root.title('ezrShell++')
        self.root.geometry('700x800')
        self.root.minsize(650, 400)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.initialize_ui()
        self.root.mainloop()

    def on_close(self):
        if isfile(Main.TEMP_FILE): remove(Main.TEMP_FILE)
        self.root.destroy()

    def run_code(self):
        with open(Main.TEMP_FILE, 'w', encoding='UTF-8') as f: f.write(self.text.get('0.0', END))

        command = f'{self.ezr_exe} "{Main.TEMP_FILE}"'

        self.console['state'] = 'normal'
        self.console.delete('0.0', END)
        try:
            proccess = Popen(command, encoding='UTF-8', stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
            out, err = proccess.communicate(self.input.get('0.0', END), 10)
            self.console.insert(END, f'{out}\n{err}')
        except TimeoutError:
            self.console.insert(END, 'Process timed out!')
        self.console['state'] = 'disabled'

    def clear_console(self):
        self.console['state'] = 'normal'
        self.console.delete('0.0', END)
        self.console['state'] = 'disabled'

    def set_ezr_exe(self):
        new = askstring('ezrShell++', 'Set Execution Command For ezr', initialvalue=self.ezr_exe)
        if new != None and new != self.ezr_exe:
            self.write_ezr_exe(new)
            self.ezr_exe = new

            showinfo('ezrShell++', f'Successfully set command to \'{new}\'')

    def initialize_ui(self):
        self.console = Text(self.root, wrap=WORD, bg="Black", height=10, highlightthickness=2, highlightcolor="white", fg='white', font=('Consolas', 15))
        self.console.insert('0.0', 'ezrShell++ Console')
        self.console.pack(fill="both", expand=1, side=TOP)
        self.console['state'] = 'disabled'

        self.input = Text(self.root, bg='Black', height=3, highlightthickness=1, highlightcolor='white', fg='white', insertbackground='white', font=('Consolas', 15))
        self.input.insert('0.0', 'User Input')
        self.input.pack(fill='x', expand=1, side=TOP)

        scrollbar = Scrollbar(self.root)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text = Text(self.root, wrap=NONE, bg="black", fg='light blue', insertbackground='light blue', font=('Cascadia Code', 20), yscrollcommand=scrollbar.set)
        self.text.pack(fill="both", expand=1, side=TOP)
        scrollbar.config(command=self.text.yview)

        menu = Menu(self.root)
        menu.add_command(label='Run', command=self.run_code)
        menu.add_command(label='Clear', command=self.clear_console)
        menu.add_command(label='ezr EC', command=self.set_ezr_exe)
        self.root.config(menu=menu)

        self.root.bind('<Control-r>', lambda _: self.clear_console())
        self.root.bind('<F5>', lambda _: self.run_code())
        
        if '_PYIBoot_SPLASH' in environ and find_spec("pyi_splash"):
            from pyi_splash import close
            close()

def main():
    Main().start()

if __name__ == '__main__': main()