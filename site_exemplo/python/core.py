from SQLiteCRUD import SQLiteCRUD 

# Create an instance of the SQLiteCRUD class
db_manager = SQLiteCRUD()

# Create users
db_manager.create_user("Alice Smith", "alice@example.com")
db_manager.create_user("Bob Johnson", "bob@example.com")

# Read all users
print("All users:", db_manager.get_all_users())

# Read a specific user
user = db_manager.get_user_by_id(1)
if user:
    print("User with ID 1:", user)

# Update a user
db_manager.update_user_email(1, "alice.s@example.com")
print("Updated user with ID 1:", db_manager.get_user_by_id(1))

# Delete a user
db_manager.delete_user(2)
print("All users after deletion:", db_manager.get_all_users())

# Close the connection
db_manager.close()