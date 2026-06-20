

class Critic(Agent):

    PROMPT = '''
            You are a teacher grading an essay submission. \
            Generate critique and recommendations for the user's submission. \
            Provide detailed recommendations, including requests for length, depth, style, etc.
    '''

    def __init__(self):
        super.__init__(PROMPT)
