import os
import requests
from bs4 import BeautifulSoup
import re
import tkinter as tk
from tkinter import messagebox, filedialog

def download_images(keywords, num_images, save_dir):
    # Create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Google Image search URL
    GOOGLE_IMAGE_SEARCH_URL = "https://www.google.com/search?tbm=isch&q="

    # Headers to mimic a browser visit
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    for keyword in keywords:
        print(f"Searching for {keyword}...")

        search_url = GOOGLE_IMAGE_SEARCH_URL + keyword.replace(" ", "+")
        response = requests.get(search_url, headers=HEADERS)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            img_tags = soup.find_all("img", {"src": re.compile(r"^https://")})
            
            if not img_tags:
                print(f"No images found for {keyword}.")
                continue
            
            for i, img_tag in enumerate(img_tags[:num_images]):
                img_url = img_tag['src']
                img_data = requests.get(img_url).content
                img_name = f"{keyword}_{i + 1}.jpg"
                img_path = os.path.join(save_dir, img_name)
                
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Downloaded {img_url} to {img_path}")
        else:
            print(f"Failed to search for {keyword}: {response.status_code}")

def on_download():
    keywords = keywords_entry.get().split(',')
    keywords = [keyword.strip() for keyword in keywords]
    num_images = int(num_images_entry.get())
    save_dir = save_dir_entry.get()
    if not save_dir:
        messagebox.showerror("Error", "Please select a directory to save images.")
        return
    download_images(keywords, num_images, save_dir)
    messagebox.showinfo("Success", "Images downloaded successfully!")

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_dir_entry.delete(0, tk.END)
        save_dir_entry.insert(0, directory)

# Create GUI
root = tk.Tk()
root.title("Image Downloader")

tk.Label(root, text="Enter keywords (comma-separated):").pack(pady=5)
keywords_entry = tk.Entry(root, width=50)
keywords_entry.pack(pady=5)

tk.Label(root, text="Enter the number of images to download per keyword:").pack(pady=5)
num_images_entry = tk.Entry(root, width=10)
num_images_entry.pack(pady=5)

tk.Label(root, text="Select directory to save images:").pack(pady=5)
save_dir_entry = tk.Entry(root, width=50)
save_dir_entry.pack(pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.pack(pady=5)

download_button = tk.Button(root, text="Download Images", command=on_download)
download_button.pack(pady=20)

# Run the GUI loop
root.mainloop()
