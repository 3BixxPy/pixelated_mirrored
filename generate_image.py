from PIL import Image

def mirror_image(img):
    flipped_horizontally = img.transpose(Image.FLIP_LEFT_RIGHT)

    # step1 flip horizontally and merge
    new_image = Image.new("RGB", (img.width*2, img.height*2))
    new_image.paste(img, (0,0))
    new_image.paste(flipped_horizontally, (img.width, 0))

    # step2 flip step1 result vertically
    cropped = new_image.crop((0, 0, img.width*2, img.height))
    flipped_vertically = cropped.transpose(Image.FLIP_TOP_BOTTOM)
    new_image.paste(flipped_vertically, (0, img.height))

    return new_image


def split_image_into_squares(image_path, squares_per_row):
    image = Image.open(image_path)
    img_width, img_height = image.size
    square_size = max(img_width // squares_per_row, 1)

    squares_per_col = (img_height + square_size - 1) // square_size
    image = image.resize((image.width, square_size * squares_per_col))

    mirrored_squares = []

    for i in range(squares_per_row):
        for j in range(squares_per_col):
            left = i * square_size
            upper = j * square_size
            right = left + square_size
            lower = upper + square_size

            # make the square
            square = image.crop((left, upper, right, lower))

            # mirror saquare 4x
            mirrored_square = mirror_image(square)
            mirrored_squares.append((mirrored_square, (i, j)))

    square_size = square_size * 2

    # new image where the squares will be pasted
    new_width = squares_per_row * square_size
    new_height = squares_per_col * square_size
    new_image = Image.new('RGB', (new_width, new_height))

    for square, (i, j) in mirrored_squares:
        left = i * square_size
        upper = j * square_size
        new_image.paste(square, (left, upper))

    new_image.show()
    return new_image


def main(squares, file_name):
    import tkinter as tk
    from tkinter import filedialog

    def select_file():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="select an image",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        root.destroy()
        return file_path

    image_path = select_file()

    if image_path:
        resized_image = split_image_into_squares(image_path, squares)
        resized_image.save(file_name)
        print("image saved")
    else:
        print("select a file ")

if __name__ == "__main__":
    main(squares=20, file_name="abstract_art_i_guess.jpg")
