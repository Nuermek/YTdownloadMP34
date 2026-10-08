text = "hello world"

for char in text:
    # ถ้าเป็นช่องว่าง ให้ข้ามไป หรือพิมพ์ช่องว่างเปล่าๆ
    if char == " ":
        print("(ช่องว่าง)")
        continue
        
    # สร้างข้อความตั้งแต่ 'a' ถึง ตัวอักษรปัจจุบัน (char)
    result = ""
    for i in range(ord('a'), ord(char) + 1):
        result += chr(i)
        
    print(f"{char}: {result}")