# CS361 - Software Engineering I
# Sprint 3: Content Generator - wikipedia API function
# Author: Felipe Groberio <teixeirf@oregonstate.edu>
# Date: February 13th, 2021

import wikipedia
import warnings

def get_paragraph(p,s):
    # Initialize dictionary
    page = {}

    # Ignore warnings from the Wikipedia API
    warnings.catch_warnings()
    warnings.simplefilter('ignore')

    # Remove any upper-case characters
    p = p.lower()
    s = s.lower()

    # Query wikipedia using the primary keyword
    results = wikipedia.search(p)

    # Cycle through the results
    for result in results:
        try:
            # Attempts to access the wikipedia page for a given result
            wiki_page = wikipedia.page(result)

            # Check if the primary word is present on the URL address
            url_word = wiki_page.url.lower().find(p)
            if(url_word != -1):
                lines = wiki_page.content
                # Split the wikipedia content in distinct paragraphs
                lines = lines.split('\n')
                # Cycle through the paragraphs
                for i in lines:
                    temp = i
                    i = i.lower()
                    # Check if the current paragraph has both the primary
                    #   and secondary word
                    if i.find(p) != -1 and i.find(s) != -1:
                        page.update({'url':wiki_page.url})
                        page.update({'content':temp})
                        return page
        except:
            pass
    return page
