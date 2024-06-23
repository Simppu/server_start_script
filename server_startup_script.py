import os.path
from pathlib import Path
import platform
from subprocess import Popen
import time
import threading
import sys
import time

read, write = os.pipe()
begin_time = time.time()

def get_sh_or_bat():
   
    if platform.system() == 'Windows':
        return Path('./run.bat')
    else:
        return Path('./run.sh')

def start_server_process(startup_file):

    if platform.system() == 'Windows':
        return Popen('./run.bat', text=True, shell=True, stdin=read)
    else:
        return Popen('sh ' + './run.sh',stdin=read, shell=True, text=True)


def restart_timeout(server_process, startup_file, kill_signal, restart_signal):
    while True:
        # The intervall in seconds
        # This means 12 hours
        is_killed = kill_signal.wait(12*60*60)
        if is_killed:
            break
        restart_signal.set()
        #server_process.stdin = read
        os.write(write, "stop\n".encode())
        #server_process.stdin.write("stop\n")
        server_process.wait()
        server_process = start_server_process(startup_file)
        begin_time = time.time()

def server_crash_thread(process, startup_file, kill_signal, restart_signal):
    while True:
        process.wait()
        if kill_signal.wait(5):
            break
        elif (time.time() - begin_time) < (12*60*60):
            process = start_server_process(startup_file)

def main():
    startup_file = get_sh_or_bat()
    if not startup_file.is_file():
        print("Failed to get startup file\nMake sure either 'run.bat' or 'run.sh' exists in the same directory!")
        return 
    
    server_process = start_server_process(startup_file)
    kill_signal = threading.Event()
    restart_signal = threading.Event()
    server_restart_thread = threading.Thread(target=restart_timeout, args=[server_process, startup_file, kill_signal, restart_signal])
    server_restart_thread.start()
    
    crash_thread = threading.Thread(target=server_crash_thread, args=[server_process, startup_file, kill_signal, restart_signal])
    crash_thread.start()
    
    while True:
        i = input()
        if i == 'stop':
            
            kill_signal.set()
            
            os.write(write, "stop\n".encode())
            server_process.wait()
            server_restart_thread.join()
            crash_thread.join()
            break
        else:
            os.write(write, (i + '\n').encode())
        


if __name__ == '__main__':
    main()
