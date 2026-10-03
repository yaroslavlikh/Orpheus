import mlx_whisper

check_text = []
real_text = ''
SAMPLE_RATE = 16_000

def transcribe_audio(audio):
    global check_text, real_text
    result = mlx_whisper.transcribe(audio,
                                     path_or_hf_repo="mlx-community/whisper-large-v3-turbo-4bit",
                                     no_speech_threshold=0.6,
                                     word_timestamps=True)
    words = [w for segment in result.get("segments", []) for w in segment.get("words", [])]
    tmp_text = [w["word"].strip() for w in words]

    if not check_text:
        check_text = tmp_text
        return real_text, audio

    m = 0
    while m < len(check_text) and m < len(tmp_text) and check_text[m] == tmp_text[m]:
        real_text += tmp_text[m] + ' '
        m += 1

    check_text = tmp_text[m:]

    if m > 0:
        cut_sample = int(words[m - 1]["end"] * SAMPLE_RATE)
        audio = audio[cut_sample:]

    return real_text, audio