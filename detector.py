import re

class NegationDetector:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def detect_negation(self, sentence):
        negation_words = ["不", "沒", "無", "未", "非", "否", "不想", "不要", "拒絕"]
        for word in negation_words:
            if word in sentence:
                return True
        return False

    def convert_to_positive(self, sentence):
        negation_words = re.compile(r'[不沒無未勿拒絕]|沒[^\s]*|無[^\s]*|未[^\s]*|勿[^\s]*|拒絕[^\s]*')
        text = re.sub(negation_words, "", sentence)
        positive_text = self.replace_weekdays(text)
        return positive_text

    def replace_weekdays(self, text):
        all_weekdays = ['週一', '週二', '週三', '週四', '週五']

        found_weekdays = re.findall(r'週[一二三四五]', text)

        replaced_text = text
        for weekday in found_weekdays:
            replaced_text = replaced_text.replace(weekday, ''.join([d for d in all_weekdays if d != weekday]))

        return replaced_text

    def find_negation_sentences(self, text):
        sentences = re.split(r'[，。,、]', text)
        result_sentences = []

        for i, s in enumerate(sentences):
            if self.detect_negation(s):
                positive_s = self.convert_to_positive(s)
                result_sentences.append(positive_s)
            else:
                result_sentences.append(s)

            if i < len(sentences) - 1:
                result_sentences.append(',')

        return ''.join(result_sentences)
