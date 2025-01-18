from itertools import permutations
import cv2
possible_permutations = lambda n: list(permutations(range(n)))
"""
Color data in the format:
{
color 1 : [(row, column), (row, column), ...],
color 2 : [(row, column), (row, column), ...],
...
}
"""

def check_permutation(perm, color_data = None, n = 8):
    for i in range(n-1):
        j = i+1
        if abs(i-j) == abs(perm[i] - perm[j]):
            return False
    if color_data is None:
        return True
    for color, positions in color_data.items():
        queens_in_color = 0
        for position in positions:
            if perm[position[0]] == position[1]:
                queens_in_color += 1
        if queens_in_color > 1:
            return False
    return True

def get_color_data(image_path, numberOfRows, numberOfColumns, margin = 42):
    # Read the image
    print("Reading the image..., margin = ", margin)
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    # Calculate the size of each cell
    cell_width = width // numberOfColumns
    cell_height = height // numberOfRows
    color_data = {}
    if margin > cell_width//2 or margin > cell_height//2:
        raise ValueError("Margin is too large!")
    for i in range(numberOfRows):
        for j in range(numberOfColumns):
            # Extract the cell
            cell = img[i*cell_height + margin :(i+1)*cell_height - margin, j*cell_width + margin:(j+1)*cell_width - margin]
            # Calculate the average color of the cell
            avg_color = cell.mean(axis=0).mean(axis=0)
            # Add the average color to the color_data
            if tuple(avg_color) not in color_data:
                color_data[tuple(avg_color)] = []
            color_data[tuple(avg_color)].append((i, j))
    print("Color data:")
    for i in color_data:
        print(color_data[i])
    return color_data
def show(perm):
    for i in range(n):
        for j in range(n):
            if j == perm[i]:
                print("Q", end = " ")
            else:
                print(".", end = " ")
        print()
    print()

if __name__ == "__main__":
    n = int(input("Enter the number of queens: "))
    data = get_color_data(input("File path: "), n, n)
    print("Color data:")
    for i in data:
        print(data[i], end = " ")
    print('\n')
    print("Solution:")
    for perm in possible_permutations(n):
        if check_permutation(perm, data, n):
            show(perm)
            input("Press enter to get the next solution")
    input("Press enter to exit")

'''
Features to add in the bot:
    College Schedule Bot
    Custom GPA Calculator
    Word games (e.g., word chains, riddles)
'''