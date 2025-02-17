import sqlite3

db_path = "db.sqlite3"  # مسیر فایل دیتابیس SQLite

# اتصال به دیتابیس
conn = sqlite3.connect(db_path)

# تنظیم Encoding به UTF-8
conn.text_factory = lambda x: str(x, "utf-8", "ignore")  # نادیده گرفتن کاراکترهای خراب
cursor = conn.cursor()
cursor.execute("PRAGMA encoding = 'UTF-8'")

# ذخیره تغییرات و بستن اتصال
conn.commit()
conn.close()

print("Encoding of SQLite database fixed to UTF-8.")
