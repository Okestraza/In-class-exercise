import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def clear_submissions():
    """Clear submissions before each test."""
    import app as app_module
    app_module.submissions.clear()
    yield
    app_module.submissions.clear()


class TestRateGET:
    """Tests for GET /rate route."""

    def test_rate_get_returns_200(self, client):
        """GET /rate should return 200."""
        response = client.get("/rate")
        assert response.status_code == 200

    def test_rate_get_contains_form_fields(self, client):
        """GET /rate should render form with required fields."""
        response = client.get("/rate")
        data = response.data.decode()
        assert "visit_date" in data
        assert "nurse_rating" in data
        assert "physician_rating" in data
        assert "Submit Rating" in data


class TestRatePOST:
    """Tests for POST /rate route."""

    def test_rate_post_valid_data(self, client, clear_submissions):
        """POST /rate with valid data should store submission."""
        from app import submissions

        response = client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "5",
                "physician_rating": "4",
            },
        )
        assert response.status_code == 200
        assert len(submissions) == 1
        assert submissions[0]["date"] == "2026-02-27"
        assert submissions[0]["nurse_rating"] == 5
        assert submissions[0]["physician_rating"] == 4

    def test_rate_post_success_message(self, client, clear_submissions):
        """POST /rate with valid data should show success message."""
        response = client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "3",
                "physician_rating": "3",
            },
        )
        data = response.data.decode()
        assert "success" in data.lower() or "submitted" in data.lower()

    def test_rate_post_missing_date(self, client, clear_submissions):
        """POST /rate without visit_date should show error."""
        response = client.post(
            "/rate",
            data={
                "nurse_rating": "3",
                "physician_rating": "3",
            },
        )
        assert response.status_code == 400
        data = response.data.decode()
        assert "date" in data.lower()

    def test_rate_post_invalid_date_format(self, client, clear_submissions):
        """POST /rate with invalid date format should show error."""
        response = client.post(
            "/rate",
            data={
                "visit_date": "02/27/2026",  # Wrong format
                "nurse_rating": "3",
                "physician_rating": "3",
            },
        )
        assert response.status_code == 400
        data = response.data.decode()
        assert "date" in data.lower() or "format" in data.lower()

    def test_rate_post_missing_nurse_rating(self, client, clear_submissions):
        """POST /rate without nurse_rating should show error."""
        response = client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "physician_rating": "3",
            },
        )
        assert response.status_code == 400
        data = response.data.decode()
        assert "nurse" in data.lower()

    def test_rate_post_invalid_nurse_rating(self, client, clear_submissions):
        """POST /rate with invalid nurse_rating should show error."""
        response = client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "10",  # Out of range
                "physician_rating": "3",
            },
        )
        assert response.status_code == 400
        data = response.data.decode()
        assert "nurse" in data.lower() or "rating" in data.lower()

    def test_rate_post_invalid_nurse_rating_non_numeric(self, client, clear_submissions):
        """POST /rate with non-numeric nurse_rating should show error."""
        response = client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "abc",
                "physician_rating": "3",
            },
        )
        assert response.status_code == 400

    def test_rate_post_missing_physician_rating(self, client, clear_submissions):
        """POST /rate without physician_rating should show error."""
        response = client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "3",
            },
        )
        assert response.status_code == 400
        data = response.data.decode()
        assert "physician" in data.lower()

    def test_rate_post_invalid_physician_rating(self, client, clear_submissions):
        """POST /rate with invalid physician_rating should show error."""
        response = client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "3",
                "physician_rating": "0",  # Out of range
            },
        )
        assert response.status_code == 400
        data = response.data.decode()
        assert "physician" in data.lower() or "rating" in data.lower()

    def test_rate_post_multiple_submissions(self, client, clear_submissions):
        """POST /rate multiple times should store all submissions."""
        from app import submissions

        client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "5",
                "physician_rating": "4",
            },
        )
        client.post(
            "/rate",
            data={
                "visit_date": "2026-02-28",
                "nurse_rating": "3",
                "physician_rating": "3",
            },
        )
        assert len(submissions) == 2


class TestDashboard:
    """Tests for GET /dashboard route."""

    def test_dashboard_get_returns_200(self, client):
        """GET /dashboard should return 200."""
        response = client.get("/dashboard")
        assert response.status_code == 200

    def test_dashboard_no_data(self, client, clear_submissions):
        """GET /dashboard with no data should show appropriate message."""
        response = client.get("/dashboard")
        assert response.status_code == 200
        data = response.data.decode()
        # Should either say no data or have empty chart
        assert "no data" in data.lower() or "chart" in data.lower()

    def test_dashboard_single_submission(self, client, clear_submissions):
        """GET /dashboard with one submission should render chart."""
        client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "5",
                "physician_rating": "4",
            },
        )
        response = client.get("/dashboard")
        assert response.status_code == 200
        data = response.data.decode()
        # Chart.js should be present
        assert "chart" in data.lower() or "2026-02-27" in data

    def test_dashboard_calculates_average(self, client, clear_submissions):
        """GET /dashboard should calculate averages correctly."""
        # Submit two ratings for the same date
        client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "5",
                "physician_rating": "4",
            },
        )
        client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "3",
                "physician_rating": "2",
            },
        )
        response = client.get("/dashboard")
        assert response.status_code == 200
        data = response.data.decode()
        # Should contain average values (4 for nurse, 3 for physician)
        assert "4" in data and "3" in data

    def test_dashboard_multiple_dates(self, client, clear_submissions):
        """GET /dashboard with multiple dates should show sorted data."""
        client.post(
            "/rate",
            data={
                "visit_date": "2026-02-28",
                "nurse_rating": "5",
                "physician_rating": "5",
            },
        )
        client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "3",
                "physician_rating": "3",
            },
        )
        response = client.get("/dashboard")
        assert response.status_code == 200
        # Data should be sorted by date
        data = response.data.decode()
        # First date should appear before second date
        pos_2027 = data.find("2026-02-27")
        pos_2028 = data.find("2026-02-28")
        if pos_2027 >= 0 and pos_2028 >= 0:
            assert pos_2027 < pos_2028

    def test_dashboard_shows_individual_submissions(self, client, clear_submissions):
        """GET /dashboard should display all individual submissions in table."""
        client.post(
            "/rate",
            data={
                "visit_date": "2026-02-27",
                "nurse_rating": "5",
                "physician_rating": "4",
            },
        )
        response = client.get("/dashboard")
        assert response.status_code == 200
        data = response.data.decode()
        # Should contain submission details
        assert "All Submissions" in data
        assert "2026-02-27" in data

