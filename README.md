# server_start_script
A python script to automatically restart the server every 12 hours or when it crashes

Install instructions:
- Download file
- Put file in the same folder as either run.bat or run.sh
- Run the file using python


Usage/Features:
- Like a regular server but must be ran from a commandline
- Everything MUST be ran in the terminal/cmd the server was started from, otherwise it will think it was a crash, also the gui doesn't work
- Use `stop` to close the server or you will get funy results because the threads won't close properly
- Use `restart` to trigger a manual restart
- Crash recovery
- Will send a message as a heads up to warn players before restarting
