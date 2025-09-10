# text analysis
# find most common word ✅
# find number of vowels and words count ✅
# find palindrome ✅
# let a user input word to search for and ability to replace it ✅
# make sure every sentence starts with capital letter ✅
def find_vowels(paragraph):
    vowel_count = len([vowel for vowel in paragraph if vowel in 'aeiouAEIOU'])
    return vowel_count


def make_sentence_start_with_capital_letter(words):
    for index, word in enumerate(words):  # loop over every element in the paragraph
        if words[index - 1][
            -1] in '!?.' or index == 0:  # check if previous word contains a punctuation or if it's the first word of paragraph
            words[
                index] = word.capitalize()  # returns a string of words[index] with first index being uppercase and others being lowercase
    return words  # returns the updated paragraph


def find_most_common_word(paragraph):
    freq = {}  # declare freq as a dictionary to contain word, value which represents how many times it appears in paragraph
    for word in paragraph.lower().split():  # looped over paragraph which is made lowercase and split
        freq[word] = freq.get(word,
                              0) + 1  # freq[key] gets assigned value of its key(default 0) + 1 when it's being accessed
    return max(freq, key=freq.get), freq[max(freq, key=freq.get)]  # returns most common word, value of most common word
    # in max() function, freq is the iterable and key is the new value after each elements in iterable was applied with a function
    # it then returns the element with highest key


def find_palindrome(words):
    palindromes = []
    for word in words:  # loop over every elements in words list
        reversed_word = word[::-1]  # reverses the word
        if reversed_word == word:
            palindromes.append(word)
    return palindromes


def search_for_word_in_letters(words, searched_word):
    paragraph = ' '.join(words)
    position = []
    searched_word = searched_word.lower()  # makes the string called searched_word lowercase so it can match the lower_case words in main function
    index = paragraph.find(searched_word)  # find first occurance of searched_word
    while index != -1:  # loop until no more searched_word can be found
        position.append(index)  # add occurance of searched_word to list
        index = paragraph.find(searched_word,
                               index + 1)  # index gets assigned value of the next occurance of searched_word
        # second parameter refers to what index position to start scanning from
    return position if position else None


def search_for_word_in_words(words, searched_word):
    searched_word = searched_word.lower()
    position = [pos for pos, word in enumerate(words) if
                word == searched_word]  # enumerate returns index,element of the list, in this case, pos is index while word is element
    return position if position else None


def replace_word(paragraph, searched_word, replacement):
    capital_searched_word = searched_word[0].upper() + searched_word[
        1::]  # assigns capital_searched_word with capital first letter and lowercase from second onwards
    replaced_words = paragraph.replace(searched_word, replacement)
    if replaced_words != paragraph:  # check changes are made
        return replaced_words
    else:  # if changes are not made
        replaced_words = paragraph.replace(capital_searched_word, replacement)
        return replaced_words


def main():
    paragraph = input("input paragraph: \n")
    paragraph_no_punctuation = ''.join([letter for letter in paragraph if letter.isalpha() or letter.isspace()])
    paragraph_list = paragraph.split()
    words = paragraph_no_punctuation.split()
    lowercase_words = paragraph_no_punctuation.lower().split()
    paragraph_with_starting_capitalisation = ' '.join(make_sentence_start_with_capital_letter(paragraph_list))
    print(
        f'\n\nParagraph with correct capitalisation at the start of sentence : \n{paragraph_with_starting_capitalisation}')
    print(f'\nThe number of vowels in this sentence is {find_vowels(paragraph_no_punctuation)}')
    print(f'The number of words in this paragraph is {len(words)}')
    print(f'The most common word in this sentence is {find_most_common_word(paragraph_no_punctuation)}')
    print(f'The palindromes in this list are : {find_palindrome(lowercase_words)}')
    searched_word = input("\ninput word to search for: ")
    print(
        f'{searched_word} is located at position {search_for_word_in_letters(lowercase_words, searched_word)} in terms of letters')
    print(
        f'{searched_word} is located at position {search_for_word_in_words(lowercase_words, searched_word)} in terms of words')
    replacement_word = input("\ninput replacement word: ")
    new_paragraph = replace_word(paragraph, searched_word, replacement_word)
    print(f'\n"{searched_word}" in paragraph has been replaced with "{replacement_word}"')
    print(' '.join(make_sentence_start_with_capital_letter(new_paragraph.split())))


main()