import streamlit as st

# Streamlit UI
st.title("📋 Student Attendance Tracker")

# Session state to store attendance list
if "attendance_list" not in st.session_state:
    st.session_state.attendance_list = []

# Take attendance input
name = st.text_input("Enter student name (Type 'stop' to finish):").strip()

if st.button("Add Student"):
    if name:
        if name.lower() != "stop":
            st.session_state.attendance_list.append(name)
            st.success(f"✅ {name} has been marked present!")
        else:
            st.warning("🛑 Attendance input stopped!")

# Display attendance list
st.subheader("🎯 Attendance List")
st.write(st.session_state.attendance_list)

# Check if a student is present
search_name = st.text_input("🔍 Check if a student is present:").strip()

if st.button("Check Attendance"):
    if search_name:
        if search_name.lower() in [student.lower() for student in st.session_state.attendance_list]:
            st.success(f"🎉 Yes, {search_name} is present!")
        else:
            st.error(f"❌ {search_name} is NOT present!")

# Show total student count
st.subheader(f"👥 Total Students Present: {len(st.session_state.attendance_list)}")
