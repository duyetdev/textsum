import pytext_mod
import json


def summarize(input_string, phrase_limit=1, word_limit=50):
    def prepare_text(text):
        obj = {}
        obj['id'] = '123'
        obj['text'] = text
        return pytext_mod.json_gen([obj])

    # Statistical parsing/tagging
    tagged = []
    for graf in pytext_mod.parse_doc(prepare_text(input_string)):
        tagged.append(json.loads(pytext_mod.pretty_print(graf._asdict())))

    # Get key phrases
    graph, ranks = pytext_mod.text_rank(tagged)

    key_phrase = []
    for rl in pytext_mod.normalize_key_phrases(tagged, ranks):
        key_phrase.append(json.loads(pytext_mod.pretty_print(rl._asdict())))

    # Ranking
    kernel = pytext_mod.rank_kernel(pytext_mod.json_gen(key_phrase))

    top_sens = []
    for s in pytext_mod.top_sentences(kernel, tagged):
        top_sens.append(json.loads(pytext_mod.pretty_print(s._asdict())))

    phrases = ", ".join([p for p in pytext_mod.limit_keyphrases(key_phrase, phrase_limit=phrase_limit)])
    sent_iter = sorted(pytext_mod.limit_sentences(top_sens, word_limit=word_limit), key=lambda x: x[1])
    s = []

    for sent_text, idx in sent_iter:
        s.append(pytext_mod.make_sentence(sent_text))

    graf_text = " ".join(s)
    return graf_text, phrases

if __name__ == "__main__":
    input_string = "text summarization is an application of natural language processing and is becoming more popular for its useful applications. Text summarization is a process of shortening original document and producing a summary by retaining important information of the original document. The report is to introduce this insteresting yet challenging problem."
    graf_text, phrases = summarize(input_string)

    print(graf_text)
