#!/bin/bash

# Path to your corpus
CORPUS_DIR="./mfa_align_aysegul/corpus"

# Number of speakers to create
NUM_SPEAKERS=10

# Get the list of files in the corpus
FILES=("$CORPUS_DIR"/*)

# Calculate the number of files per speaker
FILES_PER_SPEAKER=$(( ${#FILES[@]} / $NUM_SPEAKERS ))

# Create speaker directories and move files
for ((i=1; i<=NUM_SPEAKERS; i++)); do
  SPEAKER_DIR="$CORPUS_DIR/speaker$i"
  mkdir -p "$SPEAKER_DIR"
  
  # Move files to the speaker directory
  for ((j=0; j<FILES_PER_SPEAKER; j++)); do
    FILE_INDEX=$(( (i-1) * FILES_PER_SPEAKER + j ))
    if [[ $FILE_INDEX -lt ${#FILES[@]} ]]; then
      mv "${FILES[$FILE_INDEX]}" "$SPEAKER_DIR/"
    fi
  done
done

echo "Corpus split into $NUM_SPEAKERS speakers."