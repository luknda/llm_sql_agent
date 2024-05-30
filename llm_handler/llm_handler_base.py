class LLMHandlerBase:
    # Base class for handling interactions with large language models (LLMs)
    def __init__(self, config):
        self.config = config

    def configure(self):
        raise NotImplementedError("Subclasses should implement this method")

    def generate_sql_query(self, prompt):
        raise NotImplementedError("Subclasses should implement this method")

    def mock_price_prediction(self, start_price):
        raise NotImplementedError("Subclasses should implement this method")