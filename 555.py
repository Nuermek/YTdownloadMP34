Trues = True
number = 0
import time
while Trues:
    print("อีโบว์อย่าหลอน")
    time.sleep(0.1)
    number += 1
    print(number)
    if number == 100:
        Trues = False
        time.sleep(0.1)
print("Ending")
time.sleep(0.1)
print("End")