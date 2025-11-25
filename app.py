import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# Setup Streamlit page
st.set_page_config(
    page_title="AI Mind Map Generator",
    page_icon="🧠",
    layout="centered"
)

# Initialize session state
if 'generated_mindmap' not in st.session_state:
    st.session_state.generated_mindmap = None

# Setup Client
@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

MODEL_ID = "gemini-3-pro-image-preview"

def generate_mindmap(topic, api_key, theme, style, complexity, aspect_ratio="16:9", image_size="4K"):
    # Build the prompt with customizations
    prompt = f"""Create a detailed mind map about: {topic}

Theme: {theme}
Style: {style}
Complexity: {complexity}

Requirements:
- Central concept in the middle
- Main branches radiating outward with clear hierarchy
- Sub-branches with related concepts
- Use colors to differentiate categories
- Include icons or small illustrations where relevant
- Clean, organized layout with readable text
- Professional and visually appealing design
- Follow the {theme} color scheme
- {style} visual style"""

    try:
        client = get_client(api_key)
        # Call the API
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=image_size
                )
            )
        )
        
        # Handle the Image
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_data = part.inline_data.data
                img = Image.open(io.BytesIO(image_data))
                return img
                
    except Exception as e:
        st.error(f"Error generating mind map: {e}")
        return None

# Sidebar - API Key and Promotion
with st.sidebar:
    st.header("🔑 Configuration")
    
    api_key = st.text_input(
        "Google API Key:",
        type="password",
        help="Get your API key from Google AI Studio"
    )
    
    st.markdown("---")
    
    # Build Fast with AI Promotion
    st.markdown(
        """
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; 
                    border-radius: 10px; 
                    text-align: center;
                    margin: 10px 0;'>
            <h3 style='color: white; margin: 0 0 10px 0;'>🚀 Want to Build AI Apps?</h3>
            <p style='color: white; margin: 0 0 15px 0; font-size: 0.9em;'>
                Learn to build production-ready AI applications from scratch
            </p>
            <a href='https://www.buildfastwithai.com/genai-course' 
               target='_blank' 
               style='background-color: white; 
                      color: #764ba2; 
                      padding: 10px 20px; 
                      text-decoration: none; 
                      border-radius: 5px; 
                      font-weight: bold;
                      display: inline-block;'>
                Join Gen AI Crash Course →
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style='text-align: center; padding: 10px;'>
            <p style='color: #666; font-size: 0.85em; margin: 5px 0;'>
                By <b>Build Fast with AI</b>
            </p>
            <p style='color: #888; font-size: 0.75em; margin: 0;'>
                Master GenAI • Build Real Projects • Launch Fast
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    st.info("💡 **Tip**: Use specific, descriptive topics for better mind maps!")

# Main Content
# Streamlit UI
st.title("🍌 BananaBrain - AI Mind Maps")
st.markdown("Transform your ideas into beautiful, structured mind maps using Google's Gemini AI")

if not api_key:
    st.warning("⚠️ Please enter your Google API key in the sidebar to continue")
    st.info("📌 Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.stop()

# Input form
with st.form("mindmap_generation_form"):
    topic = st.text_area(
        "Enter your mind map topic:",
        placeholder="e.g., Machine Learning Fundamentals, Project Management Process, Healthy Living Tips",
        height=100,
        help="Describe the central topic or concept for your mind map"
    )
    
    st.subheader("Customization Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox(
            "Color Theme:",
            [
                "Modern Purple & Blue",
                "Professional Blue & Gray",
                "Vibrant Rainbow",
                "Nature Green & Earth Tones",
                "Warm Sunset (Orange & Pink)",
                "Minimal Black & White",
                "Ocean Blues",
                "Forest Greens",
                "Pastel Dream",
                "Dark Mode (Dark Background)"
            ],
            help="Choose the color scheme for your mind map"
        )
        
        complexity = st.selectbox(
            "Complexity Level:",
            [
                "Simple (3-5 main branches)",
                "Moderate (5-7 main branches)",
                "Detailed (7-10 main branches)",
                "Comprehensive (10+ branches)"
            ],
            index=1,
            help="How detailed should the mind map be?"
        )
    
    with col2:
        style = st.selectbox(
            "Visual Style:",
            [
                "Modern & Clean",
                "Hand-drawn / Sketch",
                "Minimalist",
                "Corporate / Professional",
                "Creative & Artistic",
                "Infographic Style",
                "Whiteboard Style",
                "Organic / Flowing"
            ],
            help="Choose the visual style of your mind map"
        )
        
        aspect_ratio = st.selectbox(
            "Aspect Ratio:",
            ["16:9", "4:3", "1:1"],
            help="16:9 is recommended for presentations"
        )
    
    # Advanced options in expander
    with st.expander("⚙️ Advanced Options"):
        image_size = st.selectbox(
            "Image Quality:",
            ["2K", "4K"],
            index=1
        )
        
        custom_instructions = st.text_area(
            "Additional Instructions (Optional):",
            placeholder="e.g., Include specific examples, focus on practical applications, add time estimates",
            height=80,
            help="Add any specific requirements or preferences"
        )
    
    submitted = st.form_submit_button("🎨 Generate Mind Map", use_container_width=True)

# Generate mind map when form is submitted
if submitted and topic:
    with st.spinner("Creating your mind map... This may take 30-60 seconds"):
        # Add custom instructions to complexity if provided
        if 'custom_instructions' in locals() and custom_instructions:
            complexity = f"{complexity}. Additional instructions: {custom_instructions}"
        
        generated_mindmap = generate_mindmap(
            topic, 
            api_key, 
            theme, 
            style, 
            complexity, 
            aspect_ratio, 
            image_size
        )
        
        if generated_mindmap:
            st.session_state.generated_mindmap = generated_mindmap
            st.success("✅ Mind map generated successfully!")
            st.balloons()

# Display the generated mind map
if st.session_state.generated_mindmap:
    st.subheader("Your Mind Map:")
    st.image(st.session_state.generated_mindmap, use_container_width=True)
    
    # Download button
    img_buffer = io.BytesIO()
    st.session_state.generated_mindmap.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📥 Download Mind Map (PNG)",
            data=img_buffer,
            file_name=f"mindmap_{topic[:30].replace(' ', '_')}.png",
            mime="image/png",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Generate Another", use_container_width=True):
            st.session_state.generated_mindmap = None
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        💡 <b>Tip:</b> For best results, be specific about your topic and choose a theme that matches your use case
    </div>
    """,
    unsafe_allow_html=True
)