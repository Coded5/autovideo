import audio_transcriber
import image_loader
import script_reader
import video_generator
import ffmpeg
import argparse
import os
import nltk
import shutil
from dotenv import load_dotenv

parser = argparse.ArgumentParser()
parser.add_argument('--input', help="Input path", required=True)
parser.add_argument('--output', help="Output path", required=True)
parser.add_argument('--model', help="Select Whisper model", default="medium.en", required=False)
parser.add_argument('--apikey', help="Pexels API key", required=False)

if __name__ == '__main__':
    load_dotenv()
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    model = "medium.en"
    api_key = ""

    if args.apikey:
        api_key = args.apikey
    else:
        api_key = os.getenv("PEXEL_API_KEY")

    if args.model:
        model = args.model

    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger')

    if os.path.exists('./temp/') and os.path.isdir('./temp/'):
        try:
            shutil.rmtree('./temp/')
        except:
            pass

    print("Transcribing Audio...")
    transcript = audio_transcriber.transcribe_audio_precise(input_path)

    print("Gettings URL")
    picture_list = script_reader.create_picture_list(transcript)
    url_list     = image_loader .get_image_urls(picture_list)
    path_table   = image_loader .download_image_from_url(url_list, './temp')

    print("Generating video")    
    try:
        video_generator.create_video(
            transcript,
            input_path,
            output_path
        )
    except ffmpeg.Error as e:
        print("An error occured stdout and stderr logged.")
        with open("stderr.log") as file:
            file.write(e.stderr.decode("utf8"))

        with open("stdout.log") as file:
            file.write(e.stdout.decode("utf8"))

