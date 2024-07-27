import streamlit as st
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time
import io


from chartfunc import create_charts, plot_to_temp_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from markdown_pdf import MarkdownPdf, Section

from prompt import Prompt
# Load environment variables
load_dotenv()

# Configure API key
api_key = st.secrets["gemini_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title('Nagar Mitra Analytics')

st.header('Upload Metrics in JSON Format')

col1, col2 = st.columns(2)

metrics = st.file_uploader("Upload Workshop Metrics here", type="json")
# with col1:

if st.button('Generate Analysis'):
    try:
        if metrics is None :
            st.error("Please upload workshop metrics.")
            st.stop()

        # Read the uploaded files
        agency_metrics = json.load(metrics)
        # market_metrics = json.load(market_file)

        # Prompt for generative model
        prompt = Prompt

        # Generate the response from the model
        response = model.generate_content([prompt, str(agency_metrics)])
        analysis = response.text
        

        def stream_data():
            for word in analysis.split(" "):
                yield word + " "
                time.sleep(0.05)

        # Generate charts
        st.subheader('Visual Analysis')
        graphs = create_charts(agency_metrics)

        if graphs:
            # Display charts in Streamlit
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(graphs['time_cost_comparison'])
                st.plotly_chart(graphs['quality_metrics'])
                st.plotly_chart(graphs['resource_utilization'])
            with col2:
                st.plotly_chart(graphs['productivity_employee_metrics'])
                st.plotly_chart(graphs['financial_overview'])
                st.plotly_chart(graphs['workshop_schedule'])
                                
        

        st.subheader('Detailed Analysis and Recommendations')
        st.write_stream(stream_data())


            # col3, col4 = st.columns(2)
            # with col3:
            #     st.plotly_chart(bar_fig)
            # with col4:
            #     st.plotly_chart(line_fig)

            # Save charts as temporary files
            # chart_files = [
            #     plot_to_temp_file(agency_pie),
            #     plot_to_temp_file(market_pie),
            #     plot_to_temp_file(bar_fig),
            #     plot_to_temp_file(line_fig)
            # ]

        # Create PDF
        pdf = MarkdownPdf()
        pdf.add_section(Section(analysis, toc=False))
        pdf.save('output2.pdf')

        with open("output2.pdf", "rb") as pdf_file:
            st.download_button(
                label="Download as PDF",
                data=pdf_file,
                file_name="market_insights.pdf",
                mime="application/pdf"
            )

            # Clean up temporary files
            # for file in chart_files:
            #     os.unlink(file)

    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON format: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.error(str(e))  # Add this line to get more details about the error    

# with col2:
#     market_file = st.file_uploader("Upload Market Metrics JSON File", type="json")




# Usage:
# graphs = create_workshop_graphs('paste.txt')