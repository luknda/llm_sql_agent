from llm_handler.gemini_handler import GeminiHandler
from llm_handler.openai_handler import OpenAIHandler

# Factory class to create the appropriate LLM handler based on the configuration
class LLMHandlerFactory:
    @staticmethod
    def create_handler(config):
        model_type = config['default']['model_type']
        if model_type == 'gemini':
            return GeminiHandler(config)
        elif model_type == 'openai':
            return OpenAIHandler(config)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")