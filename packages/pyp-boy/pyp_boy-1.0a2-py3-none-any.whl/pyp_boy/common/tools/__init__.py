import random_words

from pyp_boy.common.tools.errors import UncalledArgumentError


def generate_wordlist(length: int = 4,
                      count: int = 2,
                      debug: bool = False,
                      do_sort: bool = True,
                      no_dupes: bool = True,
                      catch_rejected: bool = False):
    """
        
            This function is included mainly for testing without having a puzzle to solve in front of you. There's no 
        guarantee that the items returned will share any letter-places. 
    |  
    
        Return Just a List:
    *******************
    Below is an example of running 'generate_wordlist' with no parameters. (Just using the defaults, hard-coded in)
    
    >>> wl = generate_wordlist()
    ['HUMP', 'PENS']
    
    Below sits yet another example, except this time we're specifying that we want 12 words in our list, each with a
    length of 5 letters.
    
    >>>  wl = generate_wordlist(length=5, count=12)
    ['DOSES', 'EASES', 'GRADE', 'GRAMS', 'HOPES', 'NOSES', 'RAISE', 'SAILS', 'SLAPS', 'SNOWS', 'SPANS', 'WELDS']
    
    
    As shown next, we can even get a bit granular on how that list is returned to us. We can ask it to not bother sorting the list before returning it, like so:
    
    >>> wl = generate_wordlist(length=4, count=20, do_sort=False)
    ['JUGS', 'HELM', 'SLED', 'STEP', 'HUGS', 'BOYS', 'DRIP', 'PANS', 'BOWS', 'FORK', 'MUCH', 'SAIL', 'OHMS', 'ARMY',
    'STOP', 'KITS', 'SALT', 'BUYS', 'DOCK', 'DRIP']
    
    
    >>> wl = generate_wordlist(length=6, count=15, debug=True)
    (['ROUNDS', 'PASSES', 'SWITCH', 'HOISTS', 'CREEKS', 'VIDEOS', 'GROUND', 'FARADS', 'ARREST', 'ROWERS', 'STEAMS',
    'BATTLE', 'SCOPES', 'DAMAGE', 'SAFETY'], 105)
        
        
        :param catch_rejected: 
        :param debug: **[ (bool) | Default: bool(False) ]**
        |  Run in debug mode? If you pass 'bool(True)' to this keyword argument the function will not only return your
        new wordlist but will return a tuple with the first element containing your wordlist, and the second element containing an integer representing the number of words fetched all-together (including words that were not equal to the length parameter).
    |  
        
        :param length: **[(int) | Default: int(4) ]** 
        | The integer representing the length of each the words contained within the list to be returned.
        
    |  
    
        :param count: **[ (int) | Default: int(2) ]**
        |  The integer representing the number of words the list should contain.
    |  
    
        :param do_sort: **[ (bool) | Default: bool(True) ]**
        |  If True (which is the default), the wordlist will be sorted alphabetically before being returned
    | 
    
        :param no_dupes: **[ (bool) | Default: bool(True) ]**
        |  *If True (which is the default)* | The function will check the list to see if a word already exists within the list, not adding it if this is the case.
        |  
        |  *If False* | The function will not process a check for duplicates before adding the word to the list
    
    |   
    """
    # Set some variables to be filled later

    # Create a var to keep track of how many words we grab to get our list (including words that didn't match the 
    # length indicated) if the 'debug' parameter is True 
    if debug:
        fetched_wcount: int = 0
        fetched_dupes: int = 0
        dupe_dict: dict = {}
        if catch_rejected:
            rej_wl = []
    else:
        if catch_rejected:
            raise UncalledArgumentError('catch-rejected', 'debug')

    w_list = []

    # Instantiate the RandomWords class
    rw = random_words.RandomWords()

    # Have the RandomWords package give us a random word, if it matches the length (in letters) that was asked for
    # upon calling the word will be added to the word list. This loops until 'w_list' has as many entries as
    # requested when called (using the parameter; 'count'
    while len(w_list) < count:

        if debug:
            fetched_wcount += 1

        word = rw.random_word()

        if len(word) == length:

            # If a dupe was found let's check to see if 'debug mode' is active. If so; we'll increment the
            # dupe count by one
            if word in w_list:
                if debug:
                    fetched_dupes += 1
                if not no_dupes:
                    w_list.append(word)
                else:
                    continue
            else:
                w_list.append(word)

        else:
            if catch_rejected and debug:
                rej_wl.append(word)

    if do_sort:
        w_list.sort()

    w_list = prepare_wordlist(w_list)

    if debug:
        stats = {
            "iterations": fetched_wcount,
            "duplicates": fetched_dupes,
            "rejected_words": ''
        }
        if catch_rejected:
            stats['rejected_words'] = rej_wl
        else:
            stats['rejected_words'] = 'Not caught'
        return w_list, stats
    else:
        return w_list


def prepare_wordlist(wordlist: list):
    """

    Calling this method with a word list as the "wordlist" parameter will return a word-list which is properly
    formatted (all caps, no whitespace characters. This method also makes sure that all words contained within the
    list are all the same length.

    Args:
        wordlist: A list containing two or more words to sanitize for GUI handling

    Returns:
        list: A word-list where all the words are all caps and arbitrary spaces removed.

    """

    # Since we might get a tuple during debugging, prepare to pull the actual word-list we want out of index 0
    if type(wordlist) == tuple:
        wordlist = wordlist[0]

    # Create a new list to be populated for return.
    new_list = []

    # Grab the length of the first word in the list to ensure uniformity with the other words.
    # TODO:
    #    * Put in checking of word length
    #    * Create an exception to be raised upon finding a word of non-conforming length
    #        * Rescue said exception smoothly, alert user of the problem and allow them to change the misfit entry
    word_length = len(wordlist[0])

    # Iterate through the original wordlist and do the following:
    #     1) Remove all whitespace from each word.
    #     2) Change the case of all letters in the words to 'upper'
    #     3) Add the newly-formatted word to the 'new_list' variable to be returned when the iterations are complete
    print(wordlist)
    for w in wordlist:
        w = w.replace(' ', '')
        w = w.upper()
        new_list.append(w)

    # Return list of newly formatted string entries, ready to be used by the PypBoy GUI!
    return new_list
