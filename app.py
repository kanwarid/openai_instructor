import os 
import openai
import instructor
from pydantic import BaseModel
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
# Now you can access the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    print("OPENAI_API_KEY environment variable not set")
else:
    print("OPENAI_API_KEY:", api_key)
# Define your desired output structure
class BookInfo(BaseModel):
    title: str = Field(..., description="""Title of the book in title case""")
    summary: str = Field(..., description="""Brief summary of the entire book
                         describing the context and theme in about 100 tokens""")
    author: str = Field(..., description="""Author Name as Last Name, First Name format
                        like Dickens, Charles""")
    publisher: str = Field(..., description="""Publisher's Name""")
    published_year: int = Field(..., description="""Publishing Year""")
    genre: str = Field(..., description="""Book genre (e.g., fiction, non-fiction, mystery, sci-fi)""")
    

client = instructor.from_openai(OpenAI(api_key=openai.api_key))

completion = client.chat.completions.create_iterable(
    model="gpt-4o-mini-2024-07-18",
    messages=[
        {
            "role": "user",
            "content": "Give me names of top trhee best selling books of all time"
        }
    ],
    response_model=BookInfo
)

# Process the completion response
for response_chunk in completion:
    # Assuming each response_chunk conforms to the BookInfo model
    book_info = response_chunk  # This should be an instance of BookInfo
    print(f"Title: {book_info.title}")
    print(f"Author: {book_info.author}")
    print(f"Publisher: {book_info.publisher}")
    print(f"Year: {book_info.published_year}")
    print(f"Genre: {book_info.genre}")
    print(f"Summary: {book_info.summary}")
    print("-" * 40)

