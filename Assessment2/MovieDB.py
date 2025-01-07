import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Info Finder")

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack(fill="both", expand=True)

        # Load and resize the background image
        try:
            self.bg_image = Image.open("background.png")  # Make sure to use your own background image file
            self.bg_image = self.bg_image.resize((600, 400), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            print(f"Error loading background image: {e}")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Enter Movie Name:", bg="lightblue")
        self.entry = tk.Entry(self.root)
        self.button = tk.Button(self.root, text="Search", command=self.search_movie)
        self.text_area = tk.Text(self.root, height=10, width=50)

        self.canvas.create_window(300, 50, window=self.label)
        self.canvas.create_window(300, 80, window=self.entry)
        self.canvas.create_window(300, 110, window=self.button)
        self.canvas.create_window(300, 200, window=self.text_area)

    def fetch_movie(self, title):
        api_key = "YOUR_API_KEY"  # Replace with your TMDb API key
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"
        response = requests.get(url)
        print(response.json())  # Print the API response for debugging
        if response.status_code == 200:
            data = response.json()
            return data['results']
        else:
            return None

    def search_movie(self):
        title = self.entry.get()
        movies = self.fetch_movie(title)
        if movies:
            self.text_area.delete('1.0', tk.END)
            for movie in movies:
                self.text_area.insert(tk.END, f"Title: {movie['title']}\n")
                self.text_area.insert(tk.END, f"Release Date: {movie['release_date']}\n")
                self.text_area.insert(tk.END, f"Overview: {movie['overview']}\n")
                self.text_area.insert(tk.END, "-"*30 + "\n")
        else:
            messagebox.showerror("Error", "Movie not found")

root = tk.Tk()
app = MovieApp(root)
root.mainloop()
