phones = set()
with open("filtered_turkish_dict.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) > 1:
            # All parts after the first word are phone symbols
            phones.update(parts[1:])
print(sorted(phones))
