class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_value(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.name} - ราคา: {self.price} บาท - จำนวน: {self.quantity}"

products = [
    Product("ปากกา", 50, 10),
    Product("สมุด", 30, 5),
    Product("ยางลบ", 15, 20),
    Product("ไม้บรรทัด", 25, 7)
]

while True:
    name = input("ชื่อสินค้า (พิมพ์ 'stop' เพื่อหยุด): ")
    if name.lower() == "stop":
        break
    try:
        price = float(input("ราคาสินค้า: "))
        quantity = int(input("จำนวนสินค้า: "))
        products.append(Product(name, price, quantity))
    except ValueError:
        print("กรุณากรอกข้อมูลให้ถูกต้อง")

print("\nสินค้าราคาต่ำกว่า 100 บาท:")
cheap_products = list(filter(lambda p: p.price < 100, products))
for p in cheap_products:
    print(p)

print("\nมูลค่ารวมของสินค้าแต่ละรายการ:")
total_values = list(map(lambda p: (p.name, p.total_value()), products))
for name, total in total_values:
    print(f"{name}: {total} บาท")

print("\nเรียงสินค้าตามมูลค่ารวม (มาก -> น้อย):")
sorted_products = sorted(products, key=lambda p: p.total_value(), reverse=True)
for p in sorted_products:
    print(f"{p.name}: {p.total_value()} บาท")
