import tkinter as tk
from tkinter import *
import compiler
compilerInstance = compiler.Compiler()
hiraganalist = compilerInstance.retrievehiraganaphrases()
import os

def unique_filename(base_name,extension):
    counter = 1
    new_filename = f"{base_name}{extension}"
    while os.path.exists(new_filename):
        new_filename = f"{base_name}({counter}){extension}"
        counter += 1
    return new_filename

def button_click():
    contents = code_text.get("1.0",tk.END)
    feedback,comments,errors = compilerInstance.compile(contents,True)
    for raw_comment in comments:
        output_Text.insert("1.0", str(raw_comment))

    for error in errors:
        output_Text.insert("1.0", str(error))

def clear():
    code_text.delete(1.0, tk.END)
    output_Text.delete(1.0, tk.END)

def store_code():
    newfilename = unique_filename("貯めるをファイル",".jal")
    with open(newfilename, "w", encoding="utf-8") as f:
      code_contents = code_text.get("1.0", tk.END)
      f.write(code_contents)

root = Tk()
root.geometry("800x500")
root.iconbitmap("icon.ico")
root.title("テスト")
root.resizable(False, False)
main_frame = Frame(root,width=900, height=350,background="#fa4f46",relief="sunken",bd=5)
main_frame.pack_propagate(False)
main_frame.pack(padx=20,pady=20)
main_frame.place(x=-10,y=-20)

borderleftframe = Frame(root,width=30, height=500,background="#fa4f46")
borderleftframe.pack()
borderleftframe.place(x = -3,y = 325)

borderrightframe = Frame(root,width=30, height=500,background="#fa4f46")
borderrightframe.pack()
borderrightframe.place(x = 775,y = 325)

borderbottomframe = Frame(root,width=800, height=20,background="#fa4f46")
borderbottomframe.pack()
borderbottomframe.place(x = 1,y = 480)

borderframe = Frame(root,width=820, height=25,background="#fa4f46")
borderframe.pack()
borderframe.place(x = -3,y = 325)

bottomframe = Frame(root,width=750, height=130,background="#ffffff",relief="sunken",bd=5,bg="white")
bottomframe.pack()
bottomframe.place(x = 25,y = 350)

executor_button = Button(root, text ="実行",command=button_click,height = 1, width = 10,background="#ffffff")
executor_button.place(x = 430,y = 318)

executor_button = Button(root, text ="クリア",command=clear,height = 1, width = 10,background="#ffffff")
executor_button.place(x = 320,y = 318)

executor_button = Button(root, text ="貯める",command=store_code,height = 1, width = 10,background="#ffffff")
executor_button.place(x = 85,y = 318)

output_Text = tk.Text(root,width=82, height=7,relief="sunken",bd=7,font=("Arial", 12),wrap=tk.WORD)
output_Text.place(x = 25,y = 350)

code_text = tk.Text(root,width=70, height=9,relief="sunken",bd=7,font=("Arial", 12),wrap=tk.WORD)
code_text.place(x=80,y=130)

scrollbar = tk.Scrollbar(root, command=code_text.yview,background="#ffffff")
scrollbar.place(x=705, y=134, height=170)
code_text.config(yscrollcommand=scrollbar.set)

code_text.tag_configure("もし", foreground="#bd5500")
code_text.tag_configure("何ら", foreground="#9c9c9c")
code_text.tag_configure("表示", foreground="#0032ba")
code_text.tag_configure("数", foreground="#3aa600")
code_text.tag_configure("err", foreground="#E4080A")

root.mainloop()