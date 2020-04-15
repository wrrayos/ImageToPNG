import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

import os
from PIL import Image

import traceback

class MainWindow:
    lst_images = []
    def __init__(self, parent):
        self.parent = parent
        placement_x = (self.parent.winfo_screenwidth()//2) - (600//2)
        placement_y = (self.parent.winfo_screenheight()//2) - (400//2)

        self.parent.title("PNG Banzai")
        self.parent.geometry(f"600x400+{placement_x}+{placement_y}")
        self.parent.minsize(600,400)
        self.initUI()
        self.parent.grid_columnconfigure(0,weight=1)
        self.parent.grid_rowconfigure(2,weight=1)

    def initUI(self):

        ''' ========== Frame 1 | Row 1 ========== '''

        frame1 = tk.Frame(self.parent,bg="red")
        tk.Label(frame1, text="◘ ◘ ◘ PNG BANZAI ◘ ◘ ◘",
                 fg="white",
                 bg="#80bfff",
                 font="courier 18 bold").grid(row=0,column=0,columnspan=3,sticky="ew")

        ''' ========== Frame 2 | Row 2 ========== '''
        frame2 = tk.Frame(self.parent)

        self.btn_choose = ttk.Button(frame2, text="Choose Image", command=self.callback_select_images)
        self.btn_delete = ttk.Button(frame2, text="Delete", command=self.callback_delete_images)
        self.btn_clear = ttk.Button(frame2, text="Clear", command=self.callback_clear_images)

        self.btn_choose.grid(row=0, column=0, sticky="nsew")
        self.btn_delete.grid(row=0, column=1, sticky="nsew")
        self.btn_clear.grid(row=0, column=2, sticky="nsew")

        ''' ========== Frame 3 | Row 3 ========== '''

        frame3 = tk.Frame(self.parent)
        self.lst_images_xscroll = tk.Scrollbar(frame3, orient=tk.HORIZONTAL)
        self.lst_images_yscroll = tk.Scrollbar(frame3, orient=tk.VERTICAL)
        self.lstbox_images = tk.Listbox(frame3, selectmode="extended",
                                        xscrollcommand=self.lst_images_xscroll.set,
                                        yscrollcommand=self.lst_images_yscroll.set)
        self.lst_images_xscroll.configure(command=self.lstbox_images.xview)
        self.lst_images_yscroll.configure(command=self.lstbox_images.yview)

        self.lstbox_images.bind("<Double-Button-1>", self.event_open_images)

        self.lstbox_images.grid(row=0, column=0, sticky="nsew")
        self.lst_images_yscroll.grid(row=0, column=1,columnspan=2, sticky="ns")
        self.lst_images_xscroll.grid(row=1, column=0, sticky="ew")

        ''' ========== Frame 4 | Row 4 ========== '''

        frame4 = tk.Frame(self.parent)
        self.btn_convert = ttk.Button(frame4, text="Convert Image", command=self.callback_convert_images)
        self.btn_exit = tk.Button(frame4, text="x",fg="white",bg="#ff4d4d", command=self.callback_exit_images)

        self.btn_convert.grid(row=0, column=0, sticky="nsew")
        self.btn_exit.grid(row=0, column=1, sticky="nsew")

        frame1.grid(row=0, column=0, sticky="nsew")
        frame2.grid(row=1, column=0, sticky="nsew")
        frame3.grid(row=2, column=0, sticky="nsew")
        frame4.grid(row=3, column=0, sticky="nsew")

        frame3.grid_rowconfigure(0,weight=1)

        frame1.grid_columnconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame3.grid_columnconfigure(0, weight=1)
        frame4.grid_columnconfigure(0, weight=1)

    # ==================== Callback Methods ==================== #

    def callback_select_images(self):
        self.tuple_images = tk.filedialog.askopenfilenames(initialdir="C:\\", title="Choose Image/s",
                                                           filetypes=(("jpeg","*.jpg"),("gif","*.gif"),("all","*.*")))


        for image in self.tuple_images:
            self.lst_images.append(image)
            self.lstbox_images.insert(tk.END,os.path.basename(image))

    def callback_delete_images(self):
        tpl_to_delete = self.lstbox_images.curselection()
        if len(tpl_to_delete) == 0:
            messagebox.showinfo("NO SELECTED ITEM", "Please select an item to delete")
        else:
            for index in tpl_to_delete:
                del self.lst_images[index]
                self.lstbox_images.delete(index)

    def callback_clear_images(self):
        self.lst_images.clear()
        self.lstbox_images.delete(0,tk.END)

    def callback_exit_images(self):
        self.parent.destroy()

    def callback_convert_images(self):
        if len(self.lst_images) == 0:
            messagebox.showinfo("NO ITEM TO CONVERT", "Please select an image before pressing the convert button")
        else:
            directory_to_save = tk.filedialog.askdirectory()
            try:
                for item in self.lst_images:
                    obj_image = Image.open(item)
                    file_name, file_extention = os.path.splitext(os.path.basename(item))
                    obj_image.save(f"{directory_to_save}/{file_name}.png")
            except IOError as e:
                messagebox.showerror("ERROR", e)
            except Exception as e:
                messagebox.showerror("ERROR",f"Error: {traceback.print_exc()}")
            else:
                messagebox.showinfo("SUCCESS","Images have been converted to PNG successfully")
                self.lstbox_images.delete(0, tk.END)
                self.lst_images.clear()

    # ==================== Event Methods ==================== #

    def event_open_images(self, event):
        tpl_selected_image = self.lstbox_images.curselection()
        if len(tpl_selected_image) == 0:
            messagebox.showerror("ERROR","The list is empty")
        else:
            os.startfile(self.lst_images[tpl_selected_image[0]])

if __name__ == "__main__":
    app = tk.Tk()
    window = MainWindow(app)
    app.mainloop()