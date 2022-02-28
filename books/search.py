import requests, abc, time

class DictionarySearch(abc.ABC):
    def __init__(self, vocab_word):
        self.vocab_word = vocab_word
        self.critical = False
        self.found = False
        self.definitions = [] #[['definiton 1.1', 'definition 1.2'], ['definiton 2.1'], ...]
        self.related = [] #[('related word', ['definition 1.1', 'definition 1.2']), ...]

    '''
    Define the vocab word
    '''
    @abc.abstractmethod
    def define():
        pass

    '''
    Print out the search result in a user friendly output
    '''
    def verbose_print(self):
        print("Definition(s):")
        if self.found:
            for i in range(0, len(self.definitions)):
                print("     {}. {}".format(i+1, "; ".join(self.definitions[i])))
        elif self.critical or len(self.related)==0:
            print("Did not find any matches")
        else:
#NOTE: CHANGED HERE
            print("{}: Not found. Here were the related words:".format(self.vocab_word.book_form))
            for word in self.related:
                print("  {}:".format(word[0]), ", ".join(word[1]))

class JishoSearch(DictionarySearch):
    def __init__(self, vocab_word):
        super().__init__(vocab_word)

    def _jisho_get_related(self, item, word):
        found = False
        word_slug = item['slug']
        if word_slug[0].isdigit():
            word_slug = []
            japanese_variants = item['japanese']
            while not found and len(japanese_variants) > 0:
                variant = japanese_variants.pop(0)
                for read_word in variant:
                    if variant[read_word] == word:
                        found = True
                    elif not found:
                        word_slug += [variant[read_word]]
            word_slug = ", ".join(word_slug)
        return found, word_slug

    '''
    Search jisho for the vocab word and get definitions or get related words if it's not found and store
    them in the object as variables
    '''
    def define(self):
#NOTE: EDIT THIS, I CHANGED IT TO DICT FORM for convenience but look into it`````````````````````````````````````````````````````````````````````````````````````
        #word = self.vocab_word.book_form
        #TODO: deal with this appropriately. this is too many requests error code
        #time.wait(120) didn't work because it made hontone time out? not sure
        word = self.vocab_word.dict_form
        print('https://jisho.org/api/v1/search/words?keyword=' + word)
        response = requests.get('https://jisho.org/api/v1/search/words?keyword=' + word)
        while response.status_code == 429:
            time.sleep(.5)
            word = self.vocab_word.dict_form
            print('https://jisho.org/api/v1/search/words?keyword=' + word)
            response = requests.get('https://jisho.org/api/v1/search/words?keyword=' + word)

        #data is a key from the json dict with meta and data
        data = response.json().get("data")

        #the data is the main component of the JSON where the definition is stored
        found = False
        # list created is a list of all slugs that have the same character set of the word
        for item in [matching_item for matching_item in data if matching_item['slug'] == word or 
        (word in [forms.get("word", None) for forms in matching_item['japanese']])]:
            if 'senses' in item:
                for key in item['senses']:
                    self.definitions.append(key['english_definitions'])
                    #self.definitions.append("; ".join(key['english_definitions']))
                found = True
            else:
                self.critical = True
        if not found:
            while not found and len(data) > 0:
                related_item = data.pop(0)
                found, word_slug = self._jisho_get_related(related_item, word)
                for definition in related_item['senses']:
                    if found:
                        self.definitions.append(definition['english_definitions'])
                    else:
                        self.related.append((word_slug, definition['english_definitions']))
        self.found = found