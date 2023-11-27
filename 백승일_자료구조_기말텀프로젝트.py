import tkinter as tk
from bintrees import FastRBTree  # B-트리 라이브러리

# B-트리 초기화
b_tree = FastRBTree()

# 거래처 정보를 B-트리에 추가하는 함수
def add_supplier():
    name = entry_name.get()
    contact = entry_contact.get()
    email = entry_email.get()
    address = entry_address.get()
    
    b_tree.insert(name, {'Contact': contact, 'Email': email, 'Address': address})
    update_listbox()

# 거래처 정보를 삭제하는 함수
def delete_supplier():
    selected_supplier = listbox.curselection()
    if selected_supplier:
        name = listbox.get(selected_supplier[0])
        b_tree.remove(name)
        update_listbox()

# 거래처 정보를 조회하는 함수
def view_supplier():
    selected_supplier = listbox.curselection()
    if selected_supplier:
        name = listbox.get(selected_supplier[0])
        info = b_tree.get(name)
        text_info.config(state=tk.NORMAL)
        text_info.delete(1.0, tk.END)
        text_info.insert(tk.END, f"Name: {name}\n")
        text_info.insert(tk.END, f"Contact: {info['Contact']}\n")
        text_info.insert(tk.END, f"Email: {info['Email']}\n")
        text_info.insert(tk.END, f"Address: {info['Address']}\n")
        text_info.config(state=tk.DISABLED)

# 리스트 상자 업데이트 함수
def update_listbox():
    listbox.delete(0, tk.END)
    for name in b_tree.keys():
        listbox.insert(tk.END, name)

# Tkinter GUI 생성
root = tk.Tk()
root.title("거래처 관리 프로그램")

frame_input = tk.Frame(root)
frame_input.pack()

label_name = tk.Label(frame_input, text="거래처명:")
label_name.grid(row=0, column=0)
entry_name = tk.Entry(frame_input)
entry_name.grid(row=0, column=1)

label_contact = tk.Label(frame_input, text="담당자명:")
label_contact.grid(row=1, column=0)
entry_contact = tk.Entry(frame_input)
entry_contact.grid(row=1, column=1)

label_email = tk.Label(frame_input, text="E메일:")
label_email.grid(row=2, column=0)
entry_email = tk.Entry(frame_input)
entry_email.grid(row=2, column=1)

label_address = tk.Label(frame_input, text="주소:")
label_address.grid(row=3, column=0)
entry_address = tk.Entry(frame_input)
entry_address.grid(row=3, column=1)

button_add = tk.Button(frame_input, text="추가", command=add_supplier)
button_add.grid(row=4, column=0)

button_delete = tk.Button(frame_input, text="삭제", command=delete_supplier)
button_delete.grid(row=4, column=1)

frame_display = tk.Frame(root)
frame_display.pack()

listbox = tk.Listbox(frame_display)
listbox.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(frame_display, orient=tk.VERTICAL)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox.config(yscrollcommand=scrollbar.set)

text_info = tk.Text(root, height=10, width=40)
text_info.pack()

button_view = tk.Button(root, text="조회", command=view_supplier)
button_view.pack()

root.mainloop()
