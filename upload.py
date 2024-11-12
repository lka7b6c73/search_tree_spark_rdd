import json
import os
import streamlit as st
import time
from datetime import datetime, timedelta
import requests
import re
import streamlit.components.v1 as components
from pymongo import MongoClient
st.set_page_config(page_title="SEARCH ENGINER", page_icon="🎬", layout="wide")
url = "https://02fb-117-6-40-134.ngrok-free.app"

class CollectionWrapper:
    def __init__(self):
        # Dùng danh sách để lưu trữ các tài liệu (tương tự như MongoDB)
        self.data = self.load_data()  # Tải dữ liệu từ file JSON
        self.current_id = max([item['_id'] for item in self.data], default=0) + 1 if self.data else 1

    def load_data(self):
        response = requests.post(url+"/account")
        results = response.json()  
    
        return results
    def save_data(self):
        response = requests.post(url+"/save", json=self.data)
    def insert_one(self, document):
        """Chèn một tài liệu mới vào collection."""
        document['_id'] = self.current_id  # Gán _id tự động
        self.data.append(document)
        self.current_id += 1
        return {"inserted_id": document['_id']}

    def find_one(self, query):
        """Tìm một tài liệu dựa trên query."""
        for document in self.data:
            if all(document.get(k) == v for k, v in query.items()):
                return document
        return None

    def update_one(self, query, update_data):
        """Cập nhật tài liệu đầu tiên tìm thấy dựa trên query."""
        for document in self.data:
            if all(document.get(k) == v for k, v in query.items()):
                document.update(update_data)
                return {"matched_count": 1, "modified_count": 1}
        return {"matched_count": 0, "modified_count": 0}

    def delete_one(self, query):
        """Xóa tài liệu đầu tiên tìm thấy dựa trên query."""
        for i, document in enumerate(self.data):
            if all(document.get(k) == v for k, v in query.items()):
                del self.data[i]
                return {"deleted_count": 1}
        return {"deleted_count": 0}

# Sử dụng class CollectionWrapper thay thế MongoDB collection
collection = CollectionWrapper()


#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
# cài đặt trước

box_style = """
    <div style="
        border: 2px solid #45434c; 
        padding: 10px; 
        border-radius: 5px; 
        background-color: #45434c; 
        height: 300px; 
        overflow-y: auto; 
        overflow-x: hidden; 
        white-space: pre-wrap;">
        {content}
    </div>
"""
# Thêm CSS để định dạng button

st.markdown("""
    <style>
    .stSidebar .stButton button {
        width: 100%;
        border-radius: 5px; /* Bỏ bo góc */
        background-color: #262730; /* Màu nền xám đen */
        color: white; /* Màu chữ trắng */
        border: 1px solid #1e1f26; /* Viền màu xám nhạt hơn */
        padding: 10px;
        font-size: 16px;
        text-align: left; /* Căn lề chữ sang phải */
        margin-bottom: 0px;
        display: flex;
        justify-content: flex-start; /* Đưa nội dung về bên phải */
    }
    .stSidebar .stButton button:hover {
        background-color: #1e1f26; /* Hiệu ứng nền khi hover */
    }
    .stSidebar .stButton {
        margin-bottom: 0px; /* Loại bỏ khoảng cách giữa các button */
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 0px 0;
        color: #ffffff;
    }
    .divider::before,
    .divider::after {
        content: "";
        flex: 1;
        border-top: 1px solid #ffffff;
        margin: 0 0px;
    }
    .divider span {
        font-weight: bold;
    }
    .custom-divider {
        border-top: 2px solid #1e1f26; /* Đoạn kẻ màu đậm hơn */
        margin: 0; /* Không có khoảng cách */
        padding: 0; /* Không có padding */
    }
    </style>
    """, unsafe_allow_html=True)
_LOREM_IPSUM = '''
Hân hạnh được gặp bạn, tôi là phần mềm tìm kiếm video Youtube bằng hệ thống Bigdata dựa vào dữ liệu phụ đề Youtube\n
Bạn chỉ việc nhấn từ khóa vào ô tìm kiếm và nhân tìm kiếm sẽ cho bạn đây đủ thông tin về các video bạn cần tìm\n
Bạn có thể nhấn vào các từ khóa ở phần lịch sử để mở lại các từ khóa mà bản thân đã tìm kiếm trước đó\n
Khi có kết quả, bạn có thể điều chỉnh sổ lượng video, ngày tháng xuất bản để phù hợp ý định của bản thân\n
Ngoài ra bạn có thể xem được video, phụ đề và chỉ số tương thích với các từ khóa mà bạn đã đưa ra\n
Cuối cùng xin chúc bạn có một ngày làm việc suôn sẻ và thuận lợi!'''
_LOREM_IPSUM_LOGIN = '''
Xin chào, tôi là phần mềm tìm kiếm video Youtube bằng hệ thống Bigdata dựa vào dữ liệu phụ đề Youtube\n
Bạn hãy đăng nhập để trải nghiệm đầy đủ nhất về tiện ích của chúng tôi.!!!!!\n
'''
linkedin = "https://raw.githubusercontent.com/sahirmaharaj/exifa/main/img/linkedin.gif"
topmate = "https://raw.githubusercontent.com/sahirmaharaj/exifa/main/img/topmate.gif"
email = "https://raw.githubusercontent.com/sahirmaharaj/exifa/main/img/email.gif"
newsletter = ("https://raw.githubusercontent.com/sahirmaharaj/exifa/main/img/newsletter.gif")
share = "https://raw.githubusercontent.com/sahirmaharaj/exifa/main/img/share.gif"
caption =     f"""
        <div style='display: flex; align-items: center;'>
            <a href = 'https://www.instagram.com/k.pear29/'><img src='{linkedin}' style='width: 35px; height: 35px; margin-right: 25px;'></a>
            <a href = 'https://web.facebook.com/profile.php?id=100090786036344'><img src='{topmate}' style='width: 32px; height: 32px; margin-right: 25px;'></a>
            <a href = 'mailto:lka7b6c73@gmail.com'><img src='{email}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            <a href = 'https://web.facebook.com/tuyet.phamanh.336'><img src='{newsletter}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
            <a href = 'https://www.kaggle.com/gqqdluck'><img src='{share}' style='width: 28px; height: 28px; margin-right: 25px;'></a>
        </div>       
        """
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#các session_state
if 'create_user' not in st.session_state:
    st.session_state.create_user = False
if 'delete_user' not in st.session_state:
    st.session_state.delete_user= False
if 'show_message_login' not in st.session_state:
    st.session_state.show_message_login = True
if 'id' not in st.session_state:
    st.session_state.id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'password' not in st.session_state:
    st.session_state.password = None   
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'account' not in st.session_state:
    st.session_state.account = False

#### giao diện client
if 'len_results' not in st.session_state:
    st.session_state.len_results = None
if 'search_results' not in st.session_state:
    st.session_state.search_results = None
if 'time_load' not in st.session_state:
    st.session_state.time_load = 0
if 'time_search' not in st.session_state:
    st.session_state.time_search = 0    
if 'search_triggered' not in st.session_state:
    st.session_state.search_triggered = False
if 'query' not in st.session_state:
    st.session_state.query = None
if "show_animation" not in st.session_state:
    st.session_state.show_animation = True
if "show_message" not in st.session_state:
    st.session_state.show_message = True
if "show_404" not in st.session_state:
    st.session_state.show_404 = False
if "show_animation" not in st.session_state:
    st.session_state.show_animation = True



#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
                                        
def account_info():
    with st.form(key="edit_account"):
        st.subheader("Thông tin tài khoản")
        st.write(f"Tên đăng nhập: {st.session_state.username}")
        st.write(f"Mật khẩu: {'*' * len(st.session_state.password)}")

        new_password = st.text_input("Nhập mật khẩu mới", type="password")
        if st.form_submit_button("Đổi mật khẩu"):
            if new_password:
                collection.update_one({"_id": st.session_state.id}, {"$set": {"password": new_password}})
                st.session_state.password = new_password
                st.success("Mật khẩu đã được đổi thành công!")
                st.rerun()
        lcol1,lcol2 = st.columns([1,1])
        with lcol1:
            if st.form_submit_button("Xóa tài khoản"):
                st.session_state.delete_user = True
        
        with lcol2:
            if st.session_state.delete_user:
                if st.form_submit_button("Xác nhận xóa tài khoản"):
                    collection.delete_one({"_id": st.session_state.id})
                    collection.save_data()
                    st.sidebar.success("Tài khoản đã được xóa thành công!. Tự động đăng xuất sau 3s")
                    time.sleep(3)
                    st.session_state.logged_in = False
                    st.session_state.account = False
                    st.session_state.show_animation = True
                    st.session_state.show_message = True
                    st.rerun()

        if st.form_submit_button("Đăng xuất"):
            st.session_state.logged_in = False
            st.session_state.show_animation = True
            st.session_state.show_message = True
            st.session_state.account = False
            st.session_state.search_triggered = False    
            collection.save_data() 
            st.rerun()


# Các hàm để lấy URL hình ảnh thu nhỏ và URL video

def get_video_thumbnail(video_id):
    thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/default.jpg"
    return thumbnail_url

def get_video_link(video_id):
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    return youtube_url

# Hàm định dạng thời gian xuất bản thành giờ:phút:giây ngày-tháng-năm
def format_publish_time(publish_time_str):
    publish_time = datetime.strptime(publish_time_str, "%Y-%m-%dT%H:%M:%SZ")
    return publish_time.strftime("%H:%M:%S %d-%m-%Y")

# Hàm tính thời gian ước chừng từ hiện tại
def time_since_publish(publish_time_str):
    publish_time = datetime.strptime(publish_time_str, "%Y-%m-%dT%H:%M:%SZ")
    time_diff = datetime.utcnow() - publish_time

    if time_diff < timedelta(minutes=1):
        return "vừa xong"
    elif time_diff < timedelta(hours=1):
        minutes = int(time_diff.total_seconds() // 60)
        return f"{minutes} phút trước"
    elif time_diff < timedelta(days=1):
        hours = int(time_diff.total_seconds() // 3600)
        return f"{hours} giờ trước"
    elif time_diff < timedelta(days=30):
        days = time_diff.days
        return f"{days} ngày trước"
    elif time_diff < timedelta(days=365):
        months = time_diff.days // 30
        return f"{months} tháng trước"
    else:
        years = time_diff.days // 365
        return f"{years} năm trước"

def preprocess_subtitles(subtitles, search_terms):
    # Tách các cụm từ tìm kiếm dựa trên dấu phẩy
    phrases = search_terms.split(',')
    
    # Loại bỏ khoảng trắng thừa ở đầu và cuối mỗi phrase
    phrases = [phrase.strip() for phrase in phrases]
    # Danh sách các màu để áp dụng cho mỗi phrase
    colors = [
    "rgb(204, 51, 0)",     # Đỏ cam tối hơn nữa
    "rgb(0, 77, 153)",     # Xanh dương tối hơn nữa
    "rgb(26, 94, 26)",     # Xanh lá tối hơn nữa
    "rgb(184, 77, 91)",    # Hồng tối hơn nữa
    "rgb(204, 102, 0)",    # Cam tối hơn nữa
    "rgb(51, 0, 102)"      # Tím tối hơn nữa
    ]
    # Tạo một từ điển để lưu số lần khớp cho mỗi cụm từ
    match_counts = {}
    phrase_colors = {}
    for i, phrase in enumerate(phrases):
        # Tìm tất cả các cụm từ trong phụ đề (không phân biệt chữ hoa chữ thường)
        matches = re.findall(re.escape(phrase), subtitles, flags=re.IGNORECASE)
        count = len(matches)
        
        # Cập nhật từ điển với số lần khớp
        match_counts[phrase] = count
        
        # Áp dụng màu từ danh sách, dùng modulo để lặp lại nếu hết màu
        color = colors[i % len(colors)]
        phrase_colors[phrase] = color
        
        # Highlight các cụm từ trong phụ đề, giữ nguyên định dạng chữ
        subtitles = re.sub(
            re.escape(phrase),
            lambda m: f'<span style="background-color: {color}; font-weight: bold;">{m.group(0)}</span>',
            subtitles,
            flags=re.IGNORECASE
        )
    return subtitles, match_counts, phrase_colors

# Bộ dữ liệu
data = [ ]
def get_subtitles(id):
    subtitles_url = url+ f"/get_subtitle_by_id?id={id}"
    response = requests.post(subtitles_url)
    return response.json()['subtitle']

@st.dialog('SHOW VIDEO YOUTUBE',width=1920)
def show_video(video_url):
    st.video(video_url, loop=False, autoplay=True, muted=False)

# Hàm tìm kiếm video
def search_videos(query):
    data = {
        "paragraph": query,
            }
    response = requests.post(url+"/get_main_search", json=data)
    results = response.json()  
    # Lấy dữ liệu kết quả và thời gian tải
    len = results.get("len",0)
    videos = results.get("result", [])
    time_load = results.get("time_load", 0)
    time_search = results.get("time_search", 0)
    return  time_load, time_search,len,videos



# Hàm để lưu kết quả tìm kiếm vào session_state
def update_search_history(results):   
    # Lưu kết quả tìm kiếm vào lịch sử, giữ tối đa 10 mục
    st.session_state.history.insert(0, results)  # Thêm vào đầu danh sách
    if len(st.session_state.history) > 10:
        st.session_state.history.pop() 
    collection.update_one({"_id": st.session_state.id}, {"$set": {"history":st.session_state.history}})
    

def click_button():   
    st.session_state.account = False
    search_data = search_videos(st.session_state.query) 
    if search_data[0]:
        st.session_state.search_triggered = True
        st.session_state.time_load, st.session_state.time_search, st.session_state.len_results,st.session_state.search_results  = search_data
        st.session_state.info = (st.session_state.query,st.session_state.time_load, st.session_state.time_search, st.session_state.len_results,st.session_state.search_results)
        update_search_history(st.session_state.info)
    else:
        st.session_state.search_triggered = False
        st.session_state.show_404 = True
        print(st.session_state.show_404)

def download_subtitles(subtitles, filename):
    st.download_button(
        label="📩",
        data=subtitles,
        file_name=filename,
        mime="text/plain"
    )


def delete_history_item(index):
    if 'history' in st.session_state:
        del st.session_state.history[index]

def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.03)

def stream_data_login():
    for word in _LOREM_IPSUM_LOGIN.split(" "):
        yield word + " "
        time.sleep(0.03)
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#### giao diện đăng nhập
if not st.session_state.logged_in:
    if not st.session_state.create_user:
        # Tạo giao diện đăng nhập
        st.sidebar.markdown(
        """
        <h2 style='display: flex; align-items: center;'>
            <img src='https://media.giphy.com/media/HMdPmZ6wwlo0idI2PH/giphy.gif' 
            width='50' height='50' style='margin-right: 0px;'/> 
            <span style='font-weight: bold; width: 100%;'>ĐĂNG NHẬP</span>
        </h2>
        """, 
        unsafe_allow_html=True)

        username = st.sidebar.text_input("Tên đăng nhập")
        password = st.sidebar.text_input("Mật khẩu", type="password")

        # Quên mật khẩu
        st.sidebar.markdown(
            f'<a href="https://web.facebook.com/profile.php?id=100090786036344" target="_blank">Quên mật khẩu?</a>',
            unsafe_allow_html=True,
        )

        # Tạo hàng các nút "Đăng nhập", "Tạo tài khoản", "Đăng nhập với tư cách khách"
        if st.sidebar.button("Đăng nhập"):
            user = collection.find_one({"username": username, "password": password })
            if user:
                st.sidebar.success("Đăng nhập thành công!")
                st.session_state.id = user['_id']
                st.session_state.username = user['username']
                st.session_state.password = user['password']
                time.sleep(0.1)
                st.session_state.history = user['history']

                st.session_state.logged_in = True
                st.rerun()
            else:
                st.sidebar.error("Tên đăng nhập hoặc mật khẩu không đúng.")

        
        if st.sidebar.button("Tạo tài khoản"):
            st.session_state.create_user = True       

    else:
        # Code xử lý sau khi đăng nhập với tư cách khách
        new_username = st.sidebar.text_input("Tên đăng nhập mới")
        new_password = st.sidebar.text_input("Mật khẩu mới", type="password")
        confirm_password = st.sidebar.text_input("Xác nhận mật khẩu", type="password")
        if st.sidebar.button("Xác nhận tạo tài khoản"):
            existing_user = collection.find_one({"username": new_username})
            if existing_user:
                st.sidebar.error("Tên đăng nhập đã tồn tại.")
            elif confirm_password ==new_password:
                collection.insert_one({"username": new_username, "password": new_password,"history":[]})
                collection.save_data()
                st.sidebar.success("Tạo tài khoản thành công!, tự động chuyển về đăng nhập sau 3 giây")
                time.sleep(3)
                st.session_state.create_user = False
                st.rerun()
            else:
                st.sidebar.error("Nhập lại mật khẩu sai")
        if st.sidebar.button("Quay lại"):
            st.session_state.create_user = False

    st.sidebar.caption(caption,unsafe_allow_html=True,)
    if st.session_state.show_message_login:
        col1, col2 = st.columns([1,3]) 
        with col1:
            st.markdown(
                """
                <h2 style='display: flex; align-items: center;'>
                    <img src='https://media.giphy.com/media/3owyplYLWlGFQk9mF2/giphy.gif?cid=ecf05e47vlulxckbrh3akfqy8hje45og5qrp42whtigdoh0h&ep=v1_stickers_search&rid=giphy.gif&ct=s' 
                    width='300' height='300' style='margin-right: 0px;'/> 
                </h2>
                """, 
                unsafe_allow_html=True)
        with col2:
            st.write_stream(stream_data_login)
            time.sleep(0.3)

#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################
#############################################################################################################

# Giao diện người dùng Streamlit

    
else:
    # title của cả giao diện
    st.sidebar.markdown(
        """
        <h2 style='display: flex; align-items: center;'>
            <img src='https://media.giphy.com/media/HMdPmZ6wwlo0idI2PH/giphy.gif' 
            width='50' height='50' style='margin-right: 0px;'/> 
            <span style='font-weight: bold; width: 100%;'>YOUTUBE SEARCH</span>
        </h2>
        """, 
        unsafe_allow_html=True)


    st.sidebar.caption(caption,
        unsafe_allow_html=True,
    )

    #text_input ở layout
    st.session_state.query = st.sidebar.text_input("", placeholder="Nhập chuỗi cần tìm...")
    #nút tìm kiếm ở layout
    
    search_button = st.sidebar.button("**Tìm kiếm  🔎**", on_click=click_button)
    st.sidebar.markdown(f"""
        <div class="divider">
            <span>Xin chào {st.session_state.username} </span>
        </div>
        """, unsafe_allow_html=True)
    if st.sidebar.button("**👤 Tài khoản**"):
        st.session_state.account = True
    #đường ranh lịch sử ở layout
    st.sidebar.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <div class="divider">
            <i class="fas fa-history"></i><span> Lịch sử</span>
        </div>
        """, unsafe_allow_html=True)

    # Hiển thị các button trong sidebar với lịch sử tìm kiếm
    if 'history' in st.session_state and st.session_state.history:
        for i, (iquery,iload,itime,ilen, iresult) in enumerate(st.session_state.history):
            if st.sidebar.button(f"🔗{iquery}", key=f"history_{i}"):
                st.session_state.info = (iquery,iload,itime,ilen,iresult)
                st.session_state.search_triggered = True
                st.session_state.account = False
            
    else:
        st.sidebar.text("Chưa có lịch sử tìm kiếm.")

    if st.session_state.account:
        st.session_state.show_animation = False
        st.session_state.show_message = False
        account_info()
    # Sắp xếp dữ liệu theo ngày xuất bản từ mới nhất đến cũ nhất
    elif st.session_state.search_triggered:
        st.session_state.show_animation = False
        st.session_state.show_message = False
        info = st.session_state.info
        if info[4]:

            col1, col2 = st.columns([1,2]) 
            with col1:
                st.write(f'Thời điểm: {info[2]} ')
            with col2:
                st.write(f" Thời gian tìm kiếm '{info[0]}': {info[1]}s")   
            
            ### bảng ngày 
            col1, col2 = st.columns([1,1]) 
            with col1:
                start_date = st.date_input("Ngày bắt đầu🛫", datetime(2023, 1, 1))
            with col2:
                end_date = st.date_input("Ngày kết thúc🛬", datetime.utcnow().date())
            start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            # Lọc kết quả dựa trên thời gian xuất bản
            results_filtered = [item for item in info[4] if start_date_str <= item["Publish Time"] <= end_date_str]
            # results_sorted = sorted(results_filtered, key=lambda x: datetime.strptime(x["Publish Time"], "%Y-%m-%dT%H:%M:%SZ"), reverse=True)
            start_index, end_index = st.slider(
                f"Tìm thấy {info[3]} kết quả ✅",
                min_value=1,
                max_value=100,  # Cần điều chỉnh tối đa theo số lượng video có thể có
                value=(1, 10),  # Giá trị mặc định, bắt đầu từ video 0 đến video 10
                step=1
                )
                 
            st.write(f'Đang hiển thị kết quả từ {start_index} đến {end_index}')
            # Hiển thị số lượng video theo trạng thái hiện tại
            videos_to_display = results_filtered[start_index-1:end_index]

            # Tạo các vùng hiển thị theo hàng ngang
            for idx, item in enumerate(videos_to_display, start=1):
                # Chia bố cục thành hai cột
                num = idx+start_index-1
                st.markdown(f"""
                <div style='text-align: center; '>
                    <hr style='border: 1px solid #555; display: inline-block; width: 2%;'>
                    <span style='position: relative; top: -25px; background: #45434c; color: white; padding: 20px 10px;'>
                        {num}
                    </span>
                    <hr style='border: 1px solid #555; display: inline-block; width: 90%;'>
                </div>
                """, unsafe_allow_html=True)

                col_image, col_info = st.columns([1, 4])  # Tỷ lệ 1:3 để hình ảnh nhỏ hơn
                with col_image:
                    # Hiển thị số thứ tự bên cạnh hình ảnh
                    st.image(get_video_thumbnail(item["Video ID"]), width=250)
                with col_info:
                    video_link = get_video_link(item["Video ID"])
                    publish_time_formatted = format_publish_time(item["Publish Time"])
                    time_since = time_since_publish(item["Publish Time"])

                    st.markdown(f"[**{item['Video Title']}**]({video_link})")

                    # Thêm một hàng ngang để hiển thị Channel và Publish Time
                    sub_col1, sub_col2 = st.columns(2)
                    with sub_col1:
                        st.write(f"**Channel**: {item['Channel']}")
                    with sub_col2:
                        st.write(f"**Publish Time**: {publish_time_formatted}")
                    sub_col1, sub_col2, sub_col3 = st.columns([1, 1, 1])

                    with sub_col1:
                        st.write(f"{time_since}")

                    with sub_col2:
                        subtitle_btn = st.button("Phụ đề 📃", key=item["ID"])

                    with sub_col3:
                        video_btn = st.button("Video 🎞️", key=-item["ID"])

                if subtitle_btn:
                    subtitles = get_subtitles(item["ID"])
                    subtitle,match_counts, phrase_colors = preprocess_subtitles(subtitles,info[0])
                    for phrase, count in match_counts.items():
                        color = phrase_colors[phrase]
                        st.markdown(
                            f"<div style='display: flex; align-items: center; line-height: 1.2; margin-bottom: 5px;'>"
                            f"<span style='display: inline-block; width: 15px; height: 15px; background-color: {color}; margin-right: 5px;'></span>"
                            f"{phrase}: {count} lần"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                    # Kiểm tra nếu từ khóa tìm kiếm không rỗng
                # Hiển thị phụ đề với các từ khóa được tô đậm
                
                    st.markdown(box_style.format(content=subtitle), unsafe_allow_html=True)    
                    download_subtitles(subtitles, f"{item['Video ID']}_{item['Video Title']}.txt")  
                if video_btn:
                    show_video(video_link)
    elif st.session_state.show_404:
        st.session_state.show_animation = False
        st.session_state.show_message = False
        st.markdown(
                """
                <div style='text-align: center; color: red;'>
                    <h1>404 Not Found🙇‍♂️🙇‍♀️🙇</h1>
                    <h2>Không tìm thấy kết quả</h2>
                    <h2>
                        <img src='https://media.giphy.com/media/EEFEyXLO9E0YE/giphy.gif?cid=ecf05e479mjja9dt8wwd2pujiwbo57vccfpr2r7adwlqb6za&ep=v1_stickers_search&rid=giphy.gif&ct=s' 
                        width='500' height='500' style='margin-right: 0px;'/> 
                    </h2>
                    <p>Xin lỗi, chúng tôi không thể tìm thấy kết quả cho từ khóa bạn đã nhập.</p>
                </div>
                """,
                unsafe_allow_html=True
        )


    # if "has_snowed" not in st.session_state:
    #     st.snow()
    #     st.session_state["has_snowed"] = True
    # giao diện chào hỏi
    if st.session_state.show_message:
        col1, col2 = st.columns([1,3]) 
        with col1:
            st.markdown(
                """
                <h2 style='display: flex; align-items: center;'>
                    <img src='https://media.giphy.com/media/n1mrBUduOjxgLOpysu/giphy.gif' 
                    width='300' height='300' style='margin-right: 0px;'/> 
                </h2>
                """, 
                unsafe_allow_html=True)
        with col2:
            col1, col2 = st.columns([1,3]) 
            with col1:
                if st.button("Video hướng dẫn sử dụng"):
                    show_video("https://www.youtube.com/watch?v=VvvXhNbFWKY")
            with col2:
                st.markdown(
                """
                <h2 style='display: flex; align-items: center;'>
                    <img src='https://media.giphy.com/media/iiesjj8ognaX77Qr50/giphy.gif' 
                    width='500' height='30' style='margin-right: 0px;'/> 
                </h2>
                """, 
                unsafe_allow_html=True)
            st.write_stream(stream_data)
            time.sleep(0.3)
            

    particles_js = """<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Particles.js</title>
    <style>
    #particles-js {
        position: fixed;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: -1; /* Send the animation to the back */
    }
    .content {
        position: relative;
        z-index: 1;
        color: white;
    }
    
    </style>
    </head>
    <body>
    <div id="particles-js"></div>
    <div class="content">
        <!-- Placeholder for Streamlit content -->
    </div>
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    <script>
        particlesJS("particles-js", {
        "particles": {
            "number": {
            "value": 300,
            "density": {
                "enable": true,
                "value_area": 800
            }
            },
            "color": {
            "value": "#ffffff"
            },
            "shape": {
            "type": "circle",
            "stroke": {
                "width": 0,
                "color": "#000000"
            },
            "polygon": {
                "nb_sides": 5
            },
            "image": {
                "src": "img/github.svg",
                "width": 100,
                "height": 100
            }
            },
            "opacity": {
            "value": 0.5,
            "random": false,
            "anim": {
                "enable": false,
                "speed": 5,
                "opacity_min": 0.2,
                "sync": false
            }
            },
            "size": {
            "value": 2,
            "random": true,
            "anim": {
                "enable": false,
                "speed": 400,
                "size_min": 0.1,
                "sync": false
            }
            },
            "line_linked": {
            "enable": true,
            "distance": 100,
            "color": "#ffffff",
            "opacity": 0.22,
            "width": 1
            },
            "move": {
            "enable": true,
            "speed": 2,
            "direction": "none",
            "random": false,
            "straight": false,
            "out_mode": "out",
            "bounce": true,
            "attract": {
                "enable": false,
                "rotateX": 600,
                "rotateY": 1200
            }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
            "onhover": {
                "enable": true,
                "mode": "grab"
            },
            "onclick": {
                "enable": true,
                "mode": "repulse"
            },
            "resize": true
            },
            "modes": {
            "grab": {
                "distance": 100,
                "line_linked": {
                "opacity": 1
                }
            },
            "bubble": {
                "distance": 400,
                "size": 2,
                "duration": 2,
                "opacity": 0.5,
                "speed": 1
            },
            "repulse": {
                "distance": 200,
                "duration": 0.4
            },
            "push": {
                "particles_nb": 2
            },
            "remove": {
                "particles_nb": 3
            }
            }
        },
        "retina_detect": true
        });
    </script>
    </body>
    </html>
    """
    if st.session_state.show_animation:
        components.html(particles_js, height=370, scrolling=False)