# Deepgram Automation

An automated Python script that handles Deepgram account creation, email verification, and API key generation using Selenium and temporary email services.

---

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Output](#output)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

---

## ✨ Features

- 🔐 **Automated Deepgram Signup**: Creates new Deepgram accounts automatically
- 📧 **Temporary Email Integration**: Uses temporary email service (smailpro.com) to bypass email verification
- ✉️ **Email Verification**: Automatically verifies email addresses
- 🔑 **API Key Generation**: Creates and retrieves API keys from Deepgram
- 💾 **CSV Storage**: Stores email and API key pairs in CSV format
- 🚫 **Append Mode**: Adds new credentials without overwriting existing data
- 🤖 **Human-like Behavior**: Simulates human interactions to avoid detection

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12 or higher** ([Download Python](https://www.python.org/downloads/))
- **Chrome Browser** (undetected_chromedriver uses Chrome)
- **pip** (Python package manager, comes with Python)
- **Git** (optional, for version control)

---

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
# Navigate to your desired directory
cd your-project-directory

# If using git
git clone <repository-url>
cd deepgram-automation

# Or extract the downloaded ZIP file
```

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies:

**On Windows (CMD):**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**On Windows (PowerShell):**

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Dependencies Installed:**

- `pandas` - Data manipulation and analysis
- `selenium` - Web browser automation
- `pyperclip` - Clipboard management
- `undetected_chromedriver` - Undetected Chrome automation
- `beautifulsoup4` - HTML/XML parsing
- `lxml` - XML processing
- `selenium_stealth` - Anti-detection for Selenium

---

## 🎯 Usage

### Running the Automation

**Step 1: Activate Virtual Environment (if not already activated)**

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

**Step 2: Run the Script**

```bash
python main.py
```

OR

```bash
python deepgram.py
```

### Example Output

```
🚀 Starting Deepgram Automation...
✅ Email copied: temp.user123@smailpro.com
✅ Deepgram signup page loaded
✅ Email filled
✅ Password filled
✅ reCAPTCHA checkbox clicked!
✅ Create Account button clicked
✅ Switched back to temporary email tab
✅ Opened verification email
✅ Verification URL extracted!
✅ Email verification completed!
✅ API key created successfully!
✅ API key copied: deepgram_abc123xyz456...
✅ API key and email stored in deepgram_api_keys.csv

🎉 Final API Key: deepgram_abc123xyz456...
```

---

## 🔄 How It Works

The automation follows these steps:

1. **Extract Temporary Email**: Generates a temporary email from smailpro.com
2. **Signup Process**:
   - Opens Deepgram signup page
   - Fills in email address
   - Enters password
   - Handles reCAPTCHA detection
   - Clicks Create Account
3. **Email Verification**:
   - Monitors temporary email inbox
   - Extracts verification link
   - Completes email verification
4. **API Key Generation**:
   - Navigates to API keys section
   - Creates new API key
   - Copies the key to clipboard
5. **Data Storage**:
   - Stores email and API key in CSV format
   - Appends to existing file without overwriting

---

## 📊 Output

### CSV File Format

The script creates/updates `deepgram_api_keys.csv`:

```
Email,API Key
temp.user123@smailpro.com,deepgram_abc123xyz456...
temp.user456@smailpro.com,deepgram_def789uvw123...
temp.user789@smailpro.com,deepgram_ghi456xyz789...
```

**Features:**

- ✅ Headers created automatically on first run
- ✅ New credentials appended with each execution
- ✅ No data loss or overwriting
- ✅ Opens in Excel, Google Sheets, or any spreadsheet application

### What to Check for Success

After running the script, verify:

1. **Console Output**: Check for ✅ checkmarks and success messages
2. **CSV File**: Look for `deepgram_api_keys.csv` in the project directory
3. **File Contents**: Open CSV file and verify email and API key are stored
4. **No Errors**: Console should show completion message

---

## 🛠️ Troubleshooting

### Issue: Chrome Browser Not Found

**Solution:**

```bash
# Install undetected_chromedriver with chromium
pip install --upgrade undetected_chromedriver
```

### Issue: Permission Denied Error

**Solution:**

```bash
# On Windows, run as Administrator or try:
python -m pip install --upgrade pip

# On macOS/Linux:
sudo pip install --upgrade pip
```

### Issue: Element Not Found / XPath Errors

**Possible Causes:**

- Deepgram website layout changed
- Network connectivity issues
- Website blocking the automation

**Solution:**

- Update XPath selectors in the code
- Check your internet connection
- Try again later
- Consider using proxy if IP is blocked

### Issue: Virtual Environment Not Activating

**Windows (PowerShell):**

```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
chmod +x .venv/bin/activate
source .venv/bin/activate
```

### Issue: ImportError: No module named 'selenium'

**Solution:**
Make sure virtual environment is activated and reinstall:

```bash
pip install -r requirements.txt --force-reinstall
```

---

## 📁 Project Structure

```
deepgram-automation/
├── deepgram.py                    # Main automation class
├── main.py                        # Entry point script
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project configuration
├── README.md                      # This file
├── deepgram_api_keys.csv         # Output file (auto-created)
└── utils/
    └── clone_human_behavior.py    # Human-like interaction helpers
```

### File Descriptions

| File                            | Purpose                                      |
| ------------------------------- | -------------------------------------------- |
| `deepgram.py`                   | Core automation logic using Selenium         |
| `main.py`                       | Entry point for running the automation       |
| `requirements.txt`              | List of all Python packages needed           |
| `utils/clone_human_behavior.py` | Helper functions for human-like interactions |

---

## 📝 Additional Commands

### Upgrade Packages

```bash
pip install --upgrade -r requirements.txt
```

### Check Installed Packages

```bash
pip list
```

### Export Current Packages

```bash
pip freeze > requirements.txt
```

### Deactivate Virtual Environment

```bash
deactivate
```

---

## ⚠️ Important Notes

- **Rate Limiting**: Running the script multiple times rapidly may trigger rate limits or IP blocking
- **Website Changes**: If Deepgram updates their website, XPath selectors may need updating
- **Temporary Email Service**: smailpro.com may change or block the service
- **API Keys**: Store your API keys securely, never commit `deepgram_api_keys.csv` to public repositories
- **Automation Ethics**: Use this responsibly and in accordance with Deepgram's Terms of Service

---

## 📞 Support

If you encounter issues:

1. Check the **Troubleshooting** section above
2. Review the console output for error messages
3. Verify all dependencies are installed: `pip list`
4. Ensure Chrome browser is up to date
5. Check your internet connection

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🔐 Security Notes

- Never share your `deepgram_api_keys.csv` file
- Add it to `.gitignore` to prevent accidental commits:
  ```
  deepgram_api_keys.csv
  .venv/
  __pycache__/
  *.pyc
  ```

---

**Last Updated**: May 2026  
**Python Version**: 3.12+  
**Status**: Active Development
