import nltk
from dotenv import load_dotenv

def create_picture_list(transcript: list[tuple[str, list[tuple[float, float, str]]]]):
    ALLOW_POS = "JN"

    pictures = []

    for text, words in transcript:
        tokenized_text = nltk.word_tokenize(text)
        picture_candidate = [( i, word ) for i, (word, pos) in enumerate(nltk.pos_tag(tokenized_text)) if pos[0] in ALLOW_POS]

        for i, word in picture_candidate:
            start, _, _ = words[i]
            
            pictures.append((start, word))

    return pictures
        
def parse_transcript(transcript_path: str) -> list[tuple[int, int, str]]:
    transcript = []
    with open(transcript_path) as file:
        
        while (line := file.readline()) != "":
            parts = line.strip().split()

            if len(parts) < 3: continue

            try:
                start, end = int(parts[0]), int(parts[1])
                text = " ".join(parts[2:])
            except ValueError:
                continue

            cleaned_text = "".join([c for c in text.lower() if c.isalnum() or c.isspace()])
            transcript.append((start, end, cleaned_text))

    return transcript

if __name__ == '__main__':
    load_dotenv()

    nltk.download('punkt_tab')
    nltk.download('average_perceptron_tagger_eng')
   
    import audio_transcriber

    transcript = audio_transcriber.transcribe_audio_precise("./test/speech.wav")
    print(create_picture_list(transcript))
    
