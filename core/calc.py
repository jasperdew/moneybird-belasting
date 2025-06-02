from typing import Dict
import pandas as pd

def aggregate(frames: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    inv  = frames['invoices']
    exp  = frames['expenses']
    omzet  = inv['total_excl_tax'].sum()
    kosten = exp['total_excl_tax'].sum()
    btw_in  = inv['tax_amount'].sum()
    btw_uit = exp['tax_amount'].sum()
    summary = pd.DataFrame([{
        "Omzet": omzet,
        "Kosten": kosten,
        "BTW te betalen": btw_in - btw_uit,
        "Winst vóór aftrek": omzet - kosten,
    }])
    return {"Omzet": inv, "Kosten": exp, "Samenvatting": summary}
