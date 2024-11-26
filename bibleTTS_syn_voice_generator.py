import pandas as pd
import os
from typing import Optional
import subprocess
import argparse

class BibleTTSGenerator():

    def __init__(self, csv: str, language: str = None, model: str = None):
        self.data = pd.read_csv(csv,
                         header=0,
                         usecols=['Unique ID', 'Sentence (Translation in Target Language )'],
                         dtype={'Unique ID': str, 'Sentence (Translation in Target Language )': str})

        self.data = self.data.rename(columns={'Unique ID': 'unique_ID', 'Sentence (Translation in Target Language )': 'sentence'})

        if language is None:
            self.language = "hausa"
        else:
            self.language = language

        os.makedirs(os.path.dirname(f"{language}/"), exist_ok=True)

        if model is None:
            self.model = "tts_models/hau/openbible/vits"
        else:
            self.model = model

    def generate_voice(self, n: Optional[int] = None):
        if n is not None:
            for row in self.data[:n].itertuples():
                self.__call_tts__(unique_ID=row.unique_ID, sentence=row.sentence, model=self.model)
        else:
            for row in self.data.itertuples():
                self.__call_tts__(unique_ID=row.unique_ID, sentence=row.sentence, model=self.model)


    def __call_tts__(self, unique_ID: str, sentence: str, model: str):
        out_path = f"{self.language}/{self.language}_{unique_ID}.wav"

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

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process some input variables.")
    parser.add_argument("--csv", type=str, required=True,help="Path to csv file to use")
    parser.add_argument("--n", type=int, required=False, help="Number of rows to use")
    parser.add_argument("--language", type=int, required=False, help="Language in which the audio is to be created. Default: Hausa")
    parser.add_argument("--model", type=int, required=False, help="Which Coqui TTS model to use. Default: tts_models/hau/openbible/vits")

    # Parse the arguments
    args = parser.parse_args()

    syn_voice_generator = BibleTTSGenerator(csv=args.csv, language=args.language, model=args.model)

    syn_voice_generator.generate_voice(n=args.n)


