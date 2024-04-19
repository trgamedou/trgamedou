from PIL import Image
import os

# مسیر پوشه حاوی تصاویر
input_folder = "./input-images"
# مسیر پوشه برای ذخیره تصاویر تبدیل شده
output_folder = "./input-images"

# اطمینان حاصل کنید که پوشه خروجی وجود دارد، اگر نه آن را ایجاد کنید
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# لیست تمام فایل‌ها در پوشه ورودی
file_list = os.listdir(input_folder)

# حلقه برای هر فایل در پوشه ورودی
for filename in file_list:
    # اگر فایل یک تصویر PNG باشد
    if filename.endswith(".png"):
        # باز کردن تصویر با استفاده از Pillow
        with Image.open(os.path.join(input_folder, filename)) as img:
            # ساخت مسیر برای تصویر خروجی (به فرض JPG)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")
            # تبدیل و ذخیره تصویر به فرمت JPG
            img.convert("RGB").save(output_path)
