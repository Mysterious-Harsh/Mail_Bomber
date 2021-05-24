import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
	base = "Win32GUI"

executables = [ cx_Freeze.Executable( "Mail_Bomber.py", base=base, icon="images/icon.ico" ) ]

cx_Freeze.setup(
    name="Mail_Bomber",
    options={
        "build_exe": {
            "packages": [ "tkinter", "pygubu", "email", "os", "smtplib", "sqlite3" ],
            "include_files": [ "images/icon.ico", "images/icon.png", "mail_bomber.ui", "add_email.ui", 'indicator.ui' ]
            }
        },
    version="0.01",
    description="multiple mail at a time",
    executables=executables
    )