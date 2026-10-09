import time

def slow_print_for_input(text, delay):
    # แปลงข้อมูลทุกอย่างให้เป็นตัวอักษร (String) เผื่อกรณีใส่ตัวเลขเข้ามา
    text = str(text) 
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay / len(text))

def slow_print(text, delay):
    # แปลงข้อมูลทุกอย่างให้เป็นตัวอักษร (String) เผื่อกรณีใส่ตัวเลขเข้ามา
    text = str(text) 
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay / len(text))
    print()  # เพิ่มบรรทัดว่างเพื่อความสวยงาม

def slow_input(prompt, delay):
    slow_print_for_input(prompt, delay)
    return input()

ask0 = slow_input("คุณจะใช้โปรแกรมไหน? :" , 2.5)

if ask0 == "1":
    # ใช้ while True เพื่อให้โปรแกรมวนลูปทำงานต่อไปเรื่อยๆ
    while True:
     ask1 = slow_input("ตัวตั้ง: ", 2.5)
     time.sleep(1)
     ask2 = slow_input("ตัวทำดำเนินการ (+, -, *, /): ", 2.5)
     time.sleep(1)
     ask3 = slow_input("ตัวดำเนินการ: ", 2.5)
     time.sleep(1)

     # คำนวณผลลัพธ์
     if ask2 == "+":
         result = float(ask1) + float(ask3)
     elif ask2 == "-":
         result = float(ask1) - float(ask3)
     elif ask2 == "*":
          result = float(ask1) * float(ask3)
     elif ask2 == "/":
        result = float(ask1) / float(ask3)
     else:
        result = "ตัวดำเนินการไม่ถูกต้อง"

    # แก้ไขจุดนี้: รวมข้อความกับผลลัพธ์เป็นชิ้นเดียว แล้วส่งเข้าฟังก์ชัน
     slow_print(f"ผลลัพธ์: {result}", 2.5)
     time.sleep(5)
    
    # สอบถามว่าต้องการทำต่อไหม
     ask4 = slow_input("คุณต้องการทำการคำนวณต่อหรือไม่? (y/n): ", 2.5)
     slow_print("Loading...", 2.5)
     time.sleep(3)
    
    # ถ้าพิมพ์คำอื่นที่ไม่ใช่ 'y' ให้หลุดออกจากลูปทันที
     if ask4.lower() != "y":
        break



# ส่วนจบการทำงาน
time.sleep(1)
slow_print("Thank you for using this program.", 2.5)
slow_print("Ending...", 2.5)
time.sleep(5)