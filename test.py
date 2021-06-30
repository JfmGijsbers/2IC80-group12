import time

def func():
    time.sleep(100)

print("Start")
try:
    func()
except KeyboardInterrupt:
    print("Interupted")
print("Done")

