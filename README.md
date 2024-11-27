# SynVoices - Bible TTS Generator

SynVoices is a Python-based tool for generating synthetic voices for Bible translations using [Coqui TTS](https://github.com/coqui-ai/TTS). This tool reads a CSV file containing Bible verses or sentences in a target language and creates audio files in the specified language.

## Features

- Converts sentences from a CSV file into audio files using Coqui TTS.
- Supports customizable TTS models.
- Automatically organizes audio files by language.
- Default support for Hausa with pre-configured settings for `tts_models/hau/openbible/vits`.

---

## Project Structure

synvoices/<br>
├── hausa/                            # Output directory for generated audio files<br>
├── .gitignore                        # Ignored files and directories<br>
├── bibleTTS_syn_voice_generator.py   # Core Python script for generating audio<br>
├── poetry.lock                       # Poetry lock file for dependency management<br>
├── pyproject.toml                    # Poetry configuration file<br>
└── README.md                         # Project documentation<br>

---

## Prerequisites

- Python 3.8 or higher
- [Coqui TTS](https://github.com/coqui-ai/TTS)
- Poetry for dependency management

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd synvoices
```

2.	Install dependencies using Poetry:
```bash
poetry install
```

3. Start poetry shell
```bash
poetry shell
```

## Usage

### Command-Line Usage

The bibleTTS_syn_voice_generator.py script processes a CSV file and generates audio files for the text it contains.

```bash
python bibleTTS_syn_voice_generator.py --csv <path-to-csv> [--n <number-of-rows>] [--language <language>] [--model <tts-model>]
```

### Arguments
	--csv: (required) Path to the CSV file containing the text data.
	--n: (optional) Number of rows to process from the CSV. Default: Process all rows.
	--language: (optional) Language for the generated audio. Default: hausa.
	--model: (optional) TTS model to use. Default: tts_models/hau/openbible/vits.

### Example
To generate audio for the first 5 rows of a CSV file using the default language and model:
```commandline
python bibleTTS_syn_voice_generator.py --csv="bmgf_cg_hausa_round12_merged - bmgf_cg_hausa_round12_merged.csv" --n=5
```

### Output

Generated audio files are saved in the <language>/ directory (e.g., hausa/) with filenames in the format <language>_<unique_ID>.wav.