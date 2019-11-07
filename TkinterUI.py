import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class MouseOverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

class ConsciencesFWIU:
    """
    A class that can start an IU process to write, from buttons, words into python console.
    """
    __owner = "ConsciencesAI"
    __creation_date = "28/09/2019"

    def __init__(self, resolution, full_options=True, load_configuration=False):
        self.__check_resolution(resolution)
        self.full_options = full_options
        self.load_configuration = load_configuration

    def __check_resolution(self, resolution):
        """
        Check if resolution is a list or tuple of at least 2 elements.
        Args:
            resolution: A list or tuple.

        Returns:

        """
        if isinstance(resolution, (list, tuple)):
            if len(resolution) > 1:
                self.resolution = resolution
            else:
                raise ValueError("'resolution' len() has to be > 1.")
        else:
            raise TypeError("'resolution' is not type() list or tuple.")

    def start(self):
        """
        Create a IU process to write, from buttons, words into python console.

        Returns:

        """
        def center_window(win, width=None, height=None, update=False):
            """
            Make the window to be centered on the screen when it pop-up.
            Args:
                win: Window to be centered.
                width: Window width.
                height: Window heigth.
                update: In case the window resolution can't be retrieved, set this to True.

            Returns: Window position and window resolution.

            """
            if update == True:
                win.update_idletasks()
                width = win.winfo_reqwidth()
                height = win.winfo_reqheight()

            screen_width = win.winfo_screenwidth() # Get the screen resolution
            screen_height = win.winfo_screenheight()

            x = screen_width / 2 - width / 2
            y = screen_height / 2 - height / 2
            return int(x), int(y), int(width), int(height)

        def root_window():
            """
            Create the main (root) window of the UI.

            Returns: The root window.

            """
            root = tk.Tk()
            root.title("Consciences IU")
            root.minsize(270, 333)
            x, y, _, _ = center_window(root, self.resolution[0], self.resolution[1])
            root.geometry("x".join(map(str, self.resolution)) + "+" + str(x) + "+" + str(y))
            root.iconbitmap("logo_conscience.ico")
            root.config(bg="#f5f2f2")

            root.rowconfigure(1, weight=1)  # To expand row inside main window.
            root.columnconfigure(0, weight=1)  # To keep widgets in place.

            return root

        def top_frame():
            """
            Create the top frame inside the root window, where the help button is placed.

            Returns:

            """
            frame_top = tk.Frame(root, bg="#f5f2f2")
            frame_top.grid(sticky=tk.W + tk.E)
            frame_inside_top = tk.Frame(frame_top) # A blank frame.
            frame_inside_top.grid(row=0, column=0)

            def help_button():
                input_code.insert(tk.END, "\nHELP")

            photo_help = tk.PhotoImage(file=r"help1.png")
            btn_help = MouseOverButton(frame_top, image=photo_help, bg="#e3e1e1", command=help_button)
            btn_help.grid(column=1, padx=2, pady=4)
            btn_help.image = photo_help  # To keep a reference to prevent from getting it garbage-collected.

            frame_top.columnconfigure(0, weight=1)

        def middle_frame():
            """
            Create the white middle frame inside the root window. Then create a Label frame inside the white frame,
            with 2 blank frames to keep proportions.

            Returns: Return the Label frame where the different widgets are going to be placed.

            """
            white_frame_middle = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")  # White middle frame.
            white_frame_middle.grid(padx=10, sticky=tk.W + tk.E + tk.N + tk.S)
            code_label_frame = tk.LabelFrame(white_frame_middle, font=("Segoe UI", "9", "bold"), text="Code Input",
                                             bg="#ffffff", bd=1)
            code_label_frame.grid(row=0, padx=20, pady=20, sticky=tk.W + tk.E + tk.N + tk.S)
            lat_blank_frame_in_white_frame = tk.Frame(white_frame_middle,
                                                      bg="#ffffff")  # Lateral blank frame inside white middle frame.
            lat_blank_frame_in_white_frame.grid(row=0, column=1, ipadx=20)
            bot_blank_frame_in_white_frame = tk.Frame(white_frame_middle,
                                                      bg="#ffffff")  # Bottom blank frame inside white middle frame.
            bot_blank_frame_in_white_frame.grid(row=1, ipady=20)

            # Columns and rows configuration
            white_frame_middle.columnconfigure(0, weight=1)  # To expand column inside white middle frame.
            white_frame_middle.rowconfigure(0, weight=1)  # To expand row inside white middle frame.
            code_label_frame.columnconfigure(0, weight=1)  # To expand column inside LabelFrame.
            code_label_frame.rowconfigure(1, weight=1)  # To expand column inside LabelFrame.

            return code_label_frame

        def frames_in_middle_frame():
            """
            Create the frames to sort the interactive widgets inside the middle frame. Add a new frame here to sort
            each group of interactive widgets.

            Returns: options_frame, text_code_frame, wait_code_frame frames where the interactive widgets are placed.

            """
            options_frame = tk.Frame(code_label_frame, bg="#ffffff")
            options_frame.grid()
            text_code_frame = tk.Frame(code_label_frame, bg="#ffffff")  # Text code frame.
            text_code_frame.grid(sticky=tk.W + tk.E + tk.N + tk.S)
            wait_code_frame = tk.Frame(code_label_frame, bg="#ffffff")  # Wait button frame.
            wait_code_frame.grid(sticky=tk.W)

            # Columns and rows configuration
            options_frame.rowconfigure(0, weight=1)  # To expand row inside input code frame.
            options_frame.columnconfigure(0, weight=1)  # To expand column inside input code frame.
            text_code_frame.columnconfigure(0, weight=2)  # To expand column inside input code frame.
            text_code_frame.rowconfigure(0, weight=1)  # To expand row inside input code frame.
            wait_code_frame.columnconfigure(0, weight=1)  # To keep column aspect where "Waiting time:" frame is placed.
            wait_code_frame.columnconfigure(1, weight=1)  # To keep column aspect where Entry frame is placed.
            wait_code_frame.columnconfigure(2, weight=1)  # To keep column aspect where Wait button frame is placed.

            return options_frame, text_code_frame, wait_code_frame

        def middle_frame_buttons():
            """
            Define the widgets placed in the frames inside the middle frame.

            Returns: input_code, the ScrolledText to receive the input.

            """
            def options_():
                """
                Define widgets in the options frame.

                Returns:

                """
                options_Spinbox = ttk.Combobox(options_frame)
                options_Spinbox.grid(row=0, pady=10, padx=10)

                def plus_button():
                    """
                    Create a button that bring up a new window with an Entry widget to retrieve "Project's name" an two
                    buttons, "Create" and "Cancel".
                    Returns:

                    """
                    # Create the toplevel window.
                    top = tk.Toplevel(root)
                    top.title("Options")
                    top.resizable(False, False)
                    top.iconbitmap("logo_conscience.ico")
                    top.config(bg="#ffffff")

                    # Define the interactive widgets inside toplevel window.
                    project_name = tk.Label(top, text="Project's name:", font=("Segoe UI", "8", "bold"), bg="#ffffff")
                    project_name.grid(row=0, column=0, pady=10, padx=10)
                    input_project = tk.Entry(top, bg="#f5f2f2", relief="sunken")
                    input_project.grid(row=0, column=1, pady=10, padx=10)
                    input_project.focus()
                    photo_consciences = tk.PhotoImage(file=r"logo_conscience1.png")
                    image_consciences = tk.Label(top, image=photo_consciences, bg="#ffffff")
                    image_consciences.image = photo_consciences  # To keep a reference to prevent from getting it
                                                                 # garbage-collected.
                    image_consciences.grid(row=0, column=2, columnspan=2, sticky=tk.W + tk.E + tk.N + tk.S)
                    create_button = MouseOverButton(top, text="Create", font=("Segoe UI", "8"), bg="#e3e1e1")
                    create_button.grid(row=1, column=2, sticky=tk.W + tk.E + tk.N + tk.S)
                    cancel_button = MouseOverButton(top, text="Cancel", font=("Segoe UI", "8"), bg="#e3e1e1")
                    cancel_button.grid(row=1, column=3, sticky=tk.W + tk.E + tk.N + tk.S)

                    # To center the toplevel window in the screen.
                    x, y, width, height = center_window(top, update=True)
                    top.geometry('%dx%d+%d+%d' % (width, height, x, y))

                    # To disable the options button while the toplevel window is opem.
                    options_button.config(state="disable")
                    # root.
                    def exit_top():
                        top.destroy()
                        options_button.config(state='normal')

                    top.protocol("WM_DELETE_WINDOW", exit_top)

                    # # Synchronise the root window movement with the toplevel window.
                    # def sync_windows(event=None):
                    #     x = root.winfo_x() + root.winfo_width() + 4
                    #     y = root.winfo_y()
                    #     top.geometry("+%d+%d" % (x, y))
                    #
                    # root.bind("<Configure>", sync_windows)

                options_button = MouseOverButton(options_frame, font=("Segoe UI", "8"), text="+", bg="#e3e1e1",
                                                 command=plus_button)
                options_button.grid(row=0, column=1, padx=10)

            def text_():
                """
                Define widgets in the text code frame.

                Returns: input_code, the ScrolledText widget.

                """
                input_code = scrolledtext.ScrolledText(text_code_frame, bg="#f5f2f2")
                input_code.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
                input_code.focus()

                def send_button():
                    input_code.insert(tk.END, "\nSENT")

                btn_code_send = MouseOverButton(text_code_frame, font=("Segoe UI", "8"), text="Send", bg="#e3e1e1",
                                                command=send_button)
                btn_code_send.grid(row=0, column=1, padx=10)

                return input_code

            def wait_():
                """
                Define widgets in the wait code frame.

                Returns:

                """
                text_wait = tk.Label(wait_code_frame, font=("Segoe UI", "8"), text="Waiting time:", bg="#ffffff")
                text_wait.grid(row=0, column=0, padx=10, pady=30)

                txt_wait = tk.Entry(wait_code_frame, bg="#f5f2f2", relief="sunken", width=4)
                txt_wait.grid(row=0, column=1, sticky=tk.W)

                def wait_button():
                    if len(txt_wait.get()) == 0:
                        pass
                    else:
                        input_code.insert(tk.END, "\nWAIT - " + txt_wait.get())

                btn_wait = MouseOverButton(wait_code_frame, font=("Segoe UI", "8"), text="Wait", bg="#e3e1e1",
                                           command=wait_button)
                btn_wait.grid(row=0, column=2, padx=10)

            options_()
            input_code = text_()
            wait_()
            return input_code

        def botton_frame():
            """
            Create the botton frame where the "Save" and "Stop" butons are placed.

            Returns: Return the botton frame.

            """
            frame_buttons = tk.Frame(root, bg="#f5f2f2")
            frame_buttons.grid(sticky=tk.W + tk.E)
            first_blank_column = tk.Frame(frame_buttons, bg="#f5f2f2") # A blank frame.
            first_blank_column.grid(row=0, column=0)

            frame_buttons.columnconfigure(0, weight=1)  # To extend blank frame.

            return frame_buttons

        def botton_frame_buttons():
            """
            Define the buttons inside the botton_frame.

            Returns:

            """
            def save_button():
                input_code.insert(tk.END, "\nSAVE")

            def stop_button():
                input_code.insert(tk.END, "\nSTOP")

            btn_save = MouseOverButton(frame_buttons, font=("Segoe UI", "8"), text="Save", width=7, bg="#e3e1e1",
                                       command=save_button)
            btn_save.grid(row=0, column=1, padx=1, pady=8)
            btn_stop = MouseOverButton(frame_buttons, font=("Segoe UI", "8"), text="Stop", width=7, bg="#e3e1e1",
                                       command=stop_button)
            btn_stop.grid(row=0, column=2, padx=10, pady=8)

        root = root_window()
        top_frame()
        code_label_frame = middle_frame()
        options_frame, text_code_frame, wait_code_frame = frames_in_middle_frame()
        input_code = middle_frame_buttons() # Add new interactive widgets inside this function.
        frame_buttons = botton_frame()
        botton_frame_buttons()
        root.mainloop()

if __name__=="__main__":
    consci = ConsciencesFWIU((500, 500))
    consci.start()
