# receipt_parser.py
import re

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# деньги вида: 1 152,00 или 308,00
money = re.findall(r"\d{1,3}(?: \d{3})*,\d{2}", text)

# дата и время
dt = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
date, time = (dt.group(1), dt.group(2)) if dt else (None, None)

# оплата
pay = re.search(r"(Банковская карта|Наличные):\s*([\d ]+,\d{2})", text)
pay_method, pay_amount = (pay.group(1), pay.group(2)) if pay else (None, None)

# итого
tot = re.search(r"ИТОГО:\s*([\d ]+,\d{2})", text)
total = tot.group(1) if tot else None

# товары (под формат твоего чека)
items = []
pat = re.compile(
    r"(?m)^\s*(\d+)\.\s*\n"          # номер
    r"(.+)\n"                       # название
    r"([\d,]+)\s*x\s*([\d ]+,\d{2})\n"  # qty x unit_price
    r"([\d ]+,\d{2})"               # line_total
)
for m in pat.finditer(text):
    items.append({
        "no": int(m.group(1)),
        "name": m.group(2).strip(),
        "qty": m.group(3),
        "unit_price": m.group(4),
        "line_total": m.group(5),
    })

def to_float(s: str) -> float:
    return float(s.replace(" ", "").replace(",", "."))

sum_items = sum(to_float(it["line_total"]) for it in items)

print("DATE:", date)
print("TIME:", time)
print("PAYMENT:", pay_method, pay_amount)
print("TOTAL:", total)
print("ITEMS:", len(items))
print("SUM ITEMS:", sum_items)

print("\nPRODUCT NAMES:")
for it in items:
    print("-", it["name"])

print("\nALL PRICES FOUND:")
print(money)