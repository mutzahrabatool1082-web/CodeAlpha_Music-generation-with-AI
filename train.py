import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical

# Load notes
with open('notes.pkl', 'rb') as f:
    notes = pickle.load(f)
    notes = notes[:40000]   # limit data for faster training

# Get unique notes
pitchnames = sorted(set(notes))
n_vocab = len(pitchnames)

# Create mapping
note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

sequence_length = 50
network_input = []
network_output = []

for i in range(0, len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]
    network_input.append([note_to_int[note] for note in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)

# Reshape input
network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
network_input = network_input / float(n_vocab)

network_output = to_categorical(network_output)

# Build LSTM Model
model = Sequential()
model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
model.add(Dropout(0.3))
model.add(LSTM(256))
model.add(Dense(256))
model.add(Dropout(0.3))
model.add(Dense(n_vocab, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam')

print("Training started...")
model.fit(network_input, network_output, epochs=3, batch_size=128)

model.save("music_model.h5")

print("Training Complete!")