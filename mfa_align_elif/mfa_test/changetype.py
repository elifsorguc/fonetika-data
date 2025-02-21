import os
import subprocess
import multiprocessing

CORPUS_DIR = "corpus"

def detect_encoding(file_path):
    """Detects file encoding using `file -I` command."""
    try:
        result = subprocess.run(["file", "-I", file_path], capture_output=True, text=True)
        encoding = result.stdout.strip().split("charset=")[-1]
        return encoding if encoding else "ISO-8859-1"  # Default fallback
    except Exception as e:
        print(f"⚠️ Error detecting encoding for {file_path}: {e}")
        return "ISO-8859-1"

def fix_encoding(file_path):
    """Converts non-UTF-8 files to UTF-8 or deletes if corrupted."""
    encoding = detect_encoding(file_path)

    if encoding == "utf-8":
        return  # Skip already UTF-8 files

    if encoding == "binary":
        print(f"🚨 Deleting corrupted file: {file_path}")
        os.remove(file_path)  # Remove non-text files
        return

    try:
        temp_file = file_path + ".utf8"
        with open(file_path, "r", encoding=encoding, errors="replace") as infile, open(temp_file, "w", encoding="utf-8") as outfile:
            outfile.write(infile.read())
        os.replace(temp_file, file_path)
        print(f"✅ Fixed encoding: {file_path} ({encoding} → UTF-8)")
    except Exception as e:
        print(f"❌ Failed to convert {file_path}: {e}")

def main():
    """Runs encoding fixes in parallel for speed."""
    lab_files = [os.path.join(CORPUS_DIR, f) for f in os.listdir(CORPUS_DIR) if f.endswith(".lab")]

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        pool.map(fix_encoding, lab_files)

if __name__ == "__main__":
    main()
