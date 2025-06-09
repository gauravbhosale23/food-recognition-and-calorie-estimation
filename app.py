from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai


# Ensure set_page_config is the first Streamlit command
st.set_page_config(
    page_title="The Nutritionist",
    page_icon="🍏",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Your other Streamlit code comes after set_page_config
st.title("Welcome to The Nutritionist App")
st.sidebar.title("Sidebar")
# Rest of your app logic goes here...


# Load environment variables
load_dotenv()

# Configure GenAI Key
genai.configure(api_key="AIzaSyD4bs12EsCxZUgk5ouqSjqsuxNHgJCMQcg")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
    }
    .uploadedFile {
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .uploadedFile:hover {
        transform: scale(1.02);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f0f0;
        border-radius: 20px;
        padding: 10px 20px;
        color: #666;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    .stMarkdown {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin: 1rem 0;
    }
    .stSpinner {
        color: #4CAF50;
    }
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ffeeba;
    }
    </style>
""", unsafe_allow_html=True)

def get_gemini_response(input_prompt, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Header with custom styling
st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); border-radius: 15px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);'>
            🥗 The Nutritionist
        </h1>
        <p style='color: white; margin: 0.5rem 0; font-size: 1.2rem; opacity: 0.9;'>
            Your AI-powered nutrition analysis companion
        </p>
    </div>
""", unsafe_allow_html=True)

# Create two columns for better layout
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
        <div style='background-color: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h3 style='color: #2E7D32; margin-bottom: 1rem;'>Upload Your Food Image</h3>
            <p style='color: #666;'>Get instant nutritional analysis of your meal!</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose an image...", 
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of your food for analysis"
    )

with col2:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(
            image, 
            caption="Your uploaded food image", 
            use_column_width=True,
            output_format="PNG"
        )

# Analysis section with gradient background
st.markdown("""
    <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 2rem; border-radius: 15px; margin: 2rem 0;'>
        <h3 style='color: #2E7D32; text-align: center; margin-bottom: 1.5rem;'>Analysis Options</h3>
    </div>
""", unsafe_allow_html=True)

# Create tabs for different analysis options with custom styling
tab1, tab2, tab3 = st.tabs(["Calories", "Nutritional Value", "Health Assessment"])

with tab1:
    calories_prompt = """
    You are an expert nutritionist. Analyze the food items in the image and calculate the total calories. 
    Provide a breakdown as follows:

    1. Item 1 - calories
    2. Item 2 - calories
    ...
    Finally, mention whether the food is healthy, balanced, or unhealthy, and suggest additional healthy foods.
    """
    if st.button("Calculate Calories", key="calories"):
        if uploaded_file is not None:
            with st.spinner("Analyzing calories..."):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(calories_prompt, image_data)
                st.markdown("""
                    <div style='background-color: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                        <h3 style='color: #2E7D32; margin-bottom: 1rem;'>Results</h3>
                        <div style='color: #333; line-height: 1.6;'>
                """ + response + "</div></div>", unsafe_allow_html=True)
        else:
            st.warning("Please upload an image first!")

with tab2:
    nutrition_prompt = """
    You are an expert nutritionist. Analyze the food items in the image and provide a detailed nutritional breakdown including:
    - Proteins
    - Carbohydrates
    - Fats
    - Vitamins
    - Minerals
    
    Also provide recommendations for nutritional improvements if needed.
    """
    if st.button("Analyze Nutritional Value", key="nutrition"):
        if uploaded_file is not None:
            with st.spinner("Analyzing nutritional value..."):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(nutrition_prompt, image_data)
                st.markdown("""
                    <div style='background-color: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                        <h3 style='color: #2E7D32; margin-bottom: 1rem;'>Results</h3>
                        <div style='color: #333; line-height: 1.6;'>
                """ + response + "</div></div>", unsafe_allow_html=True)
        else:
            st.warning("Please upload an image first!")

with tab3:
    health_prompt = """
    You are an expert nutritionist. Analyze the food items in the image and provide:
    1. Overall health assessment
    2. Potential health benefits
    3. Any health concerns
    4. Recommendations for healthier alternatives
    5. Suggestions for a balanced meal
    """
    if st.button("Get Health Assessment", key="health"):
        if uploaded_file is not None:
            with st.spinner("Generating health assessment..."):
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(health_prompt, image_data)
                st.markdown("""
                    <div style='background-color: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                        <h3 style='color: #2E7D32; margin-bottom: 1rem;'>Results</h3>
                        <div style='color: #333; line-height: 1.6;'>
                """ + response + "</div></div>", unsafe_allow_html=True)
        else:
            st.warning("Please upload an image first!")

# Footer with gradient background
st.markdown("""
    <div style='background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); padding: 2rem; border-radius: 15px; margin-top: 2rem; text-align: center;'>
        <p style='color: white; margin: 0; font-size: 1.1rem;'>
            Powered by Google Gemini AI | Made with ❤️ for healthy living
        </p>
    </div>
""", unsafe_allow_html=True)