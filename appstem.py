import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Cấu hình trang
st.set_page_config(
    page_title="STEM: Thiết kế sân thể thao tối ưu",
    layout="wide",
    page_icon="🏟️"
)

# CSS giao diện
st.markdown("""
<style>
.main {
    background-color: #f5f7f9;
}
h1 {
    color: #1E3A8A;
}
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.header("⚙️ Cấu hình thiết kế")

    P = st.number_input(
        "Nhập tổng chu vi sân (m):",
        min_value=10,
        max_value=500,
        value=100
    )

    st.info("Chu vi thường phụ thuộc vào kinh phí làm hàng rào.")

    L_test = st.slider(
        "Điều chỉnh chiều dài L (m)",
        1.0,
        P/2 - 1.0,
        P/4
    )

    W_test = P/2 - L_test
    S_test = L_test * W_test

# ===== TIÊU ĐỀ =====
st.title("🏟️ Ứng dụng Thiết kế Sân Thể thao Tối ưu")
st.caption("Dự án STEM - Trường THCS Trưng Vương | Năm học 2025-2026")

# ===== TABS =====
tab1, tab2, tab3 = st.tabs([
    "📊 Mô phỏng & Tối ưu",
    "📖 Cơ sở khoa học",
    "💰 Dự toán chi phí"
])

# ===== TAB 1 =====
with tab1:

    L_opt = P / 4
    S_max = L_opt ** 2

    col1, col2, col3 = st.columns(3)

    col1.metric("Chiều dài (L)", f"{L_test:.2f} m")
    col2.metric("Chiều rộng (W)", f"{W_test:.2f} m")
    col3.metric(
        "Diện tích hiện tại",
        f"{S_test:.2f} m²",
        delta=f"{S_test - S_max:.2f} m² so với tối ưu"
    )

    if abs(S_test - S_max) < 1:
        st.success("🎯 Kích thước gần đạt tối ưu (gần hình vuông)")
    else:
        st.warning("⚠️ Kích thước chưa đạt diện tích tối đa")

    c1, c2 = st.columns(2)

# ===== ĐỒ THỊ =====
    with c1:
        st.subheader("Đồ thị biến thiên diện tích")

        x = np.linspace(0, P/2, 200)
        y = x * (P/2 - x)

        fig, ax = plt.subplots()

        ax.plot(x, y, label="Diện tích", color="blue")

        ax.scatter(
            [L_test],
            [S_test],
            color="orange",
            s=100,
            label="Kích thước đang chọn"
        )

        ax.scatter(
            [L_opt],
            [S_max],
            color="red",
            marker="*",
            s=200,
            label="Điểm tối ưu"
        )

        ax.set_xlabel("Chiều dài L (m)")
        ax.set_ylabel("Diện tích S (m²)")
        ax.legend()

        st.pyplot(fig)

# ===== MÔ HÌNH SÂN =====
    with c2:
        st.subheader("Mô hình sân")

        fig2, ax2 = plt.subplots()

        rect = plt.Rectangle(
            (0, 0),
            L_test,
            W_test,
            color="green",
            alpha=0.6
        )

        ax2.add_patch(rect)

        ax2.set_xlim(0, L_test * 1.2)
        ax2.set_ylim(0, W_test * 1.2)

        ax2.set_aspect("equal")

        plt.title(f"Sân: {L_test:.1f}m × {W_test:.1f}m")

        st.pyplot(fig2)

# ===== TAB 2 =====
with tab2:

    st.subheader("Chứng minh toán học")

    st.latex(r"S = L \times W")

    st.latex(r"P = 2(L + W)")

    st.latex(r"W = \frac{P}{2} - L")

    st.latex(r"S = L(\frac{P}{2} - L)")

    st.latex(r"S = -\left(L - \frac{P}{4}\right)^2 + \frac{P^2}{16}")

    st.success(
        f"Diện tích lớn nhất khi L = P/4 = {L_opt:.2f} m (sân trở thành hình vuông)"
    )

# ===== TAB 3 =====
with tab3:

    st.subheader("Dự toán chi phí")

    gia_co = st.number_input(
        "Giá cỏ nhân tạo (VNĐ/m²):",
        min_value=10000,
        value=150000
    )

    tong_tien = S_test * gia_co

    st.write(f"### 💵 Tổng chi phí lát cỏ: {tong_tien:,.0f} VNĐ")
