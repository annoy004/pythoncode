from PIL import Image
from rembg import remove
 
def remove_background(input_path, output_path):
    try:
        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)
        print("Background removal successful.")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
