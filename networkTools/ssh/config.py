from dotenv import load_dotenv
import os

# YOU MAY HAVE .env FILE


load_dotenv()

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')