# -*- coding: utf-8 -*-
# raml_engine.py - Raml Calculation Engine

import random

RAML_SHAPES = {
    "1111": {"name": "جمع", "element": "خاک", "meaning": "اتصال، پیوستگی، ثبات"},
    "0000": {"name": "جمع", "element": "خاک", "meaning": "اتصال، پیوستگی، ثبات"},
    "1010": {"name": "مطلوب", "element": "هوا", "meaning": "آرامش ظاهری، ارتباط"},
    "0101": {"name": "طالب", "element": "آتش", "meaning": "اشتیاق، حرکت، جسارت"},
    "1110": {"name": "متفرق", "element": "خاک", "meaning": "پراکندگی، تردید"},
    "0111": {"name": "مجرد", "element": "هوا", "meaning": "تنهایی، استقلال"},
    "1100": {"name": "قبض", "element": "خاک", "meaning": "محدودیت، گیر کردن"},
    "0011": {"name": "انفصال", "element": "آب", "meaning": "جدایی، کاهش، وقفه"},
    "1101": {"name": "نصر", "element": "آتش", "meaning": "پیروزی، غلبه"},
    "0100": {"name": "اتصال", "element": "هوا", "meaning": "پیوند، توافق"},
    "1011": {"name": "ریان", "element": "آب", "meaning": "نرمش، سیالیت"},
    "0010": {"name": "مضاعف", "element": "آتش", "meaning": "تکرار، دوگانگی"},
    "1001": {"name": "مشهود", "element": "خاک", "meaning": "صبوری، رازداری"},
    "0110": {"name": "شاهد", "element": "آب", "meaning": "نیرنگ پنهان، احساسات"},
    "1000": {"name": "مفرد", "element": "آتش", "meaning": "تمرکز، انزوا"},
    "0100": {"name": "متوسط", "element": "هوا", "meaning": "تعادل، میانه‌روی"},
}

HOUSES = {
    1: "خود شخص (طالع)", 2: "مال و دارایی", 3: "برادران و ارتباطات نزدیک",
    4: "خانواده و خانه", 5: "فرزندان و خلاقیت", 6: "سلامتی و خدمت",
    7: "شراکت و معامله", 8: "بحران و تحول", 9: "دانش و سفر",
    10: "شغل و افتخار", 11: "دوستان و آرزوها", 12: "دشمنان و غم‌ها",
}

def generate_shape():
    rows = []
    for _ in range(4):
        num_dots = random.randint(1, 16)
        rows.append(1 if num_dots % 2 == 1 else 0)
    return rows

def shape_to_string(shape):
    return "".join(str(x) for x in shape)

def get_shape_info(shape):
    key = shape_to_string(shape)
    if key in RAML_SHAPES:
        return RAML_SHAPES[key]
    return {"name": "نامعلوم", "element": "?", "meaning": "?"}

def xor_shapes(s1, s2):
    result = []
    for a, b in zip(s1, s2):
        total = a + b
        result.append(1 if total % 2 == 1 else 0)
    return result

def build_16_houses(mothers):
    houses = {i+1: mothers[i] for i in range(4)}
    for i in range(4):
        row = [mothers[j][i] for j in range(4)]
        houses[5+i] = row
    daughters = [houses[5+i] for i in range(4)]
    for i in range(4):
        row = [daughters[j][i] for j in range(4)]
        houses[9+i] = row
    houses[13] = xor_shapes(houses[1], houses[5])
    houses[14] = xor_shapes(houses[2], houses[6])
    houses[15] = xor_shapes(houses[13], houses[14])
    houses[16] = xor_shapes(houses[15], houses[13])
    return houses

def raml_analysis(mothers):
    houses = build_16_houses(mothers)
    result = {}
    for num, shape in houses.items():
        info = get_shape_info(shape)
        if num <= 12:
            result[num] = {"house": HOUSES[num], "shape": info["name"], "element": info["element"], "meaning": info["meaning"]}
        else:
            result[num] = {"house": f"خانه {num} (سطح ۲)", "shape": info["name"], "element": info["element"], "meaning": info["meaning"]}
    return result
