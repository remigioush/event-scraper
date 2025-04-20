import streamlit as st
from playwright.sync_api import sync_playwright

st.title("Event Scraper with Playwright (Real Browser Loading)")

url = st.text_input("Paste the event link here:")

def scrape_event_info(event_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch browser invisible
        page = browser.new_page()
        page.goto(event_url)
        page.wait_for_timeout(5000)  # Wait for 5 seconds to let JavaScript fully load

        # Extract content
        title = page.locator('h1.event-title').inner_text(timeout=5000) if page.locator('h1.event-title').count() > 0 else '❌ Title not found'
        date = page.locator('div.event-datetime').inner_text(timeout=5000) if page.locator('div.event-datetime').count() > 0 else '❌ Date not found'
        place = page.locator('div.event-location').inner_text(timeout=5000) if page.locator('div.event-location').count() > 0 else '❌ Location not found'
        description = page.locator('div.event-description').inner_text(timeout=5000) if page.locator('div.event-description').count() > 0 else ''
        registration_link = page.locator('a.event-register-button').get_attribute('href') if page.locator('a.event-register-button').count() > 0 else None

        browser.close()

        return title, date, place, description, registration_link

if st.button("Scrape Event Information"):
    if url:
        try:
            title, date, place, description, registration_link = scrape_event_info(url)

            st.subheader("Event Title")
            st.write(title)

            st.subheader("Date")
            st.write(date)

            st.subheader("Location")
            st.write(place)

            st.subheader("Description")
            st.write(description)

            st.subheader("Registration Link")
            if registration_link:
                st.markdown(f"[Click here to register]({registration_link})")
            else:
                st.write("❌ Registration link not found")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a URL.")





