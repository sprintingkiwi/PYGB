import psutil
import subprocess
import os
import sys
import time


# wd = os.getcwd()
# print wd
# subprocess.Popen(['python', 'main.py'], cwd=wd)
# subprocess.Popen(['python', 'main.py'])


print(sys.argv)
pid = int(sys.argv[1])
print(pid)

# while True:
#     print psutil.pid_exists(pid)

checking = True
while checking:

    print('checking')
    if not psutil.pid_exists(pid):
        checking = False
    time.sleep(0.1)

print('restarting PYGB')


subprocess.Popen(['python', 'main.py'])
time.sleep(1)
quit()
