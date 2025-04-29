import streamlit as st
from PIL import Image
import time
from utils import load_models, generate_content

# Configure page
st.set_page_config(
    page_title="AI Campaign Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
<style>
    [data-testid="stForm"] {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stProgress > div > div > div {
        background-color: #4CAF50;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize models once
models = load_models()

# Main header
st.title("🚀 AI-Powered Campaign Generator")
st.markdown("Generate viral marketing campaigns in seconds")

# Input Form
with st.form("campaign_form"):
    col1, col2 = st.columns([1, 2])
    
    with col1:
        brand = st.text_input("Brand Name", placeholder="Your Brand", help="Enter your brand name")
        audience = st.multiselect(
            "Target Audience",
            options=["Teens", "Young Adults", "Parents", "Seniors", "Professionals"],
            default=["Young Adults"]
        )
        platform = st.selectbox(
            "Platform",
            options=["Instagram", "TikTok", "Twitter", "Facebook", "LinkedIn"]
        )
    
    with col2:
        goals = st.text_area(
            "Campaign Goals",
            placeholder="What do you want to achieve? (e.g., Increase engagement by 40%)",
            height=150
        )
    
    submitted = st.form_submit_button("✨ Generate Campaign")

# Processing Section
if submitted:
    if not brand or not platform:
        st.error("Please fill in required fields: Brand Name and Platform")
        st.stop()
    
    # Show progress
    progress_bar = st.progress(0)
    status = st.empty()
    
    try:
        # Generate prompt
        prompt = f"""
        Create a marketing campaign for {brand} targeting {', '.join(audience)} on {platform}.
        Campaign Goals: {goals}
        Generate 3 creative slogans and 5 relevant hashtags.
        """
        
        # Processing stages
        status.markdown("🔍 Analyzing your inputs...")
        progress_bar.progress(10)
        time.sleep(0.5)
        
        status.markdown("🧠 Generating creative content...")
        progress_bar.progress(30)
        
        # Generate content
        result = generate_content(prompt, models)
        progress_bar.progress(70)
        
        # Process outputs
        content = result['text'].split("Hashtags:")
        slogans = [s.strip() for s in content[0].split("Slogans:")[-1].split("\n") if s.strip()]
        hashtags = [h.strip() for h in content[1].split("\n") if h.strip()][:5]
        
        status.markdown("📊 Finalizing results...")
        progress_bar.progress(90)
        time.sleep(0.5)
        
    except Exception as e:
        st.error(f"🚨 Error generating campaign: {str(e)}")
        st.stop()
    
    finally:
        progress_bar.progress(100)
        time.sleep(0.2)
        progress_bar.empty()
    
    # Display Results
    status.success("✅ Campaign Generated!")
    
    # Results Layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎨 Visual Concept")
        st.image(result['image'], use_column_width=True)
        st.caption(f"AI-generated visual for {brand}")
    
    with col2:
        st.subheader("📝 Campaign Content")
        
        with st.expander("✨ Slogans", expanded=True):
            for i, slogan in enumerate(slogans[:3], 1):
                st.markdown(f"{i}. **{slogan}**")
        
        with st.expander("#️⃣ Hashtags"):
            cols = st.columns(2)
            for i, tag in enumerate(hashtags):
                cols[i%2].markdown(f"`#{tag}`")
        
        with st.expander("📈 Sentiment Analysis"):
            sentiment = result['sentiment'][0]
            st.metric(
                label="Overall Sentiment",
                value=sentiment['label'].title(),
                delta=f"{sentiment['score']:.0%} Confidence"
            )
    
    # Download Section
    st.download_button(
        label="📥 Download Campaign Package",
        data=result['text'],
        file_name=f"{brand}_campaign.txt",
        mime="text/plain"
    )
