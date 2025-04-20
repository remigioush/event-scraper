import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import streamlit as st

st.title("Event Scraper - View Event Details")

url = st.text_input("Paste the event link here:")

if st.button("Scrape Event Information"):
    if url:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # check if the page loads correctly
            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to find all fields safely
            title_tag = soup.find('h1', class_='event-title')
            title = title_tag.get_text(strip=True) if title_tag else '❌ Title not found'

            date_tag = soup.find('div', class_='event-datetime')
            date = date_tag.get_text(strip=True) if date_tag else '❌ Date not found'

            place_tag = soup.find('div', class_='event-location')
            place = place_tag.get_text(strip=True) if place_tag else '❌ Place not found'

            registration_tag = soup.find('a', class_='event-register-button')
            registration_link = urljoin(url, registration_tag['href']) if registration_tag else None

            description_tag = soup.find('div', class_='event-description')
            description = description_tag.get_text(strip=True) if description_tag else '❌ Description not found'

            participants = []
            speakers_section = soup.find('section', class_='event-speakers')
            if speakers_section:
                speaker_names = speakers_section.find_all('div', class_='speaker-name')
                speaker_titles = speakers_section.find_all('div', class_='speaker-title')
                for name, role in zip(speaker_names, speaker_titles):
                    participant_entry = f"{name.get_text(strip=True)} ({role.get_text(strip=True)})"
                    participants.append(participant_entry)
            else:
                participants = ["❌ No participants found"]

            # Display the information clearly
            st.subheader("Event Title")
            st.write(title)

            st.subheader("Date")
            st.write(date)

            st.subheader("Place")
            st.write(place)

            if registration_link:
                st.subheader("Registration Link")
                st.markdown(f"[Click here to register]({registration_link})")
            else:
                st.subheader("Registration Link")
                st.write("❌ Registration link not found")

            st.subheader("Participants")
            for participant in participants:
                st.write(f"- {participant}")

            st.subheader("Description")
            st.write(description)

        except Exception as e:
            st.error(f"An error occurred: {e}")

    else:
        st.warning("Please enter a URL.")

