import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_csv_file(file_path):
    df = pd.read_csv(file_path)

    df["Location"] = df["Location"].str.strip().str.lower()
    df["Room Type"] = df["Room Type"].str.strip().str.lower()
    df["Availability"] = df["Availability"].str.strip().str.lower()

    documents = df.apply(lambda row:
        f"Hotel Name: {row['Hotel Name']}, Location: {row['Location']}, Room Type: {row['Room Type']}, "
        f"Price Per Night: {row['Price Per Night (INR)']}, Amenities: {row['Amenities']}, Availability: {row['Availability']}",
        axis=1
    ).tolist()

    return df, documents

def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    return splitter.create_documents(documents)
