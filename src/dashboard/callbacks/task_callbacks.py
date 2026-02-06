import streamlit as st

from memory.conversation import ConversationBufferWindow


def _truncate(text, max_len=120):
    """Truncate text for progress display instead of making an LLM call."""
    text = str(text).strip().replace('\n', ' ')
    return text[:max_len] + '…' if len(text) > max_len else text


class TaskProgressCallback:
    def __init__(self, container, memory: ConversationBufferWindow):
        self.container = container
        self.memory = memory
        self.message = None
        self.placeholder = container

    def __call__(self, task_output):
        task_name = task_output.name if task_output.name else ''
        summary = _truncate(task_name + ': ' + task_output.summary)
        self.message = f"✅ {summary}"
        self.memory.add_task_output(task_output)
        self._update_display()

    def _update_display(self):
        self.placeholder.empty()
        with st.session_state.message_container:
            with self.placeholder:
                st.markdown(
                    f"""
                    <div style="display: flex; margin-left: 28px; color: #3D2914;">
                        {self.message}
                    </div>
                    """,
                    unsafe_allow_html=True
                )