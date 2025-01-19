# Faculty Profile Scraper

A Streamlit application that scrapes faculty profiles from universities and extracts relevant information using LangChain and LLMs.

## Features

- Web scraping of faculty profile pages
- Automatic extraction of key information:
  - University
  - Department
  - Designation
  - Name
  - Email
  - Research Area
  - Lab
  - Relevant Links
- Editable data grid
- Export functionality to CSV
- Track emailed status

## Setup

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

Run the Streamlit app with:
```bash
streamlit run app.py
```

## Usage

1. Enter a faculty profile URL in the input field
2. Click "Process URL" to scrape and analyze the profile
3. The extracted information will appear in the data grid below
4. Edit any fields manually if needed
5. Export the data to CSV using the export button

## Note

Make sure the faculty profile URLs are publicly accessible. The quality of extraction depends on the structure and content of the webpage. 