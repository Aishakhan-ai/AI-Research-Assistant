# AI Research Assistant

A beginner-friendly local AI chatbot using Python, Streamlit, and Ollama.

## Requirements
- Windows 10/11
- Python 3.10 or newer
- Ollama installed
- At least one Ollama model downloaded

## Run on Windows

1. Open Command Prompt in this folder.
2. Install dependencies:

   `py -m pip install -r requirements.txt`

3. Check your installed Ollama models:

   `ollama list`

4. Start the app:

   `py -m streamlit run app.py`

5. In the browser, enter the exact model name shown by `ollama list` in the sidebar.

Keep Ollama running while using the website.

## Troubleshooting
- If the app cannot connect, open the Ollama desktop app and try again.
- If the model is not found, copy its exact name from `ollama list` into the app sidebar.
- If `py` is not recognized, try `python` instead.
