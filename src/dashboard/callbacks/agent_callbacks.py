import streamlit as st


def _truncate(text, max_len=120):
    """Truncate text for progress display instead of making an LLM call."""
    text = str(text).strip().replace('\n', ' ')
    return text[:max_len] + '…' if len(text) > max_len else text


class AgentProgressCallback:
    def __init__(self, agent, container):
        self.container = container
        self.messages = []
        self.placeholder = container
        self.agent = agent

    def __call__(self, step_output):
        message = ''
        if hasattr(step_output, 'tool'):
            if hasattr(step_output, 'thought') and len(step_output.thought) > 0:
                message += f'\n🔍 {_truncate(step_output.thought)}'
        else:
            message = f'🤔 Thought: {_truncate(step_output)}'
        self.messages.append(message)
        self._update_display()

    def _update_display(self):
        self.placeholder.empty()
        with st.session_state.message_container:
            with self.placeholder:
                st.markdown(
                    f"""
                    <div style="display: flex; margin-left: 28px; color: #3D2914;">
                        {self.messages[-1]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )