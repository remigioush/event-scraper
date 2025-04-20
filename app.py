import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import streamlit as st

st.title("Event Scraper - View Event Details")

url = st.text_input("Paste the event link here:")

if st.button("Scrape Event Information"):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape Event Details
        title_tag = soup.find('h1', class_='event-title')
        title = title_tag.get_text(strip=True) if title_tag else 'N/A'

        date_tag = soup.find('div', class_='event-datetime')
        date = date_tag.get_text(strip=True) if date_tag else 'N/A'

        place_tag = soup.find('div', class_='event-location')
        place = place_tag.get_text(strip=True) if place_tag else 'N/A'

        registration_tag = soup.find('a', class_='event-register-button')
        registration_link = urljoin(url, registration_tag['href']) if registration_tag else 'N/A'

        description_tag = soup.find('div', class_='event-description')
        description = description_tag.get_text(strip=True) if description_tag else 'N/A'

        # Scrape Participants
        participants = []
        speakers_section = soup.find('section', class_='event-speakers')
        if speakers_section:
            speaker_names = speakers_section.find_all('div', class_='speaker-name')
