import cx_Freeze
from cx_Freeze import *

setup(
    name = "WordCalendar",
    options = {'build.exe':{'packages': ['pygame','os']}},
    executables=[
        Executable(
            "main.py",
            )
        ]
    )
