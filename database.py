import sqlite3

conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

def insert_data():
    product = input("제품 이름: ")
    if product == "9999":
        update_data()
        return
    elif product == "8888":
        delete_data()
        return
    else:
        quantity = int(input("수량: "))
        location = input("위치: ")
        uid = input("UID: ")  # 사용자로부터 UID 입력 받음
        cursor.execute("INSERT INTO inventory (product, quantity, location, uid) VALUES (?, ?, ?, ?)",
                       (product, quantity, location, uid))
        conn.commit()

def print_inventory():
    cursor.execute("SELECT rowid, * FROM inventory")
    records = cursor.fetchall()
    for row in records:
        print(f"ID: {row[0]}, 제품 이름: {row[1]}, 수량: {row[2]}, 위치: {row[3]}, UID: {row[4]}")  # UID 출력 추가

def update_data():
    print_inventory()
    record_id_input = input("수정할 항목의 ID를 입력하세요: ")
    if not record_id_input:
        return
    record_id = int(record_id_input)
    new_product = input("새 제품 이름: ")
    new_quantity = int(input("새 수량: "))
    new_location = input("새 위치: ")
    new_uid = input("새 UID: ")  # 사용자로부터 새 UID 입력 받음

    cursor.execute("UPDATE inventory SET product = ?, quantity = ?, location = ?, uid = ? WHERE rowid = ?",
                   (new_product, new_quantity, new_location, new_uid, record_id))
    conn.commit()

def delete_data():
    print_inventory()
    record_id_input = input("삭제할 항목의 ID를 입력하세요: ")
    if not record_id_input:
        return
    record_id = int(record_id_input)

    cursor.execute("DELETE FROM inventory WHERE rowid = ?", (record_id,))
    conn.commit()
    print(f"ID {record_id}의 항목이 삭제되었습니다.")

while True:
    insert_data()
    more = input("더 입력하시겠습니까? (y/n): ").lower().strip()
    if more == 'n':
        break
    elif more == '':
        continue

print_inventory()

conn.close()
