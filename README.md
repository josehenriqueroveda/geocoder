# 🌍 Geocoder CLI

This project automates the geocoding of addresses in an Excel file using the public API `geocode.maps.co`. The resulting latitude and longitude are saved back into the same file.

## 📦 Requirements

- Python 3.10+
- `.env` file containing the `GEO_API_KEY` environment variable
- Excel file must contain a column named `ADDRESS_CONCAT` with full addresses
- Columns `LAT` and `LONG` will be added if not already present

## 🔧 Installation

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEO_API_KEY=your_api_key_here
```

## 🚀 Usage via Command Line

```bash
python geocoder.py --path path/to/your/file.xlsx --start_index 0
```

## 🔁 Behavior

- Processes up to **4900** rows per run to stay under the daily API limit (5000).
- Sleeps 1.5 seconds between requests to comply with rate limits.
- Updates latitude and longitude directly in the Excel file.

## 📂 Expected Excel Structure

| ADDRESS_CONCAT          | LAT | LONG |
| ----------------------- | --- | ---- |
| 123 Example St, City... |     |      |

Columns `LAT` and `LONG` are auto-filled during execution.

## 🧪 Example Execution

```bash
python geocoder.py --path data/dataset.xlsx --start_index 100
```

---

**License**: MIT  
**Author**: Jose Henrique Roveda
