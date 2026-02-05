import streamlit as st
import json

st.set_page_config(
    page_title="JSON Formatter",
    layout="wide",
    page_icon="🧩"
)

st.title("🧩 JSON Formatter & Validator")

# ---------- SESSION STATE ----------
if "action" not in st.session_state:
    st.session_state.action = None

if "output" not in st.session_state:
    st.session_state.output = ""

if "output_type" not in st.session_state:
    st.session_state.output_type = "code"  # code | success | error


# ⬇️ Screen width ratio: Input = 1, Output = 3
col1, col2 = st.columns([1, 3])

# ---------------- LEFT COLUMN ----------------
with col1:
    input_json = st.text_area(
        "Paste your JSON here",
        height=400,
        placeholder='{\n  "name": "Mayur",\n  "role": "Developer"\n}'
    )

# ---------------- RIGHT COLUMN ----------------
with col2:
    with st.form("json_form"):
        b1, b2, b3 = st.columns(3)

        with b1:
            format_clicked = st.form_submit_button("✨ Format JSON", use_container_width=True)
        with b2:
            minify_clicked = st.form_submit_button("📦 Minify JSON", use_container_width=True)
        with b3:
            validate_clicked = st.form_submit_button("✅ Validate JSON", use_container_width=True)

        if format_clicked:
            st.session_state.action = "format"
        elif minify_clicked:
            st.session_state.action = "minify"
        elif validate_clicked:
            st.session_state.action = "validate"

    st.subheader("Output")
    output_box = st.empty()
    
    # ✅ SCROLLABLE OUTPUT CONTAINER
    with st.container(height=420):
        if st.session_state.output:
            if st.session_state.output_type == "code":
                st.code(st.session_state.output, language="json")
            elif st.session_state.output_type == "success":
                st.success(st.session_state.output)
            elif st.session_state.output_type == "error":
                st.error(st.session_state.output)

    


# ---------------- PROCESS LOGIC ----------------
if st.session_state.action and input_json.strip():
    try:
        parsed = json.loads(input_json)

        if st.session_state.action == "format":
            st.session_state.output = json.dumps(parsed, indent=4, ensure_ascii=False)
            st.session_state.output_type = "code"

        elif st.session_state.action == "minify":
            st.session_state.output = json.dumps(parsed, separators=(",", ":"))
            st.session_state.output_type = "code"

        elif st.session_state.action == "validate":
            st.session_state.output = "✅ JSON is valid"
            st.session_state.output_type = "success"

    except json.JSONDecodeError as e:
        st.session_state.output = f"❌ Invalid JSON: {str(e)}"
        st.session_state.output_type = "error"


# ---------------- RENDER OUTPUT ----------------
if st.session_state.output:
    if st.session_state.output_type == "code":
        output_box.code(st.session_state.output, language="json")
    elif st.session_state.output_type == "success":
        output_box.success(st.session_state.output)
    elif st.session_state.output_type == "error":
        output_box.error(st.session_state.output)


# ---------------- DOWNLOAD ----------------
if st.session_state.output_type == "code":
    st.download_button(
        "⬇️ Download JSON",
        st.session_state.output,
        file_name="formatted.json",
        mime="application/json"
    )
