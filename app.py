import customtkinter as ctk
from tkinter import filedialog, messagebox
from downloader import download_mp3, DownloadCancelled
import threading
import re

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("Dark")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # ===== WINDOW =====
        self.title("YouTube Music MP3 Downloader")
        self.minsize(800, 600)
        self.geometry("1100x750")
        self.resizable(True, True)

        self.cancel_event = threading.Event()
        self.download_thread = None
        self.was_cancelled = False   # 🔥 FIX 1: cancel state flag

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ===== HEADER =====
        header = ctk.CTkFrame(self, corner_radius=18)
        header.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        ctk.CTkLabel(
            header,
            text="🎵 YouTube Music MP3 Downloader",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(14, 4))

        ctk.CTkLabel(
            header,
            text="Album • Playlist • Single Song (MP3 only)",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(0, 8))

        # ===== CONTENT =====
        content = ctk.CTkFrame(self, corner_radius=18)
        content.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        # URL
        ctk.CTkLabel(content, text="YouTube Music URL").grid(row=0, column=0, pady=(12, 4))
        self.url_entry = ctk.CTkEntry(content, height=42, width=720)
        self.url_entry.grid(row=1, column=0)

        # Quality
        ctk.CTkLabel(content, text="MP3 Quality").grid(row=2, column=0, pady=(12, 4))
        self.quality_option = ctk.CTkOptionMenu(
            content,
            values=["320 kbps", "128 kbps"],
            width=200
        )
        self.quality_option.set("320 kbps")
        self.quality_option.grid(row=3, column=0)

        # Mode
        ctk.CTkLabel(content, text="Download Mode").grid(row=4, column=0, pady=(12, 4))
        self.mode_option = ctk.CTkOptionMenu(
            content,
            values=["Album / Playlist", "Single Song"],
            width=220
        )
        self.mode_option.set("Album / Playlist")
        self.mode_option.grid(row=5, column=0)

        # Output
        self.output_dir = "downloads"
        ctk.CTkButton(
            content,
            text="📁 Select Output Folder",
            command=self.select_folder
        ).grid(row=6, column=0, pady=(12, 4))

        # 🔥 FIX 2: show selected output folder
        self.output_label = ctk.CTkLabel(
            content,
            text=f"📂 Output: {self.output_dir}",
            wraplength=700,
            text_color="gray"
        )
        self.output_label.grid(row=7, column=0, pady=(0, 6))

        # Status
        self.status_label = ctk.CTkLabel(
            content,
            text="Status: Idle",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.grid(row=8, column=0, pady=6)

        self.track_label = ctk.CTkLabel(content, text="")
        self.track_label.grid(row=9, column=0, pady=4)

        self.progress = ctk.CTkProgressBar(
            content, width=720, height=18, progress_color="#1f6aa5"
        )
        self.progress.set(0)
        self.progress.grid(row=10, column=0, pady=(6, 2))

        self.percent_label = ctk.CTkLabel(content, text="0%")
        self.percent_label.grid(row=11, column=0)

        # ===== DOWNLOAD LOG =====
        ctk.CTkLabel(
            content, text="Downloaded Files", font=ctk.CTkFont(weight="bold")
        ).grid(row=12, column=0, pady=(14, 4))

        self.log_box = ctk.CTkTextbox(content, height=140)
        self.log_box.grid(row=13, column=0, sticky="ew", padx=10)
        self.log_box.configure(state="disabled")

        # ===== FOOTER =====
        footer = ctk.CTkFrame(self, corner_radius=18)
        footer.grid(row=2, column=0, padx=20, pady=15, sticky="ew")

        self.download_btn = ctk.CTkButton(
            footer, text="⬇ Download", width=200, command=self.start_download
        )
        self.download_btn.pack(side="left", padx=20, pady=10)

        self.cancel_btn = ctk.CTkButton(
            footer, text="⛔ Cancel", width=200,
            fg_color="#b91c1c", hover_color="#991b1b",
            command=self.cancel_download
        )
        self.cancel_btn.pack(side="right", padx=20, pady=10)
        self.cancel_btn.configure(state="disabled")

    # ===== ACTIONS =====
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir = folder
            self.output_label.configure(text=f"📂 Output: {self.output_dir}")

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        self.was_cancelled = False
        self.cancel_event.clear()

        self.progress.set(0)
        self.percent_label.configure(text="0%")

        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

        quality = "320" if "320" in self.quality_option.get() else "128"
        single = self.mode_option.get() == "Single Song"

        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        self.status_label.configure(text="Status: Downloading...")

        self.download_thread = threading.Thread(
            target=self.run_download,
            args=(url, quality, single),
            daemon=True
        )
        self.download_thread.start()

    def cancel_download(self):
        self.was_cancelled = True
        self.cancel_event.set()
        self.status_label.configure(text="Status: Cancelling...")

    def run_download(self, url, quality, single):
        try:
            download_mp3(
                url,
                self.output_dir,
                quality,
                single=single,
                progress_callback=self.update_progress,
                cancel_event=self.cancel_event,
            )

            # ✅ show completed only if not cancelled
            if not self.was_cancelled:
                self.status_label.configure(text="Status: Completed ✅")

        except DownloadCancelled:
            self.status_label.configure(text="Status: Cancelled ❌")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        finally:
            self.download_btn.configure(state="normal")
            self.cancel_btn.configure(state="disabled")

    # ===== PROGRESS CALLBACK =====
    def update_progress(self, d):
        status = d.get("status")

        if status == "downloading":
            percent = d.get("_percent_str", "0%")
            filename = d.get("filename", "")
            name = re.sub(r"\.(webm|m4a|mp3)", "", filename.split("/")[-1])

            self.track_label.configure(text=f"🎵 {name}")
            try:
                self.progress.set(max(0.05, float(percent.replace('%', '')) / 100))
                self.percent_label.configure(text=percent)
            except:
                pass

        elif status == "finished":
            file = d.get("filename")
            if file:
                self.log_box.configure(state="normal")
                self.log_box.insert("end", f"✔ {file}\n")
                self.log_box.configure(state="disabled")


# ===== APP ENTRY POINT =====
if __name__ == "__main__":
    app = App()
    app.mainloop()
