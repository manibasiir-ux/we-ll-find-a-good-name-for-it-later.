<<<<<<< Updated upstream
#starting
<<<<<<< Updated upstream
=======
print('this is a start')
print('we are testing')
>>>>>>> Stashed changes
'now another change''now another changeeee'
'i want to add something myself'
'another one'
'another another one'
=======
# we-ll-find-a-good-name-for-it-later.
we wi'll find a good description for it later

"""
Created on Wed Feb 11 14:10:34 2026

@author: Mani Basir

"""

#Scraping first source

import requests
from bs4 import BeautifulSoup

url = 'https://ing.com/investors/investor-relations-contacts'

web = requests.get(url)

soup = BeautifulSoup(web.text,'html')

target_information = soup.find('div',{'class':'max-container content','id':'readspeaker'})

if target_information:
    text = target_information.get_text(strip = True)
    print(text)

import re
import pandas as pd

raw_text = """
Sjoerd Miltenburg
Head of Investor Relations
sjoerd.miltenburg@ing.com
Tel:+31 20 576 6959

Angelique van der Schild
Personal assistant to Sjoerd Miltenburg
angelique.van.der.schild@ing.com
Tel:+31 20 576 2883

Bob Bakker
Investor Relations officer
bob.bakker@ing.com
Tel:+31 20 576 6295

Paul van Slobbe
Investor Relations officer
paul.van.slobbe@ing.com
Tel:+31 20 563 6371

Rian Koole
Investor Relations officer
rian.koole@ing.com
Tel:+31 20 652 3310

Laila Benomar
Investor Relations officer
laila.benomar@ing.com
Tel:+31 20 576 6253

Panos Ellinas
Investor Relations officer
panos.ellinas@ing.com
Tel:+31 20 560 4955

Amy Chen
Investor Relations officer
amy.chen@ing.com
Tel:+31 20 576 6249
"""

# Define regex patterns
email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
phone_pattern = re.compile(r"\+\d[\d\s]{6,}")
name_pattern = re.compile(r"^[A-Z][a-zA-Zëéèêäöüàç'’\-]+(?:\s[A-Z][a-zA-Zëéèêäöüàç'’\-]+)+$")

# Split the raw text into lines
lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

records = []

for i in range(0, len(lines), 4):
    name = lines[i]
    # The next lines are occupation and email, followed by phone
    email_match = email_pattern.search(lines[i+2])
    phone_match = phone_pattern.search(lines[i+3])
    
    email = email_match.group() if email_match else ''
    phone = phone_match.group() if phone_match else ''
    
    records.append([name, email, phone])

# Create DataFrame
df = pd.DataFrame(records, columns=["Name", "Email", "Phone"])

# Save to CSV
df.to_csv("first_source_lead.csv", index=False, encoding="utf-8-sig")

print(df)
print("\nSaved to first_source_lead.csv")

>>>>>>> Stashed changes

# sunday's updates: 

import pandas as pd
from playwright.async_api import async_playwright
import asyncio

# Load the CSV file with profile URLs
input_csv = "C:/Users/admin/Downloads/Netherland's_Engineer_Leads.csv"
output_csv = "Scraped_Contacts.csv"

# Read the list of profile URLs
df_profiles = pd.read_csv(input_csv)
profile_urls = df_profiles['profileUrl'].dropna().tolist()

async def scrape_contacts(profile_urls):
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        for url in profile_urls:
            print(f"Visiting: {url}")
            try:
                await page.goto(url)
                await page.wait_for_load_state('networkidle', timeout=10000)

                # Initialize variables
                email = None
                name = None

                # Extract email if visible on profile
                email_element = await page.query_selector("a[href^='mailto:']")
                if email_element:
                    email = await email_element.get_attribute("href")
                    email = email.replace("mailto:", "")

                # Extract name if available
                # Adjust the selector based on LinkedIn profile structure
                name_element = await page.query_selector("li.inline.t-24.t-black.t-normal.break-words")
                if name_element:
                    name = await name_element.inner_text()

                data.append({
                    "Profile URL": url,
                    "Name": name,
                    "Email": email
                })

            except Exception as e:
                print(f"Failed to process {url}: {e}")
                data.append({
                    "Profile URL": url,
                    "Name": None,
                    "Email": None
                })

        await browser.close()

    return pd.DataFrame(data)
