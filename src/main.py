import traceback

import pandas as pd
import streamlit as st
from presidio_anonymizer import OperatorConfig

from engine import analyzer, anonymizer_engine


st.set_page_config(
    page_title="PII detector",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "https://microsoft.github.io/presidio/",
    },
)

st.sidebar.header(
    """
PII Detector with [Microsoft Presidio](https://microsoft.github.io/presidio/)
"""
)

st.sidebar.warning("Note: Models might take some time to download. ")


st_operator = st.sidebar.selectbox(
    "De-identification approach",
    ["redact", "replace", "mask", "hash"],
    index=1,
    help="""
    Select which manipulation to the text is requested after PII has been identified.\n
    - Redact: Completely remove the PII text\n
    - Replace: Replace the PII text with a constant, e.g. <PERSON>\n
    - Synthesize: Replace with fake values (requires an OpenAI key)\n
    - Highlight: Shows the original text with PII highlighted in colors\n
    - Mask: Replaces a requested number of characters with an asterisk (or other mask character)\n
    - Hash: Replaces with the hash of the PII string\n
    - Encrypt: Replaces with an AES encryption of the PII string, allowing the process to be reversed
         """,
)

st_threshold = st.sidebar.slider(
    label="Acceptance threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.35,
    help="Define the threshold for accepting a detection as PII. See more here: ",
)


st_return_decision_process = st.sidebar.checkbox(
    "Add analysis explanations to findings",
    value=False,
    help="Add the decision process to the output table. "
    "More information can be found here: https://microsoft.github.io/presidio/analyzer/decision_process/",
)


analyzer_load_state = st.info("Starting Presidio analyzer...")

analyzer_load_state.empty()

st_entities = ["LOCATION", "ORGANIZATION", "PERSON", "CREDIT_CARD", "EMAIL_ADDRESS", "PHONE_NUMBER", "TCKN", "IBAN"]
st_allowlist = []
st_denylist = []
mask_char = "*"
number_of_chars = 15
operator_config = {
        "type": "mask",
        "masking_char": mask_char,
        "chars_to_mask": number_of_chars,
        "from_end": False,
    }

with open("src/demo_text.txt") as f:
    demo_text = f.readlines()

col1, col2 = st.columns(2)

col1.subheader("Input")
st_text = col1.text_area(
    label="Enter text", value="".join(demo_text), height=400, width=1500, key="text_input"
)


try:

    # Before
    analyzer_load_state = st.info("Starting Presidio analyzer...")
    analyzer_load_state.empty()

    st_analyze_results = analyzer.analyze(
        text=st_text,
        entities=st_entities,
        language="tr",
        score_threshold=st_threshold,
        return_decision_process=st_return_decision_process,
        allow_list=st_allowlist,
    )

    if st_operator not in ("highlight", "synthesize"):
        with col2:
            st.subheader(f"Output")
            st_anonymize_results = anonymizer_engine.anonymize(
                text=st_text,
                analyzer_results=st_analyze_results,
                operators={"DEFAULT": OperatorConfig(st_operator, operator_config)},
            )
            st.text_area(
                label="De-identified", value=st_anonymize_results.text, height=400, width=1500
            )

    st.subheader(
        "Findings"
        if not st_return_decision_process
        else "Findings with decision factors"
    )
    if st_analyze_results:
        df = pd.DataFrame.from_records([r.to_dict() for r in st_analyze_results])
        df["text"] = [st_text[res.start: res.end] for res in st_analyze_results]

        df_subset = df[["entity_type", "text", "start", "end", "score"]].rename(
            {
                "entity_type": "Entity type",
                "text": "Text",
                "start": "Start",
                "end": "End",
                "score": "Confidence",
            },
            axis=1,
        )
        df_subset["Text"] = [st_text[res.start: res.end] for res in st_analyze_results]
        if st_return_decision_process:
            analysis_explanation_df = pd.DataFrame.from_records(
                [r.analysis_explanation.to_dict() for r in st_analyze_results]
            )
            df_subset = pd.concat([df_subset, analysis_explanation_df], axis=1)
        st.dataframe(df_subset.reset_index(drop=True), use_container_width=True)
    else:
        st.text("No findings")

except Exception as e:
    print(e)
    traceback.print_exc()
    st.error(e)
