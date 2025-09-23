import os
from PIL import Image
import re

# 用於根據文件名中的數字進行排序的輔助函數
def sort_key(file_name):
    # 使用正則表達式從文件名中提取數字
    match = re.search(r'(\d+)', file_name)
    return int(match.group(1)) if match else file_name

def images_to_pdf(folder_path, output_pdf_path):
    # 獲取資料夾內所有圖片文件
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    # 確保有圖片文件
    if not image_files:
        print("No image files found.")
        return

    # 根據文件名中的數字進行排序
    image_files.sort(key=sort_key)

    # 輸出每個文件的合成順序
    print("Order of image files in the PDF:")
    for i, image_file in enumerate(image_files, start=1):
        print(f"{i}: {image_file}")

    # 加載圖片並轉換模式
    images = []
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        
        # 如果不是RGB模式，將圖片轉換為RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        images.append(image)

    # 合成PDF並保存
    if images:
        images[0].save(output_pdf_path, save_all=True, append_images=images[1:])
        print(f"PDF file saved as: {output_pdf_path}")

# 設定資料夾路徑及輸出PDF文件路徑
folder_path = 'photo'  # 替換為你的資料夾路徑
output_pdf_path = 'output.pdf'  # 輸出PDF文件的名稱

# 調用函數執行合成
images_to_pdf(folder_path, output_pdf_path)