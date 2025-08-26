#File organizer

A simple Python script that helps organize files in a directory by sorting them into folders based on their extensions. It automatically creates folders like Images, Documents, Videos, Music, etc., and moves files into them for better management.🚀 Features

Organizes files by their type (images, documents, videos, audio, archives, etc.)

Creates folders automatically if they don’t exist

Works on Windows, macOS, and Linux

Lightweight and easy to use▶️ Usage

Run the script with Python:

python organizer.py

By default, it organizes files in the current directory.

You can also specify a custom folder path:

python organizer.py "C:/Users/YourName/Downloads"

📂 Example

Before:

Downloads/ │── photo1.jpg │── music.mp3 │── resume.pdf │── movie.mp4

After running the script:

Downloads/ │── Images/ │ └── photo1.jpg │── Music/ │ └── music.mp3 │── Documents/ │ └── resume.pdf │── Videos/ │ └── movie.mp4

🔮 Future Improvements

Add support for custom folder mappings

Option to undo changes

GUI version
