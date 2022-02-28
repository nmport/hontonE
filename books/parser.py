import re
from sudachipy import tokenizer
from sudachipy import dictionary
from books.search import JishoSearch
from books.models import Word


#Japanese tokenizer from Sudachipy
TOKENIZER_OBJ = dictionary.Dictionary().create()

#INPUT: Book objec
#NOTE: called by: VIEWS.PY
def create_book_contents_object(book):
    modeC = tokenizer.Tokenizer.SplitMode.C #Using mode C for the tokenizer, which splits texts into the longest possible morphemes
    current_index = 0
    token_array = [] #array of sudachypy token objects with all the information (surface, reading form, part of speech, etc.)
    
    for line in book.content_lines:
        '''Parsing one line, and adding the individual words from that line (in order) to the BookContents object'''
        line_tokens = []
        tokens = TOKENIZER_OBJ.tokenize(line, modeC)
        for token in tokens:
            book_word = token.surface()
            # check to see if word is alpha before we add it to BookContents object arrays -- forgot why
            if book_word.isalpha():
                token_array.append(token) #sudachipy object = token
                line_tokens.append(token)

        current_index += 1

    add_book_words(token_array, book)
 



#INPUT: ordered tokens (sudachipy tokens in order), book (Book object)
#called by: create_book_contents_object (which is called by views.py)
def add_book_words(ordered_tokens, book):
    current_index = 0
    for token in ordered_tokens:
        if not Word.objects.filter(dict_form=token.dictionary_form()).first():
            book_form = token.surface()
            word = Word.objects.create(
                book_form = book_form,
                reading_form = token.reading_form(),
                dict_form = token.dictionary_form(),
                part_of_speech_array = token.part_of_speech(),
            )
        current_index += 1
        