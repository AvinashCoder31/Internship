import streamlit as st
import os
import sys
from datetime import datetime
import json

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.services.service1 import generate_travel_plan, save_travel_plan

# Page configuration
st.set_page_config(
    page_title="🌍 Travel Planner Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .travel-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    
    .weather-info {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 AI Travel Planner Agent</h1>
        <p>Powered by LangGraph & Real-time Weather Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("✈️ Plan Your Trip")
        
        # Destination input
        destination = st.text_input(
            "🏙️ Destination",
            placeholder="e.g., Paris, Tokyo, New York",
            help="Enter the city or country you want to visit"
        )
        
        # Budget selection
        budget = st.selectbox(
            "💰 Budget Range",
            ["low", "medium", "high"],
            index=1,
            help="Select your budget preference"
        )
        
        # Duration input
        duration = st.number_input(
            "📅 Duration (days)",
            min_value=1,
            max_value=30,
            value=5,
            help="How many days will you be traveling?"
        )
        
        # Interests selection
        st.subheader("🎯 Your Interests")
        interests = []
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.checkbox("🏛️ Museums"):
                interests.append("museums")
            if st.checkbox("🍽️ Food"):
                interests.append("food")
            if st.checkbox("🏛️ Architecture"):
                interests.append("architecture")
            if st.checkbox("🎨 Art"):
                interests.append("art")
            if st.checkbox("🏖️ Beaches"):
                interests.append("beaches")
        
        with col2:
            if st.checkbox("🏔️ Nature"):
                interests.append("nature")
            if st.checkbox("🛍️ Shopping"):
                interests.append("shopping")
            if st.checkbox("🌙 Nightlife"):
                interests.append("nightlife")
            if st.checkbox("🏃 Adventure"):
                interests.append("adventure")
            if st.checkbox("📿 Culture"):
                interests.append("culture")
        
        # Custom interests
        custom_interests = st.text_input(
            "➕ Other Interests",
            placeholder="hiking, photography, etc.",
            help="Add custom interests separated by commas"
        )
        
        if custom_interests:
            custom_list = [interest.strip() for interest in custom_interests.split(",")]
            interests.extend(custom_list)
        
        # Save to file option
        save_to_file = st.checkbox("💾 Save plan to file", value=True)
        
        # Generate plan button
        generate_button = st.button("🚀 Generate Travel Plan", type="primary")
    
    # Main content area
    if generate_button:
        if not destination:
            st.error("❌ Please enter a destination!")
            return
        
        if not interests:
            st.warning("⚠️ Consider adding some interests for a more personalized plan!")
        
        # Show loading spinner
        with st.spinner("🔄 Creating your personalized travel plan..."):
            # Generate the travel plan
            result = generate_travel_plan(
                destination=destination,
                budget=budget,
                duration=str(duration),
                interests=interests
            )
        
        if result["success"]:
            # Display success message
            st.markdown("""
            <div class="success-message">
                <h3>🎉 Your Travel Plan is Ready!</h3>
                <p>Generated with real-time weather data and personalized recommendations.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create tabs for different sections
            tab1, tab2, tab3 = st.tabs(["📋 Travel Plan", "🌤️ Weather Info", "💾 Save & Export"])
            
            with tab1:
                st.markdown("### 🗺️ Complete Travel Plan")
                
                # Display the travel plan in a nice format
                st.markdown(f"""
                <div class="travel-card">
                    <h4>📍 Destination: {result['destination']}</h4>
                    <p><strong>Duration:</strong> {duration} days</p>
                    <p><strong>Budget:</strong> {budget.title()}</p>
                    <p><strong>Interests:</strong> {', '.join(interests) if interests else 'General tourism'}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Display the full plan
                st.markdown("#### 📝 Detailed Itinerary")
                st.markdown(result["plan"])
            
            with tab2:
                st.markdown("### 🌤️ Current Weather Information")
                
                # Display weather info in a styled card
                st.markdown(f"""
                <div class="weather-info">
                    <h3>🌡️ Live Weather Update</h3>
                    <p style="font-size: 1.2em; margin: 0;">{result['weather_info']}</p>
                    <small>Updated in real-time via WeatherAPI</small>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("💡 The travel plan has been optimized based on current weather conditions!")
            
            with tab3:
                st.markdown("### 💾 Save & Export Options")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if save_to_file:
                        # Save the plan automatically
                        save_result = save_travel_plan(result["plan"], destination)
                        
                        if save_result["success"]:
                            st.success(f"✅ Plan saved successfully!")
                            st.info(f"📁 File location: `{save_result['filepath']}`")
                        else:
                            st.error(f"❌ Error saving file: {save_result['error']}")
                    
                    # Manual save button
                    if st.button("💾 Save to File"):
                        save_result = save_travel_plan(result["plan"], destination)
                        if save_result["success"]:
                            st.success("✅ Plan saved successfully!")
                        else:
                            st.error(f"❌ Error: {save_result['error']}")
                
                with col2:
                    # Download button for the plan
                    plan_filename = f"travel_plan_{destination.replace(' ', '_')}.md"
                    st.download_button(
                        label="📥 Download Plan",
                        data=result["plan"],
                        file_name=plan_filename,
                        mime="text/markdown"
                    )
                    
                    # Copy to clipboard (text area for easy copying)
                    st.text_area(
                        "📋 Copy Plan Text",
                        value=result["plan"],
                        height=100,
                        help="Select all and copy to clipboard"
                    )
        
        else:
            # Display error message
            st.markdown(f"""
            <div class="error-message">
                <h3>❌ Error Generating Plan</h3>
                <p>{result['error']}</p>
                <p>Please check your API keys and try again.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Information section
    else:
        # Welcome message and instructions
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ## 🎯 How It Works
            
            1. **📍 Enter Destination**: Tell us where you want to go
            2. **💰 Set Budget**: Choose your budget range (low/medium/high)
            3. **📅 Duration**: How many days will you travel?
            4. **🎯 Interests**: Select what you love to do
            5. **🚀 Generate**: Get your personalized AI-powered travel plan!
            
            ### ✨ Features
            - 🌤️ **Real-time Weather**: Live weather data integration
            - 🧠 **AI-Powered**: Uses LangGraph and Groq's Llama model
            - 📱 **Personalized**: Tailored to your interests and budget
            - 💾 **Save & Export**: Download or save your plans
            - 🔄 **Memory**: Learns from your preferences
            """)
        
        with col2:
            st.markdown("""
            ### 🔧 Requirements
            
            Make sure you have these API keys set up:
            
            - **GROQ_API_KEY** 🤖
            - **WEATHER_API_KEY** 🌤️
            - **GEOAPIFY_API_KEY** 🗺️
            
            ### 📊 Sample Destinations
            
            - 🗼 Paris, France
            - 🗾 Tokyo, Japan
            - 🗽 New York, USA
            - 🏛️ Rome, Italy
            - 🏖️ Bali, Indonesia
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🌍 Built with ❤️ using Streamlit, LangGraph & Real-time APIs</p>
        <p>Perfect for travelers who want AI-powered, personalized trip planning!</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()