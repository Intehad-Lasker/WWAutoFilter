# WaterlooWorks Filter Automation

Automatically applies **Targeted Degrees and Disciplines** filters on [WaterlooWorks](https://waterlooworks.uwaterloo.ca) so you don't have to click them manually every time.

> **Important:** Run this on your **local machine** (Windows/Mac/Linux desktop) — not GitHub Codespaces. It needs to open a real browser window for you to log in.

## Setup

> Do this once.

**1. Install Python** (if you don't have it): https://python.org/downloads

**2. Download this repo:**
```bash
git clone https://github.com/Intehad-Lasker/WWAutoFilter.git
cd WWAutoFilter
```

**3. Install dependencies:**
```bash
pip install playwright
python -m playwright install chromium
```

## Usage

```bash
python waterloo_filters.py
```

A browser window will open. Log in to WaterlooWorks (including Duo MFA) — you have 5 minutes. The script will then automatically:
1. Click **All Jobs**
2. Open **Targeted Degrees and Disciplines**
3. Check all your selected filters

Press **Enter** in the terminal when you're done to close the browser.

## Troubleshooting

**`libatk-1.0.so.0: cannot open shared object file`**
You're running in a headless environment (e.g. Codespaces). Run the script locally on your own machine instead.

**Login timed out**
The script waits 5 minutes for login. If Duo MFA takes longer, open `waterloo_filters.py` and increase the `timeout` value in `wait_for_login`.

## Customizing Your Filters

Open `waterloo_filters.py` and find the `FILTERS_TO_CHECK` list near the top.

**Delete any lines you don't want.** For example, to only keep Math and Engineering:

```python
FILTERS_TO_CHECK = [
    "ENG - Software Engineering",
    "ENG - Electrical and Computer Engineering",
    "MATH - Computer Science",
    "MATH - Statistics and Actuarial Science",
]
```

### All available filters

| Category | Options |
|---|---|
| **Themes** | Accounting and Auditing, Agricultural and Food Sciences, Architecture and Design, Business Administration, Computing: Hardware Development, Computing: Information Systems and Data Management, Computing: Software Development, Computing: Systems Support, Construction and Infrastructure Development, Cybersecurity and Cryptography, Data Science / Analytics / Reporting and Optimization, Digital and Graphic Media and Web Site Design, Environmental Management / Climate Change and Sustainability, Finance and Investment, Health Care: Therapy and Patient Care, Health Promotion and Workplace Safety, Human Resources, Insurance and Risk Management, Manufacturing and Process Engineering, Marketing and Communication, Pharmacy and Pharmaceuticals, Project and Process Management, Public Policy / Public Service and Government Relations, Recreation / Event Planning and Hospitality, Sales and Business Development, Scientific Experimental Design and Laboratory Assistance, Sport and Fitness, Supply Chain Management and Logistics, Transportation Planning and Transportation Engineering, Waste / Water and Materials Management |
| **Arts** | All Programs, Economics, English Language and Literature, Fine and Performing Arts, Global Business and Digital Arts, Humanities, Languages and Cultures, Political Science, Social Sciences, Sociology and Legal Studies |
| **Engineering** | Architectural Engineering, Architecture, Biomedical / Nanotechnology and Material Sciences, Chemical Engineering, Civil / Environmental and Geological Engineering, Electrical and Computer Engineering, Management Sciences, Mechanical and Mechatronics Engineering, Software Engineering, Systems Design |
| **Environment** | Business / Enterprise and Development, Environment / Resources and Sustainability, Geography and Environmental Management, Geomatics, Planning |
| **Health** | Kinesiology, Recreation and Leisure Studies, School of Public Health Sciences |
| **Math** | Applied Mathematics, Business, Combinatorics and Optimization, Computer Science, Computing and Financial Management, Pure Mathematics, Statistics and Actuarial Science, Teaching |
| **Science** | Biological Sciences, Business, Chemical Sciences, Earth / Environmental and Geological Sciences, Pharmacy, Physics |
| **Cross-faculty** | ARTS/ENV/MATH/SCI - Chartered Professional Accounting, ARTS/SCI - Psychology |
