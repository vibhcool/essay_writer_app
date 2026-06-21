from agents.agent import Agent

class CriticResearcher(Agent):

    PROMPT = '''
            You are a researcher charged with providing information that can \
            be used when making any requested revisions (as outlined below). \
            Generate a list of search queries that will gather any relevant information.
    '''

    def __init__(self, tools = None):
        super().__init__(self.PROMPT, tools)
