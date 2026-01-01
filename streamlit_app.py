import streamlit as st
import requests
import datetime
import streamlit.components.v1 as components

# -----------------------------------
# App Config
# -----------------------------------
st.set_page_config(
    page_title="IntraMind",
    layout="centered",
)

BACKEND_URL = "http://localhost:8000/query"

# -----------------------------------
# Session State Init
# -----------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = ""

if "last_meta" not in st.session_state:
    st.session_state.last_meta = None

def render_meta(meta):
    """Render metadata compactly: progress bar for confidence and an expander for sources."""
    # meta: {'confidence': float (0-1), 'confidence_str': '41.0%', 'sources': [...]}
    conf_val = meta.get("confidence", 0.0)
    try:
        conf_float = float(conf_val)
    except Exception:
        # fallback to parsing confidence_str if available
        conf_str = meta.get("confidence_str", "0%")
        try:
            conf_float = float(conf_str.strip('%')) / 100.0
        except Exception:
            conf_float = 0.0
    # normalize
    if conf_float < 0:
        conf_float = 0.0
    if conf_float > 1.0:
        conf_float = 1.0

    # compact layout
    st.progress(conf_float)
    st.markdown(f"**Confidence:** {meta.get('confidence_str', f'{conf_float*100:.1f}%')}")
    with st.expander("Sources", expanded=False):
        sources = meta.get("sources", [])
        if sources:
            for s in sources:
                st.markdown(f"- {s}")
        else:
            st.markdown("(no sources)")

# -----------------------------------
# Header (rendered via components for reliable styling)
# -----------------------------------
components.html(
    """
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;">
      <div style="font-size:30px; font-weight:700; margin-bottom:6px">IntraMind</div>
      <div style="color:#6c757d; margin-top:-8px">Internal Knowledge Intelligence Platform</div>
    </div>
    """,
    height=70,
)

st.divider()

# -----------------------------------
# Auth (Sidebar)
with st.sidebar:
    st.header("Authentication 🔐")
    st.session_state.jwt_token = st.text_input(
        "JWT Token",
        type="password",
        value=st.session_state.jwt_token,
        placeholder="Paste JWT token here",
    )

    if st.button("Reset Chat"):
        st.session_state.chat_history = []
        st.session_state.last_meta = None
        st.session_state.jwt_token = ""
        st.success("Chat reset.")
        rerun = getattr(st, "experimental_rerun", None)
        if callable(rerun):
            rerun()

    st.markdown("---")
    st.caption("IntraMind • Enterprise RAG • Secure • Grounded • Explainable")

# -----------------------------------
# Chat History Rendering (SINGLE SOURCE)
# -----------------------------------
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        # show timestamp if present
        if msg.get("ts"):
            st.markdown(f"_{msg['ts']}_")
        # If assistant message includes metadata, render compact inline with the message
        if msg.get("role") == "assistant" and isinstance(msg, dict) and msg.get("meta"):
            render_meta(msg["meta"])


# -----------------------------------
# Chat Input
# -----------------------------------
question = st.chat_input("Ask a question about internal documents...")

if question:
    if not st.session_state.jwt_token:
        st.error("Please enter JWT token first.")
    else:
        # 1️⃣ Save user message (with timestamp)
        st.session_state.chat_history.append(
            {"role": "user", "content": question, "ts": datetime.datetime.now().isoformat(timespec='seconds')}
        )

        with st.chat_message("user"):
            st.markdown(question)

        payload = {
            "question": question,
            "chat_history": st.session_state.chat_history[:-1],
        }

        headers = {
            "Authorization": f"Bearer {st.session_state.jwt_token}",
            "Content-Type": "application/json",
        }

        with st.chat_message("assistant"):
            with st.spinner("IntraMind is thinking..."):
                try:
                    response = requests.post(
                        BACKEND_URL,
                        json=payload,
                        headers=headers,
                        timeout=30,
                    )

                    if response.status_code == 200:
                        data = response.json()

                        answer = data.get("answer", "")
                        confidence = data.get("confidence", 0.0)
                        sources = data.get("sources", [])

                        # Format confidence as a percent with one decimal
                        formatted_conf = f"{confidence * 100:.1f}%"

                        # store both numeric and string forms
                        meta = {"confidence": float(confidence), "confidence_str": formatted_conf, "sources": sources}

                        # 2️⃣ Save assistant message with metadata and timestamp
                        assistant_msg = {"role": "assistant", "content": answer, "meta": meta, "ts": datetime.datetime.now().isoformat(timespec='seconds')}
                        st.session_state.chat_history.append(assistant_msg)

                        st.markdown(answer)

                        # show metadata inline immediately using helper
                        render_meta(meta)

                        # 3️⃣ Save metadata separately for backward compatibility
                        st.session_state.last_meta = meta

                    elif response.status_code == 401:
                        st.error("Invalid or expired JWT token.")
                    else:
                        st.error(f"Backend error: {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"Backend not reachable: {e}")

# -----------------------------------
# Footer
# -----------------------------------
st.divider()
st.caption(
    "IntraMind • Enterprise RAG • Secure • Grounded • Explainable"
)
