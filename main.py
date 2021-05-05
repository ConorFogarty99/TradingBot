import tkinter as tk
import logging


logger = logging.getLogger()
logger.debug("Important to debug")
logger.info("Basic info")
logger.warning("Warning message")
logger.error("Helps to debug error")

logger.setLevel(logging.INFO)

steam_handler = logging.StreamHandler()
formatter = logging.Formatter('')

root = tk.Tk()
root.mainloop()

