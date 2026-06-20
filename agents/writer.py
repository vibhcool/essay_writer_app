

class Writer(Agent):

    PROMPT = '''
            You are an essay assistant tasked with writing excellent 5-paragraph essays.\
            Generate the best essay possible for the user's request and the initial outline. \
            If the user provides critique, respond with a revised version of your previous attempts. \
            Utilize all the information below as needed:    
    '''

    def __init__(self):
        super.__init__(PROMPT)
