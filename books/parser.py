import re
from sudachipy import tokenizer
from sudachipy import dictionary
from books.search import JishoSearch
from books.models import Word, BookWord, BookLine


#Japanese tokenizer from Sudachipy
TOKENIZER_OBJ = dictionary.Dictionary().create()

#INPUT: Book object
#Creates BookWord and BookLine objects for Book
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

        add_book_line(line, book, line_tokens, current_index)
        current_index += 1

    add_book_words(token_array, book)
 

#INPUT: line (string), book (Book object), line_tokens (all the sudachipy tokens in the line), current_index (location of the line being passed in, in context of the book)
#Creates one (1) new BookLine object if it does not already exist for line (string)
#called by: create_book_contents_object (which is called by views.py)
def add_book_line(line, book, line_tokens, current_index):
    line_words = []
    for token in line_tokens:
        line_words.append(get_word(token))
        #NOTE: What is .first() doing?
    book_line = BookLine.objects.filter(line_japanese=line, book=book).first()
    if not book_line:
        book_line = BookLine.objects.create(
            line_japanese=line,
            book=book
        )
    for word in line_words:
        book_line.words.add(word)

    book_line.add_index(current_index)


#INPUT: ordered tokens (sudachipy tokens in order), book (Book object)
#Creates a BookWord object for every word in the book (no duplicates)
#called by: create_book_contents_object (which is called by views.py)
def add_book_words(ordered_tokens, book):
    current_index = 0
    for token in ordered_tokens:
        word = get_word(token)
        book_word = BookWord.objects.filter(book=book, word=word).first()
        if not book_word: # if no book_word is found (will be None in this case)
            book_word = BookWord.objects.create(
                book=book, 
                word=word
            )
        book_word.add_index(current_index)
        current_index += 1
        
#INPUT: token (sudachipy token)
#Returns a Word object matching the dictionary form of the token
#NOTE:later reevaluate if we want to do this by dict form
#called by: add_book_words, add_book_line
def get_word(token):
    word = Word.objects.filter(dict_form=token.dictionary_form()).first()
    if not word:
        book_form = token.surface()
        word = Word.objects.create(
            book_form = book_form,
            reading_form = token.reading_form(),
            dict_form = token.dictionary_form(),
            part_of_speech_array = token.part_of_speech(),
        )
    #NOTE: I moved it into the the Word.objects.create() call above. This way save doesn't get need to get called twice and it gets instantiated the moment of creation.
    # I see! save gets called automatically at the end of a create but i was editing it outside of the create
    # word.save() # You were missing this! It needs to save to the database in order to register foreber
    return word