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

# Print the result safely (do not expose secrets)
if db_pass:
    print("DB_PASSWORD variable exists in the environment (not displayed).")
else:
    print("DB_PASSWORD not found in environment.")