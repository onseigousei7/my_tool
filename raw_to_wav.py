import wave
import glob
import os
import librosa
import soundfile as sf

def convert_one_file(input_path, output_path):
    with open(input_path, "rb") as inp_f:
        data = inp_f.read()
        with wave.open(output_path, "wb") as out_f:
            out_f.setnchannels(1)
            out_f.setsampwidth(2)
            out_f.setframerate(48000)
            out_f.writeframesraw(data)
    y, sr = librosa.core.load(output_path, sr=32000, mono=True)
    sf.write(output_path, y, sr, subtype="PCM_16")
    

def convert_files(raw_folder):
    input_paths = glob.glob('{}/*.raw'.format(raw_folder))

    for input_path in input_paths:
        base, ext = os.path.splitext(input_path)
        basename = os.path.basename(base)
        output_path = '{}/{}.wav'.format(raw_folder, basename)
        convert_one_file(input_path, output_path)