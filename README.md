# Faculty Profile Scraper

A Streamlit application that scrapes faculty profiles from universities and extracts relevant information using LangChain and GPT-4o. The app supports batch processing of multiple URLs and persists data between sessions.

This project was created using [Cursor AI](https://cursor.sh/)'s composer feature.

## Features

- Batch processing of multiple faculty profile URLs
- Automatic data persistence using CSV storage
- Duplicate profile detection (based on email)
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
- Real-time statistics dashboard
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

Run the Streamlit app with auto-reload enabled (recommended for development):
```bash
streamlit run --server.runOnSave=true app.py
```

Or run without auto-reload:
```bash
streamlit run app.py
```

## Usage

1. Enter multiple faculty profile URLs in the text area (one URL per line)
2. Click "Process URLs" to start batch processing
3. Monitor progress with the progress bar
4. View real-time statistics in the dashboard
5. Edit extracted data directly in the grid
6. Download the complete dataset using the "Download CSV" button

## Data Persistence

- All scraped data is automatically saved to `faculty_profiles.csv`
- Data is loaded automatically when the app starts
- Changes made in the data editor are saved automatically
- Duplicate profiles (based on email) are detected and skipped

## Note

- Make sure the faculty profile URLs are publicly accessible
- The quality of extraction depends on the structure and content of the webpage
- The app uses GPT-4o for optimal extraction accuracy
- Data is persisted between sessions in the `faculty_profiles.csv` file

## Contributing

Pull requests are welcome! Feel free to contribute by:
- Adding new features
- Improving extraction accuracy
- Enhancing the UI/UX
- Fixing bugs
- Improving documentation 