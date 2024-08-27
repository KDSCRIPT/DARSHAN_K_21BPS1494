import cx_Freeze

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('client.py', base = "Win32GUI")]

cx_Freeze.setup(
    name = "ChessPro",
    options = {"build_exe" : 
        {"packages" : ["pygame"], "include_files" : ['check_characters.py', 'constants.py', 'server.py','game_functions.py','server.py']}},
    executables = executables
)