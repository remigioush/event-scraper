import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import streamlit as st

st.title("Event Scraper - View Event Details")

url = st.text_input("Paste the event link here:")

if st.button("Scrape Event Information"):
    if url:
        try:
            # Pretend to be a browser
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Smarter Title detection
            title_tag = soup.find('h1')
            title = title_tag.get_text(strip=True) if title_tag else '❌ Title not found'

            # Smarter Date detection
            date_tag = (
                soup.find('div', class_='event-datetime') or
                soup.find('div', class_='event-date') or
                soup.find('div', class_='date') or
                soup.find('div', class_='event-time')
            )
            date = date_tag.get_text(strip=True) if date_tag else '❌ Date not found'

            # Smarter Place detection
            place_tag = (
                soup.find('div', class_='event-location') or
                soup.find('div', class_='event-place') or
                soup.find('div', class_='location') or
                soup.find('div', class_='venue')
            )
            place = place_tag.get_text(strip=True) if place_tag else '❌ Place not found'

            # Smarter Registration link detection
            registration_tag = (
                soup.find('a', class_='event-register-button') or
                soup.find('a', class_='register-button') or
                soup.find('a', class_='registration-link') or
                soup.find('a', class_='signup')
            )
            registration_link = urljoin(url, registration_tag['href']) if registration_tag else None

            # Smarter Participants detection
            participants = []
            speaker_section_titles = ["Speakers", "Panelists", "Keynote Speakers", "Moderators", "Panellists"]

            for section_title in speaker_section_titles:
                # Try to find any section containing the keyword
                section = soup.find(lambda tag: tag.name in ["section", "div"] and section_title.lower() in tag.text.lower())
                if section:
                    names = section.find_all('div', class_='speaker-name')
                    roles = section.find_all('div', class_='speaker-title')
                    for name, role in zip(names, roles):
                        participant_entry = f"{name.get_text(strip=True)} ({role.get_text(strip=True)})"
                        participants.append(participant_entry)
                    break  # Stop after finding first matching section

            if not participants:
                participants = ["❌ No participants found"]

            # Smarter Description detection
            description_tag = (
                soup.find('div', class_='event-description') or
                soup.find('div', class_='description') or
                soup.find('section', class_='event-description')
            )
            description = description_tag.get_text(strip=True) if description_tag else '❌ Description not found'

            # Display the scraped information
            st.subheader("Event Title")
            st.write(title)

            st.subheader("Date")
            st.write(date)

            st.subheader("Place")
            st.write(place)

            st.subheader("Registration Link")
            if registration_link:
                st.markdown(f"[Click here to register]({registration_link})")
            else:
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





