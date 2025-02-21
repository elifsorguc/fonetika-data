from praatio import textgrid

# Load the TextGrid file
tg = textgrid.openTextgrid("output/aligned/7506.TextGrid", False)

# Print available tiers
tier_names = tg.tierNames
print(f"Available tiers: {tier_names}")

# Loop through tiers using `getTier` method
for tier_name in tier_names:
    tier = tg.getTier(tier_name)  # Correct method to access the tier
    print(f"Tier: {tier_name}")

    # Loop through intervals in the tier
    for start, end, label in tier.entries:  # Correct attribute to access intervals
        if label.strip():  # Only print non-empty labels
            print(f"{start:.2f} - {end:.2f}: {label}")
