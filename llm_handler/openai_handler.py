import openai
from .llm_handler_base import LLMHandlerBase
import datetime

class OpenAIHandler(LLMHandlerBase):
    # Handler class for interacting with the OpenAI generative model
    def __init__(self, config):
        super().__init__(config)
        self.configure()

    def configure(self):
        if not self.config['openai']['api_key']:
            raise ValueError("OpenAI API key is missing in the configuration.")
        openai.api_key = self.config['openai']['api_key']

    def generate_sql_query(self, query, schema, dates):
        prompt = " ".join(["Convert the following natural language question into a SQL query. Only provide the SQL query as the output, ensure the resulting columns have well described names: ", query, "Database schema: ", schema, "Consider dates given (if a date is given in a formal manner, read it as ISO 8601): ", dates])
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        sql_query = response['choices'][0]['message']['content'].strip()
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        return sql_query

    def mock_price_prediction(self):
        # Here, I use a hardcoded value for simplicity
        latest_price = 150.0  # This value should be fetched from a reliable source in a real implementation, possibly using the OpenAI API
        stock_name = "AAPL"

        # Generate deterministic mock prices for the next three days
        dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(1, 4)]
        predictions = []
        for i, date in enumerate(dates):
            # Simple deterministic mock algorithm: Increase price by 1% each day
            price = latest_price * (1 + 0.01 * (i + 1))
            predictions.append((date, round(price, 2)))
        
        response = f"Here are the mock price predictions for {stock_name}:\n"
        for date, price in predictions:
            response += f"{date}: ${price}\n"
        return response