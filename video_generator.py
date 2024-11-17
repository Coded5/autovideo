import ffmpeg
import os
import sys

def create_video(
    transcript: list[tuple[str, list[tuple[float, float, str]]]],
    audio_path: str,
    output_path: str
):

    time_start = transcript[0][1][0][0]
    time_end   = transcript[-1][1][-1][1]

    duration = time_end - time_start
    end_at = duration + 0.2
    color = 'white'
    width, height = 1920, 1080

    stream = (
        ffmpeg
        .input(f'color={color}:{width}x{height}:d={duration}', f='lavfi')
        .filter('fps', fps=60, round='up')
    )

    pictures = sorted(
        [file for file in os.listdir('./temp/')],
        key=lambda x: int(x.split('.')[0])
    )

    IMG_WIDTH, IMG_HEIGHT = 1280, 720

    POS_X = (width - IMG_WIDTH) // 2
    POS_Y = 32

    for i, pic in enumerate(pictures[:-10]):
        overlay = (
            ffmpeg
            .input(f"./temp/{pic}")
            .filter('scale', IMG_WIDTH, IMG_HEIGHT)
        )

        start = float(pic.split('.')[0]) / 1000
        end   = float(pictures[i + 1].split('.')[0]) / 1000 if i+1 < len(pictures) else (end_at - 0.2)

        stream = (
            ffmpeg
            .filter([stream, overlay], 'overlay', enable=f'between(t, {start}, {end})', x=POS_X, y=POS_Y)
        )

    for text, words in transcript: 
        start = words[0][0]
        end   = words[-1][1]
        stream = stream.drawtext(
            text=text,
            x='(w-text_w)/2',
            y='(h-text_h)-32',
            fontsize=48,
            fontcolor='black',
            enable=f'between(t, {start}, {end})'
        )
            
    audio = ffmpeg.input(audio_path)

    ffmpeg.output(
        stream, 
        audio, 
        output_path
    ).run(
        overwrite_output=True, 
        capture_stdout=True, 
        capture_stderr=True
    )

if __name__ == '__main__':
    import audio_transcriber 

    transcript = audio_transcriber.transcribe_audio_precise("./speech.mp3")
    try:
        create_video(transcript, './speech.mp3', './output.mp4')
    except ffmpeg.Error as e:
        with open("out.log", "w") as file:
            file.write(e.stdout.decode('utf8'))
        with open("error.log", "w") as file: 
            file.write(e.stderr.decode('utf8'))
