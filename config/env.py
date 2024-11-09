from pathlib import Path
import os
# import environ # type: ignore

# env = environ.Env()

from dotenv import load_dotenv # type: ignore

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

print(os.environ.get('EMAIL_ID'))



