import os
import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
import io

# Setup Streamlit page
st.set_page_config(
    page_title="BananaSlides - AI Slide Generator",
    page_icon="🍌",
    layout="centered"
)

# Initialize session state
if 'generated_slides' not in st.session_state:
    st.session_state.generated_slides = []

# Setup Client
@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)

MODEL_ID = "gemini-3-pro-image-preview"

def generate_slide(topic, slide_number, total_slides, slide_content, api_key, theme, style, aspect_ratio="16:9", image_size="4K"):
    """Generate a single presentation slide"""
    
    prompt = f"""Create a professional presentation slide.

Topic: {topic}
Slide {slide_number} of {total_slides}
Slide Content: {slide_content}

Theme: {theme}
Style: {style}

Requirements:
- Create a single, clean presentation slide
- Include a clear title at the top
- Use bullet points or key information in a readable layout
- Professional typography and spacing
- Follow the {theme} color scheme
- {style} visual design
- Include relevant icons or simple graphics if appropriate
- Make text large and readable
- This is slide {slide_number}, so {"make it an engaging title slide" if slide_number == 1 else "make it a content slide with key points" if slide_number < total_slides else "make it a conclusion/summary slide"}
- DO NOT include any watermarks or attribution text"""

    try:
        client = get_client(api_key)
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
        
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_data = part.inline_data.data
                img = Image.open(io.BytesIO(image_data))
                return img
                
    except Exception as e:
        st.error(f"Error generating slide {slide_number}: {e}")
        return None

def generate_slide_content(topic, num_slides, api_key):
    """Generate content outline for slides using text generation"""
    try:
        client = get_client(api_key)
        
        prompt = f"""Create a brief outline for a {num_slides}-slide presentation about: {topic}

For each slide, provide:
- A short title (max 5 words)
- 2-3 key bullet points (max 8 words each)

Format your response exactly like this:
SLIDE 1:
Title: [title here]
Points: [point 1] | [point 2] | [point 3]

SLIDE 2:
Title: [title here]
Points: [point 1] | [point 2] | [point 3]

(continue for all {num_slides} slides)

Keep it concise and impactful."""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        return response.text
        
    except Exception as e:
        st.error(f"Error generating content outline: {e}")
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
    
    st.info("💡 **Tip**: Keep topics focused for better slide generation!")

# Main Content
st.title("🍌 BananaSlides - AI Presentations")
st.markdown("Transform your ideas into beautiful presentation slides using Nano Banana Pro")

if not api_key:
    st.warning("⚠️ Please enter your Google API key in the sidebar to continue")
    st.info("📌 Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikey)")
    st.stop()

# Input form
with st.form("slide_generation_form"):
    topic = st.text_area(
        "Enter your presentation topic:",
        placeholder="e.g., Introduction to Machine Learning, Benefits of Remote Work, Climate Change Solutions",
        height=100,
        help="Describe the main topic for your presentation"
    )
    
    st.subheader("Customization Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_slides = st.selectbox(
            "Number of Slides:",
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            index=2,
            help="Choose how many slides to generate (max 10)"
        )
        
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
            help="Choose the color scheme for your slides"
        )
    
    with col2:
        style = st.selectbox(
            "Visual Style:",
            [
                "Modern & Clean",
                "Minimalist",
                "Corporate / Professional",
                "Creative & Artistic",
                "Infographic Style",
                "Bold & Impactful",
                "Elegant & Sophisticated"
            ],
            help="Choose the visual style of your slides"
        )
        
        aspect_ratio = st.selectbox(
            "Aspect Ratio:",
            ["16:9", "4:3", "1:1"],
            help="16:9 is standard for presentations"
        )
    
    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        image_size = st.selectbox(
            "Image Quality:",
            ["2K", "4K"],
            index=1
        )
        
        custom_instructions = st.text_area(
            "Additional Instructions (Optional):",
            placeholder="e.g., Focus on statistics, include examples, make it engaging for students",
            height=80,
            help="Add any specific requirements or preferences"
        )
    
    submitted = st.form_submit_button("🎨 Generate Slides", use_container_width=True)

# Generate slides when form is submitted
if submitted and topic:
    st.session_state.generated_slides = []
    
    # First, generate content outline
    with st.spinner("📝 Creating content outline..."):
        content_outline = generate_slide_content(topic, num_slides, api_key)
        
        if content_outline:
            with st.expander("📋 View Content Outline"):
                st.text(content_outline)
    
    # Generate each slide
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(num_slides):
        slide_num = i + 1
        status_text.text(f"🎨 Generating slide {slide_num} of {num_slides}...")
        progress_bar.progress((i) / num_slides)
        
        # Extract relevant content for this slide from outline
        slide_content = f"Slide {slide_num} content from: {content_outline}" if content_outline else f"Slide {slide_num} about {topic}"
        
        if custom_instructions:
            slide_content += f". Additional requirements: {custom_instructions}"
        
        slide_image = generate_slide(
            topic=topic,
            slide_number=slide_num,
            total_slides=num_slides,
            slide_content=slide_content,
            api_key=api_key,
            theme=theme,
            style=style,
            aspect_ratio=aspect_ratio,
            image_size=image_size
        )
        
        if slide_image:
            st.session_state.generated_slides.append(slide_image)
        
        progress_bar.progress((i + 1) / num_slides)
    
    status_text.empty()
    progress_bar.empty()
    
    if st.session_state.generated_slides:
        st.success(f"✅ Generated {len(st.session_state.generated_slides)} slides successfully!")
        st.balloons()

# Display generated slides
if st.session_state.generated_slides:
    st.subheader("📊 Your Presentation Slides:")
    
    # Slide navigation with tabs
    tabs = st.tabs([f"Slide {i+1}" for i in range(len(st.session_state.generated_slides))])
    
    for idx, (tab, slide) in enumerate(zip(tabs, st.session_state.generated_slides)):
        with tab:
            st.image(slide, use_container_width=True)
            
            # Individual download button
            img_buffer = io.BytesIO()
            slide.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            st.download_button(
                label=f"📥 Download Slide {idx + 1}",
                data=img_buffer,
                file_name=f"slide_{idx + 1}_{topic[:20].replace(' ', '_')}.png",
                mime="image/png",
                key=f"download_{idx}"
            )
    
    st.markdown("---")
    
    # Download all slides
    col1, col2 = st.columns(2)
    
    with col1:
        # Create a zip file with all slides
        import zipfile
        
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for idx, slide in enumerate(st.session_state.generated_slides):
                img_buffer = io.BytesIO()
                slide.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                zip_file.writestr(f"slide_{idx + 1}.png", img_buffer.getvalue())
        
        zip_buffer.seek(0)
        
        st.download_button(
            label="📦 Download All Slides (ZIP)",
            data=zip_buffer,
            file_name=f"presentation_{topic[:20].replace(' ', '_')}.zip",
            mime="application/zip",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Generate New Presentation", use_container_width=True):
            st.session_state.generated_slides = []
            st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        💡 <b>Tip:</b> For best results, be specific about your topic and keep presentations focused on key messages
    </div>
    """,
    unsafe_allow_html=True
)
