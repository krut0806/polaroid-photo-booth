import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import datetime


st.set_page_config(page_title=" Polaroid Photo Booth", layout="centered")
st.title("Polaroid Photo Booth")


layout_option = st.selectbox("Choose strip layout:", ["4 Vertical", "6 Vertical", "2x3 Grid"])

if layout_option == "4 Vertical":
    num_photos = 4
    cols, rows = 1, 4
elif layout_option == "6 Vertical":
    num_photos = 6
    cols, rows = 1, 6
else:
    num_photos = 6
    cols, rows = 3, 2




if "photos" not in st.session_state or len(st.session_state.photos) != num_photos:
    st.session_state.photos = [None] * num_photos


filters = ["None", "Black & White", "Sepia"]


def apply_filter(img: Image.Image, filter_name: str) -> Image.Image:
    if filter_name == "Black & White":
        return img.convert("L").convert("RGB")
    elif filter_name == "Sepia":
        bw = img.convert("L")
        return ImageOps.colorize(bw, "#704214", "#C0A080")
    return img


def add_polaroid_frame(img: Image.Image, caption: str) -> Image.Image:
    border_top, border_sides, border_bottom = 20, 20, 60  # Polaroid proportions
    new_w = img.width + 2 * border_sides
    new_h = img.height + border_top + border_bottom
    framed = Image.new("RGB", (new_w, new_h), "white")
    framed.paste(img, (border_sides, border_top))

    draw = ImageDraw.Draw(framed)
    try:
        font = ImageFont.truetype("arial.ttf", size=20)
    except:
        font = ImageFont.load_default()
    text_width = draw.textlength(caption, font=font)
    text_x = (new_w - text_width) // 2
    text_y = img.height + border_top + 10
    draw.text((text_x, text_y), caption, fill="black", font=font)

    return framed


st.write("### Upload or Take Photos")
for i in range(num_photos):
    st.markdown(f"#### Photo {i+1}")
    col1, col2 = st.columns(2)
    img = None

    with col1:
        uploaded = st.file_uploader("Upload", type=["png", "jpg", "jpeg"], key=f"upload_{i}")
        if uploaded:
            img = Image.open(uploaded).resize((300, 400))

    with col2:
        cap = st.camera_input("Or take a photo", key=f"camera_{i}")
        if cap:
            img = Image.open(cap).resize((300, 400))

    filter_choice = st.selectbox(f"Filter for Photo {i+1}", filters, key=f"filter_{i}")
    if img:
        img = apply_filter(img, filter_choice)
        caption = datetime.datetime.now().strftime("%B %d, %Y")
        final = add_polaroid_frame(img, caption)
        st.session_state.photos[i] = final
        st.image(final, caption=f"Preview {i+1}", width=250)


if st.button(" Generate Photo Strip [:-)]"):
    if all(p is not None for p in st.session_state.photos):
        w, h = st.session_state.photos[0].size
        spacing = 20

        if layout_option == "2x3 Grid":
            strip_w = cols * w + (cols - 1) * spacing
            strip_h = rows * h + (rows - 1) * spacing
            strip = Image.new("RGB", (strip_w, strip_h), "white")
            for r in range(rows):
                for c in range(cols):
                    idx = r * cols + c
                    x = c * (w + spacing)
                    y = r * (h + spacing)
                    strip.paste(st.session_state.photos[idx], (x, y))
        else:
            strip_w = w
            strip_h = h * num_photos + spacing * (num_photos - 1)
            strip = Image.new("RGB", (strip_w, strip_h), "white")
            for i, p in enumerate(st.session_state.photos):
                strip.paste(p, (0, i * (h + spacing)))

        st.image(strip, caption="Here is your final strip ", use_container_width=True)

        buf = io.BytesIO()
        strip.save(buf, format="PNG")
        st.download_button(" Download Strip", buf.getvalue(), "photo_strip.png", "image/png")
    else:
        st.warning("Please make sure you've added all photos.")
