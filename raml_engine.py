# ============================================
# raml_engine.py - ãæÊæÑ ãÍÇÓÈÇÊ Ñãá
# ============================================

import random

# ?? Ô˜á Ñãá ÈÇ ÊÚÈíÑ
RAML_SHAPES = {
    "1111": {"name": "ÌãÚ", "element": "ÎÇ˜", "meaning": "ÇÊÕÇá¡ íæÓÊí¡ ËÈÇÊ"},
    "0000": {"name": "ÌãÚ", "element": "ÎÇ˜", "meaning": "ÇÊÕÇá¡ íæÓÊí¡ ËÈÇÊ"},
    "1010": {"name": "ãØáæÈ", "element": "åæÇ", "meaning": "ÂÑÇãÔ ÙÇåÑí¡ ÇÑÊÈÇØ"},
    "0101": {"name": "ØÇáÈ", "element": "ÂÊÔ", "meaning": "ÇÔÊíÇŞ¡ ÍÑ˜Ê¡ ÌÓÇÑÊ"},
    "1110": {"name": "ãÊİÑŞ", "element": "ÎÇ˜", "meaning": "ÑÇ˜äÏí¡ ÊÑÏíÏ"},
    "0111": {"name": "ãÌÑÏ", "element": "åæÇ", "meaning": "ÊäåÇíí¡ ÇÓÊŞáÇá"},
    "1100": {"name": "ŞÈÖ", "element": "ÎÇ˜", "meaning": "ãÍÏæÏíÊ¡ íÑ ˜ÑÏä"},
    "0011": {"name": "ÇäİÕÇá", "element": "ÂÈ", "meaning": "ÌÏÇíí¡ ˜ÇåÔ¡ æŞİå"},
    "1101": {"name": "äÕÑ", "element": "ÂÊÔ", "meaning": "íÑæÒí¡ ÛáÈå"},
    "0100": {"name": "ÇÊÕÇá", "element": "åæÇ", "meaning": "íæäÏ¡ ÊæÇİŞ"},
    "1011": {"name": "ÑíÇä", "element": "ÂÈ", "meaning": "äÑãÔ¡ ÓíÇáíÊ"},
    "0010": {"name": "ãÖÇÚİ", "element": "ÂÊÔ", "meaning": "Ê˜ÑÇÑ¡ ÏæÇäí"},
    "1001": {"name": "ãÔåæÏ", "element": "ÎÇ˜", "meaning": "ÕÈæÑí¡ ÑÇÒÏÇÑí"},
    "0110": {"name": "ÔÇåÏ", "element": "ÂÈ", "meaning": "äíÑä äåÇä¡ ÇÍÓÇÓÇÊ"},
    "1000": {"name": "ãİÑÏ", "element": "ÂÊÔ", "meaning": "ÊãÑ˜Ò¡ ÇäÒæÇ"},
    "0100": {"name": "ãÊæÓØ", "element": "åæÇ", "meaning": "ÊÚÇÏá¡ ãíÇäåÑæí"},
}

# ÎÇäååÇí ?? Çäå Ñãá
HOUSES = {
    1: "ÎæÏ ÔÎÕ (ØÇáÚ)",
    2: "ãÇá æ ÏÇÑÇíí",
    3: "ÈÑÇÏÑÇä æ ÇÑÊÈÇØÇÊ äÒÏí˜",
    4: "ÎÇäæÇÏå æ ÎÇäå",
    5: "İÑÒäÏÇä æ ÎáÇŞíÊ",
    6: "ÓáÇãÊí æ ÎÏãÊ",
    7: "ÔÑÇ˜Ê æ ãÚÇãáå",
    8: "ÈÍÑÇä æ ÊÍæá",
    9: "ÏÇäÔ æ ÓİÑ",
    10: "ÔÛá æ ÇİÊÎÇÑ",
    11: "ÏæÓÊÇä æ ÂÑÒæåÇ",
    12: "ÏÔãäÇä æ ÛãåÇ",
}

def generate_shape():
    """ÊæáíÏ í˜ Ô˜á Ñãá ÈÇ äŞØåíäí ÊÕÇÏİí"""
    rows = []
    for _ in range(4):
        num_dots = random.randint(1, 16)
        rows.append(1 if num_dots % 2 == 1 else 0)
    return rows

def shape_to_string(shape):
    """ÊÈÏíá Ô˜á Èå ÑÔÊå (? = äŞØå¡ ? = ÎØ)"""
    return "".join(str(x) for x in shape)

def get_shape_info(shape):
    """ÏÑíÇİÊ ÇØáÇÚÇÊ í˜ Ô˜á"""
    key = shape_to_string(shape)
    if key in RAML_SHAPES:
        return RAML_SHAPES[key]
    return {"name": "äÇãÚáæã", "element": "?", "meaning": "?"}

def xor_shapes(s1, s2):
    """ÌãÚ XOR Ïæ Ô˜á (ŞÇÚÏå ÛáÈå äŞØå)"""
    result = []
    for a, b in zip(s1, s2):
        total = a + b
        result.append(1 if total % 2 == 1 else 0)
    return result

def build_16_houses(mothers):
    """ÓÇÎÊ ?? ÎÇäå ÇÒ ? ãÇÏÑ"""
    # ãÇÏÑÇä = ÎÇäååÇí ?-?
    houses = {i+1: mothers[i] for i in range(4)}
    
    # ÏÎÊÑÇä = ÎÇäååÇí ?-?
    for i in range(4):
        row = [mothers[j][i] for j in range(4)]
        houses[5+i] = row
    
    # äæååÇ = ÎÇäååÇí ?-??
    daughters = [houses[5+i] for i in range(4)]
    for i in range(4):
        row = [daughters[j][i] for j in range(4)]
        houses[9+i] = row
    
    # ÔÇåÏÇä = ÎÇäååÇí ??-??
    houses[13] = xor_shapes(houses[1], houses[5])
    houses[14] = xor_shapes(houses[2], houses[6])
    
    # ŞÇÖí = ÎÇäå ??
    houses[15] = xor_shapes(houses[13], houses[14])
    
    # ãíÒÇä = ÎÇäå ??
    houses[16] = xor_shapes(houses[15], houses[13])
    
    return houses

def raml_analysis(mothers):
    """ÊÍáíá ˜Çãá Ñãá"""
    houses = build_16_houses(mothers)
    result = {}
    for num, shape in houses.items():
        info = get_shape_info(shape)
        if num <= 12:
            result[num] = {
                "house": HOUSES[num],
                "shape": info["name"],
                "element": info["element"],
                "meaning": info["meaning"],
            }
        else:
            result[num] = {
                "house": f"ÎÇäå {num} (ÓØÍ ?)",
                "shape": info["name"],
                "element": info["element"],
                "meaning": info["meaning"],
            }
    return result
# ============ ÊÓÊ ============
if name == "__main__":
    mothers = [generate_shape() for _ in range(4)]
    print("ãÇÏÑÇä:")
    for i, m in enumerate(mothers):
        info = get_shape_info(m)
        print(f"  ÎÇäå {i+1}: {shape_to_string(m)} = {info['name']}")
    
    print("\nÊÍáíá ?? ÎÇäå:")
    result = raml_analysis(mothers)
    for num, data in result.items():
        print(f"  {num}. {data['house']}: {data['shape']} ({data['element']}) - {data['meaning']}")