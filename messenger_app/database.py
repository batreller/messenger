import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False, isolation_level=None)


# todo change db to zoga's

def create_db():
    cur = conn.cursor()
    cur.execute("""CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    login TEXT,
                    password TEXT,
                    public_name TEXT DEFAULT "NAME NOT SET",
                    is_online BOOL DEFAULT FALSE,
                    avatar TEXT DEFAULT "data:image/jpeg;base64,/9j/4QCORXhpZgAATU0AKgAAAAgABQEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAAITAAMAAAABAAEAAIKYAAIAAAArAAAAWgAAAAAAAABIAAAAAQAAAEgAAAABKGMpIE1vaGFtbWFkIFN1bGhhbiBCYWRyaSB8IERyZWFtc3RpbWUuY29tAAD/7QBSUGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAADYcAnQAKihjKSBNb2hhbW1hZCBTdWxoYW4gQmFkcmkgfCBEcmVhbXN0aW1lLmNvbRwCAAACAAT/4Qx1aHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLwA8P3hwYWNrZXQgYmVnaW49J++7vycgaWQ9J1c1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCc/Pgo8eDp4bXBtZXRhIHhtbG5zOng9J2Fkb2JlOm5zOm1ldGEvJyB4OnhtcHRrPSdJbWFnZTo6RXhpZlRvb2wgMTAuODAnPgo8cmRmOlJERiB4bWxuczpyZGY9J2h0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMnPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6cGx1cz0naHR0cDovL25zLnVzZXBsdXMub3JnL2xkZi94bXAvMS4wLyc+CiAgPHBsdXM6TGljZW5zb3I+CiAgIDxyZGY6U2VxPgogICAgPHJkZjpsaSByZGY6cGFyc2VUeXBlPSdSZXNvdXJjZSc+CiAgICAgPHBsdXM6TGljZW5zb3JVUkw+aHR0cHM6Ly93d3cuZHJlYW1zdGltZS5jb208L3BsdXM6TGljZW5zb3JVUkw+CiAgICA8L3JkZjpsaT4KICAgPC9yZGY6U2VxPgogIDwvcGx1czpMaWNlbnNvcj4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6eG1wUmlnaHRzPSdodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvcmlnaHRzLyc+CiAgPHhtcFJpZ2h0czpXZWJTdGF0ZW1lbnQ+aHR0cHM6Ly93d3cuZHJlYW1zdGltZS5jb20vYWJvdXQtc3RvY2staW1hZ2UtbGljZW5zZXM8L3htcFJpZ2h0czpXZWJTdGF0ZW1lbnQ+CiA8L3JkZjpEZXNjcmlwdGlvbj4KPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKPD94cGFja2V0IGVuZD0ndyc/Pv/bAEMACAYGBwYFCAcHBwkJCAoMFA0MCwsMGRITDxQdGh8eHRocHCAkLicgIiwjHBwoNyksMDE0NDQfJzk9ODI8LjM0Mv/CAAsIAyADIAEBIgD/xAAbAAEAAgMBAQAAAAAAAAAAAAAABQYCAwQBB//aAAgBAQAAAAHiAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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",
                    token TEXT);
                """)
    cur.execute("""CREATE TABLE messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    sender INTEGER,
                    receiver INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP);
                """)


# create_db()

def register(token: str, login: str, password: str) -> None:
    cur = conn.cursor()
    cur.execute("INSERT INTO users(login, password, token) VALUES(?, ?, ?)", (login, password, token,))


def get_user_by_token(token: str) -> tuple:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE token=?", (token,))
    return cur.fetchone()


def get_user_by_login(login: str) -> tuple:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE login=?", (login,))
    return cur.fetchone()


def get_user_by_id(id: int) -> tuple:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id=?", (id,))
    return cur.fetchone()


def send_message(text: str, sender: str, receiver: int) -> bool:
    cur = conn.cursor()
    cur.execute("INSERT INTO messages(text, sender, receiver) VALUES(?, ?, ?)", (text, sender, receiver,))
    return cur.fetchone()


def get_chats_by_id(id: str) -> list:
    cur = conn.cursor()
    cur.execute(
        "SELECT max(id), text, sender, receiver, timestamp FROM messages WHERE sender=? OR receiver=? GROUP BY sender, receiver ORDER BY id DESC;",
        (id, id,))
    chats = cur.fetchall()
    done = set()
    minuser = 0
    for chat_index in range(len(chats)):
        chat_index -= minuser
        if (str(chats[chat_index][3]) + "|" + str(chats[chat_index][2])) in done:
            chats.pop(chat_index)
            minuser += 1
            continue
        done.add(str(chats[chat_index][2]) + "|" + str(chats[chat_index][3]))
        sender = get_user_by_id(chats[chat_index][2])
        receiver = get_user_by_id(chats[chat_index][3])

        chats[chat_index] = (*chats[chat_index], sender[3], receiver[3], sender[4], receiver[4])

    return chats


def get_users_chats(user_1: int, user_2: int) -> list:
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)",
                (user_1, user_2, user_2, user_1,))
    return cur.fetchall()


def get_all_users(search_filter: str, except_user: int) -> list:
    cur = conn.cursor()
    cur.execute("SELECT id, public_name, avatar FROM users WHERE id != ? AND public_name LIKE ? || '%'",
                (except_user, search_filter,))
    return cur.fetchall()


def set_name(user_id: int, name: str) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE users SET public_name=? WHERE id==?", (name, user_id,))


def get_related_users(to_user_id: int) -> list:
    cur = conn.cursor()
    cur.execute(
        "SELECT receiver FROM messages WHERE sender=? GROUP BY receiver UNION SELECT sender FROM messages WHERE receiver=? GROUP BY sender ORDER BY receiver DESC",
        (to_user_id, to_user_id,))
    res = cur.fetchall()
    print(res)
    return res


def change_online(status: bool, user_id: int) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE users SET is_online=? WHERE id=?", (status, user_id,))


def set_avatar(user_id: int, avatar: str) -> None:
    cur = conn.cursor()
    cur.execute("UPDATE users SET avatar=? WHERE id==?", (avatar, user_id,))
