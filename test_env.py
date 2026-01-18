from dotenv import load_dotenv
import os

print("Attempting to load .env file...")

# Load the .env file
loaded = load_dotenv()

if loaded:
    print(".env file was found and loaded successfully!")
else:
    print("Warning: .env file was NOT found.")

# Try to get the password variable
db_pass = os.getenv("DB_PASSWORD")

# Print the result
print(f"The password read from the environment is: {db_pass}")