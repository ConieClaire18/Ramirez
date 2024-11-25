import streamlit as st
from PIL import Image
from datetime import datetime

# Initialize session state for biographies and dynamic fields
def init_session_state():
    if "biographies" not in st.session_state:
        st.session_state["biographies"] = []
    if "dynamic_fields" not in st.session_state:
        st.session_state["dynamic_fields"] = {}

# Function to calculate age based on birthdate
def calculate_age(birthdate):
    today = datetime.today()
    birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# Add a new biography with dynamic fields
def add_biography():
    st.title("Add a New Biography")

    with st.form("add_bio_form"):
        # Select or specify biography type
        bio_type = st.selectbox("Biography Type", ["Personal", "Professional", "Custom"])
        if bio_type == "Custom":
            bio_type = st.text_input("Enter Custom Biography Type")

        # Other biography details
        photo = st.file_uploader("Upload a photo (JPG/PNG)", type=["jpg", "jpeg", "png"])
        name = st.text_input("Name")
        birthdate = st.date_input("Birthdate", datetime(2000, 1, 1))
        address = st.text_input("Address")

        # Educational Attainment
        st.subheader("Educational Attainment")
        elementary = st.text_input("Elementary School")
        high_school = st.text_input("High School")
        senior_high = st.text_input("Senior High School")

        # Seminars and Accomplishments
        st.subheader("Seminars Attended")
        seminars = st.text_area("Enter seminars attended, one per line")
        st.subheader("Accomplishments")
        accomplishments = st.text_area("Enter accomplishments, one per line")

        # Skills and Hobbies
        st.subheader("Skills")
        skills = st.text_area("Enter your skills, one per line")
        st.subheader("Hobbies")
        hobbies = st.text_area("Enter your hobbies, one per line")

        # Add custom fields dynamically
        st.subheader("Add Custom Fields")
        dynamic_field_name = st.text_input("Enter field name to add (e.g., 'Certifications', 'Languages', etc.)")
        dynamic_field_value = st.text_area(f"Enter {dynamic_field_name} details")

        # Store the dynamic field in session state
        if dynamic_field_name and dynamic_field_value:
            if dynamic_field_name not in st.session_state["dynamic_fields"]:
                st.session_state["dynamic_fields"][dynamic_field_name] = []
            st.session_state["dynamic_fields"][dynamic_field_name].append(dynamic_field_value)

        # Submit Button
        submitted = st.form_submit_button("Save Biography")
        
        if submitted:
            new_biography = {
                "type": bio_type,
                "photo": photo.getvalue() if photo else None,
                "name": name,
                "birthdate": birthdate.strftime("%Y-%m-%d"),
                "address": address,
                "educational_attainment": {
                    "Elementary": elementary,
                    "High School": high_school,
                    "Senior High School": senior_high,
                },
                "seminars_attended": [s.strip() for s in seminars.split("\n") if s.strip()],
                "accomplishments": [a.strip() for a in accomplishments.split("\n") if a.strip()],
                "skills": [s.strip() for s in skills.split("\n") if s.strip()],
                "hobbies": [h.strip() for h in hobbies.split("\n") if h.strip()],
            }
            
            # Add dynamic fields to biography
            for field, values in st.session_state["dynamic_fields"].items():
                new_biography[field] = values
            
            st.session_state["biographies"].append(new_biography)
            st.success(f"{bio_type} biography added successfully!")

# View all biographies grouped by type
def view_all_biographies():
    st.title("View All Biographies")

    if not st.session_state["biographies"]:
        st.info("No biographies added yet. Please add a biography first.")
        return

    # Group biographies by type
    bio_types = set(bio["type"] for bio in st.session_state["biographies"])
    for bio_type in sorted(bio_types):
        st.header(f"{bio_type} Biographies")
        bios_of_type = [bio for bio in st.session_state["biographies"] if bio["type"] == bio_type]

        for index, bio in enumerate(bios_of_type):
            st.subheader(f"{bio['name']}")
            
            # Layout: Photo on the left, details on the right
            col1, col2 = st.columns([1, 2])
            with col1:
                if bio["photo"]:
                    st.image(bio["photo"], caption=f"{bio['name']}'s Photo", use_column_width=True)
                else:
                    st.info("No photo uploaded.")
            
            with col2:
                st.write(f"**Name:** {bio['name']}")
                st.write(f"**Birthdate:** {bio['birthdate']}")
                st.write(f"**Age:** {calculate_age(bio['birthdate'])} years old")
                st.write(f"**Address:** {bio['address']}")
                
                st.write(f"**Elementary:** {bio['educational_attainment']['Elementary']}")
                st.write(f"**High School:** {bio['educational_attainment']['High School']}")
                st.write(f"**Senior High School:** {bio['educational_attainment']['Senior High School']}")

                st.write("**Seminars Attended:**")
                for seminar in bio["seminars_attended"]:
                    st.write(f"- {seminar}")

                st.write("**Accomplishments:**")
                for accomplishment in bio["accomplishments"]:
                    st.write(f"- {accomplishment}")

                st.write("**Skills:**")
                for skill in bio["skills"]:
                    st.write(f"- {skill}")

                st.write("**Hobbies:**")
                for hobby in bio["hobbies"]:
                    st.write(f"- {hobby}")

                # Display dynamic fields
                for field, values in bio.items():
                    if field not in ["type", "photo", "name", "birthdate", "address", "educational_attainment", "seminars_attended", "accomplishments", "skills", "hobbies"]:
                        st.write(f"**{field}:**")
                        for value in values:
                            st.write(f"- {value}")

# Main Function
def main():
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Select an Option", ["Add Biography", "View All Biographies"])

    init_session_state()

    if menu == "Add Biography":
        add_biography()
    elif menu == "View All Biographies":
        view_all_biographies()

if __name__ == "__main__":
    main()
