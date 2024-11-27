import pandas as pd
import os
from typing import Optional
import subprocess
import argparse

class BibleTTSGenerator:
    """
    A class to generate text-to-speech (TTS) audio files for Bible translations in a specified language.
    It reads a CSV file containing text data and converts it into audio files using the Coqui TTS library.
    """

    def __init__(self, csv: str, language: str = None, model: str = None):
        """
        Initializes the BibleTTSGenerator class.

        Args:
            csv (str): Path to the input CSV file containing text data.
            language (str, optional): Language for the generated audio. Default is 'hausa'.
            model (str, optional): Coqui TTS model to use for synthesis.
                                    Default is 'tts_models/hau/openbible/vits'.
        """
        # Read the input CSV file and extract required columns
        self.data = pd.read_csv(
            csv,
            header=0,
            usecols=['Unique ID', 'Sentence (Translation in Target Language )'],
            dtype={'Unique ID': str, 'Sentence (Translation in Target Language )': str}
        )
        # Rename columns for easier access
        self.data = self.data.rename(
            columns={
                'Unique ID': 'unique_ID',
                'Sentence (Translation in Target Language )': 'sentence'
            }
        )

        # Set default language if not provided
        self.language = language if language else "hausa"

        # Create the output directory for the specified language
        os.makedirs(os.path.dirname(f"{self.language}/"), exist_ok=True)

        # Set the default TTS model if not provided
        self.model = model if model else "tts_models/hau/openbible/vits"

    def generate_voice(self, n: Optional[int] = None):
        """
        Generates audio files from the text data.

        Args:
            n (int, optional): Number of rows to process from the CSV file.
                               If not provided, all rows will be processed.
        """
        # Iterate over rows in the data and generate audio
        if n is not None:
            for row in self.data[:n].itertuples():
                self.__call_tts__(unique_ID=row.unique_ID, sentence=row.sentence, model=self.model)
        else:
            for row in self.data.itertuples():
                self.__call_tts__(unique_ID=row.unique_ID, sentence=row.sentence, model=self.model)

    def __call_tts__(self, unique_ID: str, sentence: str, model: str):
        """
        Calls the Coqui TTS CLI to generate an audio file for a given sentence.

        Args:
            unique_ID (str): Unique identifier for the sentence (used for naming the audio file).
            sentence (str): The text to convert into speech.
            model (str): The TTS model to use for synthesis.
        """
        # Define the output path for the generated audio file
        out_path = f"{self.language}/{self.language}_{unique_ID}.wav"

        # Run the Coqui TTS command
        result = subprocess.run(
            [
                "tts",
                "--text", sentence,
                "--model_name", model,
                "--out_path", out_path,
            ],
            capture_output=True,
            text=True,
        )

        # Print command output for debugging purposes
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)


if __name__ == "__main__":
    # Set up the argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Generate TTS audio files for Bible translations.")
    parser.add_argument("--csv", type=str, required=True, help="Path to the input CSV file.")
    parser.add_argument("--n", type=int, required=False, help="Number of rows to process from the CSV file.")
    parser.add_argument("--language", type=str, required=False, help="Language for the audio files. Default is 'hausa'.")
    parser.add_argument("--model", type=str, required=False, help="TTS model to use. Default is 'tts_models/hau/openbible/vits'.")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Initialize the BibleTTSGenerator with the provided arguments
    syn_voice_generator = BibleTTSGenerator(csv=args.csv, language=args.language, model=args.model)

    # Generate the TTS audio files
    syn_voice_generator.generate_voice(n=args.n)