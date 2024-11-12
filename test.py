import streamlit as st
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="ADMIN", page_icon="🎬", layout="wide")

# Kết nối tới MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["YoutubeAPI"]
collection = db["users"]

def manage_accounts():
    st.markdown(
        """
        <h1 style='display: flex; align-items: center;'>
            <img src='https://media.giphy.com/media/9VlcSot7G8JyLm7mZU/giphy.gif?cid=ecf05e4786fzyybrf7gabwc08t05rp7g3x6lyy68kvp7eduf&ep=v1_stickers_search&rid=giphy.gif&ct=s' 
            width='100' height='100' style='margin-left: 600px;'/> 
            <span style='font-weight: bold; width: 100%;'>Quản lý Tài Khoản</span>
        </h1>
        """, 
        unsafe_allow_html=True)
    
    # Lấy danh sách tài khoản từ cơ sở dữ liệu
    users = list(collection.find({}))
    if not users:
        st.write("Không có tài khoản nào.")
    else:
        # Chuyển đổi danh sách tài khoản thành DataFrame để dễ hiển thị
        df = pd.DataFrame(users)

        # Xóa cột 'history' nếu có
        if 'history' in df.columns:
            df = df.drop(columns=['history'])

        # Hiển thị mật khẩu rõ ràng
        if 'password' in df.columns:
            # Không ẩn mật khẩu
            pass
        
        col1, col2 = st.columns([1, 1])
        # Hiển thị bảng tài khoản
        with col1:
            st.dataframe(df, width=800)
        
        usernames = [user['username'] for user in users]
        with col2:
            selected_username = st.selectbox("Chọn tài khoản để chỉnh sửa", usernames)
            # Hiển thị thông tin tài khoản đã chọn
            if selected_username:
                user = collection.find_one({"username": selected_username})
                if user:
                    with st.form(key="edit_account"):
                        st.write(f"Sửa tài khoản: {user['username']}")
                        new_username = st.text_input("Tên đăng nhập mới", value=user['username'])
                        new_password = st.text_input("Mật khẩu mới", type="password", value=user['password'])
                        confirm_password = st.text_input("Xác nhận mật khẩu", type="password")
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col1:
                            if st.form_submit_button("Tạo tài khoản"):
                                if new_password == confirm_password:
                                    if collection.find_one({"username": new_username}):
                                        st.error("Tên đăng nhập đã tồn tại.")
                                    else:
                                        collection.insert_one({"username": new_username, "password": new_password, "history": []})
                                        st.success("Tạo tài khoản thành công!")
                                        st.rerun()
                                else:
                                    st.error("Mật khẩu xác nhận không khớp.")
                        with col2:
                            submitted = st.form_submit_button("Cập nhật tài khoản")
                        if submitted:
                            if new_password == confirm_password:
                                collection.update_one({"username": user['username']}, {"$set": {"username": new_username, "password": new_password}})
                                st.success("Thông tin tài khoản đã được cập nhật!")
                                st.rerun()
                            else:
                                st.error("Mật khẩu xác nhận không khớp.")
                        with col3:
                            # Xóa tài khoản
                            if st.form_submit_button(f"Xóa tài khoản {selected_username}"):
                                collection.delete_one({"username": selected_username})
                                st.success(f"Tài khoản {selected_username} đã bị xóa.")
                                st.rerun()

        # Thống kê query
        st.markdown("<h1 style='text-align: center;'>Thống kê Query</h1>", unsafe_allow_html=True)
        # Lựa chọn loại thống kê
        options = ["Thống kê tất cả tài khoản", "Thống kê theo tài khoản cụ thể", "Thống kê theo một nhóm tài khoản"]
        
        

        # Thêm phần chọn ngày bắt đầu và ngày kết thúc
        col1, col2, col3 = st.columns([2, 1,1])
        with col1:
            selection = st.selectbox("Chọn loại thống kê", options)
        with col2:
            start_date = st.date_input("Ngày bắt đầu🛫", datetime(2023, 1, 1))
        with col3:
            end_date = st.date_input("Ngày kết thúc🛬", datetime.utcnow().date())
        
        start_datetime_str = start_date.strftime("%Y-%m-%d")
        end_datetime_str = end_date.strftime("%Y-%m-%d")
        
        if selection == "Thống kê theo tài khoản cụ thể":
            usernames = [user['username'] for user in collection.find({})]
            with col1:
                selected_username = st.selectbox("Chọn tài khoản", usernames)
            users = list(collection.find({"username": selected_username}))
        elif selection == "Thống kê theo một nhóm tài khoản":
            usernames = [user['username'] for user in collection.find({})]
            with col1:
                selected_usernames = st.multiselect("Chọn các tài khoản", usernames)
            users = list(collection.find({"username": {"$in": selected_usernames}}))
        else:
            users = list(collection.find({}))
        
        query_counts = {}

        for user in users:
            if 'history' in user:
                for entry in user['history']:
                    query = entry[0]
                    time_str = entry[2]  # Định dạng thời gian trong cơ sở dữ liệu
    
                    # Chuyển đổi chuỗi thời gian thành đối tượng datetime
                    try:
                        # if isinstance(time_str, int):
                        #     time_str = str(time_str)
                        time = datetime.strptime(time_str, "%H:%M:%S %d-%m-%Y")
                    except ValueError:
                        continue  # Bỏ qua nếu thời gian không hợp lệ
                    
                    # Chỉ lọc theo ngày
                    time_date_str = time.strftime("%Y-%m-%d")

                    if query:
                        # Lọc theo thời gian
                        if start_datetime_str <= time_date_str <= end_datetime_str:
                            if query in query_counts:
                                query_counts[query] += 1
                            else:
                                query_counts[query] = 1

        if query_counts:
            # Hiển thị bảng thống kê
            col1, col2 = st.columns([1, 3])
            query_df = pd.DataFrame(list(query_counts.items()), columns=["Query", "Count"])
            with col1:
                st.dataframe(query_df)

            # Vẽ biểu đồ hình tròn
            fig, ax = plt.subplots()
            ax.pie(query_counts.values(), labels=query_counts.keys(), autopct='%1.1f%%', startangle=90)
            ax.axis("equal")
            with col2:
                st.pyplot(fig)
        else:
            st.write("Không có dữ liệu lịch sử để thống kê.")

manage_accounts()
