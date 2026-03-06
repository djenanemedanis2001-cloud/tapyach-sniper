import re

print("--- أداة إصلاح البروكسيات ---")
print("حط الليستة المخربة هنا (دير Collé)، وكي تكمل دير Entrée زوج خطرات:")

lines = []
while True:
    line = input()
    if line:
        lines.append(line)
    else:
        break

cleaned_proxies = []

for line in lines:
    # نحيو الفراغات
    text = line.strip()
    if not text: continue

    # الخوارزمية: نحوسو على آخر نقطة "."
    # ومن بعد نفرقو بين الرقم تاع IP والرقم تاع Port
    try:
        last_dot_index = text.rfind('.')
        if last_dot_index != -1:
            suffix = text[last_dot_index+1:] # مثلاً 23314186
            prefix = text[:last_dot_index+1] # مثلاً 47.252.11.
            
            # نجربو نقسمو السافيكس
            # عادة الرقم الأخير فالـ IP يكون فيه بين 1 و 3 أرقام
            # والبور يكون فيه بين 2 و 5 أرقام
            
            found = False
            for i in range(1, 4): # i هو طول الرقم الأخير تاع IP
                if i >= len(suffix): break
                
                ip_part = suffix[:i]
                port_part = suffix[i:]
                
                # شرط: جزء IP لازم يكون أقل من 255
                if int(ip_part) <= 255:
                    # لقيناها!
                    fixed_proxy = f"{prefix}{ip_part}:{port_part}"
                    cleaned_proxies.append(fixed_proxy)
                    found = True
                    break
            
            if not found:
                print(f"⚠️ ما قدرتش نسقم هذا: {text}")
    except:
        pass

# الحفظ في الملف
with open("proxies.txt", "w") as f:
    for p in cleaned_proxies:
        f.write(p + "\n")

print(f"\n✅ سي بون! سقمنا {len(cleaned_proxies)} بروكسي وحطيناهم في proxies.txt")