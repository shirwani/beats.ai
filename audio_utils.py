import librosa
import librosa.display
import numpy as np
from scipy.stats import mode
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='librosa')
warnings.filterwarnings("ignore", category=FutureWarning, module='librosa')


def analyze_audio_features(audio_file):
    """Compute key, time signature, tempo, energy, danceability, and more."""

    # 🎵 Load the audio file
    y, sr = librosa.load(audio_file, sr=None)

    # 🎚️ Compute Tempo (BPM)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = round(float(tempo), 4)

    # 🔥 Compute Energy Level (RMS Energy)
    rms = librosa.feature.rms(y=y)[0]
    mean_rms = np.mean(rms)
    energy_level = "Low" if mean_rms < 0.02 else "Medium" if mean_rms < 0.06 else "High"

    # 🕺 Compute Danceability (Using Zero Crossing Rate)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    mean_zcr = np.mean(zcr)
    danceability_score = (bpm / 200) + (1 - mean_zcr)  # Scaled metric
    danceability = "Low" if danceability_score < 0.4 else "Medium" if danceability_score < 0.7 else "High"

    # 🎼 Compute Melodic Complexity (Pitch Variation)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    unique_pitches = np.sum(np.any(pitches > 0, axis=0))
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    harmonic_variability = np.var(chroma)
    complexity_score = (unique_pitches / 100) + (harmonic_variability / 10)
    complexity = "Simple" if complexity_score < 0.3 else "Moderate" if complexity_score < 0.7 else "Complex"

    # 🎤 Compute Speechiness (Higher ZCR = More Speech)
    speechiness_score = np.mean(zcr)

    # 🔊 Compute Loudness
    loudness_db = 20 * np.log10(np.mean(rms))
    if np.isinf(loudness_db) and loudness_db < 0:
        loudness_db = -100

    # 🎵 Compute Valence (Happiness Level via Spectral Brightness)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    mean_brightness = np.mean(spectral_centroid)
    valence_score = (mean_brightness / 5000) + (tempo / 200)
    valence_score = min(max(valence_score, 0), 1)  # Keep within 0 - 1 range

    # 🎼 Compute Key and Mode
    chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = chroma_cqt.mean(axis=1)
    key_index = np.argmax(chroma_mean)
    key_mapping = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    detected_key = key_mapping[key_index]
    if chroma_mean[0] > chroma_mean[5]:
        mode_estimation = "Major"
        key_mode = 1
    else:
        mode_estimation = "Minor"
        key_mode = 0


    # 🥁 Compute Time Signature
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    beat_intervals = np.diff(librosa.frames_to_time(beat_frames, sr=sr))
    if len(beat_intervals) > 0:
        avg_beat_interval = float(mode(np.round(tempo / beat_intervals))[0])
    else:
        avg_beat_interval = 4  # Default to 4/4 if no beats detected
    time_signature = int(avg_beat_interval)/4

    # 🎶 Store all results
    results = {
        "tempo":            bpm,
        "energy":           round(float(mean_rms), 4),
        "danceability":     round(float(danceability_score), 4),
        "complexity":       round(float(complexity_score), 4),
        "speechiness":      round(float(speechiness_score), 4),
        "loudness":         round(float(loudness_db), 4),
        "valence":          round(float(valence_score), 4),
        "time_signature":   time_signature,
        "key":              int(key_index),
        "key_mode":         key_mode
    }

    print(f"\n🎵 Analysis for: {audio_file}")
    for key, value in results.items():
        print(f"🔹 {key}: {value}")

    return results

