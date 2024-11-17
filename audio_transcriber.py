import whisper

def transcribe_audio(audio_path) -> list[tuple[int, int, str]]:
    model = whisper.load_model("medium.en")
    raw_transcript: dict = model.transcribe(audio_path) #stop pyright from being angy 
    
    transcript = []

    for segment in raw_transcript['segments']:
        start = int(float(segment['start']) * 1000)
        end   = int(float(segment['end']) * 1000)
        text  = segment['text']        

        cleaned_text = "".join([c for c in text.strip().lower() if c.isalnum() or c.isspace()])
        transcript.append((start, end, cleaned_text))

    return transcript

def transcribe_audio_precise(audio_path: str, model_type: str) -> list[tuple[str, list[tuple[float, float, str]]]]:
    model = whisper.load_model(model_type)
    raw_transcript: dict = model.transcribe(audio_path, word_timestamps=True)

    transcript = []

    for segment in raw_transcript['segments']:
        text  = segment['text']
        words = segment['words']
 
        cleaned_text = "".join([c for c in text.strip().lower() if c.isalnum() or c.isspace()])
        cleaned_words = []
        for word_segment in words:
            word  = word_segment['word']
            word_start = float(word_segment['start'])
            word_end   = float(word_segment['end'])

            cleaned_word = "".join([c for c in word.strip().lower() if c.isalnum()])
            cleaned_words.append((word_start, word_end, cleaned_word))

        transcript.append((cleaned_text, cleaned_words))

    return transcript