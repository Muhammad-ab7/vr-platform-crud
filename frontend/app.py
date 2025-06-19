import streamlit as st
import requests
import pandas as pd
import re

API_URL = "http://backend:8000"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'signup_mode' not in st.session_state:
    st.session_state.signup_mode = False

st.title("VR Platform Panel")

# --- LOGIN / SIGNUP SECTION ---
def login():
    st.subheader("Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")

    if st.button("Login"):
        # Input validation
        if not login_username or not login_password:
            st.warning("Please enter both username and password.")
            return
        try:
            res = requests.post(f"{API_URL}/login", json={"username": login_username, "password": login_password})
            if res.status_code == 200:
                user = res.json()
                st.session_state.authenticated = True
                st.session_state.current_user = user
                st.session_state.role = user.get("role", "user")
                st.success(f"Welcome, {login_username}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
        except Exception:
            st.error("Backend not reachable.")



def is_valid_email(email):
    # Basic email regex pattern
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def signup():
    st.subheader("Signup")
    signup_username = st.text_input("Enter Username")
    signup_email = st.text_input("Your Email")
    signup_password = st.text_input("Choose Password", type="password")

    if st.button("Create Account"):
        # Validation
        if not signup_username or not signup_email or not signup_password:
            st.warning("All fields are required.")
            return

        if len(signup_username.strip()) < 3:
            st.warning("Username must be at least 3 characters long.")
            return

        if not is_valid_email(signup_email.strip()):
            st.warning("Please enter a valid email address.")
            return

        if len(signup_password) < 6:
            st.warning("Password must be at least 6 characters long.")
            return

        try:
            res = requests.post(f"{API_URL}/signup", json={
                "username": signup_username.strip(),
                "email": signup_email.strip(),
                "password": signup_password
            })
            if res.status_code == 200:
                st.success("Account created successfully! Please login.")
                st.session_state.signup_mode = False
                st.rerun()
            else:
                st.error(res.json().get("detail", "Signup failed."))
        except Exception:
            st.error("Backend not reachable.")


# --- Toggle Between Login & Signup ---
if not st.session_state.authenticated:
    if st.session_state.signup_mode:
        signup()
        if st.button("Already have an account? Login"):
            st.session_state.signup_mode = False
            st.rerun()

    else:
        login()
        if st.button("Don't have an account? Signup"):
            st.session_state.signup_mode = True
            st.rerun()

    st.stop()

# --- LOGOUT ---
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()


# --- AUTHENTICATED AREA ---
menu = st.sidebar.selectbox("Choose Option", ["Users", "Devices"])

if st.session_state.authenticated:
    st.info(f"Logged in as {st.session_state.current_user['username']} ({st.session_state.role})")


if menu == "Users":
    st.header("Users")

    st.subheader("READ Users")

    if st.button("Refresh Users"):
        st.session_state["refresh_users"] = True
        st.rerun()

    if "refresh_users" not in st.session_state:
        st.session_state["refresh_users"] = True

    if st.session_state["refresh_users"]:
        try:
            users = requests.get(f"{API_URL}/users").json()
            # Filter out admin users
            filtered_users = [user for user in users if user["role"] != "admin"]

            # Display in a table
            df_users = pd.DataFrame(filtered_users)
            if not df_users.empty:
                df_users = df_users[["user_id", "username", "email", "role"]]
                df_users.columns = ["User ID", "Username", "Email", "Role"]
                st.dataframe(df_users, use_container_width=True, height=400)
            else:
                st.info("No non-admin users found.")
        except:
            st.error("Could not fetch users from backend.")


    # Only admin can Add/Update/Delete
    if st.session_state.role == "admin":

        st.subheader("CREATE")

        def is_valid_email(email):
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return re.match(pattern, email)

        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Add User"):
            if not username or not email or not password:
                st.warning("All fields are required.")
            elif len(username.strip()) < 3:
                st.warning("Username must be at least 3 characters long.")
            elif not is_valid_email(email.strip()):
                st.warning("Please enter a valid email address.")
            elif len(password) < 6:
                st.warning("Password must be at least 6 characters long.")
            else:
                # Make the API call only if inputs are valid
                res = requests.post(f"{API_URL}/users", json={
                "username": username.strip(),
                "email": email.strip(),
                "password": password
            })
                if res.status_code == 200:
                    st.success("User added successfully!")
                    st.session_state["refresh_users"] = True
                    st.rerun()
                else:
                    st.error("Failed to add user.")


        st.subheader("Update User")
        user_id_to_update = st.number_input("Enter User ID to Update", min_value=0)
        new_username = st.text_input("New Username")
        new_email = st.text_input("New Email")
        new_password = st.text_input("New Password", type="password")

        if st.button("Update User"):
            if not new_username or not new_email or not new_password:
                st.warning("All fields are required.")
            elif len(new_username.strip()) < 3:
                st.warning("Username must be at least 3 characters long.")
            elif not is_valid_email(new_email.strip()):
                st.warning("Please enter a valid email address.")
            elif len(new_password) < 6:
                st.warning("Password must be at least 6 characters long.")
            else:
                # Proceed with update request
                res = requests.put(
                    f"{API_URL}/users/{user_id_to_update}",
                    json={
                        "username": new_username.strip(),
                        "email": new_email.strip(),
                        "password": new_password
                    }
                )
            if res.status_code == 200:
                st.success("User updated successfully!")
                st.session_state["refresh_users"] = True
                st.rerun()
            else:
                st.error("Failed to update user.")
                

        st.subheader("Delete User")
        user_id_to_delete = st.number_input("Enter User ID to Delete", min_value=0)
        if st.button("Delete User"):
            res = requests.delete(f"{API_URL}/users/{user_id_to_delete}")
            if res.status_code == 200:
                st.success("User deleted successfully!")
                st.session_state["refresh_users"] = True
                st.rerun()
            else:
                st.error("Failed to delete user.")

elif menu == "Devices":
    st.header("Devices")

    # Initialize session state only once
    if "refresh_devices" not in st.session_state:
        st.session_state["refresh_devices"] = True

    # Button to manually refresh
    if st.button("Refresh Devices"):
        st.session_state["refresh_devices"] = True
        st.rerun()

    # Automatically refresh devices list when flagged
    if st.session_state["refresh_devices"]:
        try:
            devices = requests.get(f"{API_URL}/devices").json()
            if devices:
                df_devices = pd.DataFrame(devices)
                df_devices = df_devices[["device_id", "device_type", "serial_number", "registered_at"]]
                df_devices.columns = ["Device ID", "Type", "Serial No", "Registered At"]
                st.dataframe(df_devices, use_container_width=True, height=400)
            else:
                st.info("No devices found.")
        except requests.exceptions.RequestException:
            st.error("Could not fetch devices from backend.")
        st.session_state["refresh_devices"] = False  # Reset flag AFTER success

    # ----- Buy Device Section -----
    st.subheader("Buy a Device")
    device_id_to_buy = st.number_input("Enter Device ID to Buy", min_value=1, key="buy_device_id")

    buy_clicked = st.button("Buy Device")
    if buy_clicked:
        try:
            res = requests.delete(f"{API_URL}/devices/{device_id_to_buy}")
            if res.status_code == 200:
                st.session_state["refresh_devices"] = True  # Mark for refresh
                st.success("You have successfully purchased the device!")
                st.rerun()  # 🔄 This stops execution and reruns from the top
            else:
                st.error("Purchase failed. Device might not exist.")
        except requests.exceptions.RequestException:
            st.error("Could not reach backend.")



    #  Only admins can Create/Update/Delete
    if st.session_state.get("role") == "admin":
        st.subheader("CREATE Device")

        device_type = st.text_input("Device Type", key="create_device_type")
        serial_number = st.text_input("Serial Number", key="create_serial")

        if st.button("Add Device"):
            res = requests.post(
                f"{API_URL}/devices",
                json={
                    "device_type": device_type,
                    "serial_number": serial_number
            }
            )
            if res.status_code == 200:
                st.success("Device added successfully!")
                st.session_state["refresh_devices"] = True
                st.rerun()
            else:
                st.error("Failed to add device.")

        st.subheader("UPDATE Device")
        device_id_to_update = st.number_input("Device ID to Update", min_value=1, key="update_device_id")
        new_device_type = st.text_input("New Device Type", key="update_device_type")
        new_serial_number = st.text_input("New Serial Number", key="update_serial")

        if st.button("Update Device"):
            res = requests.put(
                f"{API_URL}/devices/{device_id_to_update}",
                json={
                    "device_type": new_device_type,
                    "serial_number": new_serial_number
                }
            )
            if res.status_code == 200:
                st.success("Device updated successfully!")
                st.session_state["refresh_devices"] = True
                st.rerun()
            else:
                st.error("Failed to update device.")

        st.subheader("DELETE Device")
        device_id_to_delete = st.number_input("Device ID to Delete", min_value=1, key="delete_device_id")

        if st.button("Delete Device"):
            res = requests.delete(f"{API_URL}/devices/{device_id_to_delete}")
            if res.status_code == 200:
                st.success("Device deleted successfully!")
                st.session_state["refresh_devices"] = True
                st.rerun()
            else:
                st.error("Failed to delete device.")

