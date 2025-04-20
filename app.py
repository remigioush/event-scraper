import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import streamlit as st
import re

st.title("Event Scraper - Extract Full Event Info")

url = st.text_input("Paste the event link here:")

if st.button("Scrape Event Information"):
    if url:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract Title
            title_tag = soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else '❌ Title not found'

            # Extract Registration Link
            registration_tag = soup.find('a', class_='event-register-button')
            registration_link = urljoin(url, registration_tag['href']) if registration_tag else None

            # Extract Description
            description_tag = soup.find('div', class_='event-description')
            description_text = description_tag.get_text(separator="\n", strip=True) if description_tag else ''

            # Initialize extracted fields
            date_info = "❌ Date not found"
            location_info = "❌ Location not found"
            panellists_list = []

            # Use regex to find Date, Location, Panellists
            if description_text:
                # Find Date
                date_match = re.search(r'Date[:\\-]?\\s*(.*)', description_text, re.IGNORECASE)
                if date_match:
                    date_info = date_match.group(1).strip()

                # Find Location
                location_match = re.search(r'Location[:\\-]?\\s*(.*)', description_text, re.IGNORECASE)
                if location_match:
                    location_info = location_match.group(1).strip()

                # Find Panellists
                panellists_section = re.split(r'Panellists[:\\-]', description_text, flags=re.IGNORECASE)
                if len(panellists_section) > 1:
                    panellists_text = panellists_section[1]
                    panellists_lines = panellists_text.strip().split('\n')
                    for line in panellists_lines:
                        line = line.strip()
                        if line:
                            panellists_list.append(line)

            # Display extracted info
            st.subheader("Title")
            st.write(title)

            st.subheader("Date")
            st.write(date_info)

            st.subheader("Location")
            st.write(location_info)

            st.subheader("Panellists")
            if panellists_list:
                for panellist in panellists_list:
                    st.write(f"- {panellist}")
            else:
                st.write("❌ No panellists found")

            st.subheader("Registration Link")
            if registration_link:
                st.markdown(f"[Click here to register]({registration_link})")
            else:
                st.write("❌ Registration link not found")

        except Exception as e:
            st.error(f"An error occurred: {e}")

    else:
        st.warning("Please enter a URL.")





