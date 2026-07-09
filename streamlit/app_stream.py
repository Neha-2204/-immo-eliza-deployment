import streamlit as st
import requests
from PIL import Image

st.set_page_config(page_title="Real Estate Price Predictor", page_icon="🏠", layout="centered")

API_URL = "https://immo-eliza-api-ocrq.onrender.com/predict"

# --- Design tokens ---
# Deep slate-teal (trust, finance) + muted brass (value, estate) on a warm
# paper background. Serif display face for the header, clean sans for body.
COLOR_PRIMARY = "#1F3A3D"      # deep slate-teal
COLOR_PRIMARY_DARK = "#152A2C"
COLOR_ACCENT = "#B08D57"       # muted brass
COLOR_BG = "#F4F5F1"           # warm paper
COLOR_CARD = "#FFFFFF"
COLOR_BORDER = "#E4E1D8"
COLOR_TEXT = "#26261F"
COLOR_MUTED = "#6E6C61"
COLOR_SIDEBAR = "#1F3A3D"      # sidebar background (slate-teal)
COLOR_SIDEBAR_TEXT = "#F4F5F1"
COLOR_EXPANDER_BG = "#EFE8D8"  # soft brass-tinted box for the optional-details expander

# --- Custom styling ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {COLOR_TEXT};
    }}

    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background-color: {COLOR_BG};
    }}
    [data-testid="stHeader"] {{
        background-color: transparent;
    }}

    /* Tighten the top padding of the page. */
    .block-container {{
        padding-top: 1.5rem;
    }}

    /* Banner image (main content only) — cap the height so it doesn't
       dominate the viewport on load, and crop it to fill that height. */
    [data-testid="stMain"] [data-testid="stImage"] img,
    .main [data-testid="stImage"] img {{
        max-height: 260px;
        width: 100%;
        object-fit: cover;
        border-radius: 10px;
    }}
    [data-testid="stMain"] [data-testid="stImage"],
    .main [data-testid="stImage"] {{
        margin-bottom: 0.5rem;
    }}

    /* Sidebar image — keep its own spacing separate from the banner rule
       above, so "About" isn't crammed against the photo. */
    [data-testid="stSidebar"] [data-testid="stImage"] {{
        margin-bottom: 1rem;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {COLOR_SIDEBAR};
    }}
    [data-testid="stSidebar"] * {{
        color: {COLOR_SIDEBAR_TEXT} !important;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(244,245,241,0.25);
    }}

    /* Header */
    .main-header {{
        border-top: 3px solid {COLOR_ACCENT};
        border-bottom: 1px solid {COLOR_BORDER};
        padding: 1.75rem 0 1.5rem 0;
        text-align: center;
        margin-bottom: 2rem;
    }}
    .main-header h1 {{
        font-family: 'Libre Baskerville', serif;
        color: {COLOR_PRIMARY};
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.2px;
    }}
    .main-header p {{
        color: {COLOR_MUTED};
        font-size: 0.95rem;
        margin-top: 0.4rem;
        font-style: italic;
    }}

    /* Cards */
    .card {{
        background: {COLOR_CARD};
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        border-radius: 6px;
        border: 1px solid {COLOR_BORDER};
        margin-bottom: 1.5rem;
    }}

    /* Real Streamlit container (st.container(border=True)) styled to match
       the .card look above — this one actually wraps its contents, unlike
       a <div> injected via st.markdown across multiple calls. */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: {COLOR_CARD};
        border-radius: 6px;
        border: 1px solid {COLOR_BORDER} !important;
    }}
    .card h3 {{
        margin-top: 0;
        font-family: 'Libre Baskerville', serif;
        font-size: 1.15rem;
        color: {COLOR_PRIMARY};
        font-weight: 700;
    }}

    /* Section labels */
    .section-label {{
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.75rem;
        color: {COLOR_MUTED};
        font-weight: 600;
        margin-bottom: 0.25rem;
    }}

    .required-note {{
        font-size: 0.8rem;
        color: {COLOR_MUTED};
        margin-top: -0.5rem;
        margin-bottom: 1rem;
    }}
    .required-note span {{
        color: {COLOR_ACCENT};
        font-weight: 700;
    }}

    /* Optional-details expander styled as a colored box */
    [data-testid="stExpander"] {{
        background: {COLOR_EXPANDER_BG};
        border: 1px solid {COLOR_ACCENT};
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }}
    [data-testid="stExpander"] summary {{
        font-weight: 600;
        color: {COLOR_PRIMARY};
    }}
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
        background: {COLOR_EXPANDER_BG};
        border-radius: 0 0 8px 8px;
        padding: 0.5rem 0.5rem 1rem 0.5rem;
    }}

    /* Buttons */
    div.stButton > button {{
        background: {COLOR_PRIMARY};
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.7rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: background 0.15s ease;
    }}
    div.stButton > button:hover {{
        background: {COLOR_PRIMARY_DARK};
        color: white;
    }}

    /* Result panel */
    .price-result {{
        background: {COLOR_PRIMARY};
        padding: 2rem;
        border-radius: 6px;
        text-align: center;
        margin-top: 1.5rem;
        border-left: 4px solid {COLOR_ACCENT};
    }}
    .price-result p {{
        color: rgba(255,255,255,0.75);
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.8rem;
    }}
    .price-result h2 {{
        font-family: 'Libre Baskerville', serif;
        color: white;
        font-size: 2.4rem;
        margin: 0.3rem 0 0 0;
    }}

    footer {{visibility: hidden;}}
    .footer-note {{
        text-align: center;
        color: {COLOR_MUTED};
        font-size: 0.8rem;
        margin-top: 2rem;
    }}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
image_sidebar = Image.open('assets/housepic.jpg')
st.sidebar.image(image_sidebar, width=300)
with st.sidebar:
    st.markdown("### About")
    st.write(
        "This tool estimates Belgian property prices using an XGBoost "
        "regression model, trained on real estate listing data."
    )
    st.markdown("---")
    st.markdown("### How it works")
    st.write(
        "1. Fill in the property details\n"
        "2. Click Predict Price\n"
        "3. The request goes to a live FastAPI backend\n"
        "4. The model returns an instant estimate"
    )
    st.markdown("---")
    st.caption("Built as part of the Immo Eliza deployment project.")

# --- Header ---
image_banner = Image.open('assets/banner.jpg')
st.image(image_banner, width=900)

st.markdown("""
<div class="main-header">
    <h1>Real Estate Price Predictor</h1>
    <p>Powered by XGBoost — an instant price estimate for a Belgian property</p>
</div>
""", unsafe_allow_html=True)

# --- Required fields ---
with st.container(border=True):
    st.markdown("### Property Basics")
    st.markdown('<p class="required-note"><span>*</span> Required fields</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        bedrooms = st.number_input("Bedrooms *", min_value=1, max_value=10, value=None, placeholder="e.g. 3")
        property_type = st.selectbox("Property Type *", ["Select", "House", "Apartment"])
    with col2:
        living_area = st.number_input("Living Area (m²) *", min_value=50, max_value=1000, value=None, placeholder="e.g. 150")
        province = st.selectbox("Province *", [
            "Select", "Brussels Capital Region", "Flanders", "Liège", "Antwerp",
            "East Flanders", "West Flanders", "Hainaut", "Namur",
            "Limburg", "Walloon Brabant", "Flemish Brabant", "Luxembourg"
        ])

st.markdown("<br>", unsafe_allow_html=True)


# --- Optional fields ---
with st.expander("➕ Add more details for a more accurate estimate"):
    col3, col4 = st.columns(2)
    with col3:
        bathrooms = st.number_input("Bathrooms", min_value=1, max_value=10, value=None, placeholder="e.g. 1")
        #total_area = st.number_input("Total Area (m²)", min_value=50, value=None, placeholder="e.g. 180")
        facades = st.number_input("Facades", min_value=0, max_value=4, value=None, placeholder="e.g. 2")
        parking_count = st.number_input("Parking Spots", min_value=0, max_value=10, value=None, placeholder="e.g. 1")
        has_garage = 1 if (parking_count or 0) > 0 else 0
        has_garden = st.checkbox("Has Garden")
        if has_garden:
            garden_area = st.number_input("Garden Area (m²)", min_value=0, value=None, placeholder="e.g. 50")
        else:
            garden_area = None
        is_prestigious = st.checkbox("Nearby City is Prestigious")
        has_elevator = st.checkbox("Has Elevator")

    with col4:
        state_of_building = st.selectbox("State of Building", [None, "Excellent", "Good", "To renovate", "To restore"])
        epc_score = st.selectbox("EPC Score", [None, "A", "B", "C", "D", "E", "F", "G"])
        kitchen_equipped = st.selectbox("Kitchen", [None, "Not installed", "USA not installed", "Installed", "Fully equipped"])
        building_year = st.number_input("Building Year", min_value=1800, max_value=2026, value=None, placeholder="e.g. 2000")

        knows_coordinates = st.checkbox("I know the exact latitude & longitude")
        if knows_coordinates:
            st.caption(
                "Look it up on [latlong.net](https://www.latlong.net/) — "
                "type the address and copy the coordinates shown."
            )
            latitude = st.number_input("Latitude", min_value=49.0, max_value=51.5, value=None, format="%.5f", placeholder="e.g. 50.85000")
            longitude = st.number_input("Longitude", min_value=2.5, max_value=6.5, value=None, format="%.5f", placeholder="e.g. 4.35000")
        else:
            latitude = None
            longitude = None

if latitude is None:
    latitude = 50.85
if longitude is None:
    longitude = 4.35

st.markdown("<br>", unsafe_allow_html=True)

# --- Validation ---
def get_missing_fields():
    missing = []
    if bedrooms is None:
        missing.append("Bedrooms")
    if living_area is None:
        missing.append("Living Area")
    if property_type == "Select":
        missing.append("Property Type")
    if province == "Select":
        missing.append("Province")
    return missing

# --- Predict button ---
if st.button("Predict Price"):
    missing_fields = get_missing_fields()

    if missing_fields:
        st.error(f"Please fill in the required fields: {', '.join(missing_fields)}")
    else:
        payload = {
            "data": {
                "bedrooms": bedrooms,
                "living_area_m2": living_area,
                "property_type": property_type,
                "province": province,
                "bathrooms": bathrooms,
                "total_area_m2": None,
                "facades": facades,
                "has_garage": int(has_garage),
                "parking_count": parking_count,
                "has_garden": int(has_garden),
                "garden_area_m2": garden_area,
                "state_of_the_building": state_of_building,
                "epc_score": epc_score,
                "has_elevator": int(has_elevator),
                "kitchen_equipped": kitchen_equipped,
                "building_year": building_year,
                "is_nearby_city_prestigious": int(is_prestigious),
                "latitude": latitude,
                "longitude": longitude,
            }
        }

        with st.spinner("Contacting the prediction service... this may take up to a minute if it's waking up."):
            try:
                response = requests.post(API_URL, json=payload, timeout=60)
                response.raise_for_status()
                result = response.json()

                if result.get("prediction") is not None:
                    price = result["prediction"]
                    price_per_m2 = price / living_area

                    st.markdown(f"""
                    <div class="price-result">
                        <p>Estimated Price</p>
                        <h2>€{price:,.2f}</h2>
                    </div>
                    """, unsafe_allow_html=True)

                    st.metric("Price per m²", f"€{price_per_m2:,.0f}")

                else:
                    st.error("The API couldn't generate a prediction. Please check your inputs.")

            except requests.exceptions.RequestException as e:
                st.error(f"Could not reach the prediction API: {e}")

st.markdown('<p class="footer-note">Note: Prediction from a model- not an official valuation.</p>', unsafe_allow_html=True)