from SQLiteCRUD import SQLiteCRUD


def get_users():
    return SQLiteCRUD.get_all_users()