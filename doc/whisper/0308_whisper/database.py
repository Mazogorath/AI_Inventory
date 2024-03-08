import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

def insert_data():
    product = input("제품 이름: ")
    if product == "9999":
        update_data()
        return  # update_data 호출 후 insert_data 함수로 돌아오도록 함
    else:
        quantity = int(input("수량: "))
        location = input("위치: ")
        cursor.execute("INSERT INTO inventory (product, quantity, location) VALUES (?, ?, ?)",
                       (product, quantity, location))
        conn.commit()

def print_inventory():
    cursor.execute("SELECT rowid, * FROM inventory")
    records = cursor.fetchall()
    for row in records:
        print(f"ID: {row[0]}, 제품 이름: {row[1]}, 수량: {row[2]}, 위치: {row[3]}")

def update_data():
    print_inventory()
    record_id_input = input("수정할 항목의 ID를 입력하세요: ")
    if not record_id_input:  # 아무것도 입력하지 않은 경우
        return  # 바로 함수 종료하고 insert_data로 돌아감
    record_id = int(record_id_input)
    new_product = input("새 제품 이름: ")
    new_quantity = int(input("새 수량: "))
    new_location = input("새 위치: ")

    cursor.execute("UPDATE inventory SET product = ?, quantity = ?, location = ? WHERE rowid = ?",
                   (new_product, new_quantity, new_location, record_id))
    conn.commit()

while True:
    insert_data()
    more = input("더 입력하시겠습니까? (y/n): ").lower().strip()
    if more == 'n':
        break
    elif more == '':
        continue

print_inventory()

conn.close()
