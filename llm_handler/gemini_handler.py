import google.generativeai as genai
from .llm_handler_base import LLMHandlerBase
import datetime

class GeminiHandler(LLMHandlerBase):
    # Handler class for interacting with the Gemini generative model
    def __init__(self, config):
        super().__init__(config)
        self.configure()

    def configure(self):
        if not self.config['gemini']['api_key']:
            raise ValueError("Gemini API key is missing in the configuration.")
        genai.configure(api_key=self.config['gemini']['api_key'])
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_sql_query(self, query, schema, dates):
        prompt = " ".join(["Convert the following natural language question into a SQL query. Only provide the SQL query as the output, ensure the resulting columns have good described names: ", query, "Database schema: ", schema, "Consider dates given (if a date is given in a formal manner, read it as ISO 8601): ", dates])
        response = self.model.generate_content(prompt)
        sql_query = response._result.candidates[0].content.parts[0].text
        # Clean up the SQL query by removing any surrounding code block markers
        sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
        return sql_query
    
    def mock_price_prediction(self):
        # Here, I use a hardcoded value for simplicity
        latest_price = 150.0  # This value should be fetched from a reliable source in a real implementation, possibly using the Gemini API
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