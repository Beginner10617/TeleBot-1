import cv2
from PIL import Image, ImageDraw, ImageFont
ascii_chars_quantized = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

def get_avg_brightness(cell):   # cell must be in greyscale
    return cv2.mean(cell)[0]

def get_char(brightness):
    return ascii_chars_quantized[int(brightness/25.6)]

def ascii_art(image_path, numberOfRows=None, numberOfColumns=None):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Image not found")
        return
    height, width = img.shape
    if numberOfRows is None and numberOfColumns is None:
        numberOfRows = height // 10
        numberOfColumns = width // 10
    cell_width = width // numberOfColumns
    cell_height = height // numberOfRows
    output = """"""
    for i in range(numberOfRows):
        for j in range(numberOfColumns):
            cell = img[i*cell_height:(i+1)*cell_height, j*cell_width:(j+1)*cell_width]
            brightness = get_avg_brightness(cell)
            output += get_char(brightness)
        output += '\n'
    return output

def ascii_to_image(ascii_art, font_path="Fonts/Courier.ttf", font_size=12, output_path="ascii_art.png"):
    lines = ascii_art.splitlines()
    
    # Load monospaced font
    font = ImageFont.truetype(font_path, font_size)
    
    # Calculate width and height of the font for a single line
    # Using the getbbox method on the longest line of ASCII art
    bbox = font.getbbox(max(lines, key=len))
    img_width = bbox[2] - bbox[0]  # right - left
    char_height = bbox[3] - bbox[1]  # bottom - top
    
    # Calculate image dimensions
    img_height = len(lines) * char_height  # height of the image
    
    # Create image
    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)
    
    # Draw text
    for i, line in enumerate(lines):
        draw.text((0, i * char_height), line, fill="black", font=font)

    # Save image
    image.save(output_path)
    print(f"ASCII art saved as {output_path}")

if __name__ == "__main__":
    ascii_art = ascii_art("images/Download-20250109222918.jpg")
    print(ascii_art)
    ascii_to_image(ascii_art, output_path="ascii_art.png")