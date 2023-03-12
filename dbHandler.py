import sqlite3
db_path = 'chat.db'

def create_table():
    conn = sqlite3.connect(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS chathistory (id INTEGER PRIMARY KEY AUTOINCREMENT, chatid INTEGER, role TEXT, content TEXT)")
    conn.commit()
    conn.close()

def add_entry(role: str, content: str, chatid: int):
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT INTO chathistory (role, content, chatid) VALUES (?, ?, ?)", (role, content, chatid))
    conn.commit()
    conn.close()


def get_chat(chatid: int) -> list:
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT id, role, content from chathistory where chatid = ?", (chatid,))
    chat_history = sorted([{'id': row[0], 'role': row[1], 'content': row[2]} for row in cursor], key=lambda x: x['id'])
    conn.commit()
    conn.close()
    return chat_history

def delete_chat(chatid: int):
    conn = sqlite3.connect(db_path)
    conn.execute("DELETE FROM chathistory where chatid = ?", (chatid,))
    conn.commit()
    conn.close()

def get_last_chatid() -> int:
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("SELECT max(chatid) from chathistory")
    last_chat = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return last_chat