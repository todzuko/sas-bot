import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src_bot.bot import run


try:
    run()
except Exception as e:
    with open("../src_bot/log.txt", "a") as f:
        f.write(str(e) + '\n')
