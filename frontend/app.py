import streamlit as st
import requests

API_URL = "http://backend:8000"

st.title("VR Platform Admin Panel")

menu = st.sidebar.selectbox("Choose Option", ["Users", "Devices"])

if menu == "Users":
    st.header("CREATE")

    # Add User
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Add User"):
        res = requests.post(f"{API_URL}/users", json={"username": username, "email": email, "password": password})
        if res.status_code == 200:
            st.success("User added successfully!")
        else:
            st.error("Failed to add user.")

    # Display List of Users
    st.subheader("READ")
    users = requests.get(f"{API_URL}/users").json()
    st.write(users)

    # Update User
    st.subheader("Update User")
    user_id_to_update = st.number_input("Enter User ID to Update", min_value=1)
    new_username = st.text_input("New Username")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    if st.button("Update User"):
        res = requests.put(f"{API_URL}/users/{user_id_to_update}", json={"username": new_username, "email": new_email, "password": new_password})
        if res.status_code == 200:
            st.success("User updated successfully!")
        else:
            st.error("Failed to update user.")

    # Delete User
    st.subheader("Delete User")
    user_id_to_delete = st.number_input("Enter User ID to Delete", min_value=1)
    if st.button("Delete User"):
        res = requests.delete(f"{API_URL}/users/{user_id_to_delete}")
        if res.status_code == 200:
            st.success("User deleted successfully!")
        else:
            st.error("Failed to delete user.")

elif menu == "Devices":
    st.header("CREATE Device")

    user_id = st.number_input("User ID", min_value=1, key="create_user_id")
    device_type = st.text_input("Device Type", key="create_device_type")
    serial_number = st.text_input("Serial Number", key="create_serial")

    if st.button("Add Device"):
        res = requests.post(
            f"{API_URL}/devices",
            json={
                "user_id": user_id,
                "device_type": device_type,
                "serial_number": serial_number
            }
        )
        if res.status_code == 200:
            st.success("Device added successfully!")
        else:
            st.error("Failed to add device.")

    st.subheader("READ Devices")
    devices = requests.get(f"{API_URL}/devices").json()
    st.write(devices)

    st.subheader("UPDATE Device")
    device_id_to_update = st.number_input("Enter Device ID to Update", min_value=1, key="update_device_id")
    new_user_id = st.number_input("New User ID", min_value=1, key="update_user_id")
    new_device_type = st.text_input("New Device Type", key="update_device_type")
    new_serial_number = st.text_input("New Serial Number", key="update_serial")

    if st.button("Update Device"):
        res = requests.put(
            f"{API_URL}/devices/{device_id_to_update}",
            json={
                "user_id": new_user_id,
                "device_type": new_device_type,
                "serial_number": new_serial_number
            }
        )
        if res.status_code == 200:
            st.success("Device updated successfully!")
        else:
            st.error("Failed to update device.")

    st.subheader("DELETE Device")
    device_id_to_delete = st.number_input("Enter Device ID to Delete", min_value=1, key="delete_device_id")

    if st.button("Delete Device"):
        res = requests.delete(f"{API_URL}/devices/{device_id_to_delete}")
        if res.status_code == 200:
            st.success("Device deleted successfully!")
        else:
            st.error("Failed to delete device.")
