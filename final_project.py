from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs
import os
from io import BytesIO
from reportlab.pdfgen import canvas
import requests

load_dotenv()

generated_response = {}


def extract_video_id(link):
    """Extract the video ID from a YouTube video link."""
    parsed_url = urlparse(link)
    if parsed_url.netloc == "www.youtube.com":
        query_params = parse_qs(parsed_url.query)
        return query_params.get("v", [None])[0]
    elif parsed_url.netloc == "youtu.be":
        return parsed_url.path.lstrip("/")
    return None


def generate(video_id):

    def GetSubtitles(video_id):
        op = YouTubeTranscriptApi.get_transcript(video_id)
        op_use = TextFormatter.format_transcript(op,op)
        return op_use

    def transcript_to_pdf(lines):
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer)

        # Set font and font size
        pdf.setFont("Helvetica", 9)

        # Add title (optional)
        pdf.drawString(50, 750, "YouTube Transcript")

        # Write each line of transcript with a line spacing
        y_pos = 700  # Starting position for the text

        for line in lines:
            pdf.drawString(50, y_pos, line)
            y_pos -= 15  # Adjust Y position for each line (line spacing)

        # Save the PDF document
        pdf.save()

        # Write the PDF content to a file (optional)
        with open("transcript.pdf", "wb") as output_file:
            output_file.write(pdf_buffer.getvalue())


    load_dotenv()
    #groq_api_key=os.environ['GROQ_API_KEY']
   
    groq_api_key= str(os.getenv("groq_api_key"))

    embeddings=HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5",model_kwargs={'device':'cpu'},encode_kwargs={'normalize_embeddings':True})
    llm=ChatGroq(groq_api_key=groq_api_key,
                model_name="llama3-70b-8192")
    prompt=ChatPromptTemplate.from_template(
        """
        You are a YouTube Comment Replying Chatbot.  
        Your task is to generate appropriate and relevant replies to YouTube comments based **only** on the provided context.  

        ### Instructions:
        - **Do not use external knowledge**—reply strictly based on the given context.  
        - **Keep responses concise and natural**, like a human reply.  
        - **Maintain a conversational and engaging tone** that fits YouTube discussions.
        <context>
        {context}
        <context>
        Questions:{input}

        """
        )

    #video_id = extract_video_id(video_link)
    if type(video_id)==str:
                
        subtitles = GetSubtitles(video_id)
        lines=subtitles.splitlines()
        transcript_to_pdf(lines)
        pdf_loader = PyPDFLoader("transcript.pdf")
        pdf_docs=pdf_loader.load()
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
        pdf_final_documents=text_splitter.split_documents(pdf_docs)
        pdf_vectors=FAISS.from_documents(pdf_final_documents,embeddings)
        document_chain = create_stuff_documents_chain(llm, prompt)
        pdf_retriever = pdf_vectors.as_retriever()
        pdf_retrieval_chain = create_retrieval_chain(pdf_retriever, document_chain)

        for id in questionsWithId:
            pdf_prompt=questionsWithId[id]
            if pdf_prompt:
                response=pdf_retrieval_chain.invoke({"input":pdf_prompt})
                generated_response[id] = response['answer']
                

def postReplyComment(id,text):
    token = str(os.getenv("token"))
    if token == "No token found":
        print("login first")
        return
    
    url = "https://www.googleapis.com/youtube/v3/comments?part=id,snippet"

    headers = {
        "Authorization": "Bearer "+token,
        "Content-Type": "application/json"
    }

    data = {
        "snippet": {
            "parentId": id,
            "textOriginal": text
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())


VIDEO_LINK = "https://youtu.be/sNVpbS4a8Fc?si=VLjOh-qUkMEFqn_U"

API_KEY = str(os.getenv("API_KEY"))
VIDEO_ID = extract_video_id(VIDEO_LINK)
URL = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={VIDEO_ID}&key={API_KEY}"


response = requests.get(URL)
data = response.json()
questionsWithId = {}

for item in data["items"]:
    comment_id = item["id"]  # Comment Thread ID
    comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    questionsWithId[comment_id] = comment_text
    #print(f"Comment ID: {comment_id}, Comment: {comment_text}")


generate(VIDEO_ID)

for each in generated_response:
    postReplyComment(each,generated_response[each])
    print(each,questionsWithId[each],generated_response[each],sep ="||||")
    print("_--------------------------------------------------------_")
        