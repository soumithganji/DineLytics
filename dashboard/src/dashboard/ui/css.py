import streamlit as st

def apply_css():
    # Light warm color theme based on #E8C49B
    st.markdown(f"""
    <style>
        /* Reset default Streamlit styles */
        #root > div:first-child {{
            background-color: transparent;
        }}
        
        /* Sidebar container - lighter warm tone */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #D4A574, #C4956A) !important;
            padding: 0;
        }}

        /* Main app background - warm peach */
        .stApp {{
            background: #E8C49B;
            min-height: 100vh;
        }}

        /* Top header bar - match background */
        header[data-testid="stHeader"] {{
            background: #E8C49B !important;
        }}

        /* Header elements - brown color */
        header[data-testid="stHeader"] button,
        header[data-testid="stHeader"] svg,
        header[data-testid="stHeader"] [data-testid="stToolbar"],
        header[data-testid="stHeader"] [data-testid="stToolbar"] button,
        header[data-testid="stHeader"] [data-testid="stToolbar"] svg,
        [data-testid="collapsedControl"],
        [data-testid="collapsedControl"] *,
        [data-testid="collapsedControl"] svg,
        [data-testid="collapsedControl"] svg path,
        [data-testid="collapsedControl"] button,
        button[data-testid="baseButton-headerNoPadding"],
        button[data-testid="baseButton-headerNoPadding"] svg {{
            color: #8B5A2B !important;
            fill: #8B5A2B !important;
            stroke: #8B5A2B !important;
        }}

        /* Deploy button text */
        header[data-testid="stHeader"] span,
        header[data-testid="stHeader"] p {{
            color: #3D2914 !important;
        }}

        /* Source file changed status widget - brown links */
        [data-testid="stStatusWidget"],
        [data-testid="stStatusWidget"] *,
        [data-testid="stStatusWidget"] a,
        [data-testid="stStatusWidget"] button,
        .stStatusWidget a,
        .stStatusWidget button {{
            color: #8B5A2B !important;
        }}

        .main .block-container {{
            background: transparent !important;
            padding: 0;
            margin-left: 0% !important;
            position: relative;
            width: 100% !important;
        }}

        /* Message cards */
        [data-testid="stChatMessage"] {{
            background: rgba(255, 255, 255, 0.4) !important;
            border: 1px solid rgba(139, 90, 43, 0.2);
            border-radius: 8px;
            margin: 2rem 0 !important;
            padding: 1rem;
            max-width: 800px;
            width: 100%;
            position: relative;
            text-align: left !important;
            clear: both !important;
        }}

        .chat-card {{
            background: rgba(255, 255, 255, 0.5);
            padding: 20px;
            border-radius: 10px;
            margin: 10px 0;
        }}

        [data-testid="stChatMessage"] {{
            font-size: 18px !important;
        }}

        /* Custom chat message for avatar-less display */
        .chat-message-wrapper {{
            display: flex;
            width: 100%;
            margin: 0.5rem 0;
        }}
        
        .chat-message-wrapper.user-message {{
            justify-content: flex-end;
        }}
        
        .chat-message-wrapper.assistant-message {{
            justify-content: flex-start;
        }}
        
        /* Chat bubble styling - warm colors */
        .chat-bubble {{
            max-width: 75%;
            padding: 1rem;
            border-radius: 12px;
            color: #3D2914;
            font-size: 16px;
            word-wrap: break-word;
        }}
        
        /* User message - same as AI (cream white) */
        .chat-message-wrapper.user-message .chat-bubble {{
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(139, 90, 43, 0.15);
        }}
        
        /* AI message - cream white */
        .chat-message-wrapper.assistant-message .chat-bubble {{
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid rgba(139, 90, 43, 0.15);
        }}
        
        /* Style tables inside chat messages */
        .chat-bubble table {{
            width: 100%;
            border-collapse: collapse;
            margin: 0.5rem 0;
            font-size: 14px;
        }}
        
        .chat-bubble th, .chat-bubble td {{
            border: 1px solid rgba(139, 90, 43, 0.3);
            padding: 8px 12px;
            text-align: left;
            color: #3D2914;
        }}
        
        .chat-bubble th {{
            background: rgba(139, 90, 43, 0.15);
            font-weight: 600;
        }}
        
        .chat-bubble tr:hover {{
            background: rgba(139, 90, 43, 0.08);
        }}
        
        .chat-bubble p {{
            margin: 0.5rem 0;
            color: #3D2914;
        }}
        
        .chat-bubble p:first-child {{
            margin-top: 0;
        }}
        
        .chat-bubble p:last-child {{
            margin-bottom: 0;
        }}

        /* Redesigned Chat Input Styling - cream with brown accents */
        div[data-testid="stChatInput"] {{
            position: fixed;
            bottom: 2vh;
            left: 50%;
            transform: translateX(-50%);
            background-color: #FFF8F0 !important;
            opacity: 1 !important;
            width: 80% !important;
            max-width: 800px;
            padding: 8px 12px !important;
            border-radius: 12px !important;
            border: 1px solid rgba(139, 90, 43, 0.3) !important;
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            justify-content: flex-start !important;
            z-index: 99999 !important;
            box-shadow: 0 4px 15px rgba(139, 90, 43, 0.2) !important;
        }}

        /* Target the input wrapper */
        div[data-testid="stChatInput"] > div:first-child {{
            background-color: transparent !important;
            border: none !important;
            flex-grow: 1 !important;
            flex-shrink: 1 !important;
            margin: 0 12px 0 0 !important;
            width: 100% !important;
            align-self: center !important;
        }}

        /* Reset all internal containers */
        div[data-baseweb="base-input"], 
        div[data-baseweb="textarea"],
        div[data-baseweb="textarea"] > div {{
            background-color: transparent !important;
            border: none !important;
            width: 100% !important;
            max-width: none !important;
        }}

        /* Target the textarea directly */
        div[data-testid="stChatInput"] textarea {{
            background-color: transparent !important;
            color: #3D2914 !important;
            border: none !important;
            box-shadow: none !important;
            padding: 4px 48px 4px 0 !important;
            width: 100% !important;
            resize: none !important;
            line-height: 1.5 !important;
            min-height: 36px !important;
            display: flex !important;
            align-items: center !important;
            caret-color: #3D2914 !important;
        }}

        div[data-testid="stChatInput"] textarea::placeholder {{
            color: #8B5A2B !important;
            opacity: 0.6 !important;
        }}

        /* Redesigned Send Button - brown background, white icon */
        div[data-testid="stChatInput"] button,
        div[data-testid="stChatInput"] button[kind="primary"],
        div[data-testid="stChatInput"] button[kind="secondary"],
        div[data-testid="stChatInput"] [data-testid="baseButton-secondary"],
        div[data-testid="stChatInput"] [data-testid="baseButton-primary"] {{
            background: #8B5A2B !important;
            background-color: #8B5A2B !important;
            border-radius: 8px !important;
            width: 36px !important;
            height: 36px !important;
            min-width: 36px !important;
            min-height: 36px !important;
            flex-shrink: 0 !important;
            margin: 0 !important;
            align-self: center !important;
            position: relative !important;
            transition: all 0.2s ease;
            color: white !important;
            border: 0 !important;
            border-width: 0 !important;
            border-style: none !important;
            border-color: transparent !important;
            outline: 0 !important;
            outline-width: 0 !important;
            box-shadow: none !important;
        }}

        div[data-testid="stChatInput"] button:focus,
        div[data-testid="stChatInput"] button:active,
        div[data-testid="stChatInput"] button:focus-visible {{
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            background: #8B5A2B !important;
        }}

        /* Remove any box from all inner elements and wrappers */
        div[data-testid="stChatInput"] button *,
        div[data-testid="stChatInput"] button div,
        div[data-testid="stChatInput"] button span,
        div[data-testid="stChatInput"] button p,
        div[data-testid="stChatInput"] button::before {{
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }}

        /* Target BaseWeb button inner elements */
        div[data-testid="stChatInput"] [data-baseweb] {{
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            background: transparent !important;
        }}

        /* Hide default Streamlit send icon */
        div[data-testid="stChatInput"] button svg {{
            display: none !important;
        }}

        /* Custom paper plane send icon */
        div[data-testid="stChatInput"] button::after {{
            content: '' !important;
            display: block !important;
            width: 18px !important;
            height: 18px !important;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512' fill='white'%3E%3Cpath d='M476.59 227.05l-.16-.07L49.35 49.84A23.56 23.56 0 0027.14 52 24.65 24.65 0 0016 72.59v113.29a24 24 0 0019.52 23.57l232.93 43.07a4 4 0 010 7.86L35.53 303.45A24 24 0 0016 327v113.31A23.57 23.57 0 0026.59 460a23.94 23.94 0 0013.22 4 24.55 24.55 0 009.52-1.93L476.4 285.94l.19-.09a32 32 0 000-58.8z'/%3E%3C/svg%3E") !important;
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            background-color: transparent !important;
        }}

        div[data-testid="stChatInput"] button:hover {{
            background: #6B4423 !important;
            transform: scale(1.05);
        }}

        /* Text colors - dark brown for readability */
        p, h1, h2, h3, h4, h5, h6 {{
            color: #3D2914 !important;
        }}

        /* Scrollbar styling - warm tones */
        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: rgba(139, 90, 43, 0.1);
        }}

        ::-webkit-scrollbar-thumb {{
            background: rgba(139, 90, 43, 0.3);
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(139, 90, 43, 0.5);
        }}

    </style>
    """, unsafe_allow_html=True)