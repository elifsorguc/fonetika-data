import os

# List of lab file numbers to remove
lab_numbers_to_remove = {
    "648", "2464", "6443", "6558", "6712", "6822", "7262", "7480", "8184", "8932",
    "9015", "9030", "9979", "11457", "11490", "11576", "11621", "11634", "11651",
    "11886", "12989", "13464"
}

lab_folder = "corpus"

# Remove matching .lab files
for num in lab_numbers_to_remove:
    lab_file = os.path.join(lab_folder, f"{num}.lab")
    if os.path.exists(lab_file):
        os.remove(lab_file)
        print(f"✅ Removed: {lab_file}")
    else:
        print(f"⚠️ Not found: {lab_file}")

print("🎯 Cleanup complete!")
