from zipfile import ZipFile
import pandas as pd
import io
import re

PATTERNS = {
    "invoices": r"(sales_|verkoop).*\.csv",
    "expenses": r"(purchases_|inkoop).*\.csv",
    "bank": r"bank.*\.csv",
}

def load_moneybird_zip(uploaded_bytes: bytes) -> dict[str, pd.DataFrame]:
    with ZipFile(io.BytesIO(uploaded_bytes)) as z:
        frames = {}
        for info in z.infolist():
            for key, pat in PATTERNS.items():
                if re.match(pat, info.filename, re.I):
                    frames[key] = pd.read_csv(z.open(info))
        return frames
