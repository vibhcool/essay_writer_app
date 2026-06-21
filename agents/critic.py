from agents.agent import Agent

class Critic(Agent):

    PROMPT = '''
            You are a teacher grading an essay submission. \
            Generate critique and recommendations for the user's submission. \
            Provide detailed recommendations, including requests for length, depth, style, etc.
    '''

    def __init__(self, tools = None):
        super().__init__(self.PROMPT, tools)
