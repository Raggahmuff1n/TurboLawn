import streamlit as st

st.title("TurboLawn")
st.write("Welcome to TurboLawn - Your lawn management solution")

# Add your main functionality here
def main():
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "Services", "Schedule", "Contact"])
    
    if page == "Home":
        home_page()
    elif page == "Services":
        services_page()
    elif page == "Schedule":
        schedule_page()
    elif page == "Contact":
        contact_page()

def home_page():
    st.header("Home")
    st.write("TurboLawn helps you manage your lawn care needs efficiently.")
    
def services_page():
    st.header("Services")
    st.write("Our lawn care services include:")
    services = ["Mowing", "Fertilization", "Weed Control", "Aeration", "Seeding"]
    for service in services:
        st.write(f"- {service}")
    
def schedule_page():
    st.header("Schedule Service")
    name = st.text_input("Name")
    email = st.text_input("Email")
    service = st.selectbox("Service", ["Mowing", "Fertilization", "Weed Control", "Aeration", "Seeding"])
    date = st.date_input("Preferred Date")
    if st.button("Schedule"):
        st.success(f"Thank you {name}! Your {service} service has been scheduled for {date}.")
    
def contact_page():
    st.header("Contact Us")
    st.write("Phone: 555-LAWN")
    st.write("Email: contact@turbolawn.com")

if __name__ == "__main__":
    main()
