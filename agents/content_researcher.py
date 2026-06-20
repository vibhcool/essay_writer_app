

class ContentResearcher(Agent):

    PROMPT = '''
            You are a researcher charged with providing information that can \
            be used when writing the following essay. Generate a list of search queries that will gather \
            any relevant information.
    '''

    def __init__(self):
        super.__init__(PROMPT)
