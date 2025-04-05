from customtkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO
import yt_dlp
from tkinter import filedialog

# === App mian things i think ===
app = CTk()
app.geometry("800x600")
app.title("Yeet The Video 🎬")
set_appearance_mode("dark")
set_default_color_theme("blue")

# === Global Variables (just put it yoursilf) ===
download_folder = ""

# === Status Label (the top text you see)===
status_label = CTkLabel(app, text="Paste a link and Yeet it 🔗", font=("Arial", 20, "bold"))
status_label.pack(pady=(25, 10))

# === Input Section the box  ===
top_frame = CTkFrame(app, fg_color="transparent")
top_frame.pack(pady=(5, 20))

entry = CTkEntry(master=top_frame, placeholder_text="Paste video link", width=450)
entry.pack(side="left", padx=(0, 12))

lookup_btn = CTkButton(master=top_frame, text="Lookup 🔍", command=lambda: click_handler())
lookup_btn.pack(side="left")

# === Video Info Box (yt) ===
info_frame = CTkFrame(app, corner_radius=12)
info_frame.configure(width=740, height=280)
info_frame.place_forget()

thumb_label = CTkLabel(info_frame, text="")
thumb_label.grid(row=0, column=0, rowspan=3, padx=(20, 15), pady=20)

title_label = CTkLabel(info_frame, text="Video Title Here", font=("Arial", 16, "bold"), wraplength=400, justify="left")
title_label.grid(row=0, column=1, sticky="w", pady=(30, 10), padx=(0, 10))

mp4_btn = CTkButton(info_frame, text="Download MP4 🌐", width=180, command=lambda: download_video(entry.get(), "mp4"))
mp4_btn.grid(row=1, column=1, sticky="w", pady=(5, 5), padx=(0, 10))

mp3_btn = CTkButton(info_frame, text="Download MP3 🎵", width=180, command=lambda: download_video(entry.get(), "mp3"))
mp3_btn.grid(row=2, column=1, sticky="w", pady=(5, 5), padx=(0, 10))

# === Output Console Box ===
output_box = CTkTextbox(app, width=700, height=140, corner_radius=10)
output_box.place_forget()

def show_output(text):
    output_box.place(relx=0.5, rely=1.0, anchor="s")
    output_box.configure(state="normal")
    output_box.insert("end", f"{text}\n")
    output_box.configure(state="disabled")
    output_box.see("end")

# === Video Info Box with Real Image, Title ===
def show_video_info(thumbnail_url, title_text):
    try:
        response = requests.get(thumbnail_url)
        img_data = Image.open(BytesIO(response.content)).resize((240, 135))
        img_data = img_data.convert("RGB")

        bordered_img = Image.new("RGB", (250, 145), (40, 40, 40))  #
        bordered_img.paste(img_data, (5, 5))  

        tk_image = CTkImage(light_image=bordered_img, size=(250, 145))
        thumb_label.configure(image=tk_image, text="")
        thumb_label.image = tk_image

    except Exception as e:
        fallback = Image.new("RGB", (250, 145), (60, 60, 60))
        tk_image = CTkImage(light_image=fallback, size=(250, 145))
        thumb_label.configure(image=tk_image, text="")
        thumb_label.image = tk_image

    title_label.configure(text=title_text)
    status_label.configure(text="🎥 Video Info Loaded!")
    info_frame.place(relx=0.5, rely=0.58, anchor="center")

# === Select Save Location ( it is using tkinter so the ugly thing you seeing it bec of this thing ) ===
def choose_download_folder():
    folder = filedialog.askdirectory()
    if folder:
        return folder
    return ""

# === yt_dlp Download Function ===
def download_video(url, format_code):
    global download_folder

    download_folder = choose_download_folder()
    if not download_folder:
        show_output("❌ Download cancelled. No folder selected.")
        return

    show_output(f"💾 Saving to: {download_folder}")
    show_output(f"📁 Starting {format_code.upper()} download...")

    ydl_opts = {'outtmpl': f'{download_folder}/%(title)s.%(ext)s'}

    if format_code == "mp4":
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        })
    elif format_code == "mp3":
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        show_output(f"✅ Download complete!")
    except Exception as e:
        show_output(f"❌ Error: {e}")

# === yt_dlp Info Extract ===
def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title'),
            'thumbnail': info.get('thumbnail')
        }

# === ho yo ya this helps to make the input work by enter to  ===
def click_handler():
    url = entry.get().strip()
    output_box.place_forget()
    show_output(f"🔍 Looking up: {url}")

    if not url:
        show_output("⚠️ Please enter a valid URL.")
        return

    try:
        data = get_video_info(url)
        show_video_info(data['thumbnail'], data['title'])
        show_output("✅ Found video info successfully!")
    except Exception as e:
        status_label.configure(text="⚠️ Failed to get video info.")
        show_output(f"❌ Error: {e}")

# === Enter Key Support (ya i dont really what this is ) ===
app.bind("<Return>", lambda e: click_handler())

app.mainloop()

#btw reader you are totaly gay 
#what you looking for like bra this is not a good code 
