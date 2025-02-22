import streamlit as st

# Initialize session state variables
if "password" not in st.session_state:
    st.session_state.password = None  # Store password securely
if "attendance_set" not in st.session_state:
    st.session_state.attendance_set = {"admin", "interpreter"}  # Initial entries
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False  # Track login status
if "attendance_active" not in st.session_state:
    st.session_state.attendance_active = True  # Control attendance input

# Set Password (Only Once)
st.title("🔐 Teacher's Secure Attendance System")

if st.session_state.password is None:
    st.subheader("🛠️ Set Up a Password (Only Once)")
    new_password = st.text_input("Enter a password:", type="password")
    if st.button("Set Password"):
        if new_password:
            st.session_state.password = new_password
            st.success("✅ Password has been set! Now hidden for security.")

# Attendance Input (Only if attendance is active)
st.subheader("📋 Mark Attendance")
student_name = st.text_input("Enter your full name:")

if st.session_state.attendance_active:
    if st.button("Submit Attendance"):
        if student_name and student_name.lower() != "stop":
            st.session_state.attendance_set.add(student_name)
            st.success(f"✅ {student_name} marked present!")
else:
    st.warning("🛑 Attendance has been stopped. Submission disabled.")

# Stop Attendance (Disables Attendance Submission)
if st.button("Stop Attendance"):
    st.session_state.attendance_active = False
    st.warning("🛑 Attendance marking has been stopped!")

# Teacher Login (Password Check)
st.subheader("🔑 Teacher Login")
teacher_password = st.text_input("Enter teacher's password:", type="password")

if st.button("Login"):
    if teacher_password == st.session_state.password:
        st.session_state.authenticated = True
        st.success("✅ Access Granted!")
    else:
        st.error("❌ Incorrect Password!")

# Show Attendance Only If Logged In
if st.session_state.authenticated:
    st.subheader(f"👥 Total Students Present: {len(st.session_state.attendance_set) - 2}")
    st.write(list(st.session_state.attendance_set - {'admin', 'interpreter'}))

    # Check for a specific student
    search_name = st.text_input("🔍 Check if a student is present:")
    if st.button("Check Attendance"):
        if search_name in st.session_state.attendance_set:
            st.success(f"🎉 Yes, {search_name} is present!")
        else:
            st.error(f"❌ {search_name} is NOT present!")

# Logout Button
if st.session_state.authenticated and st.button("Logout"):
    st.session_state.authenticated = False
    st.warning("🔒 Logged out!")

