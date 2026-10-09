import time

def slow_text(text, delay):
    for cha in text:
        print(cha, end='', flush=True)
        time.sleep(delay / len(text))

a = "I"
d = "V"
i = "N"
f = "F"
b = "L"
c = "O"
e = "E"
g = "R"
f = "F"
h = "E"
i = "N"

sum = str(a) + " " + str(b) + str(c) + str(d) + str(e)  + " " + str(f) + str(g) + str(h) + str(i)

slow_text( sum , 1)