import requests
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv() # Load the environment variables

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "fc5863d6-b718-4ba7-9158-d43ea09066fd"
FLOW_ID = "e5e837db-ff19-45a1-ae69-4d1df9d262da"
APPLICATION_TOKEN = os.environ.get('APP_TOKEN')
ENDPOINT = "Customer" # You can set a specific endpoint name in the flow settings


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    st.title("James Chat interface")

    message = st.text_area("Enter your message", placeholder="Ask a question")

    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return
    try:
        with st.spinner("Running the flow..."):
            response = run_flow(message)
        
        response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
        st.markdown(response)
    except Exception as e:
        st.error(str(e))

if __name__ == "__main__":
    main()
    

#result = run_flow('What are the shipping times?')
#print(result)
