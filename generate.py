import pickle
import numpy as np
from tensorflow.keras.models import load_model
from music21 import stream, note, chord

# Load notes
with open('notes.pkl', 'rb') as f:
    notes = pickle.load(f)

pitchnames = sorted(set(notes))
n_vocab = len(pitchnames)

note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

model = load_model("music_model.h5")

sequence_length = 100

start = np.random.randint(0, len(notes)-sequence_length)
pattern = notes[start:start+sequence_length]
pattern = [note_to_int[n] for n in pattern]

prediction_output = []

for note_index in range(200):   # Generate 200 notes
    prediction_input = np.reshape(pattern, (1, sequence_length, 1))
    prediction_input = prediction_input / float(n_vocab)

    prediction = model.predict(prediction_input, verbose=0)
    index = np.argmax(prediction)
    result = int_to_note[index]

    prediction_output.append(result)

    pattern.append(index)
    pattern = pattern[1:len(pattern)]

# Convert to MIDI
offset = 0
output_notes = []

for pattern in prediction_output:
    if ('.' in pattern) or pattern.isdigit():
        notes_in_chord = pattern.split('.')
        notes = []
        for current_note in notes_in_chord:
            new_note = note.Note(int(current_note))
            notes.append(new_note)
        new_chord = chord.Chord(notes)
        new_chord.offset = offset
        output_notes.append(new_chord)
    else:
        new_note = note.Note(pattern)
        new_note.offset = offset
        output_notes.append(new_note)

    offset += 0.5

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp='generated_music.mid')

print("Music Generated! Check generated_music.mid")