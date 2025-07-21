# polaroid-photo-booth
A web-based photo booth that captures real-time polaroid-style photo strips. Choose your layout, apply retro filters, add captions or auto date stamps, and download a clean printable strip — all from your browser.


## Features:

- **Upload or Take Photos Live** (via webcam)
- Apply filters:  
  - None  
  - Black & White  
  - Sepia  
  - (More filters can be added easily!)
-  Choose Layout:
  - 4 Vertical
  - 6 Vertical
  - 2x3 Grid
- Each photo has a **polaroid-style white border**
-  Automatically adds **current date** below each photo
-  Download your final photo strip as an image

---

## How to Run It Locally

 1. Clone the repo

git clone https://github.com/krut0806/polaroid-photo-booth.git
cd photo-booth

2. Create and activate a virtual environment
source venv/bin/activate 

3. Install dependencies
pip install -r requirements.txt

4.Run the Streamlit app
streamlit run photo_booth.py



