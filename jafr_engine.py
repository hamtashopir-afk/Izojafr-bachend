jafr_result = full_jafr(req.name, req.mother_name, req.question)
    mothers = [[random.randint(0, 1) for _ in range(4)] for _ in range(4)]
    raml_result = raml_analysis(mothers)
    prompt = f"""
    User "{req.name}" asked:
    "{req.question}"
    --- Jafr Results ---
    Jafr Akbar: {jafr_result['akbar']['name']} - {jafr_result['akbar']['meaning']}
    Jafr Asghar: {jafr_result['asghar']['name']} - {jafr_result['asghar']['meaning']}
    Akhlat: {jafr_result['akhlat']['khilt']} ({jafr_result['akhlat']['tab']})
    --- Raml Results ---
    Judge: {raml_result[15]['shape']} - {raml_result[15]['meaning']}
    House 7: {raml_result[7]['shape']} - {raml_result[7]['meaning']}
    House 10: {raml_result[10]['shape']} - {raml_result[10]['meaning']}
    Combine these two methods and provide a unified, comprehensive interpretation in Persian.
    """
    ai_text = await get_ai_interpretation(prompt)
    return {
        "method": "combined",
        "jafr": jafr_result,
        "raml": raml_result,
        "interpretation": ai_text,
        "disclaimer": "This analysis is for entertainment and educational purposes only. Final decisions rest with your reason and trust in God."
    }

@app.get("/")
def root():
    return {"message": "Jafr & Raml AI API is running", "status": "ok"}

# -*- coding: utf-8 -*-
# jafr_engine.py - Jafr Calculation Engine

ABJAD = {
    'ا': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9, 'ی': 10,
    'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80, 'ص': 90,
    'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
    'پ': 2, 'چ': 3, 'ژ': 7, 'گ': 20,
}

def abjad(text):
    total = 0
    for char in text:
        if char in ABJAD:
            total += ABJAD[char]
    return total

MANAZEL = {
    1: ("شرطین", "آغاز پادشاهی، تولد یک جنبش نوین"),
    2: ("بطین", "ثروت نهان، گنجی که با صبر بیرون می‌آید"),
    3: ("ثریا", "برکت و رحمت، دوران آبادانی"),
    4: ("دبران", "نزاع و چالش، اما با مدیریت هوشمندانه"),
    5: ("هقعه", "غم پنهان، اما با حکمتی در باطن"),
    6: ("هنعه", "دشمنی پنهان، با هوشیاری قابل دفع"),
    7: ("ذراع", "قدرت نظامی، پیروزی با تلفات"),
    8: ("نثره", "آرامش موقت، فرصتی برای بازسازی"),
    9: ("طرف", "اختلاف عقیده، تفرقه در جمع"),
    10: ("جبهه", "عزت و شکوه، ظهور یک رهبر"),
    11: ("زبره", "پیروزی همراه با چانه‌زنی"),
    12: ("صرفه", "تغییر ناگهانی، چرخش سرنوشت"),
    13: ("عواء", "سفر شاهانه، دیده‌شدن"),
    14: ("سماک", "عدالت و امنیت، ثبات قضایی"),
    15: ("غفر", "بخشش و عفو، پایان سختی"),
    16: ("زبانا", "خصومت علنی، پیروزی حق بر باطل"),
    17: ("اکلیل", "تاج‌گذاری، موفقیت بی‌نظیر"),
    18: ("قلب", "انقلاب و شورش، تغییر اساسی"),
    19: ("شوله", "تأثیر عمیق، آتش و هرج‌ومرج"),
    20: ("نعائم", "خبر مسرت‌بخش، گشایش"),
    21: ("بلده", "تمرکز قدرت، تثبیت پایتخت"),
    22: ("سعد ذابح", "فداکاری بزرگ، قربانی برای هدف والا"),
    23: ("سعد بلع", "باران رحمت، پایان قحطی"),
    24: ("سعد سعود", "اقبال عظیم، عصر طلایی"),
    25: ("سعد اخبیه", "گشایش راز، کشف توطئه"),
    26: ("فرغ مقدم", "پایان یک دوران، سقوط حاکم"),
    27: ("فرغ مؤخر", "نتیجه‌گیری نهایی، پیروزی قطعی"),
    28: ("بطن‌الحوت", "پایان جهان‌بینی کهن، تولد اندیشه نو"),
}

BORJ = {
    1: ("حمل", "آتش", "نیل به مقصود، شتاب"),
    2: ("ثور", "خاک", "مال و آرامش، کندی"),
    3: ("جوزا", "باد", "تغییر و دوگانگی"),
    4: ("سرطان", "آب", "ابهام و خستگی"),
    5: ("اسد", "آتش", "غلبه و عزت"),
    6: ("سنبله", "خاک", "کسب و کار، دقت"),
    7: ("میزان", "باد", "تعادل و شراکت"),
    8: ("عقرب", "آب", "خطر و راز"),
    9: ("قوس", "آتش", "سفر و آرزو"),
    10: ("جدی", "خاک", "زحمت و تأخیر"),
    11: ("دلو", "باد", "آرزوی دور، کمک غیبی"),
    12: ("حوت", "آب", "سرگشتگی، صبر"),
}

def jafr_akbar(number):
    remainder = number % 28
    if remainder == 0: remainder = 28
    name, meaning = MANAZEL[remainder]
    return {"type": "jafr_akbar", "remainder": remainder, "name": name, "meaning": meaning}

def jafr_asghar(number):
    remainder = number % 12
    if remainder == 0: remainder = 12
    name, element, meaning = BORJ[remainder]
    return {"type": "jafr_asghar", "remainder": remainder, "name": name, "element": element, "meaning": meaning}

def akhlat(number):
    remainder = number % 4
    mapping = {
        1: ("خون (دم)", "گرم و تر", "کبد", "شرق", "بهار"),
        2: ("صفرا", "گرم و خشک", "کیسه صفرا", "غرب", "تابستان"),
        3: ("بلغم", "سرد و تر", "مغز", "شمال", "پاییز"),
        0: ("سودا", "سرد و خشک", "طحال", "جنوب", "زمستان"),
    }
    kh, tab, ozv, jahat, fasl = mapping[remainder]
    return {"type": "akhlat", "remainder": remainder, "khilt": kh, "tab": tab, "member": ozv, "direction": jahat, "season": fasl}

def full_jafr(name, mother_name, question):
    q_abjad = abjad(question)
    n_abjad = abjad(name)
    m_abjad = abjad(mother_name)
    total = q_abjad + n_abjad + m_abjad
    return {
        "total": total,
        "akbar": jafr_akbar(total),
        "asghar": jafr_asghar(total),
        "akhlat": akhlat(total),
    }
