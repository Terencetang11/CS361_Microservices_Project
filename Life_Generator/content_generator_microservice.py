
import Life_Generator.wikipedia_API_query as wikiAPI

def CG(request, receive):

    while True:
        # pop words from queue
        words = request.get()

        # query wikipedia
        wiki = wikiAPI.get_paragraph(words[0], words[1])

        # If no results are returned, inform user and exit
        if (wiki == {}):
            receive.put('Information not available.')
        else:
            receive.put(wiki['content'])
    return
