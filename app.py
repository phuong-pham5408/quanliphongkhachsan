import streamlit as st
import pandas as pd
from datetime import datetime, date, time

# Config trang
st.set_page_config(
    page_title="L'Aura Fine Dining | Nhà Hàng 5 Sao",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho phong cách Nhà hàng 5 sao (Dark & Gold Theme)
st.markdown("""
    <style>
        /* Base Styling */
        .main {
            background-color: #0E0E10;
            color: #F1F1F1;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        
        /* Gold Text Gradient */
        .gold-header {
            background: linear-gradient(135deg, #DFAC6C 0%, #C68B59 50%, #E8D0B5 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            text-align: center;
            letter-spacing: 2px;
        }
        
        /* Subtitle Styling */
        .gold-subtitle {
            color: #DFAC6C;
            text-align: center;
            font-style: italic;
            letter-spacing: 1px;
            margin-bottom: 25px;
        }

        /* Cards */
        .luxury-card {
            background: #1A1A1E;
            border: 1px solid #2D2B2A;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            transition: transform 0.3s ease;
        }
        
        /* Custom Buttons */
        .stButton>button {
            background: linear-gradient(135deg, #C68B59 0%, #AA7243 100%);
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            letter-spacing: 1px;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #DFAC6C 0%, #C68B59 100%);
            color: #000000;
            box-shadow: 0 0 12px rgba(223, 172, 108, 0.5);
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #141416;
            border-right: 1px solid #2D2B2A;
        }

        /* Metric Styling */
        [data-testid="stMetricValue"] {
            color: #DFAC6C !important;
        }

        /* Divider */
        hr {
            border-color: #2D2B2A !important;
        }
    </style>
""", unsafe_style_color=True)

# Khởi tạo Session State cho giỏ hàng và danh sách đặt bàn
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'reservations' not in st.session_state:
    st.session_state.reservations = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# Dữ liệu thực đơn
MENU_DATA = {
    "Món Khai Vị": [
        {
            "id": "f1",
            "name": "Gan Ngỗng Áp Chảo (Foie Gras)",
            "desc": "Gan ngỗng Pháp áp chảo, mứt fig ngọt dịu, xốt giảm bớt béo thơm lừng và bánh mì Brioche.",
            "price": 950000,
            "img": "https://images.unsplash.com/photo-1582170327334-a08ce1eefb59?q=80&w=800&auto=format&fit=crop"
        },
        {
            "id": "f2",
            "name": "Sò Điệp Hokkaido Trứng Cá Caviar",
            "desc": "Sò điệp Hokkaido áp chảo bơ tỏi, kem bơ chanh và trứng cá tầm Caviar cao cấp.",
            "price": 850000,
            "img": "https://images.unsplash.com/photo-1626200926732-44675b3fd4b6?q=80&w=800&auto=format&fit=crop"
        }
    ],
    "Món Chính": [
        {
            "id": "f3",
            "name": "Bò Wagyu A5 Miyazaki Steak",
            "desc": "Thăn ngoại bò Wagyu A5 nướng than hoa, dùng kèm nấm Truffle đen và xốt rượu vang đỏ Bordeaux.",
            "price": 2800000,
            "img": "https://images.unsplash.com/photo-1544025162-8111f4a76154?q=80&w=800&auto=format&fit=crop"
        },
        {
            "id": "f4",
            "name": "Tôm Hùm Thermidor Đút Lò",
            "desc": "Tôm hùm Alaska đút lò sốt kem phô mai Gruyère, nấm tôm và măng tây hấp.",
            "price": 1950000,
            "img": "https://images.unsplash.com/photo-1625937751876-4515cd8e78db?q=80&w=800&auto=format&fit=crop"
        }
    ],
    "Tráng Miệng": [
        {
            "id": "f5",
            "name": "Bánh Chocolate Lava Vàng 24K",
            "desc": "Socola Bỉ chảy kem tươi vanilla Bourbon Madagascar, phủ lá vàng 24K nguyên chất.",
            "price": 450000,
            "img": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?q=80&w=800&auto=format&fit=crop"
        }
    ],
    "Rượu & Thức Uống": [
        {
            "id": "d1",
            "name": "Château Margaux 2015 (Chai)",
            "desc": "Rượu vang đỏ thượng hạng xứ Bordeaux, vị đượm sâu thanh lịch.",
            "price": 12500000,
            "img": "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?q=80&w=800&auto=format&fit=crop"
        },
        {
            "id": "d2",
            "name": "L'Aura Golden Signature Cocktail",
            "desc": "Sự pha trộn giữa Single Malt Scotch, syrup hoa sâm ngọc linh và bụi vàng 24k.",
            "price": 550000,
            "img": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=800&auto=format&fit=crop"
        }
    ]
}

def format_price(amount):
    return f"{amount:,.0f} ₫".replace(",", ".")

# Hàm quản lý giỏ hàng
def add_to_cart(item):
    for cart_item in st.session_state.cart:
        if cart_item["id"] == item["id"]:
            cart_item["quantity"] += 1
            st.toast(f"Đã tăng số lượng '{item['name']}' trong giỏ!", icon="🥂")
            return
    st.session_state.cart.append({**item, "quantity": 1})
    st.toast(f"Đã thêm '{item['name']}' vào giỏ hàng!", icon="✨")

# Sidebar - Điều hướng chính
with st.sidebar:
    st.markdown("<h1 class='gold-header'>L'AURA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 13px;'>FINE DINING & LOUNGE</p>", unsafe_allow_html=True)
    st.divider()

    menu_option = st.radio(
        "Danh mục điều hướng",
        ["🏛️ Giới Thiệu", "🍽️ Thực Đơn & Gọi Món", "📅 Đặt Bàn", "🛍️ Giỏ Hàng & Thanh Toán", "📞 Liên Hệ"],
        index=0
    )

    st.divider()
    
    # Hiển thị tóm tắt giỏ hàng
    total_cart_items = sum(item["quantity"] for item in st.session_state.cart)
    st.metric(label="Món ăn đã chọn", value=f"{total_cart_items} món")

# --- TRANG 1: GIỚI THIỆU ---
if menu_option == "🏛️ Giới Thiệu":
    st.markdown("<h1 class='gold-header'>L'AURA FINE DINING</h1>", unsafe_allow_html=True)
    st.markdown("<p class='gold-subtitle'>Đánh Thức Giác Quan - Nâng Tầm Ẩm Thực</p>", unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=1600&auto=format&fit=crop", use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='luxury-card' style='text-align: center;'>
            <h3 style='color: #DFAC6C;'>3 SAO MICHELIN</h3>
            <p style='color: #AAA;'>Khẳng định đẳng cấp thế giới với đội ngũ siêu đầu bếp quốc tế.</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='luxury-card' style='text-align: center;'>
            <h3 style='color: #DFAC6C;'>KHÔNG GIAN THƯỢNG LƯU</h3>
            <p style='color: #AAA;'>Tầm nhìn Panorama ôm trọn thành phố từ tầng cao nhất.</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='luxury-card' style='text-align: center;'>
            <h3 style='color: #DFAC6C;'>RƯỢU VANG BỘ BỘT</h3>
            <p style='color: #AAA;'>Bộ sưu tập hơn 500 dòng vang quý hiếm trên khắp thế giới.</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Về Chúng Tôi")
    st.write("""
    Nằm ở trái tim thành phố, **L'AURA** mang lại trải nghiệm ẩm thực đỉnh cao với phong cách kiến trúc tân cổ điển châu Âu kết hợp vẻ hiện đại sang trọng. 
    Mỗi món ăn tại đây không chỉ là một khẩu phần thưởng thức mà là một tác phẩm nghệ thuật được chăm chút tỉ mỉ từ nguyên liệu tươi ngon bậc nhất.
    """)

# --- TRANG 2: THỰC ĐƠN & GOI MÓN ---
elif menu_option == "🍽️ Thực Đơn & Gọi Món":
    st.markdown("<h1 class='gold-header'>THỰC ĐƠN HẢO HẠNG</h1>", unsafe_allow_html=True)
    st.markdown("<p class='gold-subtitle'>Trải Nghiệm Những Hương Vị Đột Phá</p>", unsafe_allow_html=True)

    category = st.tabs(list(MENU_DATA.keys()))

    for idx, (cat_name, items) in enumerate(MENU_DATA.items()):
        with category[idx]:
            for item in items:
                col_img, col_info, col_btn = st.columns([1.2, 2.5, 1])
                with col_img:
                    st.image(item["img"], use_container_width=True)
                with col_info:
                    st.markdown(f"### {item['name']}")
                    st.write(item["desc"])
                    st.markdown(f"**Giá:** <span style='color: #DFAC6C; font-size: 18px; font-weight: bold;'>{format_price(item['price'])}</span>", unsafe_allow_html=True)
                with col_btn:
                    st.write("")
                    st.write("")
                    if st.button("➕ Chọn Món", key=f"btn_{item['id']}"):
                        add_to_cart(item)
                st.divider()

# --- TRANG 3: ĐẶT BÀN ---
elif menu_option == "📅 Đặt Bàn":
    st.markdown("<h1 class='gold-header'>ĐẶT BÀN TRƯỚC</h1>", unsafe_allow_html=True)
    st.markdown("<p class='gold-subtitle'>Chuẩn Bị Cho Buổi Tiệc Hoàn Hảo Của Bạn</p>", unsafe_allow_html=True)

    with st.form("reservation_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Họ và Tên (*)")
            phone = st.text_input("Số Điện Thoại (*)")
            res_date = st.date_input("Ngày Đặt", min_value=date.today())
        with col2:
            guests = st.number_input("Số Khách", min_value=1, max_value=20, value=2)
            res_time = st.time_input("Giờ Đặt", value=time(19, 0))
            area = st.selectbox("Khu Vực Ưu Tiên", ["Sảnh Chính (Main Hall)", "Phòng VIP Riêng Tư", "Góc Cửa Sổ Ngắm Băng Đăng", "Tầng Thượng Lounge"])

        notes = st.text_area("Yêu Cầu Đặc Biệt (Ví dụ: Sinh nhật, Kỷ niệm ngày cưới, Dị ứng thực phẩm...)")
        
        submitted = st.form_submit_button("👑 XÁC NHẬN ĐẶT BÀN")

        if submitted:
            if not full_name or not phone:
                st.error("Vui lòng điền đầy đủ Họ tên và Số điện thoại!")
            else:
                res_code = f"LAURA-{datetime.now().strftime('%d%m%Y%H%M%S')}"
                st.session_state.reservations.append({
                    "code": res_code,
                    "name": full_name,
                    "phone": phone,
                    "date": str(res_date),
                    "time": str(res_time),
                    "guests": guests,
                    "area": area,
                    "notes": notes
                })
                st.success(f"Đặt bàn thành công! Mã xác nhận của quý khách là: **{res_code}**")
                st.info("Nhân viên chăm sóc khách hàng L'Aura sẽ gọi điện xác nhận trong vòng 15 phút.")

# --- TRANG 4: GIỎ HÀNG & THANH TOÁN ---
elif menu_option == "🛍️ Giỏ Hàng & Thanh Toán":
    st.markdown("<h1 class='gold-header'>ĐƠN HÀNG CỦA BẠN</h1>", unsafe_allow_html=True)
    st.markdown("<p class='gold-subtitle'>Kiểm Tra Món Ăn & Thanh Toán Trực Tuyến</p>", unsafe_allow_html=True)

    if not st.session_state.cart:
        st.warning("Giỏ hàng của bạn đang trống! Hãy sang mục 'Thực Đơn' để chọn món.")
    else:
        cart_df = []
        total_amount = 0

        for idx, item in enumerate(st.session_state.cart):
            item_total = item["price"] * item["quantity"]
            total_amount += item_total
            cart_df.append({
                "Tên Món": item["name"],
                "Đơn Giá": format_price(item["price"]),
                "Số Lượng": item["quantity"],
                "Thành Tiền": format_price(item_total)
            })

        st.table(pd.DataFrame(cart_df))

        col_left, col_right = st.columns([2, 1])

        with col_right:
            st.markdown(f"### Tổng Cộng: <span style='color: #DFAC6C;'>{format_price(total_amount)}</span>", unsafe_allow_html=True)
            if st.button("🗑️ Xóa Sạch Giỏ Hàng"):
                st.session_state.cart = []
                st.rerun()

        with col_left:
            st.subheader("Phương Thức Thanh Toán")
            pay_method = st.radio(
                "Chọn hình thức thanh toán",
                ["Thanh toán qua Ví MoMo / ZaloPay", "Chuyển khoản Ngân hàng (QR Code)", "Thanh toán trực tiếp tại nhà hàng"]
            )

            if pay_method == "Chuyển khoản Ngân hàng (QR Code)":
                st.info("Mã QR Thanh Toán Tự Động:")
                # Mô phỏng QR Code VietQR
                st.image("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=LAURA-RESTAURANT-PAYMENT", width=200)

            if st.button("💳 XÁC NHẬN THANH TOÁN"):
                order_id = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.session_state.orders.append({
                    "order_id": order_id,
                    "items": st.session_state.cart,
                    "total": total_amount,
                    "payment_method": pay_method
                })
                st.session_state.cart = []
                st.balloons()
                st.success(f"Thanh toán thành công! Mã đơn hàng: **{order_id}**. Cảm ơn quý khách!")

# --- TRANG 5: LIÊN HỆ ---
elif menu_option == "📞 Liên Hệ":
    st.markdown("<h1 class='gold-header'>LIÊN HỆ & VỊ TRÍ</h1>", unsafe_allow_html=True)
    st.markdown("<p class='gold-subtitle'>Luôn Sẵn Sàng Phục Vụ Quý Khách</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### Thông Tin Nhà Hàng
        * **ĐịA chỉ:** Tầng 68, Bitexco Financial Tower, Quận 1, TP. Hồ Chí Minh
        * **Hotline Đặt Bàn:** 1900 888 999 - 0909 123 456
        * **Email:** reservation@laurafinedining.com
        * **Giờ mở cửa:** 
            * Trưa: 11:30 - 14:30
            * Tối: 18:00 - 23:00
        """)
    with col2:
        st.markdown("### Vị Trí Trên Bản Đồ")
        st.map(pd.DataFrame({'lat': [10.771550], 'lon': [106.704221]}))
