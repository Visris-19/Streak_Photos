# Streak_Photos

A Python application for maintaining your GitHub streak by automating photo uploads.

## Overview
This tool helps maintain GitHub activity by automating periodic commits of photo changes using the Google Photos API. Perfect for keeping your GitHub contribution graph active.

## Features
- Automated photo uploads
- GitHub streak maintenance
- Google Photos API integration
- Scheduled commits

## Setup Requirements
- Python 3.8+
- Google Cloud Platform account
- Google Photos API credentials
- GitHub account

## Project Structure
```
Streak_Photos/
│
├── src/
│   ├── __init__.py
│   ├── photo_handler.py
│   └── github_handler.py
│
├── config/
│   └── settings.py
│
├── tests/
│   └── __init__.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository
```bash
git clone https://github.com/Visris-19/Streak_Photos.git
cd Streak_Photos
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Configuration
1. Set up Google Cloud Project
2. Enable Google Photos API
3. Download credentials to `client_secrets.json`
4. Configure GitHub authentication

## Usage
```bash
python src/main.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Author
Vishal Pandey - [@Visris-19](https://github.com/Visris-19)