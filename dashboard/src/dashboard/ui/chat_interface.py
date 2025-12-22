import os
import streamlit as st
import markdown

from memory.conversation import ConversationBufferWindow
from utils.chat_utils import generate_unique_thread_id, save_chat_history

# Create the custom JavaScript component
js_code = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const inputField = document.querySelector('[data-testid="stTextInput"] input');
    const sendButton = document.querySelector('.send-button');

    // Handle button click
    sendButton.addEventListener('click', function() {
        if (inputField.value.trim() !== '') {
            submitMessage();
        }
    });

    // Handle Enter key press
    inputField.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && inputField.value.trim() !== '') {
            submitMessage();
        }
    });

    function submitMessage() {
        const submitEvent = new Event('submit', {
            'bubbles': true,
            'cancelable': true
        });
        inputField.form.dispatchEvent(submitEvent);
    }
});
</script>
"""

def render_chat_messages():
    if st.session_state.current_thread is not None:
        # Render messages for the current thread
        for msg in st.session_state.chat_history[st.session_state.current_thread]['messages']:
            role_class = "user-message" if msg["role"] == "user" else "assistant-message"
            # Convert markdown to HTML for proper table rendering
            content_html = markdown.markdown(msg["content"], extensions=['tables', 'nl2br'])
            st.markdown(f'<div class="chat-message-wrapper {role_class}"><div class="chat-bubble">{content_html}</div></div>', unsafe_allow_html=True)


def handle_flow_interaction(prompt, flow, container=None):
    if prompt:  # Using the prompt from the text_input
        st.session_state.show_placeholder = False
        if container:
            container.empty()

        if st.session_state.current_thread is None:
            st.session_state.current_thread = generate_unique_thread_id()
            st.session_state.chat_history[st.session_state.current_thread] = {}
            # st.session_state.memory = ConversationBufferWindow(window_size=10)
            st.session_state.chat_history[st.session_state.current_thread]['messages'] = []
            st.session_state.chat_history[st.session_state.current_thread]['conversation'] = ConversationBufferWindow(window_size=10)

            # st.session_state.messages = []  # Reset messages for the new thread

        # Append user message
        user_message = {"role": "user", "content": prompt}
        st.session_state.chat_history[st.session_state.current_thread]['messages'].append(user_message)

        # Convert markdown to HTML and render user message
        user_html = markdown.markdown(prompt, extensions=['tables'])
        st.markdown(f'<div class="chat-message-wrapper user-message"><div class="chat-bubble">{user_html}</div></div>', unsafe_allow_html=True)

        flow.state.conversation_history = st.session_state.chat_history[st.session_state.current_thread]['conversation']

        if not isinstance(st.session_state.chat_history[st.session_state.current_thread]['conversation'], ConversationBufferWindow):
            data = st.session_state.chat_history[st.session_state.current_thread]['conversation']
            st.session_state.chat_history[st.session_state.current_thread]['conversation'] = ConversationBufferWindow.from_dict(data)

        flow.state.conversation_history = st.session_state.chat_history[st.session_state.current_thread]['conversation']

        flow.state.current_query = prompt
        
        with st.spinner("Processing your query..."):
            flow.kickoff()
                
        # Clear progress messages after execution
        flow.clear_progress()

        # Append assistant response
        response = flow.state.response
        assistant_message = {"role": "assistant", "content": response}
        st.session_state.chat_history[st.session_state.current_thread]['messages'].append(assistant_message)

        # Convert markdown to HTML and render assistant message
        response_html = markdown.markdown(response, extensions=['tables', 'nl2br'])
        st.markdown(f'<div class="chat-message-wrapper assistant-message"><div class="chat-bubble">{response_html}</div></div>', unsafe_allow_html=True)

        # st.session_state.messages = st.session_state.chat_history[st.session_state.current_thread]['messages']
        st.session_state.show_placeholder = False
        save_chat_history()
        st.session_state.text_input = ""




def create_chat_interface(flow_class, mongodb_uri, database_name, collection_names):
    placeholder_spot = st.empty()

    col1, col2, col3 = st.columns([1, 20, 1])
    st.session_state.message_container = col2

    # print(st.session_state.message_container)

    with st.session_state.message_container:
        # Move history rendering inside the container
        render_chat_messages()
        
        flow = flow_class()
        
        prompt = st.chat_input("What is your question?")
        if prompt:
            # Clear the placeholder immediately
            placeholder_spot.empty()
            handle_flow_interaction(prompt, flow, placeholder_spot)

    # display messages or placeholder
    if st.session_state.show_placeholder:
        with placeholder_spot.container():

            st.markdown("""
                <style>
                .main-header {
                    position: fixed; /* Ensure it can be positioned */
                    font-family: Georgia, 'Times New Roman', serif !important;
                    font-size: 3.5rem !important;
                    top: 100px;
                    left: 50%;
                    transform: translateX(-50%);
                    text-align: center;
                    z-index: 10;
                    color: #3D2914 !important;
                }

                .subheader {
                    position: fixed; /* Ensure it can be positioned */
                    top: 180px;
                    left: 50%;
                    transform: translateX(-50%);
                    text-align: center;
                    z-index: 10;
                    color: #3D2914 !important;
                }

                /* Feature container */
                .feature-container {
                    position: fixed; /* Fix relative to viewport */
                    bottom: 100px; /* Space from the bottom of the viewport */
                    left: 50%; /* Center horizontally */
                    transform: translateX(-50%); /* Ensure exact centering */
                    display: flex; /* Flex layout for child elements */
                    justify-content: space-between; /* Space between child elements */
                    gap: 10px; /* Add space between feature boxes */
                    width: 90%; /* Adjust width for responsiveness */
                    max-width: 700px; /* Optional: prevent too wide a container */
                    background-color: transparent; /* Light background for visibility */
                    padding: 20px; /* Padding inside the container */
                    border-radius: 12px; /* Rounded corners */
                    z-index: 9999; /* Ensure it's above other elements */
                }

                /* Feature box */
                .feature-box {
                    background-color: rgba(255, 255, 255, 0.6); /* Cream white background */
                    border-radius: 15px; /* Rounded corners */
                    padding: 20px;
                    flex: 2; /* Equal width for all boxes */
                    text-align: center; /* Center text inside each box */
                    color: #3D2914; /* Dark brown text */
                    height: auto; /* Allows box to grow with content */
                    max-height: 50%; /* Takes full height of container */
                    border: 1px solid rgba(139, 90, 43, 0.2);
                }
                .feature-box h3 {
                    color: #3D2914;
                    font-size: 1rem;
                    margin-bottom: 0.5rem;
                    font-weight: 600;
                    text-align: center;
                }
                .feature-content {
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                    flex-grow: 1; /* Allows content to expand */
                }

                .feature-item {
                    background-color: rgba(255, 255, 255, 0.7);
                    padding: 8px 12px;
                    margin: 4px 0;
                    border-radius: 8px;
                    color: #3D2914;
                    font-size: 0.9rem;
                    border: 1px solid rgba(139, 90, 43, 0.15);
                }
                </style>
                """, unsafe_allow_html=True)

            # Main header and subheader
            # Main header and subheader
            st.markdown("<h3 class='main-header'>DineLytics</h3>", unsafe_allow_html=True)
            st.markdown(
                "<p class='subheader'>Explore Trends, Sales and Item performance interactively with insights from restaurant data.</p>",
                unsafe_allow_html=True)

            # Feature boxes with styled items
            st.markdown("""
                <div class="feature-container">
                    <div class="feature-box">
                        <h3>Examples</h3>
                        <div class="feature-item">What are the sales of pizza till now?</div>
                        <div class="feature-item">Show me daily revenue trend for November 2025</div>
                        <div class="feature-item">What are the top 10 best-selling products?</div>
                        <div class="feature-item">What percentage of orders were cancelled?</div>
                    </div>

                </div>
                """, unsafe_allow_html=True)
