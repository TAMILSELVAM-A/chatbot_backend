from services.data_loader import load_csv_file, split_text
from vectorstore.vectordb import create_vector_store, retrieve_answer
from services.model_loader import load_llm
from app.config import SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
import pandas as pd
from services.booking import is_valid_date, book_hotel, check_booking_status
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, '../data/Leela_palace.csv')

df = pd.read_csv(CSV_PATH)


# Load data
try:
    file_path = CSV_PATH
    df, documents = load_csv_file(file_path)
    text_chunks = split_text(documents)
except Exception as e:
    print(f"Error loading or processing data: {e}")
    raise

# Create vector store
try:
    vector_store = create_vector_store(text_chunks)
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
except Exception as e:
    print(f"Error creating vector store: {e}")
    raise

# Load LLM model
try:
    llm = load_llm()
except Exception as e:
    print(f"Error loading LLM model: {e}")
    raise

# Create prompt template
try:
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ('human', "{input}")
    ])
except Exception as e:
    print(f"Error creating prompt template: {e}")
    raise

# Create chains
try:
    qanda_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, qanda_chain)
except Exception as e:
    print(f"Error creating chains: {e}")
    raise

user_session = {}

def process_query(user_id: str, query: str) -> str:
    try:
        query = query.lower().strip()

        if query in ["bye", "quit", "exit"]:
            if user_id in user_session:
                del user_session[user_id]  # Clear session if ongoing
            return "Thank you for chatting with The Leela Palace. Have a great day! 😊"
        
        elif "check booking" in query or "booking status" in query:
            user_session[user_id] = {"step": "check_booking"}
            return "Please provide your Booking ID to check the status."
        
        elif "book" in query:
            try:
                df = pd.read_csv(file_path)  # Read hotel locations
                available_locations = df["Location"].unique()
                location_options = "\n".join([f"- {loc}" for loc in available_locations])
            except Exception as e:
                return f"Error retrieving hotel locations: {e}"

            user_session[user_id] = {"step": "ask_location"}
            return f"Which location are you looking to book a hotel in?\nAvailable locations:\n{location_options}"
        
        elif user_id not in user_session:
            try:
                return rag_chain.invoke({"input": query})['answer']
            except Exception as e:
                return f"Error processing your query: {e}"

        current_step = user_session[user_id]["step"]

        if current_step == "ask_location":
            location = query.title()
            try:
                df = pd.read_csv(file_path)
                if location.lower() not in df["Location"].str.lower().unique():
                    return "Sorry, we don't have a hotel at this location. Try another location."
            except Exception as e:
                return f"Error validating location: {e}"

            user_session[user_id]["location"] = location
            user_session[user_id]["step"] = "ask_room_type"

            try:
                available_rooms = df[df["Location"].str.lower() == location.lower()]["Room Type"].unique()
                room_options = "\n".join([f"- {room}" for room in available_rooms])
                return f"Great! Available room types in {location}:\n{room_options}\nPlease select a room type."
            except Exception as e:
                return f"Error retrieving room types: {e}"
        
        elif current_step == "ask_room_type":
            room_type = query.title()
            user_session[user_id]["room_type"] = room_type
            user_session[user_id]["step"] = "ask_guest_name"
            return "Got it! Please provide your name for the booking."
        
        elif current_step == "ask_guest_name":
            user_session[user_id]["guest_name"] = query
            user_session[user_id]["step"] = "ask_checkin"
            return "Thanks! Please enter your check-in date (YYYY-MM-DD)."
        
        elif current_step == "ask_checkin":
            if not is_valid_date(query):
                return "Invalid date! Please enter a valid check-in date (YYYY-MM-DD)."
            user_session[user_id]["checkin_date"] = query
            user_session[user_id]["step"] = "ask_checkout"
            return "Noted! Now, please enter your check-out date (YYYY-MM-DD)."
        
        elif current_step == "ask_checkout":
            if not is_valid_date(query) or query <= user_session[user_id]["checkin_date"]:
                return "Invalid date! Check-out must be after check-in and in valid format (YYYY-MM-DD)."
            user_session[user_id]["checkout_date"] = query

            try:
                session = user_session[user_id]
                booking_result = book_hotel(
                    session["location"],
                    session["room_type"],
                    session["guest_name"],
                    session["checkin_date"],
                    session["checkout_date"]
                )
                del user_session[user_id]
                return booking_result
            except Exception as e:
                return f"Error booking hotel: {e}"
        
        elif current_step == "check_booking":
            try:
                status_result = check_booking_status(query)
                del user_session[user_id]
                return status_result
            except Exception as e:
                return f"Error checking booking status: {e}"
        
        return rag_chain.invoke({"input": query})['answer']
    
    except Exception as e:
        return f"An unexpected error occurred: {e}"