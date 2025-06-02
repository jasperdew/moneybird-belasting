import streamlit as st
from core.loader import load_moneybird_zip
from core.calc import aggregate
from core.ocr import extract_fields
import pandas as pd, io

st.title("ZZP-Belastingoverzicht uit Moneybird + privé-aftrek")

zip_file = st.file_uploader("Moneybird ZIP-export", type="zip")
if zip_file:
    data = load_moneybird_zip(zip_file.read())
    dfs = aggregate(data)
    st.subheader("Samenvatting")
    st.dataframe(dfs["Samenvatting"])

    st.subheader("Handmatige correcties")
    corr = st.experimental_data_editor(pd.DataFrame(columns=["omschrijving","type","bedrag","btw"]))
    # verwerk corr …

    st.subheader("Upload privé-aftrekposten")
    extra_docs = st.file_uploader("Documenten (PDF/JPG/PNG)", accept_multiple_files=True,
                                  type=["pdf","jpg","jpeg","png"])
    aftrek = []
    for doc in extra_docs:
        aftrek.append(extract_fields(doc.read()))
    aftrek_df = pd.DataFrame(aftrek)
    st.dataframe(aftrek_df)

    if st.button("Genereer Excel"):
        # combine & write
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as xls:
            for name, df in {**dfs, "Privé aftrekposten": aftrek_df, "Correcties": corr}.items():
                df.to_excel(xls, sheet_name=name[:31], index=False)
        st.download_button("Download Excel", buffer.getvalue(), "zzp_belasting.xlsx")
