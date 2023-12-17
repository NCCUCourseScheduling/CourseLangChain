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
        week_text = self.replace_time_indicators(text)
        pattern1 = r'週[一二三四五六日] \d+ 點(?:[前後]|以前|以後|之前|之後)'
        if re.search(pattern1, week_text):
            week_text = re.sub(r'前', 'TEMP', week_text)
            week_text = re.sub(r'後', '前', week_text)
            positive_text = re.sub(r'TEMP', '後', week_text)
            return positive_text
        pattern2 = r'週[一二三四五六日](?:上午|早上|下午)(?:[前後]|以前|以後|之前|之後)'
        if re.search(pattern2, week_text):
            week_text = re.sub(r'前', 'TEMP', week_text)
            week_text = re.sub(r'後', '前', week_text)
            positive_text = re.sub(r'TEMP', '後', week_text)
            return positive_text
        pattern3 = r'週[一二三四五六日](?:上午|早上|下午)'
        if re.search(pattern3, week_text):
            week_text = re.sub(r'上午', 'TEMP', week_text)
            week_text = re.sub(r'早上', 'TEMP', week_text)
            week_text = re.sub(r'下午', '早上', week_text)
            positive_text = re.sub(r'TEMP', '下午', week_text)
            return positive_text

        positive_text = self.replace_weekdays(week_text)
        #print(positive_text)
        return positive_text

    def replace_time_indicators(self, text):
        text = re.sub(r'禮拜', '週', text)
        text = re.sub(r'星期', '週', text)
        return text

    def replace_weekdays(self, text):
        all_weekdays = ['週一', '週二', '週三', '週四', '週五']

        found_weekdays = re.findall(r'週[一二三四五]', text)
        #print(found_weekdays)
        replaced_text = re.sub(r'週[一二三四五]', '', text)
        #print(replaced_text)
        for weekday in found_weekdays:
            all_weekdays.remove(weekday)
        replaced_text = ''.join(all_weekdays) + replaced_text
        #print(replaced_text)

        return replaced_text

    def find_negation_sentences(self, text):
        sentences = re.split(r'[，。,、]', text)
        result_sentences = []

        for i, s in enumerate(sentences):
            s = self.replace_time_indicators(s)
            if self.detect_negation(s):
                positive_s = self.convert_to_positive(s)
                result_sentences.append(positive_s)
            else:
                result_sentences.append(s)

            if i < len(sentences) - 1:
                result_sentences.append(',')

        return ''.join(result_sentences)


negation_detector = NegationDetector(verbose=True)
text_to_check = "星期一週三不排課、星期二 10 點後不排、星期四 12 點之前不排、星期五下午不排課，禮拜三下午不行，禮拜四早上以前不要"
result_text = negation_detector.find_negation_sentences(text_to_check)
#print("original:")
#print(text_to_check)
#print("result:")
#print(result_text)
