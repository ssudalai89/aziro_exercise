
# Aziro Exercise: Automated UI Test Suite

## Overview

This repository contains an automated UI test suite for validating the functionality of a web application as part of the Aziro recruitment process. The tests are implemented using Python, Selenium WebDriver, and pytest, following the Page Object Model (POM) design pattern for maintainability and scalability.

## Project Structure

```
aziro_exercise/
├── conftest.py                # Pytest fixtures and browser setup
├── requirements.txt           # Python dependencies
├── pages/
│   ├── base_page.py           # Base page object (common logic)
│   └── home_page.py           # Home page object (table & dropdown logic)
├── tests/
│   └── test_step_table_column_validation.py  # Main test suite
└── README.md                  # Project documentation
```

## Test Development Summary
- **Page Object Model:** Implemented `HomePage` class to encapsulate UI logic for table and dropdown validation.
- **Robust Error Handling:** All page and test methods use try-except blocks and logging for clear diagnostics.
- **Test Coverage:**
  - Table column validation
  - Non-empty column headers
  - Traffic rank extraction for specific entries
  - Dropdown expansion and data presence
  - Detailed company information validation in expanded dropdowns
- **Logging:** All actions and errors are logged for easy debugging and traceability.

## How to Run the Tests

1. **Install Python (>=3.8 recommended)**
2. **Create and activate a virtual environment (optional but recommended):**
	```powershell
	python -m venv venv
	.\venv\Scripts\activate
	```
3. **Install dependencies:**
	```powershell
	pip install -r requirements.txt
	```
4. **Run the test suite:**
	```powershell
	pytest -v -s tests/test_step_table_column_validation.py
	```

## Key Test Scenarios

- **Table Column Validation:** Ensures the home page table columns match expected values.
- **Header Non-Empty Check:** Asserts that no column header is empty.
- **Traffic Rank Validation:** Extracts and verifies the traffic rank for a specific website entry.
- **Dropdown Data Validation:** Scrolls to the bottom, expands each dropdown, and checks that revealed rows contain non-empty data.
- **Company Details Validation:** After expanding dropdowns, checks for the presence and correctness of company details (e.g., Company Name, Location, Telephones, Contacts) in the expanded content, even if structured as multi-line text.

## Technologies Used

- Python
- Selenium WebDriver
- pytest
- webdriver-manager
- beautifulsoup4 (for robust HTML parsing)

## Logging & Error Handling

- All actions, assertions, and errors are logged using Python's `logging` module.
- Try-except blocks ensure that failures are reported with clear error messages.

## Customization

- You can adjust expected column names, company detail fields, and other parameters in `pages/home_page.py` as needed for your application.

## Troubleshooting

- If tests fail due to browser issues, ensure Chrome is installed and up-to-date.
- If dependencies are missing, re-run `pip install -r requirements.txt`.
- Review log output for detailed error diagnostics.

## Contact

For any questions or issues, please contact the repository owner or submit an issue.
