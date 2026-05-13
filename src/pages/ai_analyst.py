import streamlit as st

from src.chatbot.cricket_agent import generate_ai_summary, is_openai_available
from src.chatbot.query_engine import answer_cricket_query
from src.ui.charts import create_bar_chart


SUGGESTED_QUESTIONS = [
    "Top death over batters after 2020",
    "Compare V Kohli and RG Sharma",
    "Best bowlers in powerplay overs",
    "Most consistent IPL batter",
    "Similar players to V Kohli",
    "Highest boundary percentage batters",
]


def show_ai_analyst(matches, deliveries):
    st.header("AI Cricket Analyst")
    st.markdown("---")

    _render_status_bar()

    if "ai_analyst_messages" not in st.session_state:
        st.session_state.ai_analyst_messages = [
            {
                "role": "assistant",
                "content": "Ask me IPL analytics questions. I can compare players, rank phase specialists, explain advanced metrics, and find similar players.",
            }
        ]

    with st.expander("Try These Questions", expanded=True):
        cols = st.columns(3)
        for index, question in enumerate(SUGGESTED_QUESTIONS):
            if cols[index % 3].button(question, key=f"suggested_question_{index}"):
                _handle_user_query(question, matches, deliveries)

    for message in st.session_state.ai_analyst_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            _render_artifacts(message)

    user_query = st.chat_input("Ask a cricket analytics question...")

    if user_query:
        _handle_user_query(user_query, matches, deliveries)
        st.rerun()


def _handle_user_query(user_query, matches, deliveries):
    st.session_state.ai_analyst_messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    result = answer_cricket_query(user_query, matches, deliveries)
    answer = generate_ai_summary(
        user_query,
        result.context_for_llm(),
        result.answer,
    )

    st.session_state.ai_analyst_messages.append(
        {
            "role": "assistant",
            "content": answer,
            "result": result,
        }
    )


def _render_artifacts(message):
    result = message.get("result")

    if result is None:
        return

    if result.data is not None:
        with st.expander("View Data", expanded=False):
            st.write(result.data)

    if result.chart_type == "bar" and result.chart_data is not None:
        fig = create_bar_chart(
            result.chart_data,
            x=result.x,
            y=result.y,
            color=result.color,
            title=result.title or "Cricket Analytics Result",
            x_axis_title=result.x,
            y_axis_title=result.y,
        )
        st.plotly_chart(fig, use_container_width=True)


def _render_status_bar():
    col1, col2, col3 = st.columns(3)

    col1.metric("Mode", "AI + Rules" if is_openai_available() else "Rules Engine")
    col2.metric("Data Scope", "Processed IPL")
    col3.metric("Session Memory", "Enabled")

    if not is_openai_available():
        st.caption(
            "OpenAI summarization is optional. Set OPENAI_API_KEY and install openai to enable LLM-polished responses."
        )
