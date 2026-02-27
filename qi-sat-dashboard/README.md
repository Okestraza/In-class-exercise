# Flask QI Dashboard Prototype

A minimal Quality Improvement (QI) patient satisfaction dashboard built with Flask and Chart.js. Submissions are stored in-memory (no database required).

## Features

- **Rating Form** (`GET /rate`): Submit visit date, nurse courtesy rating, and physician courtesy rating (1–5 scale)
- **Form Validation** (`POST /rate`): Validates inputs and stores submissions in-memory
- **Dashboard** (`GET /dashboard`): Displays line chart with average scores over time using Chart.js
- **Test Suite**: Comprehensive pytest tests using Flask's test client

## Project Structure

```
qi-sat-dashboard/
├── app.py                 # Flask application
├── templates/
│   ├── rate.html          # Rating submission form
│   └── dashboard.html     # Dashboard with Chart.js
├── tests/
│   └── test_app.py        # pytest tests
├── requirements.txt       # Dependencies
└── README.md              # This file
```

## Installation

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the Flask development server:

```bash
python app.py
```

The app will be available at `http://localhost:5000`

### Routes

- **`GET /rate`** - Display the rating form
- **`POST /rate`** - Submit ratings (validates and stores in-memory)
- **`GET /dashboard`** - View the dashboard with average ratings chart

## Running Tests

Run pytest to execute the test suite:

```bash
pytest tests/test_app.py -v
```

### Test Coverage

The test suite includes:
- **Form rendering**: Verify `/rate` returns form with required fields
- **Valid submissions**: Store submissions correctly in-memory
- **Input validation**: Date format, rating range (1–5), required fields
- **Error handling**: Display error messages for invalid inputs
- **Multiple submissions**: Handle multiple entries for same/different dates
- **Dashboard**: Calculate and display average ratings, handle empty data

## Data Model

Submissions are stored as a list of dictionaries in `app.submissions`:

```python
{
    "date": "2026-02-27",        # Visit date (YYYY-MM-DD format)
    "nurse_rating": 5,            # 1–5
    "physician_rating": 4         # 1–5
}
```

## Design Notes

- **In-Memory Storage**: All data is stored in the `submissions` list and will be lost when the server restarts
- **Date Handling**: Visit dates are stored as strings in `YYYY-MM-DD` format
- **Averaging**: Daily averages are calculated on-the-fly when rendering the dashboard
- **Chart.js Library**: Loaded from CDN (https://cdn.jsdelivr.net/npm/chart.js)

## Example Usage

1. Open `http://localhost:5000/rate`
2. Fill out the form:
   - Visit Date: 2026-02-27
   - Nurse Courtesy: 5
   - Physician Courtesy: 4
3. Click "Submit Rating"
4. Click "View Dashboard" to see the chart

## Future Enhancements

- Add database persistence (SQLite, PostgreSQL, etc.)
- Add more detailed analytics and filtering
- Add user authentication
- Implement CSV export of ratings
- Add date range filtering on dashboard
