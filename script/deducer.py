import re
from collections import Counter

# import openai
# openai.api_key = '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'

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

import const


class Deducer:
    def deduce_gpt3(self, item):
        print('TODO donwload gpt model and use it locally, without paying to OpenAI')
        return item
        for key, question in [
            ('location', 'Przy jakiej ulicy znajduje się mieszkanie? Podaj nazwę ulicy lub "Brak danych".'),
            ('animals', 'Czy można mieszkać ze zwierzętami? Wybierz "Tak", "Nie", "Brak danych".'),
            ('shower', 'Czy mieszkanie posiada prysznic? Wybierz "Tak", "Nie", "Brak danych".'),
            ('bath', 'Czy mieszkanie posiada wannę? Wybierz "Tak", "Nie", "Brak danych".'),
            ('balcony', 'Czy mieszkanie posiada balkon? Wybierz "Tak", "Nie", "Brak danych".'),
            ('dishwasher', 'Czy mieszkanie posiada zmywarkę? Wybierz "Tak", "Nie", "Brak danych".'),
            ('induction_stove', 'Czy mieszkanie posiada kuchenkę indukcyjną? Wybierz "Tak", "Nie", "Brak danych".'),
            ('deposit', 'Jaka jest wielkość kaucji? Podaj wartość liczbową lub "Brak danych".'),
        ]:
            if item[f'deduced_gpt_{key}'] == '': continue
            prompt = f'Przeanalizuj poniższe ogłoszenie i odpowiedź na pytanie: {question}\nTreść ogłoszenia:\n' + item['whole_text']
            responses = []
            for _ in range(10):
                res = openai.Completion.create(engine="text-davinci-002", prompt=prompt, temperature=0.5, max_tokens=256,
                                           top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
                res = res['choices'][0]['text'].strip().lower()
                res = re.sub(rf'[^0123456789{const.REGEX_POLISH_AZ} ]', '', res).strip()
                responses.append(res)
            counter = Counter(responses)
            res, n = counter.most_common()[0]
            item[f'deduced_gpt_{key}'] = res
            item[f'deduced_gpt_certainty_{key}'] = f'{10 * n}%'
        return item
    
    def deduce_gpt3(self, item):
        print('TODO donwload gpt model and use it locally, without paying to OpenAI')
        return item
        keys = ['location', 'animals', 'shower', 'bath', 'balcony', 'dishwasher', 'induction_stove', 'deposit']
        if all(item[f'deduced_gpt_{key}'] != '' for key in keys):
            return item
        
        prompt = f'Przeanalizuj poniższe ogłoszenie i odpowiedź na pytania, podając każdą odpowiedź w nowej linii.\n'
        prompt += 'Treść ogłoszenia:\n"' + item['whole_text'] + '"'
        prompt += 'Pytania:\n'
        prompt += 'Przy jakiej ulicy znajduje się mieszkanie? Podaj nazwę ulicy lub "Brak danych".\n'
        prompt += 'Czy można mieszkać ze zwierzętami? Wybierz "Tak", "Nie", "Brak danych".\n'
        prompt += 'Czy mieszkanie posiada prysznic? Wybierz "Tak", "Nie", "Brak danych".\n'
        prompt += 'Czy mieszkanie posiada wannę? Wybierz "Tak", "Nie", "Brak danych".\n'
        prompt += 'Czy mieszkanie posiada balkon? Wybierz "Tak", "Nie", "Brak danych".\n'
        prompt += 'Czy mieszkanie posiada zmywarkę? Wybierz "Tak", "Nie", "Brak danych".\n'
        prompt += 'Czy mieszkanie posiada kuchenkę indukcyjną? Wybierz "Tak", "Nie", "Brak danych".\n'
        prompt += 'Jaka jest wielkość kaucji? Podaj wartość liczbową lub "Brak danych".\n'
        responses = {k: [] for k in keys}
        for _ in range(10):
            res = openai.Completion.create(engine="text-davinci-002", prompt=prompt, temperature=0.5, max_tokens=256,
                                        top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0)
            res = res['choices'][0]['text'].strip().lower()
            res = res.split('\n')
            for k, r in zip(keys, res):
                r = re.sub(rf'[^0123456789{const.REGEX_POLISH_AZ} ]', '', res).strip()
                responses[k].append(res)
        for key in keys:
            counter = Counter(responses[k])
            res, n = counter.most_common()[0]
            item[f'deduced_gpt_{key}'] = res
            item[f'deduced_gpt_certainty_{key}'] = f'{10 * n}%'
        return item
    
    def deduce_gpt2(self, item):
        # https://huggingface.co/gpt2
        # prompt = f'Przeanalizuj poniższe ogłoszenie i odpowiedź na pytanie: Przy jakiej ulicy znajduje się mieszkanie? Podaj nazwę ulicy lub "Brak danych".\nTreść ogłoszenia:\n' + item['whole_text']
        prompt = item['whole_text'] + 'Przy jakiej ulicy znajduje się mieszkanie? Podaj nazwę ulicy lub "Brak danych"'
        
        model = pipeline('text-generation', model='gpt2')
        res = model(prompt, max_length=30, num_return_sequences=1)
        print(res)
        
    def deduce_llama_decapoda(self, item):
        # https://huggingface.co/decapoda-research/llama-7b-hf
        prompt = f'Przeanalizuj poniższe ogłoszenie i odpowiedź na pytanie: Przy jakiej ulicy znajduje się mieszkanie? Podaj nazwę ulicy lub "Brak danych".\nTreść ogłoszenia:\n' + item['whole_text']
        
        model = 'decapoda-research/llama-7b-hf'
        tokenizer = AutoTokenizer.from_pretrained(model)
        model = AutoModelForCausalLM.from_pretrained(model)
        encoded_input = tokenizer(prompt)
        res = model(encoded_input)
        print(res)
        
    def deduce_llama_vmware(self, item):
        # https://huggingface.co/VMware/open-llama-0.3T-7B-open-instruct-v1.1
        prompt = f'Przeanalizuj poniższe ogłoszenie i odpowiedź na pytanie: Przy jakiej ulicy znajduje się mieszkanie? Podaj nazwę ulicy lub "Brak danych".\nTreść ogłoszenia:\n' + item['whole_text']
        
        model = 'VMware/open-llama-0.3T-7B-open-instruct-v1.1'
        tokenizer = AutoTokenizer.from_pretrained(model)
        model = AutoModelForCausalLM.from_pretrained(model)
        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        output1 = model.generate(input_ids, max_length=512)
        input_length = input_ids.shape[1]
        output1 = output1[:, input_length:]
        res = tokenizer.decode(output1[0])
        print(res)
    
    def deduce_bert_multilingual(self, item):
        # https://huggingface.co/henryk/bert-base-multilingual-cased-finetuned-polish-squad2
        model = 'henryk/bert-base-multilingual-cased-finetuned-polish-squad2'
        model = pipeline('question-answering', model=model, tokenizer=model)
        res = model({
            'context': item['whole_text'],
            # 'question': 'Przeanalizuj poniższe ogłoszenie i odpowiedź na pytanie: Przy jakiej ulicy znajduje się mieszkanie? Podaj nazwę ulicy lub "Brak danych"'})
            'question': 'Przy jakiej ulicy znajduje się mieszkanie?'})
        print(res['answer'])
        

    def deduce_value(self, text, regex, index):
        if match := re.search(regex, text, re.IGNORECASE):
            print(f'deduced {match.group(index)}')
            return match.group(index)
    
    def deduce_bool(self, text, regex):
        print(f'deducong {regex}')
        return re.search(regex, text, re.IGNORECASE) is not None

    def deduce_surrounding_text(self, text, regex, padding):
        if match := re.search(regex, text, re.IGNORECASE):
            start, end = match.span(0)
            new_start = max(start - padding, 0)
            try: new_start = new_start + text[new_start:start + 1].rindex('\n') + 1
            except: pass
            new_end = min(end + padding, len(text))
            try: new_end = end + text[end:new_end + 1].index('\n')
            except: pass
            return text[new_start:new_end]

    def deduce_deposit(self, text):
        if t := self.deduce_surrounding_text(text, rf'depozyt[{const.REGEX_POLISH_AZ}]+', 10):
            return re.sub(r'[^0-9]', '', t).strip()
        if t := self.deduce_surrounding_text(text, rf'kaucj[{const.REGEX_POLISH_AZ}]+', 10):
            print(t)
            return re.sub(r'[^0-9]', '', t).strip()

    def deduce_regex(self, item):
        if item['deduced_regex_location'] == '': item['deduced_regex_location'] = self.deduce_value(item['whole_text'], rf'(ul[{const.REGEX_POLISH_AZ}.]*)([{const.REGEX_POLISH_AZ}0-9 ]+)', 2)
        if item['deduced_regex_shower'] == '': item['deduced_regex_shower'] = self.deduce_bool(item['whole_text'], rf'przysznic[{const.REGEX_POLISH_AZ}]+')
        if item['deduced_regex_bath'] == '': item['deduced_regex_bath'] = self.deduce_bool(item['whole_text'], rf'wann[{const.REGEX_POLISH_AZ}]+')
        if item['deduced_regex_balcony'] == '': item['deduced_regex_balcony'] = self.deduce_bool(item['whole_text'], rf'balkon[{const.REGEX_POLISH_AZ}]+')
        if item['deduced_regex_dishwasher'] == '': item['deduced_regex_dishwasher'] = self.deduce_bool(item['whole_text'], rf'zmywark[{const.REGEX_POLISH_AZ}]+')
        if item['deduced_regex_induction_stove'] == '': item['deduced_regex_induction_stove'] = self.deduce_bool(item['whole_text'], rf'indukc[{const.REGEX_POLISH_AZ}]+')
        if item['deduced_regex_animals'] == '': item['deduced_regex_animals'] = self.deduce_surrounding_text(item['whole_text'], rf'zwierz[{const.REGEX_POLISH_AZ}]+', 30)
        if item['deduced_regex_deposit'] == '': item['deduced_regex_deposit'] = self.deduce_deposit(item['whole_text'])
        return item
