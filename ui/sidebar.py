import streamlit as st

from ui.chat_utils import truncate_message, switch_thread, create_new_thread


# Cache the CSS to prevent re-rendering on every interaction
@st.cache_data
def get_sidebar_css():
    return """
    <style>
    .thread-container {
        margin: 0px !important;
        padding: 0px !important;
    }

    .stButton {
        margin: 0px !important;
        padding: 0px !important;
    }

    .stButton > button {
        margin: 1px !important;
        padding: 8px !important;
        width: 100% !important;
    }
    .stButton:first-child > button {
        margin-bottom: 2px !important;
    }

    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
    }

    .element-container {
        margin: 0px !important;
        padding: 0px !important;
    }
    div[data-testid="stVerticalBlock"] > div {
        gap: 0rem !important;
        padding: 0rem !important;
    }

    div[class*="stVerticalBlock"] {
        margin: 3px !important;
        gap: 0rem !important;
        padding: 0rem !important;
    }

    .stButton,
    .stMarkdown,
    div[data-testid="column"] {
        margin: 0px !important;
        padding: 0px !important;
    }

    .stButton > button {
        margin: 0px !important;
        padding: 8px !important;
    }

    .element-container,
    .stMarkdown > div {
        margin: 0px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    /* Target the button text directly */
    [data-testid="stButton"] button p {
        font-size: 0.9rem !important;
    }
    </style>
    """


def render_sidebar():
    st.markdown(
        """
        <style>
            .sidebar-title {
                font-family: Georgia, 'Times New Roman', serif !important;
                text-align: center !important;
                padding: 0rem 0 !important;
                font-size: 3rem !important;
                color: #3D2914 !important;
                margin-bottom: 0.5rem!important;
            }
            /* Navigation menu */
            .support-nav-item {
                position: relative;
            }
            .support-nav-item .support-dropdown {
                display: block;
                position: absolute;
                left: 0;
                background-color: #D4A574 !important;
                padding: 10px;
                width: 102%;
                z-index: 1000;
                border-radius: 8px;
                color: #3D2914 !important;
                text-align: center !important;
                visibility: hidden;
                opacity: 0;
                transition: opacity 0.3s, visibility 0s linear 1s;
            }
            .support-nav-item:hover .support-dropdown {
                visibility: visible;
                opacity: 1;
                transition-delay: 1s;
            }
            .email-item {
                padding: 8px;
                margin: 5px 0;
                border-bottom: 1px solid rgba(61, 41, 20, 0.2);
            }
             /* Chat list section */
            .chat-list-header {
                padding: 1px 10px;
                color: rgba(61, 41, 20, 0.7);
                align-items: center;
                font-size: 1.2rem;
                font-weight: 100;
            }

            /* User profile section */
            .user-profile {
                position: fixed;
                bottom: 20px;
                left: 10px;
                width: 230px;
                padding: 16px 24px;
                background: rgba(255, 255, 255, 0.3);
                display: flex;
                align-items: left;
                gap: 12px;
                border-radius: 8px;
                z-index: 100;
            }
            .user-profile:hover {
                background: rgba(255, 255, 255, 0.4);
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(139, 90, 43, 0.2);
            }
            .user-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                background-image: url('https://pbs.twimg.com/profile_images/1557071011467739136/mBfyJP5B_400x400.jpg');
                background-size: cover;
                background-position: center;
            }

            .user-info {
                flex-grow: 1;
            }

            .user-name {
                color: #3D2914;
                font-size: 1rem;
                align-items: center;
            }

            .user-email {
                color: rgba(61, 41, 20, 0.7);
                font-size: 1rem;
                align-items: center;
            }
            .stButton > button {
                margin: 0px;
                padding: 12px 16px;
                background: rgba(255, 255, 255, 0.7) !important;
                border-radius: 12px;
                color: #5D4E37 !important;
                text-align: center;
                cursor: pointer;
                transition: all 0.2s ease;
                width: 100%;
                border: none !important;
                border-left: 4px solid #C4A57B !important;
                box-shadow: 0 2px 8px rgba(139, 90, 43, 0.08);
                font-size: 0.95rem;
            }

            .stButton > button:hover {
                background: #FFF8F0 !important;
                box-shadow: 0 4px 12px rgba(139, 90, 43, 0.15);
                transform: translateY(-1px);
            }

            /* Section header */
            .section-header {
                color: #3D2914;
                font-size: 20px;
                margin: 24px 0 16px 0;
                padding: 0 12px;
            }
            /* Optional: Add hover effect */
            .sidebar-title:hover {
                color: rgba(61, 41, 20, 0.8) !important;
            }


        </style>

        """,
        unsafe_allow_html=True
    )
    # sidebar items
    st.markdown("""
                
            """, unsafe_allow_html=True)
    # Chat List Section
    st.markdown('<div class="chat-list-header"></div>', unsafe_allow_html=True)

    # Functions for thread management


    # Apply custom styling
    st.markdown(get_sidebar_css(), unsafe_allow_html=True)

    if st.button("+New Thread", key="new_thread_btn", use_container_width=True):
        create_new_thread()

    # Limit to most recent 10 threads for performance
    sorted_threads = sorted(st.session_state.chat_history.items(), key=lambda x: float(x[0]), reverse=True)[:20]
    
    for thread_id, thread in sorted_threads:
        try:
            first_message = thread['messages'][0]["content"] if thread else "No messages yet"
            first_message = truncate_message(first_message, length=30)
        except (IndexError, KeyError, TypeError):
            first_message = "No messages yet"

        if st.button(f"{first_message}", key=f"switch_{thread_id}", use_container_width=True):
            switch_thread(thread_id)
