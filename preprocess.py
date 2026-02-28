import os
from music21 import converter, note, chord
import pickle

notes = []

# Walk through all files in dataset and subfolders
for root, dirs, files in os.walk("dataset"):
    for file in files:
        if file.endswith(".mid") or file.endswith(".midi"):
            file_path = os.path.join(root, file)
            print("Parsing", file_path)
            try:
                midi = converter.parse(file_path)
                for element in midi.flat.notes:
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        notes.append('.'.join(str(n) for n in element.normalOrder))
            except Exception as e:
                print(f"Could not parse {file_path}: {e}")

print("Total notes extracted:", len(notes))

with open('notes.pkl', 'wb') as f:
    pickle.dump(notes, f)

print("Preprocessing Complete!") 