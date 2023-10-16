import mysql.connector
import tkinter as tk
from tkinter import messagebox

# MySQL 서버에 연결
connection = mysql.connector.connect(
    host="localhost",  # 호스트 주소
    user="root",  # MySQL 사용자명
    password="1234",  # 사용자 비밀번호
    database="correspondent_management"  # 데이터베이스명
)

cursor = connection.cursor()

# 거래처 테이블 생성 (이미 테이블이 존재하지 않을 경우)
create_table_query = """
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255),
    customer_address VARCHAR(255),
    contact_name VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(15)
)
"""
cursor.execute(create_table_query)

class Customer:
    def __init__(self, customer_name, customer_address, contact_name, contact_email, contact_phone):
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone

def add_customer():
    customer_name = customer_name_entry.get()
    customer_address = customer_address_entry.get()
    contact_name = contact_name_entry.get()
    contact_email = contact_email_entry.get()
    contact_phone = contact_phone_entry.get()

    customer = Customer(customer_name, customer_address, contact_name, contact_email, contact_phone)

    # 데이터베이스에 거래처 정보 저장
    insert_query = "INSERT INTO customers (customer_name, customer_address, contact_name, contact_email, contact_phone) VALUES (%s, %s, %s, %s, %s)"
    values = (customer.customer_name, customer.customer_address, customer.contact_name, customer.contact_email, customer.contact_phone)
    cursor.execute(insert_query, values)
    connection.commit()

    messagebox.showinfo("성공", f"{customer.customer_name}이(가) 추가되었습니다.")
def delete_customer():
    customer_name = delete_name_entry.get()
    
    try:
        cursor = connection.cursor()

        # 입력한 거래처명과 일치하는 모든 레코드 삭제
        query = "DELETE FROM customers WHERE customer_name = %s"
        cursor.execute(query, (customer_name,))
        connection.commit()
        cursor.close()
        messagebox.showinfo("성공", f"{customer_name}과 관련된 정보가 모두 삭제되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"삭제 중 오류가 발생했습니다: {str(e)}")
    
def find_customer_by_name():
    search_name = search_name_entry.get()
    query = "SELECT * FROM customers WHERE customer_name = %s"
    cursor.execute(query, (search_name,))
    customers = cursor.fetchall()

    if customers:
        result_text.delete(1.0, tk.END)  # 결과 텍스트 지우기
        result_text.insert(tk.END, f"{search_name}의 정보:\n")
        for customer in customers:
            result_text.insert(tk.END, f"거래처명: {customer[1]}\n")
            result_text.insert(tk.END, f"주소: {customer[2]}\n")
            result_text.insert(tk.END, f"담당자명: {customer[3]}\n")
            result_text.insert(tk.END, f"E메일: {customer[4]}\n")
            result_text.insert(tk.END, f"연락처: {customer[5]}\n")
            result_text.insert(tk.END, "\n")
    else:
        messagebox.showinfo("알림", f"{search_name}을 찾을 수 없습니다.")

def display_all_customers():
    query = "SELECT * FROM customers"
    cursor.execute(query)
    customers = cursor.fetchall()

    if customers:
        result_text.delete(1.0, tk.END)  # 결과 텍스트 지우기
        result_text.insert(tk.END, "전체 거래처 목록:\n")
        for customer in customers:
            result_text.insert(tk.END, f"거래처명: {customer[1]}\n")
            result_text.insert(tk.END, f"주소: {customer[2]}\n")
            result_text.insert(tk.END, f"담당자명: {customer[3]}\n")
            result_text.insert(tk.END, f"E메일: {customer[4]}\n")
            result_text.insert(tk.END, f"연락처: {customer[5]}\n")
            result_text.insert(tk.END, "\n")
    else:
        messagebox.showinfo("알림", "거래처 목록이 비어 있습니다.")


# Tkinter 창 생성
root = tk.Tk()
root.title("거래처 관리 프로그램")

# 거래처 추가 입력 폼
customer_name_label = tk.Label(root, text="거래처명")
customer_name_label.pack()
customer_name_entry = tk.Entry(root)
customer_name_entry.pack()

customer_address_label = tk.Label(root, text="주소")
customer_address_label.pack()
customer_address_entry = tk.Entry(root)
customer_address_entry.pack()

contact_name_label = tk.Label(root, text="담당자명")
contact_name_label.pack()
contact_name_entry = tk.Entry(root)
contact_name_entry.pack()

contact_email_label = tk.Label(root, text="E메일")
contact_email_label.pack()
contact_email_entry = tk.Entry(root)
contact_email_entry.pack()

contact_phone_label = tk.Label(root, text="연락처")
contact_phone_label.pack()
contact_phone_entry = tk.Entry(root)
contact_phone_entry.pack()

add_button = tk.Button(root, text="거래처 추가", command=add_customer)
add_button.pack()
# 거래처 삭제 폼
delete_name_label = tk.Label(root, text="거래처명으로 삭제")
delete_name_label.pack()
delete_name_entry = tk.Entry(root)
delete_name_entry.pack()

delete_button = tk.Button(root, text="거래처 삭제", command=delete_customer)
delete_button.pack()

# 거래처 조회 폼
search_name_label = tk.Label(root, text="거래처명으로 조회")
search_name_label.pack()
search_name_entry = tk.Entry(root)
search_name_entry.pack()

search_button = tk.Button(root, text="조회", command=find_customer_by_name)
search_button.pack()

# 전체 목록 조회
display_button = tk.Button(root, text="전체 거래처 목록 조회", command=display_all_customers)
display_button.pack()

# 조회 결과 텍스트 박스
result_text = tk.Text(root)
result_text.pack()



root.mainloop()

# MySQL 연결 닫기
cursor.close()
connection.close()
