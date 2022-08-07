from st_aggrid import AgGrid
import streamlit as st
import pandas as pd
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport
from PIL import Image
import codecs
import streamlit.components.v1 as components
import sweetviz as sv

def st_display_sweetviz(report_html,width=1000,height=500):
	report_file = codecs.open(report_html,'r')
	page = report_file.read()
	components.html(page,width=width,height=height,scrolling=True)

st.set_page_config(layout = 'wide')

#Add a logo to the sidebar (optional)
logo = Image.open(r'C:\Users\david\Desktop\2020-09-20 16.43.22.jpg')
st.sidebar.image(logo, width=120)

#add an expander to provide some information about the app
with st.sidebar.expander("About the app"):
    st.write("""
    This data profiling app was built by David Moniz using Streamlit and utilizing Sweetviz and Pandas Profiling packages You can use the app to quickly generate a comprehensive data profiling and EDA report without the need to write any python code. \n\nThe app has the minimum mode (recommended) and the complete code. The complete code includes more sophisticated analysis such as correlation analysis or interactions between variables which may requires expensive computations.
    """)

#add an app title
st.markdown(""" <style> .font{font-size:30px ; font-family: 'Cooper Black; color: #FF9633;}
    </style>""", unsafe_allow_html=True)
st.markdown('<p class="font">Import your data and generate an Exploratory Data Analysis report easily...</p>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload your CSV file:", type = ['csv'])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    option1 = st.sidebar.radio(
        "What variables do you want to include in the report?",
        ('All variables', 'A subset of variables'))

    if option1 == 'All variables':
        df = df

    elif option1 == 'A subset of variables':
        var_list = list(df.columns)
        option3 = st.sidebar.multiselect(
            'Select variable(s) you want to include in the report.', var_list)
        df = df[option3]

    grid_response = AgGrid(
       df,
       editable = True,
       height = 300,
       width = '100%',
    )

    updated = grid_response['data']
    df1 = pd.DataFrame(updated)

    if st.button('Generate Pandas Profiling Report'):
        profile = ProfileReport(df)
        st_profile_report(profile)
    elif st.button('Generate Sweetviz Report'):
        report = sv.analyze(df)
        report.show_html()
        st_display_sweetviz("SWEETVIZ_REPORT.html")
