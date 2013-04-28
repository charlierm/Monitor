import ctypes
import sys
import os

if sys.platform == "win32":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        raise Exception("Monitor must be run as an admin")

else:
    if os.geteuid() != 0:
        raise Exception("Monitor must be run as root")


from monitor import app
app.run(debug=True, host="0.0.0.0")
