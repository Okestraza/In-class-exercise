from flask import Flask, render_template, request, jsonify
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# In-memory storage for submissions
# Each entry: {"date": "YYYY-MM-DD", "nurse_rating": int, "physician_rating": int}
submissions = []


def validate_rating(value):
    """Validate that a rating is an integer between 1 and 5."""
    try:
        rating = int(value)
        if 1 <= rating <= 5:
            return True, rating
        return False, None
    except (ValueError, TypeError):
        return False, None


def validate_date(date_string):
    """Validate that a date string is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


@app.route("/rate", methods=["GET"])
def rate_get():
    """Display the rating form."""
    return render_template("rate.html")


@app.route("/rate", methods=["POST"])
def rate_post():
    """Handle form submission and validation."""
    visit_date = request.form.get("visit_date", "").strip()
    nurse_rating = request.form.get("nurse_rating", "").strip()
    physician_rating = request.form.get("physician_rating", "").strip()
    
    errors = []
    
    # Validate date
    if not visit_date:
        errors.append("Visit date is required.")
    elif not validate_date(visit_date):
        errors.append("Visit date must be in YYYY-MM-DD format.")
    
    # Validate nurse rating
    if not nurse_rating:
        errors.append("Nurse courtesy rating is required.")
    else:
        valid, rating = validate_rating(nurse_rating)
        if not valid:
            errors.append("Nurse courtesy rating must be a number between 1 and 5.")
        else:
            nurse_rating = rating
    
    # Validate physician rating
    if not physician_rating:
        errors.append("Physician courtesy rating is required.")
    else:
        valid, rating = validate_rating(physician_rating)
        if not valid:
            errors.append("Physician courtesy rating must be a number between 1 and 5.")
        else:
            physician_rating = rating
    
    if errors:
        # Re-display form with errors
        return render_template(
            "rate.html",
            errors=errors,
            visit_date=request.form.get("visit_date", ""),
            nurse_rating=request.form.get("nurse_rating", ""),
            physician_rating=request.form.get("physician_rating", ""),
        ), 400
    
    # Store submission
    submissions.append({
        "date": visit_date,
        "nurse_rating": nurse_rating,
        "physician_rating": physician_rating,
    })
    
    return render_template("rate.html", success=True)


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """Display dashboard with Chart.js line chart."""
    # Compute daily averages
    daily_data = defaultdict(lambda: {"nurse_ratings": [], "physician_ratings": []})
    
    for submission in submissions:
        date = submission["date"]
        daily_data[date]["nurse_ratings"].append(submission["nurse_rating"])
        daily_data[date]["physician_ratings"].append(submission["physician_rating"])
    
    # Calculate averages and sort by date
    chart_data = {}
    for date in sorted(daily_data.keys()):
        nurse_avg = sum(daily_data[date]["nurse_ratings"]) / len(daily_data[date]["nurse_ratings"])
        physician_avg = sum(daily_data[date]["physician_ratings"]) / len(daily_data[date]["physician_ratings"])
        chart_data[date] = {
            "nurse_avg": round(nurse_avg, 2),
            "physician_avg": round(physician_avg, 2),
        }
    
    dates = sorted(chart_data.keys())
    nurse_averages = [chart_data[date]["nurse_avg"] for date in dates]
    physician_averages = [chart_data[date]["physician_avg"] for date in dates]
    
    # Sort submissions by date (descending, most recent first)
    sorted_submissions = sorted(submissions, key=lambda x: x["date"], reverse=True)
    
    return render_template(
        "dashboard.html",
        dates=dates,
        nurse_averages=nurse_averages,
        physician_averages=physician_averages,
        all_submissions=sorted_submissions,
    )


if __name__ == "__main__":
    app.run(debug=True)
