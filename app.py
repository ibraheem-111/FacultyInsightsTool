import streamlit as st
import pandas as pd
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with default configuration
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"),
    temperature=0,
    max_tokens=8000
)

# Set page config
st.set_page_config(page_title="Faculty Profile Scraper", layout="wide")
st.title("Faculty Profile Scraper")

# File path for storing the data
DATA_FILE = "faculty_profiles.csv"

# Load existing data from CSV if it exists
def load_existing_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(
        columns=['University', 'Department', 'Emailed', 'Designation', 
                'Name', 'Email', 'Research Area', 'Lab', 'Relevant Links']
    )

# Initialize session state
if 'faculty_data' not in st.session_state:
    st.session_state.faculty_data = load_existing_data()

# Function to scrape and process faculty data
def process_faculty_url(url):
    try:
        # Load and split the webpage content
        loader = WebBaseLoader(url)
        docs = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
        splits = text_splitter.split_documents(docs)
        
        # Combine all splits into one text
        combined_text = " ".join([split.page_content for split in splits])
        
        # Create prompt template
        template = """
        Extract faculty information from the following webpage content. 
        If a piece of information is not found, write "Not found".
        
        Webpage content: {text}
        
        Please extract and format the following information:
        - University:
        - Department:
        - Designation (e.g., Professor, Associate Professor):
        - Name:
        - Email:
        - Research Area:
        - Lab (if any):
        - Relevant Links (including the input URL):
        
        Format the response as a pipe-separated string in this exact order:
        University|Department|Designation|Name|Email|Research Area|Lab|Relevant Links
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        # Create the chain
        chain = prompt | llm | StrOutputParser()
        
        # Run the chain
        result = chain.invoke({"text": combined_text})
        
        # Split the result and create a dictionary
        fields = result.strip().split('|')
        data = {
            'University': fields[0],
            'Department': fields[1],
            'Emailed': False,
            'Designation': fields[2],
            'Name': fields[3],
            'Email': fields[4],
            'Research Area': fields[5],
            'Lab': fields[6],
            'Relevant Links': fields[7] + ", " + url
        }
        
        return data
        
    except Exception as e:
        st.error(f"Error processing URL: {str(e)}")
        return None

# Create two columns for the layout
col1, col2 = st.columns([2, 1])

with col1:
    # URL input area
    urls = st.text_area("Enter faculty profile URLs (one per line):", height=150)
    
    if st.button("Process URLs"):
        if urls:
            url_list = [url.strip() for url in urls.split('\n') if url.strip()]
            
            if url_list:
                progress_bar = st.progress(0)
                for i, url in enumerate(url_list):
                    with st.spinner(f"Processing URL {i+1}/{len(url_list)}..."):
                        data = process_faculty_url(url)
                        if data:
                            # Check if this profile already exists (based on email)
                            if not st.session_state.faculty_data.empty and data['Email'] in st.session_state.faculty_data['Email'].values:
                                st.warning(f"Profile with email {data['Email']} already exists. Skipping...")
                                continue
                                
                            # Add new data to DataFrame
                            st.session_state.faculty_data = pd.concat([
                                st.session_state.faculty_data,
                                pd.DataFrame([data])
                            ], ignore_index=True)
                            
                            # Save to CSV after each successful scrape
                            st.session_state.faculty_data.to_csv(DATA_FILE, index=False)
                            
                    progress_bar.progress((i + 1) / len(url_list))
                
                st.success("All URLs processed successfully!")
        else:
            st.warning("Please enter at least one URL")

with col2:
    # Statistics
    st.subheader("Statistics")
    if not st.session_state.faculty_data.empty:
        st.write(f"Total Profiles: {len(st.session_state.faculty_data)}")
        st.write(f"Universities: {st.session_state.faculty_data['University'].nunique()}")
        st.write(f"Departments: {st.session_state.faculty_data['Department'].nunique()}")
        st.write(f"Emailed: {st.session_state.faculty_data['Emailed'].sum()}")

# Display and edit the DataFrame
st.subheader("Faculty Profiles Database")
edited_df = st.data_editor(
    st.session_state.faculty_data,
    num_rows="dynamic",
    use_container_width=True,
    key="data_editor"
)

# Update the session state and save to CSV when data is edited
if not edited_df.equals(st.session_state.faculty_data):
    st.session_state.faculty_data = edited_df
    edited_df.to_csv(DATA_FILE, index=False)

# Export functionality
if st.download_button(
    label="Download CSV",
    data=edited_df.to_csv(index=False),
    file_name="faculty_profiles.csv",
    mime="text/csv"
):
    st.success("File downloaded successfully!") 