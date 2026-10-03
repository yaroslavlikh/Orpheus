from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

name = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(name, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(name).to("mps")

def translate(text):
    print("Перевод текста...")
    inputs = tok(text, return_tensors="pt", padding=True).to("mps")
    out = model.generate(**inputs, forced_bos_token_id=tok.convert_tokens_to_ids("rus_Cyrl"), max_new_tokens=200)
    return tok.batch_decode(out, skip_special_tokens=True)