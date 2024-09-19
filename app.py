import textwrap
import dotenv
from dotenv import load_dotenv
import markdown_it
import streamlit as st
import os
import google.generativeai as genai

load_dotenv()

def to_markdown(text):
    text = text.replace('•', '  *')
    return markdown_it(textwrap.indent(text, '> ', predicate=lambda _: True))


genai.configure(api_key=os.getenv("AIzaSyCtXRoHFvElhnHzwFO4qazg3utSEHgS6yY"))


def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text


START_PRICE = 100  
MIN_PRICE = 70  
MAX_PRICE = 120  


def negotiate_price(user_price, current_price):
    if user_price >= current_price:
        return f"Great! Your offer of ${user_price} has been accepted."
    elif user_price >= MIN_PRICE:
        counter_offer = (current_price + user_price) / 2  
        return f"How about we meet halfway at ${counter_offer:.2f}?"
    else:
        return f"Sorry, the lowest I can go is ${MIN_PRICE}. Would you like to accept that?"

st.set_page_config(page_title="E-commerce Negotiation Chatbot")

st.header("Feel free to negotiate the product price with me or ask anything else!")

input_text = st.text_input("Enter your offer or start a conversation:", key="input")
submit = st.button("Send")

if submit:
    try:

        user_price = float(input_text)
        response = negotiate_price(user_price, START_PRICE)
    except ValueError:
        response = get_gemini_response(input_text)

    st.subheader("The Response is")
    st.write(response)
