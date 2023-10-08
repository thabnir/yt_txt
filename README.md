# yt_txt

yt_txt is a practical Python program built to convert spoken data in YouTube videos into written text with the [Whisper ASR](https://openai.com/research/whisper).

## Prerequisites

To set up, you will require:

- Python 3.x (should be compatible with Python 3.8+)
- Any additional dependencies stipulated in the 'requirements.txt' document.

Ensure you have the [`ffmpeg`](https://ffmpeg.org/) command-line tool installed in your environment. It is available from most package managers:

```bash
# on Ubuntu or Debian
sudo apt update && sudo apt install ffmpeg

# on Arch Linux
sudo pacman -S ffmpeg

# on MacOS using Homebrew (<https://brew.sh/>)
brew install ffmpeg

# on Windows using Chocolatey (<https://chocolatey.org/>)
choco install ffmpeg

# on Windows using Scoop (<https://scoop.sh/>)
scoop install ffmpeg
```

You may need to install [Rust](http://rust-lang.org/) if [tiktoken](https://github.com/openai/tiktoken) does not offer a pre-built wheel for your platform.

## Installation

Initiate the set up process by cloning this repo to your local environment or by downloading the script file.

Next, proceed to install the essential Python packages by executing the following command:

```bash
pip install -r requirements.txt
```

## Usage

Run the yt_txt script by using the following command and provide the URL of the video that needs transcription:

```bash
python yt_txt.py <YouTube_URL>
```

Replace <YouTube_URL> with the URL of your desired video.

By default, the audio of the video will be downloaded as an mp3 file and saved to the `audio` directory, and the transcription will be saved as a txt file in the `transcripts` directory.

You can customize the output directory and other options using command-line arguments. Use the -h or --help flag to see available options and their descriptions.

The transcript will be printed to the console and saved in a text file with the same name as the video title in the specified output directory.

## Licensing

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Acknowledgements

- [Whisper ASR](https://github.com/openai/whisper) - The Automatic Speech Recognition system by [OpenAI](https://openai.com/).
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A command-line program to download videos from YouTube and other sites.

The primary script file for this program is yt_txt.py.
