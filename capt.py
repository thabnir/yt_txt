import os
import time
import yt_dlp
import argparse
import whisper
import logging


def download_video(youtube_url: str, output_directory: str) -> dict:
    yt_dlp.std_headers["User-Agent"] = "Mozilla/5.0"
    yt_dlp.std_headers["Referer"] = "https://www.youtube.com/"
    yt_dlp.std_headers["Origin"] = "https://www.youtube.com/"

    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "no_check_certificate": True,
        "outtmpl": os.path.join(output_directory, "%(title)s.%(ext)s"),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
        # get the title of the video
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict  # type: ignore


def transcribe_audio(audio_file_path: str, model_version: str):
    model = whisper.load_model(model_version)
    return model.transcribe(audio_file_path)


def main():
    parser = argparse.ArgumentParser(
        description="Download a YouTube video and transcribe its audio using Whisper."
    )
    parser.add_argument("youtube_url", help="YouTube video URL")
    parser.add_argument(
        "--output-directory",
        "-o",
        default="./transcripts",
        help="Output directory for transcripts (default: 'transcripts')",
    )
    parser.add_argument(
        "--audio-file-path",
        "-a",
        default="./audio",
        help="Audio file path (default: 'audio')",
    )
    parser.add_argument(
        "--model",
        default="tiny",
        help="tiny.en, tiny, base.en, base, small.en, small, medium.en, medium, large-v1, large-v2, large. Default: tiny",
    )
    parser.add_argument(
        "--language",
        "-l",
        default="en",
        help="Language code (default: 'en')",
    )
    parser.add_argument(
        # quiet
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress all output except for errors",
    )

    args = parser.parse_args()

    # Set up logging
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    if (
        args.language == "en"
        and "large" not in args.model
        and not args.model.endswith(".en")
    ):
        # if it's english, use the .en models for better results
        # large models don't have english-only versions
        args.model = args.model + ".en"

    # Create the output directory if it doesn't exist
    os.makedirs(args.audio_file_path, exist_ok=True)

    # Download the YouTube video
    info = download_video(args.youtube_url, args.audio_file_path)
    title = info["title"]
    logging.info(f"Downloaded video: {title}")

    # Find the downloaded audio file (assuming it's in mp3 format)
    # at {audio_file_path}{title}.mp3
    audio_path = os.path.join(args.audio_file_path, title + ".mp3")

    if not audio_path:
        logging.error("No audio files found in the output directory.")
    else:
        # Transcribe the audio using the Whisper command-line tool
        logging.info(f"Transcribing audio for {audio_path} with {args.model}...")
        start = time.time()

        transcript = transcribe_audio(audio_path, args.model)

        end = time.time()
        elapsed = end - start
        logging.info(f"Transcription took {elapsed} seconds.")
        text = transcript["text"]

        print(text)

        filename = os.path.basename(audio_path)  # remove extension
        filename = os.path.splitext(filename)[0] + ".txt"
        filename = os.path.join(args.output_directory, filename)

        if not os.path.exists(args.output_directory):
            os.makedirs(args.output_directory)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)  # type: ignore
        logging.info(f"Output to {filename}")


if __name__ == "__main__":
    main()
