import os
import pandas as pd
import torchaudio
import datasets

# Function to load audio dataset
def load_audio_data(audio_path, text_path):
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read().strip()  # Read the transcript
        
    return [{"audio": audio_path, "text": text}]

# Load training and validation data
dataset_dict = {
    "train": load_audio_data("./dataset/train.mp3", "./dataset/train.txt"),
    "validation": load_audio_data("./dataset/validation.mp3", "./dataset/validation.txt"),
}

# Convert to Hugging Face dataset format
dataset = datasets.DatasetDict({
    split: datasets.Dataset.from_pandas(pd.DataFrame(data))
    for split, data in dataset_dict.items()
})

# Convert audio column to Hugging Face Audio format
dataset = dataset.cast_column("audio", datasets.Audio(sampling_rate=16000))

# Print dataset structure
print(dataset)

dataset.save_to_disk("hf_audio_dataset")

dataset.push_to_hub("elifsorguc/fonetika")
