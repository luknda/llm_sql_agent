# LLM SQL Query Agent

## Overview

This project implements an agent capable of understanding and responding to natural language queries by generating SQL queries and returning the retrieved data. It also supports exporting the data to a CSV file and providing mock stock price forecasts.

## Features

- **Natural Language to SQL:** Converts natural language questions into SQL queries.
- **Data Export:** Exports query results to a CSV file.
- **Price Prediction Mocking:** Provides fictional stock price forecasts for the next three days.
- **Error Handling:** Handles invalid SQL queries, database errors, and incorrect inputs gracefully.

## Setup

### Prerequisites

- Python 3.6 or higher
- Virtual environment tool (optional but recommended)

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository_url>
   cd <repository_directory>

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt

4. **Set up the database:**
   ```bash
   python create_db.py

## Usage

1. **Run the agent:**
   ```bash
   python agent.py

2. **Follow the prompts:**
    - Enter your query in natural language.
    - Specify the date range (if using specific dates, remember to respect YYYY-MM-DD format).
    - Choose whether to export the results to a CSV file.

3. **Example:**
   Enter your query: Show me the average high minus low, group by month
   Enter the date range (if using very specific dates, remember to respect YYYY-MM-DD): July through December 
   Do you want to export the result to a CSV file? (yes/no): yes
   Enter the full path and file name for the CSV file (e.g., /path/to/file.csv): C:/Users/crash/Desktop/output.csv

4. **Mock Price Predictions:**
   - After processing the query, the agent will ask if you want price predictions for the next three days.
   - Respond with "yes" or "no".

## Configuration
The agent's configuration is stored in config.yaml. Update the API keys and model types as needed.

### Example 
    default:
    model_type: gemini

    gemini:
    api_key: your_gemini_api_key

    openai:
    api_key: your_openai_api_key


## Extending the Agent with a New LLM
To add support for a new LLM, follow these steps:
1. **Create a New Handler:**
   Create a new handler class in a new file (e.g., new_llm_handler.py) inheriting from LLMHandlerBase.
    ```bash
    from .llm_handler_base import LLMHandlerBase
    class NewLLMHandler(LLMHandlerBase):
        def __init__(self, config):
            super().__init__(config)
            self.configure()

        def configure(self):
            # Add configuration code for the new LLM
            pass

        def generate_sql_query(self, query, schema, dates):
            # Implement the logic to generate SQL query using the new LLM
            pass

        def mock_price_prediction(self):
            # Implement the logic for mock price prediction
            pass

2. **Update the Factory:**
Update llm_handler_factory.py to include the new handler.
    ```bash
    from llm_handler.new_llm_handler import NewLLMHandler
    class LLMHandlerFactory:
        @staticmethod
        def create_handler(config):
            model_type = config['default']['model_type']
            if model_type == 'gemini':
                return GeminiHandler(config)
            elif model_type == 'openai':
                return OpenAIHandler(config)
            elif model_type == 'new_llm':
                return NewLLMHandler(config)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")

3. **Update the Factory:**
Add the configuration for the new LLM in config.yaml.
    ```bash
    default:
      model_type: new_llm

    new_llm:
      api_key: your_new_llm_api_key
    # Add any other necessary configuration options here

4. **Update requirements.txt:**
Add any new dependencies required for the new LLM.

## Files
 - agent.py: Main script to run the agent.
 - config.yaml: Configuration file for API keys and model types.
 - create_db.py: Script to set up the SQLite database.
 - llm_handler_base.py: Base class for LLM handlers.
 - gemini_handler.py: Handler for Gemini LLM.
 - openai_handler.py: Handler for OpenAI LLM.
 - llm_handler_factory.py: Factory class to create LLM handlers.
 - requirements.txt: List of required Python packages.
 - README.md: Documentation for the project.