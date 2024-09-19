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

genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Sorry, I couldn't process your request. Please try again later."

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

def handle_user_input(user_input):
    user_input = user_input.lower()
    
    if "negotiate" in user_input or "price" in user_input:
        return "Sure! What price are you offering?"

    elif "discount" in user_input or "reduce" in user_input:
        if "%" in user_input:
            try:
                discount = float(user_input.split("%")[0].split()[-1])
                return f"Thank you for requesting a {discount}% discount. I'll check if that's possible."
            except ValueError:
                return "I didn't understand the discount percentage. Could you provide a valid number?"
        else:
            return "What discount percentage are you looking for?"

    elif "offer" in user_input and "$" in user_input:
        try:
            user_price = float(user_input.split("$")[1])
            return negotiate_price(user_price, START_PRICE)
        except ValueError:
            return "I didn't understand the price. Could you provide a valid amount?"

    elif "accept" in user_input or "agree" in user_input:
        return "Great! Your offer has been accepted. Thank you!"

    elif "decline" in user_input or "reject" in user_input:
        return "Sorry to hear that. The lowest I can go is $70. Would you like to accept that?"

    else:
        return get_gemini_response(user_input)

st.set_page_config(page_title="E-commerce Negotiation Chatbot")

st.header("Feel free to negotiate the product price with me or ask anything else!")

input_text = st.text_input("Enter your offer or start a conversation:", key="input")
submit = st.button("Send")

if submit:
    response = handle_user_input(input_text)
    
    st.subheader("Bot")
    st.write(response)
