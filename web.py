import streamlit as st
import os

# Initialize session state for biography data
def initialize_bio_data():
    if "bio_data" not in st.session_state:
        st.session_state.bio_data = {
            "name": "Conie Claire Ramirez",  # Default name
            "age": 18,  # Default age
            "birthdate": "August 17, 2006",  # Default birthdate
            "address": "San Isidro, Surigao City",  # Default address
            "bio": "",
            "elementary": [{"school": "San Isidro Elementary School", "year": "2014-2018"}],
            "high_school": [{"school": "Mainit National High School", "year": "2018-2022"}],
            "senior_high": [{"school": "Surigao del Norte National High School", "year": "2022-2024"}],
            "college": [{"school": "Surigao del Norte State University", "year": "2024-2028"}],
            "seminars_attended": [
                {"seminar": "Leadership Training", "year": "2019"},
                {"seminar": "Church Training", "year": "2022"}
            ],
            "accomplishments": [
                "Graduated with Honors",
                "Passed the Entrance Exam and Interview"
            ],
            "image": None,
        }

# Function to create the biography string for download
def create_bio_string():
    bio_data = st.session_state.bio_data
    bio_str = f"Name: {bio_data['name']}\n"
    bio_str += f"Age: {bio_data['age']}\n"
    bio_str += f"Birthdate: {bio_data['birthdate']}\n"
    bio_str += f"Address: {bio_data['address']}\n"
    bio_str += f"Biography: {bio_data['bio']}\n\n"
    
    bio_str += "Educational Attainment:\n"
    for edu in bio_data.get("elementary", []):
        bio_str += f"  - Elementary: {edu['school']} ({edu['year']})\n"
    for edu in bio_data.get("high_school", []):
        bio_str += f"  - High School: {edu['school']} ({edu['year']})\n"
    for edu in bio_data.get("senior_high", []):
        bio_str += f"  - Senior High: {edu['school']} ({edu['year']})\n"
    for edu in bio_data.get("college", []):
        bio_str += f"  - College: {edu['school']} ({edu['year']})\n"
    
    bio_str += "\nSeminars Attended:\n"
    for seminar in bio_data.get("seminars_attended", []):
        bio_str += f"  - {seminar['seminar']} ({seminar['year']})\n"
    
    bio_str += "\nAccomplishments:\n"
    for acc in bio_data.get("accomplishments", []):
        bio_str += f"  - {acc}\n"
    
    return bio_str

# Streamlit application
st.title("Biography")

# Initialize biography data
initialize_bio_data()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([ 
    "Biography", 
    "Educational Attainment", 
    "Seminars Attended", 
    "Accomplishments", 
    "Upload Image", 
    "View Biography"
])

with tab1:
    st.subheader("Personal Biography")
    st.session_state.bio_data["name"] = st.text_input("Name", value=st.session_state.bio_data.get("name", ""))
    st.session_state.bio_data["age"] = st.number_input("Age", value=st.session_state.bio_data.get("age", 0), min_value=0)
    st.session_state.bio_data["birthdate"] = st.text_input("Birthdate", value=st.session_state.bio_data.get("birthdate", ""))
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Save Biography"):
            st.success("Biography saved successfully!")

with tab2:
    st.subheader("Educational Attainment")
    
    # Editable fields to add new educational records
    st.write("### Add Educational Records")

    # Function to display editable education records
    def display_education_section(edu_type, edu_data_key):
        with st.expander(edu_type):
            for idx, edu in enumerate(st.session_state.bio_data.get(edu_data_key, [])):
                col1, col2 = st.columns([4, 1])
                with col1:
                    school_name = st.text_input(f"School Name ({edu_type})", value=edu["school"], key=f"school_{edu_data_key}_{idx}")
                    year_attended = st.text_input(f"Year Attended ({edu_type})", value=edu["year"], key=f"year_{edu_data_key}_{idx}")
                with col2:
                    if st.button(f"Delete {edu_type} Record", key=f"delete_{edu_data_key}_{idx}"):
                        st.session_state.bio_data[edu_data_key].remove(edu)
                        st.experimental_rerun()
                
                if school_name and year_attended:
                    st.session_state.bio_data[edu_data_key][idx]["school"] = school_name
                    st.session_state.bio_data[edu_data_key][idx]["year"] = year_attended
                else:
                    st.warning("Please provide both school name and year.")
            
            new_school = st.text_input(f"New School Name ({edu_type})", key=f"new_school_{edu_data_key}")
            new_year = st.text_input(f"New Year ({edu_type})", key=f"new_year_{edu_data_key}")
            if st.button(f"Add {edu_type} Record"):
                if new_school and new_year:
                    st.session_state.bio_data[edu_data_key].append({"school": new_school, "year": new_year})
                    st.success(f"{edu_type} record added successfully!")
                else:
                    st.warning(f"Please provide both school name and year.")
    
    # Display editable education sections
    display_education_section("Elementary", "elementary")
    display_education_section("High School", "high_school")
    display_education_section("Senior High", "senior_high")
    display_education_section("College", "college")

with tab3:
    st.subheader("Seminars Attended")
    seminar = st.text_input("Seminar Name")
    seminar_year = st.text_input("Seminar Year")
    
    if st.button("Add Seminar"):
        if seminar and seminar_year:
            st.session_state.bio_data["seminars_attended"].append({"seminar": seminar, "year": seminar_year})
            st.success("Seminar added successfully!")
        else:
            st.warning("Please provide both seminar name and year.")
    
    st.write("### Seminars Attended")
    for seminar in st.session_state.bio_data.get("seminars_attended", []):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"- {seminar['seminar']} ({seminar['year']})")
        with col2:
            if st.button(f"Delete Seminar: {seminar['seminar']}", key=f"delete_seminar_{seminar['seminar']}"):
                st.session_state.bio_data["seminars_attended"].remove(seminar)
                st.experimental_rerun()

with tab4:
    st.subheader("Accomplishments")
    accomplishments_text = st.text_area(
        "Add your accomplishments (one per line, starting with '-')", 
        value="\n".join(st.session_state.bio_data.get("accomplishments", []))
    )
    
    if st.button("Save Accomplishments"):
        st.session_state.bio_data["accomplishments"] = [
            line.strip() for line in accomplishments_text.split("\n") if line.strip()
        ]
        st.success("Accomplishments saved successfully!")
    
    st.write("### Accomplishments List")
    for acc in st.session_state.bio_data.get("accomplishments", []):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"- {acc}")
        with col2:
            if st.button(f"Delete Accomplishment: {acc}", key=f"delete_acc_{acc}"):
                st.session_state.bio_data["accomplishments"].remove(acc)
                st.experimental_rerun()

with tab5:
    st.subheader("Upload Profile Image")
    uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        image_path = f"uploaded_image_{uploaded_image.name}"
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())
        st.session_state.bio_data["image"] = image_path
        st.success("Image uploaded successfully!")
    
    if st.session_state.bio_data.get("image"):
        st.image(st.session_state.bio_data["image"], caption="Uploaded Profile Image")

with tab6:
    st.subheader("Complete Biography")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.session_state.bio_data.get("image"):
            st.image(st.session_state.bio_data["image"], caption="Profile Image")
        else:
            st.write("No image uploaded.")
    
    with col2:
        st.write(f"### Name: {st.session_state.bio_data.get('name', '')}")
        st.write(f"### Age: {st.session_state.bio_data.get('age', '')}")
        st.write(f"### Birthdate: {st.session_state.bio_data.get('birthdate', '')}")
        st.write(f"### Address: {st.session_state.bio_data.get('address', '')}")
        st.write(f"### Biography: {st.session_state.bio_data.get('bio', '')}")
    
    st.write("### Educational Attainment:")
    for edu in st.session_state.bio_data.get("elementary", []):
        st.write(f"- Elementary: {edu['school']} ({edu['year']})")
    for edu in st.session_state.bio_data.get("high_school", []):
        st.write(f"- High School: {edu['school']} ({edu['year']})")
    for edu in st.session_state.bio_data.get("senior_high", []):
        st.write(f"- Senior High: {edu['school']} ({edu['year']})")
    for edu in st.session_state.bio_data.get("college", []):
        st.write(f"- College: {edu['school']} ({edu['year']})")
    
    st.write("### Seminars Attended:")
    for seminar in st.session_state.bio_data.get("seminars_attended", []):
        st.write(f"- {seminar['seminar']} ({seminar['year']})")

    st.write("### Accomplishments:")
    for acc in st.session_state.bio_data.get("accomplishments", []):
        st.write(f"- {acc}")
    
    # Create biography string for download
    bio_string = create_bio_string()
    
    # Button to download the biography
    st.download_button(
        label="Download Biography",
        data=bio_string,
        file_name="biography.txt",
        mime="text/plain"
    )