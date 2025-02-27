
# ################### working Good but title missing ###################################
# import os
# import io
# import streamlit as st
# from PIL import Image
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.lib.units import cm
# from reportlab.pdfgen import canvas
# from reportlab.lib.utils import ImageReader

# # Configuration constants
# MARGIN_TOP = 1.5 * cm  # Reduced top margin for better title placement
# GAP_TITLE_IMAGE = 1 * cm
# FONT_SIZE_TITLE = 20  # Increased font size for better visibility
# PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)
# ROTATION_OPTIONS = [0, 90, 180, 270]
# TITLE_COLOR = (0.2, 0.2, 0.2)  # Dark gray for professional look

# def create_pdf(images_data, progress_bar=None):
#     """Create PDF with images and titles, showing progress."""
#     buffer = io.BytesIO()
#     c = canvas.Canvas(buffer, pagesize=landscape(A4))
#     total_images = len(images_data)
    
#     for idx, (img, title, rotation) in enumerate(images_data, 1):
#         try:
#             # Rotate image and convert to RGB
#             if rotation != 0:
#                 img = img.rotate(rotation, expand=True)
#             if img.mode in ('RGBA', 'P'):
#                 img = img.convert('RGB')
            
#             # Calculate dimensions after rotation
#             img_width, img_height = img.size
#             aspect_ratio = img_height / img_width
            
#             # Dynamic width based on image orientation
#             base_width_percent = 0.75 if aspect_ratio < 1 else 0.85  # Wider for portrait
#             max_img_width = PAGE_WIDTH * base_width_percent
            
#             # Calculate drawing dimensions
#             img_draw_width = min(max_img_width, PAGE_WIDTH)
#             img_draw_height = img_draw_width * aspect_ratio
            
#             # Vertical space constraints
#             max_img_height = PAGE_HEIGHT - MARGIN_TOP - GAP_TITLE_IMAGE - 3 * cm
#             if img_draw_height > max_img_height:
#                 img_draw_height = max_img_height
#                 img_draw_width = img_draw_height / aspect_ratio
            
#             # Create page with professional styling
#             c.setFillColorRGB(1, 1, 1)
#             c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
            
#             # Draw professional title
#             c.setFont("Helvetica-Bold", FONT_SIZE_TITLE)
#             c.setFillColorRGB(*TITLE_COLOR)
#             title_width = c.stringWidth(title, "Helvetica-Bold", FONT_SIZE_TITLE)
#             title_x = (PAGE_WIDTH - title_width) / 2
#             title_y = PAGE_HEIGHT - MARGIN_TOP + 0.5 * cm  # Fine-tuned position
#             c.drawString(title_x, title_y, title)
            
#             # Add subtle underline below title
#             c.setLineWidth(0.5)
#             c.setStrokeColorRGB(0.8, 0.8, 0.8)
#             c.line(title_x, title_y - 2, title_x + title_width, title_y - 2)
            
#             # Draw image with shadow effect
#             img_x = (PAGE_WIDTH - img_draw_width) / 2
#             img_y = title_y - GAP_TITLE_IMAGE - img_draw_height
            
#             # Add subtle shadow
#             c.setFillColorRGB(0.9, 0.9, 0.9)
#             c.rect(img_x + 3, img_y - 3, img_draw_width, img_draw_height, fill=True)
            
#             # Draw actual image
#             img_buffer = io.BytesIO()
#             img.save(img_buffer, format='JPEG', quality=95)
#             img_buffer.seek(0)
#             c.drawImage(ImageReader(img_buffer), img_x, img_y, 
#                        width=img_draw_width, height=img_draw_height,
#                        mask='auto')
            
#             c.showPage()
            
#             if progress_bar:
#                 progress_bar.progress(idx / total_images)
#         except Exception as e:
#             st.error(f"Error processing {title}: {str(e)}")
#             continue
    
#     c.save()
#     buffer.seek(0)
#     return buffer

# def main():
#     st.title("Professional Image to PDF Converter 📷→📄")
    
#     # Initialize session state
#     if 'rotations' not in st.session_state:
#         st.session_state.rotations = {}

#     # File uploader with multiple selection
#     uploaded_files = st.file_uploader(
#         "Upload images (PNG, JPG, JPEG)", 
#         type=["png", "jpg", "jpeg"], 
#         accept_multiple_files=True
#     )
    
#     # Show preview and rotation controls
#     images_data = []
#     if uploaded_files:
#         st.subheader("Image Preparation")
        
#         for file in uploaded_files:
#             # Initialize rotation for new files
#             if file.name not in st.session_state.rotations:
#                 st.session_state.rotations[file.name] = 0
                
#             try:
#                 img = Image.open(file)
#                 title = os.path.splitext(file.name)[0]
                
#                 col1, col2 = st.columns([2, 3])
                
#                 with col1:
#                     # Enhanced preview with rotation
#                     preview_img = img.copy()
#                     current_rotation = st.session_state.rotations[file.name]
#                     if current_rotation != 0:
#                         preview_img = preview_img.rotate(current_rotation, expand=True)
                    
#                     st.image(
#                         preview_img,
#                         caption=f"Preview: {file.name}",
#                         use_column_width=True,
#                         output_format="JPEG"
#                     )
                
#                 with col2:
#                     # Professional rotation controls
#                     new_rotation = st.selectbox(
#                         label=f"Rotation for {file.name}",
#                         options=ROTATION_OPTIONS,
#                         index=ROTATION_OPTIONS.index(current_rotation),
#                         key=f"rot_{file.name}",
#                         format_func=lambda x: f"{x}°"  # Show degree symbol
#                     )
#                     st.session_state.rotations[file.name] = new_rotation
                    
#                     # Detailed image info
#                     st.markdown(f"""
#                     **Original Dimensions:** {img.size[0]}×{img.size[1]} pixels  
#                     **Current Rotation:** {new_rotation}°  
#                     **File Name:** `{file.name}`  
#                     **Orientation:** {'Portrait' if img.height > img.width else 'Landscape'}
#                     """)
                
#                 images_data.append((img, title, new_rotation))
                
#             except Exception as e:
#                 st.error(f"Error processing {file.name}: {str(e)}")

#     # PDF generation section
#     if uploaded_files and st.button("Generate Professional PDF"):
#         with st.spinner("Creating High-Quality PDF..."):
#             progress_bar = st.progress(0)
#             try:
#                 pdf_buffer = create_pdf(images_data, progress_bar)
#                 st.success("PDF Created Successfully!")
                
#                 # Enhanced download section
#                 st.markdown("---")
#                 col1, col2 = st.columns([3, 2])
#                 with col1:
#                     st.markdown("### PDF Ready for Download")
#                     st.markdown("Your professional document is complete. Click below to download.")
#                 with col2:
#                     st.download_button(
#                         label="📥 Download PDF",
#                         data=pdf_buffer,
#                         file_name="professional_images.pdf",
#                         mime="application/pdf",
#                         type="primary",
#                         use_container_width=True
#                     )
                
#             except Exception as e:
#                 st.error(f"PDF creation failed: {str(e)}")
#             finally:
#                 progress_bar.empty()

# if __name__ == "__main__":
#     main()









##### working fine #############



# import os
# import io
# import streamlit as st
# from PIL import Image
# from reportlab.lib.pagesizes import A4, landscape
# from reportlab.lib.units import cm
# from reportlab.pdfgen import canvas
# from reportlab.lib.utils import ImageReader

# # Configuration constants
# MARGIN_TOP = 1.5 * cm
# GAP_TITLE_IMAGE = 1 * cm
# FONT_SIZE_TITLE = 25
# PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)
# ROTATION_OPTIONS = [0, 90, 180, 270]
# TITLE_COLOR = (0.2, 0.2, 0.2)

# def create_pdf(images_data, progress_bar=None):
#     """Create PDF with optimized image dimensions based on orientation."""
#     buffer = io.BytesIO()
#     c = canvas.Canvas(buffer, pagesize=landscape(A4))
#     total_images = len(images_data)
    
#     for idx, (img, title, rotation) in enumerate(images_data, 1):
#         try:
#             # Apply rotation and convert to RGB
#             if rotation != 0:
#                 img = img.rotate(rotation, expand=True)
#             if img.mode in ('RGBA', 'P'):
#                 img = img.convert('RGB')
            
#             # Get dimensions after rotation
#             img_width, img_height = img.size
#             aspect_ratio = img_height / img_width
#             is_portrait = img_height > img_width
            
#             # Calculate maximum available height
#             max_available_height = PAGE_HEIGHT - MARGIN_TOP - GAP_TITLE_IMAGE - 3 * cm
            
#             # Orientation-based dimension calculation
#             if is_portrait:
#                 # Portrait: Maximize width (85% of page width)
#                 max_width = PAGE_WIDTH * 0.85
#                 img_draw_width = min(max_width, PAGE_WIDTH)
#                 img_draw_height = img_draw_width * aspect_ratio
                
#                 # Check height constraints
#                 if img_draw_height > max_available_height:
#                     img_draw_height = max_available_height
#                     img_draw_width = img_draw_height / aspect_ratio
#             else:
#                 # Landscape: Maximize height (100% of available height)
#                 img_draw_height = min(max_available_height, max_available_height)
#                 img_draw_width = img_draw_height / aspect_ratio
                
#                 # Check width constraints
#                 if img_draw_width > PAGE_WIDTH:
#                     img_draw_width = PAGE_WIDTH
#                     img_draw_height = img_draw_width * aspect_ratio

#             # Page setup
#             c.setFillColorRGB(1, 1, 1)
#             c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
            
#             # Draw title
#             c.setFont("Helvetica-Bold", FONT_SIZE_TITLE)
#             c.setFillColorRGB(*TITLE_COLOR)
#             title_width = c.stringWidth(title, "Helvetica-Bold", FONT_SIZE_TITLE)
#             c.drawString((PAGE_WIDTH - title_width)/2, PAGE_HEIGHT - MARGIN_TOP + 0.5*cm, title)
            
#             # Draw image with shadow
#             img_x = (PAGE_WIDTH - img_draw_width) / 2
#             img_y = PAGE_HEIGHT - MARGIN_TOP - GAP_TITLE_IMAGE - img_draw_height
            
#             # Shadow effect
#             c.setFillColorRGB(0.9, 0.9, 0.9)
#             c.rect(img_x + 3, img_y - 3, img_draw_width, img_draw_height, fill=True)
            
#             # Actual image
#             img_buffer = io.BytesIO()
#             img.save(img_buffer, format='JPEG', quality=95)
#             img_buffer.seek(0)
#             c.drawImage(ImageReader(img_buffer), img_x, img_y, 
#                        width=img_draw_width, height=img_draw_height)
            
#             c.showPage()
            
#             if progress_bar:
#                 progress_bar.progress(idx / total_images)
#         except Exception as e:
#             st.error(f"Error processing {title}: {str(e)}")
#             continue
    
#     c.save()
#     buffer.seek(0)
#     return buffer

# def main():
#     st.title("Professional Image to PDF Converter")
    
#     # Initialize session state
#     if 'rotations' not in st.session_state:
#         st.session_state.rotations = {}

#     # File uploader
#     uploaded_files = st.file_uploader(
#         "Upload images", 
#         type=["png", "jpg", "jpeg"], 
#         accept_multiple_files=True
#     )
    
#     # Image processing
#     images_data = []
#     if uploaded_files:
#         st.subheader("Image Preparation")
        
#         for file in uploaded_files:
#             if file.name not in st.session_state.rotations:
#                 st.session_state.rotations[file.name] = 0
                
#             try:
#                 img = Image.open(file)
#                 title = os.path.splitext(file.name)[0]
                
#                 col1, col2 = st.columns([2, 3])
                
#                 with col1:
#                     current_rotation = st.session_state.rotations[file.name]
#                     preview_img = img.rotate(current_rotation, expand=True) if current_rotation != 0 else img
#                     st.image(preview_img, caption=file.name, use_column_width=True)
                
#                 with col2:
#                     new_rotation = st.selectbox(
#                         f"Rotation for {file.name}",
#                         options=ROTATION_OPTIONS,
#                         index=ROTATION_OPTIONS.index(current_rotation),
#                         format_func=lambda x: f"{x}°"
#                     )
#                     st.session_state.rotations[file.name] = new_rotation
                    
#                     # Display orientation info
#                     final_width, final_height = preview_img.size
#                     orientation = "Portrait" if final_height > final_width else "Landscape"
#                     st.markdown(f"""
#                     **Final Dimensions:** {final_width}×{final_height}  
#                     **Orientation:** {orientation}  
#                     **Rotation Applied:** {new_rotation}°
#                     """)
                
#                 images_data.append((img, title, new_rotation))
                
#             except Exception as e:
#                 st.error(f"Error processing {file.name}: {str(e)}")

#     # PDF generation
#     if uploaded_files and st.button("Generate PDF"):
#         with st.spinner("Creating PDF..."):
#             progress_bar = st.progress(0)
#             try:
#                 pdf_buffer = create_pdf(images_data, progress_bar)
#                 st.success("PDF creation completed!")
                
#                 # Download section
#                 st.download_button(
#                     "📥 Download PDF",
#                     data=pdf_buffer,
#                     file_name="professional_portfolio.pdf",
#                     mime="application/pdf"
#                 )
                
#             except Exception as e:
#                 st.error(f"PDF creation failed: {str(e)}")
#             finally:
#                 progress_bar.empty()

# if __name__ == "__main__":
#     main()










############## working with




import os
import io
import streamlit as st
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Configuration constants
MARGIN_TOP = 1.5 * cm
GAP_TITLE_IMAGE = 1 * cm
FONT_SIZE_TITLE = 25
PAGE_WIDTH, PAGE_HEIGHT = landscape(A4)
ROTATION_OPTIONS = [0, 90, 180, 270]
TITLE_COLOR = (0.2, 0.2, 0.2)

def create_pdf(images_data, progress_bar=None):
    """Create PDF with user-defined or optimized image dimensions."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    total_images = len(images_data)
    
    for idx, (img, title, rotation, custom_enabled, width_cm, height_cm) in enumerate(images_data, 1):
        try:
            # Apply rotation and convert to RGB
            if rotation != 0:
                img = img.rotate(rotation, expand=True)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate drawing dimensions
            if custom_enabled:
                img_draw_width = width_cm * cm
                img_draw_height = height_cm * cm
            else:
                # Auto-sizing logic
                img_width, img_height = img.size
                aspect_ratio = img_height / img_width
                max_available_height = PAGE_HEIGHT - MARGIN_TOP - GAP_TITLE_IMAGE - 3 * cm
                
                if img_height > img_width:  # Portrait
                    max_width = PAGE_WIDTH * 0.85
                    img_draw_width = min(max_width, PAGE_WIDTH)
                    img_draw_height = img_draw_width * aspect_ratio
                    
                    if img_draw_height > max_available_height:
                        img_draw_height = max_available_height
                        img_draw_width = img_draw_height / aspect_ratio
                else:  # Landscape
                    img_draw_height = min(max_available_height, max_available_height)
                    img_draw_width = img_draw_height / aspect_ratio
                    
                    if img_draw_width > PAGE_WIDTH:
                        img_draw_width = PAGE_WIDTH
                        img_draw_height = img_draw_width * aspect_ratio

            # Page setup
            c.setFillColorRGB(1, 1, 1)
            c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
            
            # Draw title
            c.setFont("Helvetica-Bold", FONT_SIZE_TITLE)
            c.setFillColorRGB(*TITLE_COLOR)
            title_width = c.stringWidth(title, "Helvetica-Bold", FONT_SIZE_TITLE)
            c.drawString((PAGE_WIDTH - title_width)/2, PAGE_HEIGHT - MARGIN_TOP + 0.5*cm, title)
            
            # Calculate image position
            img_x = (PAGE_WIDTH - img_draw_width) / 2
            img_y = PAGE_HEIGHT - MARGIN_TOP - GAP_TITLE_IMAGE - img_draw_height
            
            # Shadow effect
            c.setFillColorRGB(0.9, 0.9, 0.9)
            c.rect(img_x + 3, img_y - 3, img_draw_width, img_draw_height, fill=True)
            
            # Draw image
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG', quality=95)
            img_buffer.seek(0)
            c.drawImage(ImageReader(img_buffer), img_x, img_y, 
                       width=img_draw_width, height=img_draw_height)
            
            c.showPage()
            
            if progress_bar:
                progress_bar.progress(idx / total_images)
        except Exception as e:
            st.error(f"Error processing {title}: {str(e)}")
            continue
    
    c.save()
    buffer.seek(0)
    return buffer

def main():
    st.title("Image to PDF Converter with Custom Sizing")
    
    # Initialize session state
    session_keys = ['rotations', 'custom_enabled', 'custom_width', 'custom_height']
    for key in session_keys:
        if key not in st.session_state:
            st.session_state[key] = {}

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload images", 
        type=["png", "jpg", "jpeg"], 
        accept_multiple_files=True
    )
    
    # Image processing
    images_data = []
    if uploaded_files:
        st.subheader("Image Preparation")
        
        for file in uploaded_files:
            file_key = file.name
            try:
                img = Image.open(file)
                title = os.path.splitext(file.name)[0]
                
                col1, col2 = st.columns([2, 3])
                
                with col1:
                    current_rotation = st.session_state.rotations.get(file_key, 0)
                    preview_img = img.rotate(current_rotation, expand=True) if current_rotation != 0 else img
                    st.image(preview_img, caption=file.name, use_column_width=True)
                
                with col2:
                    # Rotation control
                    new_rotation = st.selectbox(
                        f"Rotation for {file.name}",
                        options=ROTATION_OPTIONS,
                        index=ROTATION_OPTIONS.index(current_rotation),
                        format_func=lambda x: f"{x}°",
                        key=f"rot_{file_key}"
                    )
                    st.session_state.rotations[file_key] = new_rotation
                    
                    # Custom size controls
                    custom_enabled = st.checkbox(
                        f"Custom size for {file.name}",
                        value=st.session_state.custom_enabled.get(file_key, False),
                        key=f"cust_en_{file_key}"
                    )
                    st.session_state.custom_enabled[file_key] = custom_enabled
                    
                    if custom_enabled:
                        default_width = st.session_state.custom_width.get(file_key, 10.0)
                        width_cm = st.number_input(
                            f"Width (cm) for {file.name}",
                            min_value=1.0,
                            max_value=29.7,
                            value=default_width,
                            step=0.5,
                            key=f"w_{file_key}"
                        )
                        st.session_state.custom_width[file_key] = width_cm
                        
                        default_height = st.session_state.custom_height.get(file_key, 10.0)
                        height_cm = st.number_input(
                            f"Height (cm) for {file.name}",
                            min_value=1.0,
                            max_value=21.0,
                            value=default_height,
                            step=0.5,
                            key=f"h_{file_key}"
                        )
                        st.session_state.custom_height[file_key] = height_cm
                    
                    # Display orientation info
                    final_width, final_height = preview_img.size
                    orientation = "Portrait" if final_height > final_width else "Landscape"
                    info_text = f"""
                    **Final Dimensions:** {final_width}×{final_height}  
                    **Orientation:** {orientation}  
                    **Rotation Applied:** {new_rotation}°
                    """
                    if custom_enabled:
                        info_text += f"\n**Custom Size:** {width_cm}cm × {height_cm}cm"
                    st.markdown(info_text)
                
                images_data.append((
                    img,
                    title,
                    new_rotation,
                    custom_enabled,
                    st.session_state.custom_width.get(file_key, 10.0),
                    st.session_state.custom_height.get(file_key, 10.0)
                ))
                
            except Exception as e:
                st.error(f"Error processing {file.name}: {str(e)}")
                continue

    # PDF generation
    if uploaded_files and st.button("Generate PDF"):
        with st.spinner("Creating PDF..."):
            progress_bar = st.progress(0)
            try:
                pdf_buffer = create_pdf(images_data, progress_bar)
                st.success("PDF creation completed!")
                
                st.download_button(
                    "📥 Download PDF",
                    data=pdf_buffer,
                    file_name="Generated.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"PDF creation failed: {str(e)}")
            finally:
                progress_bar.empty()

if __name__ == "__main__":
    main()












