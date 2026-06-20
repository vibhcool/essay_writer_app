

class Agent:

    client = None
    default_prompt = ''

    def __init__(self, default_prompt: str):
        self.init()
        self.default_prompt = default_prompt


    def init(self):
        self.client = ChatOpenAI(
            model="anthropic/claude-sonnet-4.6",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL")
        )
    
    def get_init_message(self):
        return SystemMessage(self.default_prompt)