A Python-based command-line tool to organize files in a directory into categorized subfolders (like Documents, Images, Videos, etc.). It also supports logging and customizable log file locations.

🚀 Features

- Automatically sorts files by extension into predefined categories.
- Handles common file types: documents, images, videos, audio, archives, executables, code, and others.
- Logs all operations with timestamps for traceability.
- Command-line interface (CLI) with helpful options.
- Error-handling for file move conflicts and invalid directories.
- Skips subdirectories and its own script/log files during processing.

📦 Categories

Supported file type categories:

- Documents: .pdf, .docx, .txt, .xlsx, .pptx, .csv, .rtf, .odt
- Images: .jpg, .jpeg, .png, .gif, .bmp, .svg, .tiff, .webp
- Videos: .mp4, .mov, .avi, .mkv, .flv, .wmv, .webm, .m4v
- Audio: .mp3, .wav, .aac, .flac, .ogg, .m4a, .wma
- Archives: .zip, .rar, .7z, .tar, .gz, .bz2
- Executables: .exe, .msi, .dmg, .pkg, .deb, .rpm
- Code: .py, .js, .html, .css, .java, .cpp, .c, .php, .json, .xml
- Others: All unmatched files

🛠️ Requirements

- Python 3.13
- Standard Libraries Used:
  - `os`
  - `shutil`
  - `logging`
  - `datetime`
  - `argparse`

📄 Usage

bash
Organize current directory
python file_organizer.py .

Organize a specific directory (e.g., Downloads)
python file_organizer.py ~/Downloads

Organize with custom log directory
python file_organizer.py . --log-dir ~/logs

View supported categories
python file_organizer.py --categories
