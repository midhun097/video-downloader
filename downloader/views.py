from yt_dlp import YoutubeDL
from django.http import FileResponse, HttpResponse
from django.shortcuts import render
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")


def home(request):
    return render(request, "home.html")


def download_video(request):
    if request.method == "POST":
        url = request.POST.get("url")
        quality = request.POST.get("quality")

        os.makedirs(DOWNLOAD_DIR, exist_ok=True)

        if quality == "best":
            format_code = "best"
        else:
            format_code = f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]"

        ydl_opts = {
            "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            "format": format_code,
            "merge_output_format": "mp4",
            "noplaylist": True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                filename = ydl.prepare_filename(info)

                # If merged to mp4, fix extension
                if not filename.endswith(".mp4"):
                    filename = filename.rsplit(".", 1)[0] + ".mp4"

            return FileResponse(
                open(filename, "rb"),
                as_attachment=True,
                filename=os.path.basename(filename),
            )

        except Exception as e:
            return HttpResponse(f"❌ Error: {e}")
