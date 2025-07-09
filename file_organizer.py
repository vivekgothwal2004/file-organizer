import os
import shutil
import logging
from datetime import datetime
import argparse

# Define file type categories
FILE_CATEGORIES = {
    "Documents": ['.pdf', '.docx', '.txt', '.xlsx', '.pptx', '.csv', '.rtf', '.odt'],
    "Images": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tiff', '.webp'],
    "Videos": ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.m4v'],
    "Others": [],  # Default category for unmatched files
    "Audio": ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'],
    "Archives": ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    "Executables": ['.exe', '.msi', '.dmg', '.pkg', '.deb', '.rpm'],
    "Code": ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.json', '.xml']
}


def setup_logging(log_dir=None):
    """
    Configure logging for the file organizer.
    Args:
        log_dir (str): Optional directory to store log files
    """
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = f"file_organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path = os.path.join(log_dir, log_filename) if log_dir else log_filename

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filemode='w'  # Overwrite existing log file
    )


def organize_files(target_dir, log_dir=None):
    """
    Organize files in the target directory with error handling and logging.
    Args:
        target_dir (str): Directory to organize
        log_dir (str): Optional directory for log files
    Returns:
        tuple: (success: bool, files_processed: int)
    """
    setup_logging(log_dir)

    try:
        # Validate target directory
        if not os.path.isdir(target_dir):
            raise ValueError(f"Invalid directory: {target_dir}")

        logging.info(f"Starting file organization in: {target_dir}")
        print(f"\nOrganizing files in: {target_dir}")

        # Create category folders if they don't exist
        for category in FILE_CATEGORIES:
            try:
                category_path = os.path.join(target_dir, category)
                if not os.path.exists(category_path):
                    os.makedirs(category_path)
                    logging.info(f"Created directory: {category_path}")
                    print(f"Created {category} directory")
            except Exception as e:
                logging.error(f"Error creating {category} directory: {str(e)}")
                print(f"Error creating {category} directory: {str(e)}")
                continue

        # Create 'Others' folder for uncategorized files
        others_path = os.path.join(target_dir, "Others")
        if not os.path.exists(others_path):
            os.makedirs(others_path)
            logging.info(f"Created directory: {others_path}")
            print("Created Others directory")

        # Scan and classify files
        file_count = 0
        for filename in os.listdir(target_dir):
            try:
                file_path = os.path.join(target_dir, filename)

                # Skip directories, the script itself, and log files
                if (os.path.isdir(file_path) or
                        filename == os.path.basename(__file__) or
                        filename.startswith('file_organizer_') and filename.endswith('.log')):
                    continue

                # Get file extension
                _, ext = os.path.splitext(filename)
                ext = ext.lower()

                # Find the appropriate category
                moved = False
                for category, extensions in FILE_CATEGORIES.items():
                    if ext in extensions:
                        dest_dir = os.path.join(target_dir, category)
                        shutil.move(file_path, os.path.join(dest_dir, filename))
                        logging.info(f"Moved {filename} to {category}")
                        print(f"Moved {filename} to {category}")
                        moved = True
                        file_count += 1
                        break

                # If file doesn't match any category, move to 'Others'
                if not moved:
                    shutil.move(file_path, os.path.join(others_path, filename))
                    logging.info(f"Moved {filename} to Others")
                    print(f"Moved {filename} to Others")
                    file_count += 1

            except shutil.Error as e:
                logging.error(f"File already exists in destination: {filename} - {str(e)}")
                print(f"Warning: {filename} already exists in destination")
            except Exception as e:
                logging.error(f"Error processing {filename}: {str(e)}")
                print(f"Error processing {filename}: {str(e)}")
                continue

        logging.info(f"File organization complete. Processed {file_count} files.")
        print(f"\nFile organization complete. Processed {file_count} files.")
        return True, file_count

    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        print(f"\nFatal error: {str(e)}")
        return False, 0


def display_categories():
    """Display the file categories and their extensions."""
    print("\nFile Categories and Extensions:")
    print("-" * 40)
    for category, extensions in FILE_CATEGORIES.items():
        print(f"{category + ':':<12} {', '.join(extensions)}")
    print("Others:      All other file types")
    print("-" * 40)


def main():
    """
    Command-line interface for the file organizer.
    """
    parser = argparse.ArgumentParser(
        description="Organize files in a directory by their types.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  Organize current directory:   file_organizer.py .
  Organize Downloads:          file_organizer.py ~/Downloads
  With custom log directory:   file_organizer.py . --log-dir ~/logs
  Show categories:             file_organizer.py --categories"""
    )
    parser.add_argument(
        "directory",
        nargs="?",
        help="Directory to organize (default: current directory)",
        default="."
    )
    parser.add_argument(
        "--log-dir",
        help="Directory to save log files (default: current directory)"
    )
    parser.add_argument(
        "--categories",
        help="Display file categories and extensions",
        action="store_true"
    )

    args = parser.parse_args()

    if args.categories:
        display_categories()
        return

    success, count = organize_files(args.directory, args.log_dir)
    if not success:
        print("\nFile organization completed with errors. Check the log file for details.")
    elif count == 0:
        print("\nNo files were processed. The directory may be empty or already organized.")
    else:
        print("\nFile organization completed successfully!")

if __name__ == "__main__":
    main()