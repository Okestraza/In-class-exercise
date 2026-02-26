# Patient Experience QI Dashboard (Flask + Copilot Agent)

## Overview
In this 1-hour exercise, you will use **GitHub Copilot Agent** to build a lightweight **Quality Improvement (QI) dashboard**. The application allows patients to submit satisfaction ratings and allows clinicians/analysts to view **average patient satisfaction over time**.

This is a **prototype** focused on:
- QI thinking (measure → visualize → improve)
- Human–AI collaboration using an **agentic coding workflow**
- Rapid prototyping with Flask

> ⚠️ **Important scope note**  
> This application uses an **in-memory Python data structure** (no database).  
> This is intentional for teaching speed and clarity. In real-world QI systems, durable storage and concurrency controls are required.

---

## Learning Objectives
By completing this assignment, you will be able to:

1. Use **GitHub Copilot Agent** to:
   - Plan a multi-step software task
   - Implement a Flask application across multiple files
   - Run tests and iteratively fix issues
2. Build a basic **patient experience data collection workflow**
3. Create a simple **QI dashboard** with time-series visualization

---

## Application Requirements

### Functional Requirements
Your Flask application must include:

#### 1. Patient Rating Route
- **GET `/rate`**
  - Displays a form with:
    - Visit date
    - Nurse courtesy rating (1–5)
    - Physician courtesy rating (1–5)

- **POST `/rate`**
  - Validates inputs
  - Stores the submission in an **in-memory data structure**
  - Redirects to the dashboard

#### 2. QI Dashboard Route
- **GET `/dashboard`**
  - Displays a **line chart** of:
    - Average nurse courtesy score over time
    - Average physician courtesy score over time
  - One line per role (nurse vs physician)

#### 3. Data Storage
- Use an **in-memory Python structure** (e.g., a list of dictionaries)
- No SQLite, no files, no external services

#### 4. Testing
- Include **at least one pytest**
- Test must:
  - Submit a rating using Flask’s test client
  - Confirm the dashboard route responds successfully

---

## Expected Project Structure

```
qi-sat-dashboard/
├── app.py
├── store.py
├── requirements.txt
├── templates/
│   ├── rate.html
│   └── dashboard.html
└── tests/
    └── test_app.py
```

---

## Agent‑First Workflow (Required)

This assignment **must be completed using GitHub Copilot Agent**.  
Do **not** jump straight to manual coding.

You are being evaluated on **how you collaborate with the agent**, not just the final app.

---

## Step‑by‑Step Instructions

### Step 1: Planning (Do NOT write code yet)

**Your responsibility**
- Switch Copilot Chat to **Agent mode**
- Provide the prompt below
- Review the plan carefully before proceeding

**Agent responsibility**
- Propose a file structure
- Break the task into logical steps
- Do *not* write implementation code yet

#### Prompt A — Planning
```
Plan a Flask QI dashboard prototype (no database).

Requirements:
- Application contained in folder qi-sat-dashboard
- GET /rate renders a form with:
  - visit date
  - nurse courtesy rating (1–5)
  - physician courtesy rating (1–5)
- POST /rate validates inputs and stores submissions in an in-memory Python structure
- GET /dashboard shows a Chart.js line chart of average scores over time (two lines)
- Include a minimal pytest using Flask test client

Output:
- File tree
- Step-by-step implementation plan
- No code yet
```

---

### Step 2: Implementation

**Your responsibility**
- Review proposed files and logic
- Accept or reject agent changes thoughtfully
- Watch for over-engineering

**Agent responsibility**
- Create files
- Implement routes, templates, and store logic
- Follow the approved plan

#### Prompt B — Implementation
Now is your chance to make sure that Agent understood your assignment and that you agree with the plan of action. Review what Agent generated, and if you agree, you can simply respond with: `implement the plan.`

If anything doesn't match your expectations, here is where you provide feedback. Below is a very strict prompt that you can use if Agent's original plan doesn't match your expectations.
```
Implement the plan.

Create:
- app.py (Flask routes)
- store.py (in-memory list or dict + aggregation helpers)
- templates/rate.html
- templates/dashboard.html
- tests/test_app.py
- requirements.txt

Constraints:
- Use an in-memory Python data structure only
- Use Chart.js via CDN
- Pass Python lists to JavaScript using Jinja's tojson filter
- Validate that ratings are integers 1–5 and visit date is required
```

---
### Step 3: Testing and Iteration
Your Agent may have already written the pytest modules and attempted to run the tests. If not, you will need to explicitly instruct the Agent to do so. If pytest has not already been run, a prompt to run tests is included below in prompt C.

**Your responsibility**
- Ensure tests reflect real user behavior
- Confirm failures are fixed correctly (not just silenced)

**Agent responsibility**
- Write pytest(s)
- Run tests
- Fix failures iteratively

#### Prompt C — Testing
```
Write and run pytest.

Tests should:
1. POST a valid rating to /rate using Flask test client
2. Confirm GET /dashboard returns HTTP 200
3. Optionally verify that aggregated data contains the submitted date

Run pytest and fix any failures until all tests pass.
Summarize what you changed to make tests pass.
```

✅ **Checkpoint:** Tests must pass.

---

### Step 4: Visualization
At this point, Agent should have created a working application and will have tested its functionality using pytest. Now you will need to run it to see if it meets your expectations. To run the app, you'll need to run the following in the `TERMINAL`:
```bash
cd qi-sat-dashboard
python app.py
```

Now open the app in your browser and visit the /rate route to enter some patient satisfaction scores, then visit /dashboard to view the dashboard.

**Your responsibility**
- Ensure the chart matches the QI question
- Confirm nurse and physician lines are clearly labeled

**Agent responsibility**
- Aggregate daily averages
- Pass labels and data arrays to the template
- Render a Chart.js line chart

> Hint: The dashboard should answer  
> **“Are courtesy scores changing over time?”**

---


## Evaluation Criteria

| Area | What We’re Looking For |
|-----|------------------------|
| Agent usage | Clear plan-first workflow |
| QI thinking | Sensible aggregation & visualization |
| Code quality | Simple, readable, appropriate for prototype |
| Testing | Realistic test using Flask test client |
| Reflection | Insight into human–AI collaboration |

---

## Real‑World QI Discussion (After the Lab)

Be prepared to discuss:
- Why in‑memory storage is unsafe in production
- How this dashboard would change with:
  - Persistent storage
  - Multiple users
  - Formal QI methodologies (run charts, control limits)
- How agentic tools could accelerate QI prototyping in practice

---

## Academic Integrity & AI Use
- You **are expected** to use GitHub Copilot Agent
- You are **responsible** for reviewing and understanding all code
- Treat the agent as a **junior collaborator**, not an oracle

---

**End of assignment.**
