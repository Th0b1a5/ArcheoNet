import base64
import os
from tkinter import filedialog, Tk

def generate_assets_string():
    # Hide the main tkinter window
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    # 1. Select the file
    file_path = filedialog.askopenfilename(
        title="Select Image to Encode",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp *.gif")]
    )

    if not file_path:
        print("No file selected.")
        return

    # 2. Get file extension for the data header
    ext = os.path.splitext(file_path)[1].replace(".", "").lower()
    if ext == "jpg": ext = "jpeg"

    # 3. Read and Encode
    with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # 4. Format the output
    variable_name = "IMAGE_DATA"
    full_output = f'{variable_name} = "{encoded_string}"'
    
    # 5. Print to console (and optionally save to file)
    print("\n" + "="*30)
    print(f"SUCCESS: {os.path.basename(file_path)} encoded.")
    print("="*30 + "\n")
    print(full_output)
    print("\n" + "="*30)
    print("Copy the line starting with IMAGE_DATA and paste it into assets.py")

if __name__ == "__main__":
    generate_assets_string()