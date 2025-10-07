# 🗺️ Google Maps B2B Leads Scraper & Cleaner

A complete Python toolkit to **scrape verified business leads from Google Maps** and then **clean and normalize** the data for professional use.  
Built using `Selenium`, `BeautifulSoup`, and `Pandas`.

---

## 🚀 Features

### 🕵️ Scraper (`main.py`)
- Scrapes **business names, ratings, reviews, addresses, phones, and websites**
- Works for **multiple cities and categories**
- Automatically exports clean CSV files
- Lightweight and optimized for performance

### 🧹 Cleaner (`clean_data.py`)
- Extracts **ZIP codes** from addresses using regex
- Cleans and normalizes website URLs (removes tracking)
- Reorders CSV columns for better readability
- Saves the cleaned dataset in a new file

## 🧠 Requirements

- Python **3.8+**
- Google Chrome browser
- ChromeDriver (same version as Chrome)
- Internet connection

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/google-maps-b2b-leads-scraper.git
cd google-maps-b2b-leads-scraper
```

# 2. Install dependencies
pip install -r requirements.txt

## ▶️ Usage Guide
### 1️⃣ Run the Scraper
```bash
scraper.py
```

### You’ll be asked for:

-City names (comma separated)

-Category (e.g., restaurants, schools, gyms)

-Number of leads per city

### Example:Enter place(s):
-Dhaka, Chittagong
-Enter category: restaurants
-Enter number of leads per city: 30

### This will create an output file like:
```
restaurants_Dhaka_Chittagong_leads.csv
```

### 2️⃣ Clean the Scraped Data
Once your CSV is generated, clean it for better formatting:
```bash
cleaning.py
```

### ✅ This script will:

-Extract ZIP codes from the Address column

-Clean and standardize Website URLs

-Reorder columns: Name | Address | Zip Code | Website

Save results as:
```
cleaned_restaurants_output.csv
```

| Name            | Address                      | Zip Code | Phone          | Website                                          |
| --------------- | ---------------------------- | -------- | -------------- | ------------------------------------------------ |
| Pizza Hut       | Gulshan 2, Dhaka, Bangladesh | 1212     | +880 123456789 | [https://pizzahutbd.com](https://pizzahutbd.com) |
| The Coffee Bean | Dhanmondi 27, Dhaka          | 1209     | +880 987654321 | [https://coffeebean.com](https://coffeebean.com) |


## 🧩 Technologies Used
Python 3

-Selenium → Automate browser navigation

-BeautifulSoup4 → Parse HTML

-Pandas → Clean and export structured data

-Regex → Extract ZIP codes

## 📄 License

MIT License © 2025 [Your Name]

You’re free to use, modify, and share this project with attribution.

## 🌟 Contribution

Pull requests are welcome!

### If you find a bug or have feature ideas:

-Fork the repo

-Create a new branch (feature/my-feature)

-Submit a pull request 🚀

## Author
### Sabit AL Fahad

-🛠️ Freelancer | Web Scraper | Data Automation Expert

-📧 sabitalfahad.info@gmail.com




