import streamlit as st
from PIL import Image
from st_pages import Page, Section, show_pages, add_page_title
from st_pages import show_pages_from_config


st.set_page_config(
    page_title='Home',
    page_icon='🎲'
)

#image_path = 'pngwing.com.png'
image = Image.open( 'pngwing.com.png' )
st.sidebar.image( image, width=230 )

st.sidebar.markdown( '# La Place Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Wagner Sobrinho and Comunidade DS' )

st.write( '# La Place Company Growth Dashboard' )

st.markdown(
    """
        Growth Dashboad foi construido para acompanhar as métricas de crescimento de Entregadores e Restaurantes.
        ### Como utilizar este Dashboard.
        - Visão Empresa
            - Visão Gerencial:   Métricas gerais de comportamento.
            - Visão Tática:      Indicadores semanais de crescimento.
            - Visão Geográfica:  Insights de geolocalização.
        - Visão Entregadores
            - Acompanhamento dos indicadores semanais de crescimento.
        - Visão Restaurantes
            - Acompanhamento dos indicadores semanais de crescimento dos restaurantes.
        ### Ask for help
        - Time de Data Science no Discord
            - wagnersobrinho    
    """)