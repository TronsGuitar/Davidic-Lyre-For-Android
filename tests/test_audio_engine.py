"""Tests for audio engine WAV generation."""

import os
import tempfile
import wave

from app.audio_engine import generate_placeholder_wav, ensure_samples


class TestGeneratePlaceholderWav:
    def test_creates_wav_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.wav")
            generate_placeholder_wav(path, frequency=110.0, duration=0.5)
            assert os.path.exists(path)

    def test_wav_properties(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.wav")
            generate_placeholder_wav(path, frequency=110.0, duration=0.5, sample_rate=44100)
            with wave.open(path, "r") as wf:
                assert wf.getnchannels() == 1
                assert wf.getsampwidth() == 2
                assert wf.getframerate() == 44100
                assert wf.getnframes() == int(44100 * 0.5)

    def test_creates_parent_directories(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "sub", "dir", "test.wav")
            generate_placeholder_wav(path, frequency=110.0, duration=0.3)
            assert os.path.exists(path)


class TestEnsureSamples:
    def test_generates_missing_samples(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            orig_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                notes = ["A2", "B2"]
                freqs = [110.0, 123.47]
                paths = ensure_samples(notes, freqs)
                assert len(paths) == 2
                for note in notes:
                    assert os.path.exists(paths[note])
            finally:
                os.chdir(orig_cwd)
