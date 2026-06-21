from agents.agent import Agent


class Planner(Agent):

    PROMPT = '''
            You are an expert writer tasked with writing a high level outline of an essay. \
            Write such an outline for the user provided topic. Give an outline of the essay along with any relevant notes \
            or instructions for the sections.  
    '''

    def __init__(self, tools = None):
        super().__init__(self.PROMPT, tools)
