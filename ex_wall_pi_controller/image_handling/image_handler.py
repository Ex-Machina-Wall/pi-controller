import urllib.request
from PIL import Image, ImageEnhance
from pathlib import Path
import numpy as np
from typing import Union


class ImageHandler:
    DOWNLOAD_LOCATION = r'/home/pi/repos/all-ex-machina-wall-repos/pi-controller/ex_wall_pi_controller/image_handling/downloads'  
    SAVE_LOCATION = r'/home/pi/repos/all-ex-machina-wall-repos/pi-controller/ex_wall_pi_controller/image_handling/images'  
    
    def __init__(self):
        pass
    
    def get_num_frames(self, name: str) -> int:
        img = Image.open(Path(self.SAVE_LOCATION, name))
        return img.n_frames

    def _open_saved_image(self, path: Path, resize: tuple = (17, 13), frame: int = None) -> np.array:
        img = Image.open(path)
        if img.is_animated:
            img.seek(frame)
        converter = ImageEnhance.Color(img)
        img = converter.enhance(4)
        img = img.resize(resize)
        img.save(Path(path.parent, f"{path.stem}_small.png"), "PNG")
        
        # Convert the resized image to a NumPy array
        image_array = np.array(img)
        return image_array

    def get_image_from_url(self, url: str) -> np.array:
        download_path = Path(self.DOWNLOAD_LOCATION, "downloaded_image.png")
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)     AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36')
        opener.retrieve(url, download_path)
        return self._open_saved_image(download_path)
        
    
    def open_saved_image(self, name: str, frame: int = None) -> np.array:
        return self._open_saved_image(Path(self.SAVE_LOCATION, name), frame=frame)



def main():
    img_handler = ImageHandler()
    img_handler.get_image_from_url(url="https://i.gifer.com/embedded/download/7ZNJ.gif")


if __name__ == "__main__":
    main()
