from PIL import Image
import os, math


def rows_cols(img_list:list):
    n = len(img_list)
    cols = int(math.ceil(n**0.5))
    rows = math.ceil(n/cols)

    return cols, rows, n


def create_ct_sheet(folder_path:str, img_ext:str, thumb_size: tuple[int,int] | None = None):

    img_list:list[str] = [img for img in os.listdir(folder_path) if img.lower().endswith(img_ext)]

    if not img_list:
        raise ValueError(f"nie znaleziono obrazów z rozszerzeniem {img_ext} w folderze {folder_path}")
    
    if thumb_size is None:
        thumb_size = Image.open(os.path.join(folder_path, img_list[0])).size   

    thumb_w, thumb_h = thumb_size
    cols, rows, n = rows_cols(img_list)

    sheet_w = cols * thumb_w
    sheet_h = rows * thumb_h

    sheet = Image.new("RGB", (sheet_w,sheet_h), color=(30,30,30))

    for idx in range(rows * cols):
        if idx < n:
            col = idx % cols
            row = idx // cols
            x = col * thumb_w
            y = row * thumb_h

            img_file_path = os.path.join(folder_path, img_list[idx])
            img = Image.open(img_file_path)
            img.thumbnail((thumb_w, thumb_h))
            sheet.paste(img, (x, y))


    sheet.save("contact_sheet.png")

    print(f"{img_list}\n {n}")

