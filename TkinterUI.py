import tkinter as tk
from tkinter import scrolledtext

class ConsciencesFWIU:
    """
    A class that can start an IU process to write, from buttons, words into python console.
    """
    __owner = "ConsciencesAI"
    __creation_date = "28/09/2019"

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

    def __init__(self, resolution, full_options=True, load_configuration=False):
        ConsciencesFWIU.__check_resolution(self, resolution)
        self.full_options = full_options
        self.load_configuration = load_configuration

    def start(self):
        # Main Window
        root = tk.Tk()
        root.title("Consciences IU")
        root.geometry("x".join(map(str, self.resolution)))
        #root.resizable(False,False) # Disable window resize.
        root.iconbitmap("logo_conscience.ico")
        root.config(bg="#f5f2f2")


        # Help Frames
        frame_top = tk.Frame(root, bg="#f5f2f2")
        frame_top.grid(row=0, column=0, sticky=tk.W + tk.E)
        frame_inside_top = tk.Frame(frame_top) # A blank frame.
        frame_inside_top.grid(row=0, column=0)

        photo = tk.PhotoImage(file=r"help1.png")
        btn_help = tk.Button(frame_top, image=photo)
        btn_help.grid(column=1, row=0, padx=2, pady=4)
        btn_help.image = photo  # To keep a reference.

        # root.columnconfigure(0, weight=1)
        frame_top.columnconfigure(0, weight=1)

        # Middle Frame
        frame_middle = tk.Frame(root, bg="#ffffff", bd=2, relief="groove") # White middle frame.
        frame_middle.grid(row=1, column=0, padx=10, sticky=tk.W + tk.E + tk.N + tk.S)
        frame_inside_middle = tk.LabelFrame(frame_middle, font=("Segoe UI", "9", "bold"), text="Code Input",
                                            bg="#ffffff", bd=1)
        frame_inside_middle.grid(row=0, column=0, padx=20, pady=20, sticky=tk.W + tk.E + tk.N + tk.S)
        frame_in_inside_middle1 = tk.Frame(frame_inside_middle, bg="#ffffff") # Text code frame.
        frame_in_inside_middle1.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S)
        frame_in_inside_middle2 = tk.Frame(frame_inside_middle, bg="#ffffff") # Wait button frame.
        frame_in_inside_middle2.grid(row=1, column=0, sticky=tk.W)
        frame_inside_middle_1 = tk.Frame(frame_middle, bg="#ffffff") # Lateral blank frame inside white middle frame.
        frame_inside_middle_1.grid(row=0, column=1, ipadx=30)
        frame_inside_middle_2 = tk.Frame(frame_middle, bg="#ffffff") # Bottom blank frame inside white middle frame.
        frame_inside_middle_2.grid(row=1, column=0, ipady=30)

        input_code = scrolledtext.ScrolledText(frame_in_inside_middle1, bg="#f5f2f2")
        input_code.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E + tk.W + tk.N + tk.S)
        input_code.focus()
        btn_code_send = tk.Button(frame_in_inside_middle1, font=("Segoe UI", "8"), text="Send")
        btn_code_send.grid(row=0, column=1, padx=10)

        text_wait = tk.Label(frame_in_inside_middle2, font=("Segoe UI", "8"), text="Waiting time:", bg="#ffffff")
        text_wait.grid(row=0, column=0, padx=10, pady=30)
        txt_wait = tk.Entry(frame_in_inside_middle2, bg="#f5f2f2", relief="sunken", width=4)
        txt_wait.grid(row=0, column=1, sticky=tk.W)
        btn_wait =tk.Button(frame_in_inside_middle2, font=("Segoe UI", "8"), text="Wait")
        btn_wait.grid(row=0, column=2, padx=10)

        root.rowconfigure(1, weight=1)  # To extend row inside main window.
        frame_middle.columnconfigure(0, weight=1) # To extend column inside white middle frame.
        frame_middle.rowconfigure(0, weight=1) # To extend row inside white middle frame.
        frame_inside_middle.columnconfigure(0, weight=1) # To extend column inside LabelFrame.
        frame_inside_middle.rowconfigure(0, weight=1) # To extend column inside LabelFrame.
        frame_in_inside_middle1.columnconfigure(0, weight=1) # To extend column inside input code frame.
        frame_in_inside_middle1.rowconfigure(0, weight=1) # To extend row inside input code frame.

        # Buttons Frame
        frame_buttons = tk.Frame(root, bg="#f5f2f2")
        frame_buttons.grid(row=2, column=0, sticky=tk.W + tk.E)
        frame_inside_buttons = tk.Frame(frame_buttons, bg="#f5f2f2") # A blank frame.
        frame_inside_buttons.grid(row=0, column=0)

        btn_save = tk.Button(frame_buttons, font=("Segoe UI", "8"), text="SAVE", width=7)
        btn_save.grid(row=0, column=1, padx=1, pady=8)
        btn_stop = tk.Button(frame_buttons, font=("Segoe UI", "8"), text="STOP", width=7)
        btn_stop.grid(row=0, column=2, padx=10, pady=8)

        root.columnconfigure(0, weight=1) # To keep widgets in place.
        frame_buttons.columnconfigure(0, weight=1) # To extend blank frame.

        root.mainloop()

if __name__=="__main__":
    consci = ConsciencesFWIU((500, 500))
    consci.start()