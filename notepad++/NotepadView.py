import tkinter as tk
from tkinter import ttk
from tkinter import font, colorchooser, messagebox, filedialog
import NotepadController
import traceback


class Notepad:
    def __init__(self, root):
        self.root = root
        self.url = ''
        self.text_changed = False
        self.show_status_bar = tk.BooleanVar()
        self.show_status_bar.set(True)
        self.show_toolbar = tk.BooleanVar()
        self.show_toolbar.set(True)
        self.notepadController = NotepadController.Controller()
        self.root.geometry('1200x800')
        self.root.title('MyNotePad')
        self.root.wm_iconbitmap('icons/icon.ico')
        self.set_icons()
        self.set_menu_bar()
        self.set_file_sub_menu()
        self.set_edit_sub_menu()
        self.set_view_sub_menu()
        self.set_color_sub_menu()
        self.set_tool_bar()
        self.set_canvas()
        self.set_status_bar()
        self.set_file_menu_event_bindings()
        self.set_tool_bar_event_bindings()
        self.root.protocol("WM_DELETE_WINDOW", self.exit_func)
        self.characters = 0
        self.words = 0
        self.change_font()

    def set_icons(self):
        self.new_icon = tk.PhotoImage(file='icons/new.png')
        self.open_icon = tk.PhotoImage(file='icons/open.png')
        self.save_icon = tk.PhotoImage(file='icons/save.png')
        self.save_as_icon = tk.PhotoImage(file='icons/save_as.png')
        self.exit_icon = tk.PhotoImage(file='icons/exit.png')
        self.copy_icon = tk.PhotoImage(file='icons/copy.png')
        self.paste_icon = tk.PhotoImage(file='icons/paste.png')
        self.cut_icon = tk.PhotoImage(file='icons/cut.png')
        self.clear_all_icon = tk.PhotoImage(file='icons/clear_all.png')
        self.find_icon = tk.PhotoImage(file='icons/find.png')
        self.tool_bar_icon = tk.PhotoImage(file='icons/tool_bar.png')
        self.status_bar_icon = tk.PhotoImage(file='icons/status_bar.png')
        self.light_default_icon = tk.PhotoImage(file='icons/light_default.png')
        self.light_plus_icon = tk.PhotoImage(file='icons/light_plus.png')
        self.dark_icon = tk.PhotoImage(file='icons/dark.png')
        self.red_icon = tk.PhotoImage(file='icons/red.png')
        self.monokai_icon = tk.PhotoImage(file='icons/monokai.png')
        self.night_blue_icon = tk.PhotoImage(file='icons/night_blue.png')

    def set_menu_bar(self):
        self.menu_bar = tk.Menu()
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.color_theme = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.menu_bar.add_cascade(label="Color Theme", menu=self.color_theme)
        self.root.config(menu=self.menu_bar)

    def set_file_sub_menu(self):
        self.file_menu.add_command(label='New', image=self.new_icon, compound=tk.LEFT, accelerator='Ctrl+N',
                                   command=self.new_file)
        self.file_menu.add_command(label='Open', image=self.open_icon, compound=tk.LEFT, accelerator='Ctrl+O',
                                   command=self.open_file)
        self.file_menu.add_command(label='Save', image=self.save_icon, compound=tk.LEFT, accelerator='Ctrl+S',
                                   command=self.save_file)
        self.file_menu.add_command(label='Save As', image=self.save_as_icon, compound=tk.LEFT, accelerator='Alt+S',
                                   command=self.save_as)
        self.file_menu.add_command(label='Exit', image=self.exit_icon, compound=tk.LEFT, accelerator='Ctrl+Q',
                                   command=self.exit_func)

    def set_edit_sub_menu(self):
        self.edit_menu.add_command(label='Copy', image=self.copy_icon, compound=tk.LEFT, accelerator='Ctrl-C',
                                   command=lambda: self.text_editor.event_generate("<<Copy>>"))
        self.edit_menu.add_command(label='Paste', image=self.paste_icon, compound=tk.LEFT, accelerator='Ctrl-V',
                                   command=lambda: self.text_editor.event_generate("<<Paste>>"))
        self.edit_menu.add_command(label='Cut', image=self.cut_icon, compound=tk.LEFT, accelerator='Ctrl-X',
                                   command=lambda: self.text_editor.event_generate("<<Cut>>"))
        self.edit_menu.add_command(label='Clear All', image=self.clear_all_icon, compound=tk.LEFT, accelerator='Alt-X',
                                   command=lambda: self.text_editor.delete(1.0, tk.END))
        self.edit_menu.add_command(label='Find', image=self.find_icon, compound=tk.LEFT, accelerator='Ctrl-F',
                                   command=self.find_func)

    def set_view_sub_menu(self):
        self.view_menu.add_checkbutton(label='Tool Bar', onvalue=True, offvalue=False, variable=self.show_toolbar,
                                  image=self.tool_bar_icon, compound=tk.LEFT, command=self.hide_toolbar)
        self.view_menu.add_checkbutton(label='Status Bar', onvalue=True, offvalue=False, variable=self.show_status_bar,
                                  image=self.status_bar_icon, compound=tk.LEFT, command=self.hide_status_bar)

    def hide_status_bar(self):
        if self.show_status_bar:
            self.status_bar.pack_forget()
            self.show_status_bar = False
        else:
            self.status_bar.pack(side=tk.BOTTOM)
            self.show_status_bar = True

    def hide_toolbar(self):
        if self.show_toolbar:
            self.tool_bar.pack_forget()
            self.show_toolbar = False
        else:
            self.text_editor.pack_forget()
            self.status_bar.pack_forget()
            self.tool_bar.pack(side=tk.TOP, fill=tk.X)
            self.text_editor.pack(fill=tk.BOTH, expand=True)
            self.status_bar.pack(side=tk.BOTTOM)
            self.show_toolbar = True

    def new_file(self, e=None):
        if self.text_editor.get(1.0, "end-1c") != '':
            self.save_as()
        self.url = ''
        self.text_editor.insert(1.0, '')
        self.root.title("MyNotepad")

    def open_file(self, e=None):
        if self.url != '' and self.text_editor.get(1.0, "end-1c") != '':
            ans = messagebox.askyesnocancel(title="MyNotepad", message="Do you want to save?")
            if ans == True:
                self.save_as()
            elif ans == None:
                return
        try:
            self.url = filedialog.askopenfilename(title="Select file", filetypes=[("All Files", "*.*")])
            if self.url == '':
                return
            self.msz, self.base = self.notepadController.read_file(self.url)
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, self.msz)
            self.root.title(self.base + "-MyNotePad")
            self.text_editor.edit_modified(False)
        except FileNotFoundError:
            messagebox.showerror("Error!", "Please select a file to read")
            print(traceback.format_exc())

    def save_dialog(self):
        self.url = filedialog.asksaveasfile(mode='w', defaultextension='.ntxt', filetypes=[("All Files", "*.*"), (
            "Text Documents", "*.txt")])  # this function itself  creates a file.

        # print("url value is ", self.url)

    def save_file(self, e=None):
        # end-1c jo aakhri character text ne add kiya tha wo delete kar dega
        plain_text = self.text_editor.get(1.0, "end-1c")
        try:
            if self.url == '':
                self.save_dialog()
            if self.url == None:
                self.url = ''
                return
            print(self.url, plain_text)
            self.notepadController.save_file(plain_text, self.url)
            self.text_changed = False
            print("after text changed")
        except Exception:
            messagebox.showerror("Error!", "Please select a file to save")
            print(traceback.format_exc())

    def save_as_dialog(self):
        self.url = filedialog.asksaveasfile(mode='w', defaultextension='.ntxt',
                                            filetypes=[(".ntxt", "*.ntxt"), ("All Files", "*.*"),
                                                       ("Text Documents", "*.txt")])

    def save_as(self, e=None):
        plain_text = self.text_editor.get(1.0, "end-1c")
        try:
            self.save_as_dialog()
            if self.url == None:
                self.url = ''
                return
            self.notepadController.save_as(plain_text, self.url)
            self.text_changed = False
        except:
            messagebox.showerror("Error!", "Please insert the name of the file to save")
            print(traceback.format_exc())


    def find_func(self, e=None):
        self.find_dialogue = tk.Toplevel()
        self.find_dialogue.geometry('450x250+500+200')
        self.find_dialogue.title('Find')
        self.find_dialogue.resizable(0, 0)

        # Frame
        self.find_frame = ttk.LabelFrame(self.find_dialogue, text='Find/Replace')
        self.find_frame.pack(pady=20)

        # lables
        self.text_find_label = ttk.Label(self.find_frame, text='Find : ')
        self.text_replace_label = ttk.Label(self.find_frame, text= 'Replace')

        # entry
        self.find_input = ttk.Entry(self.find_frame, width=30)
        self.text_replace_input = ttk.Entry(self.find_frame, width=30)
        self.find_input.focus_set()
        # button
        self.find_button = ttk.Button(self.find_frame, text='Find', command=self.find)
        self.replace_button = ttk.Button(self.find_frame, text='Replace', command=self.replace)

        # label grid
        self.text_find_label.grid(row=0, column=0, padx=4, pady=4)
        self.text_replace_label.grid(row=1, column=0, padx=4, pady=4)

        # entry grid
        self.find_input.grid(row=0, column=1, padx=4, pady=4)
        self.text_replace_input.grid(row=1, column=1, padx=4, pady=4)

        #button grid
        self.find_button.grid(row=2, column=0, padx=8, pady=4)
        self.replace_button.grid(row=2, column=1, padx=8, pady=4)

        self.find_dialogue.mainloop()

    def find(self):
        text_to_search = self.find_input.get()
        self.text_editor.tag_remove('match', '1.0', tk.END)
        matches = 0
        if text_to_search :
            first_pos = '1.0'
            while True:
                first_pos=self.text_editor.search(text_to_search, first_pos, stopindex=tk.END)
                if not first_pos:
                    break
                last_pos = f'{first_pos}+{len(text_to_search)}c'
                self.text_editor.tag_add("match", first_pos, last_pos)
                matches +=1
                first_pos = last_pos
                self.text_editor.tag_config("match", background="yellow", foreground="black")
            if matches:
                messagebox.showinfo("Match found", f'{text_to_search} occurs {matches} times')

    def replace(self):
        text_to_search = self.find_input.get()
        text_to_replace =  self.text_replace_input.get()
        self.all_text = self.text_editor.get(1.0, "end-1c")
        # text_to_search:
        #   first_pos = '1.0'
        self.new_text = self.all_text.replace(text_to_search,text_to_replace)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, self.new_text)

    def set_tool_bar(self):
        self.tool_bar = ttk.Label(root)
        self.tool_bar.pack(side= tk.TOP, fill= tk.X)

        self.font_tuple = tk.font.families()
        self.font_family = tk.StringVar()
        self.font_box = ttk.Combobox(self.tool_bar, width=30, textvariable=self.font_family, state='readonly', values=self.font_tuple)
        self.font_box.current(self.font_tuple.index('Arial'))
        self.font_box.grid(row=0, column=0, padx=5)

        self.size_var = tk.IntVar()
        self.font_size_box = ttk.Combobox(self.tool_bar, width=14, textvariable=self.size_var, state='readonly')
        self.font_size_box['values'] = tuple(range(8,81))
        self.font_size_box.current(4)
        self.font_size_box.grid(row=0, column=1, padx=5)

        self.bold_icon = tk.PhotoImage(file='icons/bold.png')
        self.bold_btn = ttk.Button(self.tool_bar, image= self.bold_icon)
        self.bold_btn.grid(row=0, column=2, padx=5)

        self.italic_icon = tk.PhotoImage(file='icons/italic.png')
        self.italic_btn = ttk.Button(self.tool_bar, image=self.italic_icon)
        self.italic_btn.grid(row=0, column=3, padx=5)

        self.underline_icon = tk.PhotoImage(file='icons/underline.png')
        self.underline_btn = ttk.Button(self.tool_bar, image=self.underline_icon)
        self.underline_btn.grid(row=0, column=4, padx=5)

        self.font_color_icon = tk.PhotoImage(file='icons/font_color.png')
        self.font_color_btn = ttk.Button(self.tool_bar, image=self.font_color_icon)
        self.font_color_btn.grid(row=0, column=5, padx=5)

        self.align_left_icon = tk.PhotoImage(file='icons/align_left.png')
        self.align_left_btn = ttk.Button(self.tool_bar, image=self.align_left_icon)
        self.align_left_btn.grid(row=0, column=6, padx=5)

        self.align_center_icon = tk.PhotoImage(file='icons/align_center.png')
        self.align_center_btn = ttk.Button(self.tool_bar, image=self.align_center_icon)
        self.align_center_btn.grid(row=0, column=7, padx=5)

        self.align_right_icon = tk.PhotoImage(file='icons/align_right.png')
        self.align_right_btn = ttk.Button(self.tool_bar, image=self.align_right_icon)
        self.align_right_btn.grid(row=0, column=8, padx=5)

        self.mike_icon = tk.PhotoImage(file='icons/microphone.png')
        self.mike_btn = ttk.Button(self.tool_bar, image=self.mike_icon)
        self.mike_btn.grid(row=0, column=9, padx=5)

    def set_tool_bar_event_bindings(self):
        self.current_font_family = 'Arial'
        self.current_font_size = 12
        self.font_box.bind("<<ComboboxSelected>>", self.change_font)
        self.font_size_box.bind("<<ComboboxSelected>>", self.change_fontsize)
        self.bold_btn.configure(command=self.change_bold)
        self.italic_btn.configure(command=self.change_italic)
        self.underline_btn.configure(command=self.change_underline)
        self.font_color_btn.configure(command=self.change_font_color)
        self.align_right_btn.configure(command=self.align_right)
        self.align_center_btn.configure(command=self.align_center)
        self.align_left_btn.configure(command=self.align_left)
        self.mike_btn.configure(command=self.saySomething)

    def change_font(self, e=None):
        self.current_font_family = self.font_family.get()
        self.text_editor.configure(font=(self.current_font_family, self.current_font_size))

    def change_fontsize(self, e=None):
        self.current_font_size = self.size_var.get()
        self.text_editor.configure(font=(self.current_font_family, self.current_font_size))

    def change_bold(self, e=None):
        self.text_property = tk.font.Font(font=self.text_editor['font'])
        if self.text_property['weight'] == 'normal':
            self.text_editor.configure(font=(self.current_font_family,self.current_font_size,'bold'))
        else:
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'normal'))

    def change_italic(self, e=None):
        self.text_property = tk.font.Font(font=self.text_editor['font'])
        if self.text_property['slant'] == 'roman':
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'italic'))
        else:
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'roman'))

    def change_underline(self, e=None):
        self.text_property = tk.font.Font(font=self.text_editor['font'])
        if self.text_property['underline'] == 0:
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'underline'))
        else:
            self.text_editor.configure(font=(self.current_font_family, self.current_font_size, 'normal'))


    def change_font_color(self, e=None):
        color_var = tk.colorchooser.askcolor()
        self.text_editor.configure(fg=color_var[1])

    def align_right(self, e=None):
        text_content = self.text_editor.get(1.0, 'end')
        self.text_editor.tag_config('right', justify=tk.RIGHT)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, 'right')
        self.text_editor.focus_set()

    def align_left(self, e=None):
        text_content = self.text_editor.get(1.0, 'end')
        self.text_editor.tag_config('left', justify=tk.LEFT)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, 'left')
        self.text_editor.focus_set()

    def align_center(self, e=None):
        text_content = self.text_editor.get(1.0, 'end')
        self.text_editor.tag_config('center', justify=tk.CENTER)
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(tk.INSERT, text_content, 'center')
        self.text_editor.focus_set()

    def set_color_sub_menu(self):
        self.count =0
        self.theme_choice = tk.StringVar()
        self.color_icons = (self.light_default_icon, self.light_plus_icon, self.dark_icon, self.red_icon, self.monokai_icon,
                        self.night_blue_icon)
        self.color_dict = {'Light Default ': ('#000000', '#ffffff'), 'Light Plus': ('#474747', '#e0e0e0'),
                       'Dark': ('#c4c4c4', '#2d2d2d'), 'Red': ('#2d2d2d', '#ffe8e8'), 'Monokai': ('#d3b774', '#474747'),
                       'Night Blue': ('#ededed', '#6b9dc2')}
        for i in self.color_dict:
            self.color_theme.add_radiobutton(label=i, image=self.color_icons[self.count],
                                                               variable=self.theme_choice, compound=tk.LEFT,
                                                               command=self.change_theme)
            self.count += 1

    def change_theme(self):
        theme_name=self.theme_choice.get()
        self.text_editor.config(background=self.color_dict[theme_name][1],foreground=self.color_dict[theme_name][0])

    def saySomething(self, e=None):
        try:
            self.takeAudio = self.notepadController.saysomeThing()
            if self.takeAudio == "":
                messagebox.showinfo("say again", "speech not recognized!!")
            elif self.takeAudio == "open file":
                self.open_file()
            elif self.takeAudio == "save file":
                self.save_file()
            elif self.takeAudio == "new file":
                self.new_file()
            elif self.takeAudio == "file save":
                self.save_file()
            elif self.takeAudio == "close app":
                self.exit_func()
            elif self.takeAudio == "text bold":
                self.change_bold()
            elif self.takeAudio == "text italic":
                self.change_italic()
            elif self.takeAudio == "text underline":
                self.change_underline()
            elif self.takeAudio == "search":
                self.find_func()
            elif self.takeAudio == "hide statusbar":
                self.hide_status_bar()
            elif self.takeAudio == "hide toolbar":
                self.hide_toolbar()
            else:
                messagebox.showerror("Error", "Audio not matched")
        except Exception:
            messagebox.showerror("Error", "Some problem in device")
            print(traceback.format_exc())

    def set_canvas(self):
        self.text_editor = tk.Text(self.root)
        #self.text_font = tk.font.Font(family='Arial')
        #self.text_editor.config(font=self.text_font)
        self.text_editor.config(wrap='word', relief=tk.FLAT)
        self.text_editor.focus_set()
        self.scroll_bar = tk.Scrollbar(self.root)
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_editor.pack(fill=tk.BOTH, expand=True)
        self.scroll_bar.config(command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=self.scroll_bar.set)
        self.text_changed = False
        self.text_editor.bind('<<Modified>>', self.changed)

    def changed(self, e=None):
        content = self.text_editor.get(1.0, "end-1c").split()
        self.words = len(content)
        self.characters = len(self.text_editor.get(1.0, "end-1c"))
        self.status_bar.config(text=f" Status Bar   Characters  {self.characters}  Words  {self.words} ")
        if self.text_editor.edit_modified():
            self.text_changed = True
        self.text_editor.edit_modified(False)

    def set_status_bar(self):
        self.status = 'Status Bar'
        self.status_bar = ttk.Label(self.root, text=self.status)
        self.status_bar.pack(side=tk.BOTTOM)
        self.count = 0

    def set_file_menu_event_bindings(self):
        self.root.bind("<Control-n>", self.new_file)
        self.root.bind("<Control-N>", self.new_file)
        self.root.bind("<Control-o>", self.open_file)
        self.root.bind("<Control-O>", self.open_file)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-S>", self.save_file)
        self.root.bind("<Alt-s>", self.save_as)
        self.root.bind("<Alt-S>", self.save_as)
        self.root.bind("<Control-q>", self.exit_func)
        self.root.bind("<Control-Q>", self.exit_func)
        self.root.bind("<Control-C>", self.text_editor.event_generate("<<Copy>>"))
        self.root.bind("<Control-c>", self.text_editor.event_generate("<<Copy>>"))
        self.root.bind("<Control-X>", self.text_editor.event_generate("<<Cut>>"))
        self.root.bind("<Control-x>", self.text_editor.event_generate("<<Cut>>"))
        self.root.bind("<Control-V>", self.text_editor.event_generate("<<Paste>>"))
        self.root.bind("<Control-v>", self.text_editor.event_generate("<<Paste>>"))
        self.root.bind("<Alt-X>", self.text_editor.delete(1.0, tk.END))
        self.root.bind("<Alt-x>", self.text_editor.delete(1.0, tk.END))
        self.root.bind("<Control-F>", self.find_func)
        self.root.bind("<Control-f>", self.find_func)
        #self.root.bind("<Enter>", self.find)
        #self.root.bind("<Enter>", self.replace)
        #self.root.bind("<Control-A>", self.select)
        #self.root.bind("<Control-a>", self.text_editor.event_generate("<<SelectNextWord>>"))

    def select(self, e=None):
        self.text_editor.tag_add("match", "1.0", "end-1c")
        self.text_editor.tag_config("match", background="yellow", foreground="white")


    def exit_func(self, event=None):
        result = messagebox.askyesno("Cool", "Do you want to quit?")
        if result == False:
            return
        try:
            if self.url == '':
                if len(self.text_editor.get("1.0", 'end-1c')) == 0:
                    self.text_changed = False
            if self.text_changed:
                mbox = messagebox.askyesnocancel('Warning', 'Do you want to save file ?')
                if mbox == None:
                    return
                if mbox == True:
                    content = self.text_editor.get(1.0, 'end-1c')
                    if self.url == '':
                        self.save_dialog()
                        self.notepadController.save_file(content, self.url)
                    else:
                        self.notepadController.save_file(content, self.url)
            messagebox.showinfo("Have a good day!", "Thank you for using \"MyNotePad\" ")
            self.root.destroy()

        except:
            messagebox.showerror("Error!", "Please Select File to Save")
            print(traceback.format_exc())

    def run(self):
        self.root.mainloop()


root = tk.Tk()
obj = Notepad(root)
obj.run()
