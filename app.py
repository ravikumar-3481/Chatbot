import streamlit as st
import pandas as pd
import difflib
import time
import io
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="Chat with Ravi's AI",
    page_icon="🤖",
    layout="centered"
)

# --- Load Data ---
@st.cache_data
def load_qa_data():
    """Loads the Q&A dataset. Uses local file if available, else falls back to embedded data."""
    # Embedded fallback data just in case the CSV isn't in the same directory
    csv_data = """Category,Question,Personalized Answer
General,Who are you?,"Hi! I am Ravi Kumar Vishwakarma, a B.Tech CSE student specializing in AI, ML, Data Science, and Full-Stack Development. I bridge the gap between raw data and actionable business intelligence!"
General,What is your educational background?,"I am pursuing a B.Tech in Computer Science & Engineering with a minor in Mathematics. My math background helps me deeply understand the algorithms behind Machine Learning."
General,Are you looking for a job?,"Yes! I am currently open to internships, full-time roles, and freelance projects in Data Science, AI Engineering, and Full-Stack Development."
General,Are you open to relocation?,"Absolutely. I am open to relocating for the right opportunity, including international roles in places like the US or Dubai, as well as remote positions."
Experience,What dId you do at Cognizant and Future Intern?,"During my time there, I developed predictive dashboards that improved decision-making speed by 40% and built machine learning models that identified at-risk business trends with 85% accuracy."
Experience,Can you explain the 92% predictive accuracy on your profile?,"Definitely! I achieved 92% accuracy in an e-commerce sales forecasting project. I cleaned the dataset, performed feature engineering, and fine-tuned models to predict future sales trends accurately."
Experience,Tell me about your data pipeline experience.,"I have engineered scalable data pipelines processing over 50,000+ records. By implementing strict validation checks and handling anomalies, I ensure 99% data integrity for downstream analytics."
Tech Skills,What is your AI/ML tech stack?,"My core data stack includes Python, Pandas, NumPy, Scikit-Learn, and deep learning frameworks, along with data visualization tools and SQL for database management."
Tech Skills,What is your full-stack development experience?,"I have architected full-stack platforms supporting 1,000+ users. I typically use React and Tailwind CSS for the frontend, and Node.js or Python (FastAPI/Flask/Streamlit) for the backend to integrate ML models seamlessly."
Tech Skills,How good are your coding and problem-solving skills?,"I love algorithmic challenges! I have solved over 50 problems on LeetCode, which helps me write highly optimized and efficient code for my data ecosystems."
Projects,How does your Stock Prediction app work?,"It is a web application built using Python and Streamlit. It utilizes machine learning algorithms to analyze historical market data and forecast future stock trends."
Projects,Tell me about the gesture-controlled drawing app.,"I built it using computer vision! It uses OpenCV for video capture and Google's MediaPipe framework to track hand landmarks, allowing users to draw on the screen just by moving their fingers."
Contact,How can I download your resume?,"You can download my latest resume by clicking the 'Hire me' or 'View Resume' buttons right at the top of my portfolio's home page!"
Contact,How can I contact you or schedule an interview?,"You can use the 'Contact' form on my website, or connect with me directly on LinkedIn. I'd love to chat!"
Personal,What do you do for fun outside of coding?,"When I am not training AI models or solving LeetCode problems, you can probably find me relaxing and listening to high-bass Haryanvi music!"
"""
    file_name = "chatbot_qa_dataset.csv"
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.read_csv(io.StringIO(csv_data))

df = load_qa_data()

# --- Rule-Based Logic Engine ---
def get_bot_response(user_input, dataframe):
    """Determines the best response based on string similarity and keywords."""
    user_input_lower = user_input.lower()
    
    # 1. Try to find a close match using difflib (String Similarity)
    questions = dataframe['Question'].tolist()
    # cutoff=0.5 means it requires a 50% match to trigger the answer
    matches = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)
    
    if matches:
        best_match = matches[0]
        answer = dataframe[dataframe['Question'] == best_match]['Personalized Answer'].values[0]
        return answer
        
    # 2. Fallback to Keyword Matching if no close question is found
    keyword_responses = {
        "hi": "Hello! I am Ravi's AI assistant. How can I help you today?",
        "hello": "Hi there! I am Ravi's virtual assistant. Ask me about his projects or skills!",
        "skills": "Ravi is highly skilled in Python, Machine Learning, Data Analytics, React, and Node.js.",
        "experience": "Ravi has worked on predictive dashboards at Cognizant & Future Intern, improving decision speeds by 40%.",
        "projects": "Ravi has built cool things like a Stock Prediction app and a Gesture-Controlled drawing app!",
        "resume": "You can easily download Ravi's resume using the 'View Resume' button on his portfolio.",
        "contact": "You can reach out to Ravi via the contact form on his site or through his LinkedIn profile.",
        "hire": "Ravi is currently open to full-time roles, internships, and freelance projects!"
    }
    
    for word, response in keyword_responses.items():
        if word in user_input_lower:
            return response
            
    # 3. Ultimate Fallback for unrecognized inputs
    return ("I'm a simple rule-based bot, so I didn't quite catch that! "
            "Try asking me about Ravi's **skills**, **projects**, **experience**, or how to **contact** him.")


# --- UI Layout ---
st.title("🤖 Chat with Ravi")
st.markdown("Welcome! I am an AI assistant trained on Ravi Kumar Vishwakarma's portfolio. Ask me anything about his experience, skills, or projects.")

# Sidebar with quick prompts
with st.sidebar:
    st.header("💡 Try asking me:")
    for q in df['Question'].sample(5).tolist(): # Show 5 random questions
        st.write(f"- *{q}*")
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit")

# --- Chat History Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I am Ravi's AI assistant. What would you like to know about him?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input & Processing ---
if prompt := st.chat_input("Ask me about Ravi's skills or projects..."):
    
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get Bot Response
    response = get_bot_response(prompt, df)

    # Display assistant response in chat message container with a typing effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate typing speed
        for chunk in response.split(" "):
            full_response += chunk + " "
            time.sleep(0.05) 
            message_placeholder.markdown(full_response + "▌")
            
        message_placeholder.markdown(full_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
