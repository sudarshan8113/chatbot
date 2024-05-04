import streamlit as st
import requests
import os

# Set the API key and model name
API_KEY = "esecret_dn8hv9jc1zlv83nbutlimnde5g"
MODEL_NAME = "meta-llama/Meta-Llama-3-70B-Instruct"

# Set the base URL
BASE_URL = "https://api.endpoints.anyscale.com/v1"

# Set the page configuration
st.set_page_config(
    page_title="Helpful Chatbot",
    page_icon=":robot_face:",
    initial_sidebar_state="expanded"
)

# Add a header
st.title("Helpful Chatbot")

# Add a text area for the user to enter their prompt
prompt_container = st.container()
with prompt_container:
    st.header("Enter your prompt:")
    prompt = st.text_area("", height=50, placeholder="Type something...")

# Add a button to submit the query
submit_button = st.button("Submit")

# Move these to the sidebar
with st.sidebar:
    # Add a header for the sidebar
    st.header("Settings")

    # Add a dropdown for the model selection
    st.header("Select a model:")
    model_options = [
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "meta-llama/Meta-Llama-3-70B-Instruct",
        "codellama/CodeLlama-70b-Instruct-hf",
        "mistralai/Mistral-7B-Instruct-v0.1",
        "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "mistralai/Mixtral-8x22B-Instruct-v0.1"
    ]
    selected_model = st.selectbox("", model_options)

    # Add a slider to adjust the temperature
    st.header("Adjust the temperature:")
    temperature = st.slider("", 0.0, 1.0, 0.7)

    # Add a checkbox to enable/disable chat history
    st.header("Show chat history:")
    show_chat_history = st.checkbox("")

# Create a chat history container
chat_history = st.container()

# Define a function to send the request to the API
def send_request(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": selected_model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
    return response

# Define a function to display the response
def display_response(response):
    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"]
        st.success(result)
    else:
        error_response = response.json()
        st.error(f"An error occurred: {error_response['error']['message']}")

# Define a function to update the chat history
def update_chat_history(prompt, response):
    if show_chat_history:
        chat_history.write(f"User: {prompt}")
        chat_history.write(f"Chatbot: {response.json()['choices'][0]['message']['content']}")

# Send the request to the API when the submit button is clicked
if submit_button:
    response = send_request(prompt)
    display_response(response)
    update_chat_history(prompt, response)