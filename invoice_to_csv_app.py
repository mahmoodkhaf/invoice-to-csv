import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="Invoice to CSV", layout="centered")

st.title("📄 Invoice PDF to CSV Converter")

uploaded_file = st.file_uploader("Upload your PDF invoice", type="pdf")

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    
    st.subheader("🔍 Extracted Text Preview")
    st.text(text[:1000])  # Show a preview

    # Naive line parsing (depends on your invoice style)
    lines = text.split('\n')
    data = []
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            possible_amount = parts[-1].replace('$', '').replace(',', '')
            if possible_amount.replace('.', '', 1).isdigit():
                item = ' '.join(parts[:-2])
                date = parts[-2]
                amount = parts[-1]
                data.append([date, item, amount])

    if data:
        df = pd.DataFrame(data, columns=["Date", "Description", "Amount"])
        st.success("✅ Data extracted successfully!")

        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            "invoice_data.csv",
            "text/csv"
        )
    else:
        st.warning("Couldn’t extract structured data. Try another invoice or format.")
