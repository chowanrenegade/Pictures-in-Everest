# Part Number Comparator (Picture Status)

This utility streamlines the process of auditing inventory media. It compares a **"Needs Price"** master list against an **"Everest"** data export to identify which items are currently flagged as having images.

---

## 🚀 Features

* **Dual-Column Logic:** Scans both `PICTURE` and `NEW PICTURE` columns in the Everest export for a 'T' (True) flag.
* **Smart Filtering:** Uses `pandas` to handle mixed data types (numbers/text) and case sensitivity automatically.
* **Instant Extraction:** Only exports the rows from your "Needs Price" list that satisfy the picture requirements.
