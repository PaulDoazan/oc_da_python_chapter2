# OC DA Python Chapter 2

## Scraping Data with Python on books.toscrape.com

In order to get books data in CSV format, follow these steps:

### 1. Install a Virtual Environment

```bash
python -m venv env
```

### 2. Activate the Virtual Environment

**Windows:**

```bash
env\Scripts\activate
```

**Mac/Linux:**

```bash
source env/bin/activate
```

### 3. Execute the Script

```bash
python main.py
```

Once completed, you will find the CSV file in the `result` directory.

As a suggestion made by my mentor, the scraping is implemented on a multithread requests process. It aims at reducing
the total time of process by executing several requests at same time, though results are exactly the same.
Monitoring time gives the following results :

- main.py : 1067.98 seconds
- multithread.py : 123.89 seconds