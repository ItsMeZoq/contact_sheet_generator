from PIL import Image
import os, math

class ContactSheet:
    def __init__(self, folder_path: str, img_ext: str = "jpg", thumb_size: tuple[int,int] | None = None, bg_color=(30,30,30)):
        self.folder_path = folder_path
        self.img_ext = img_ext.lower()
        self.thumb_size = thumb_size
        self.bg_color = bg_color
        self.img_list = self._load_images()
        self.n = len(self.img_list)
        self.cols, self.rows = self._calculate_grid()

    def _load_images(self):
        img_list = [img for img in os.listdir(self.folder_path) if img.lower().endswith(self.img_ext)]
        img_list.sort()
        if not img_list:
            raise ValueError(f"images with extension '{self.img_ext}' not found in {self.folder_path}")
        return img_list

    def _calculate_grid(self):
        n = self.n
        cols = int(math.ceil(n**0.5))
        rows = math.ceil(n / cols)
        return cols, rows

    def generate(self, output_name="contact_sheet.png"):
        if self.thumb_size is None:
            first_img_path = os.path.join(self.folder_path, self.img_list[0])
            self.thumb_size = Image.open(first_img_path).size

        thumb_w, thumb_h = self.thumb_size
        sheet_w = self.cols * thumb_w
        sheet_h = self.rows * thumb_h

        sheet = Image.new("RGB", (sheet_w, sheet_h), color=self.bg_color)

        for idx in range(self.rows * self.cols):
            if idx < self.n:
                col = idx % self.cols
                row = idx // self.cols
                x = col * thumb_w
                y = row * thumb_h

                img_file_path = os.path.join(self.folder_path, self.img_list[idx])
                img = Image.open(img_file_path)
                img.thumbnail((thumb_w, thumb_h))
                sheet.paste(img, (x, y))

        output_path = os.path.join(self.folder_path, output_name)
        sheet.save(output_path)
        print(f"Contact sheet saved: {output_path} ({self.n} images, grid {self.cols}x{self.rows})")

