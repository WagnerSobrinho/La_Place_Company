# Libraries
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# bibliotecas necessárias
import folium
import pandas as pd
import streamlit as st
from PIL import Image

from streamlit_folium import folium_static

st.set_page_config( page_title='Visão Empresa', page_icon='📈', layout='wide')

# =====================================================================================================
# Funções
#======================================================================================================
def country_maps ( df1 ):
    """ Esta função tem a responsabilidade de plotar um mapa
        Tipos de ações:
        1. Filtra as colunas 'City', 'Road_traffic_density', 'Delivery_location_latitude' e 'Delivery_location_longitude'
        2. Agrupar por 'City' e 'Road_traffic_density'
        3. Tirar a mediana
        4. Criar e plotar um mapa c/ marcadores
        
        Input: Dataframe
        Output: Mapa com as localizações de entrega         
    """
    df_mapa = ( df1[['City', 'Road_traffic_density', 'Delivery_location_latitude',
                   'Delivery_location_longitude' ]].groupby(['City', 'Road_traffic_density'])
                                                   .median()
                                                   .reset_index() )
    # Desenhar o mapa
    map = folium.Map( zoom_start=11 )
    for index, location_info in df_mapa.iterrows():
        folium.Marker( [location_info['Delivery_location_latitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']] ).add_to( map )
            
        folium_static( map, width=1024, height=600 )
    
        return None


def order_share_by_week( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de linha
        Tipos de ações:
        1. Dataframe 1 - Contar as entregas por semana
        2. Filtra as colunas 'ID', 'week_of_year'
        3. Agrupar por 'week_of_year'
        4. Contar as linhas
        5. Dataframe 2 - Contar os entregadores únicos por semana
        5. Filtra as colunas com os dados 'Delivery_person_ID', 'week_of_year'
        6. Agrupar por 'week_of_year'
        7. Contar as linhas com valores únicos
        8. Unir Dataframe 1 c/ Dataframe 2
        9. Divisão das entregas por semana pelos entregadores únicos por semana
        10.Desenhar e plotar um gráfico de linhas
                      
        Input: Dataframe
        Output: Gráfico de linhas         
    """    
    # Quantidade entregas por semana
    df_aux1 = df1[['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    # Quantidade de entregadores únicos por semana
    df_aux2 = df1[['Delivery_person_ID', 'week_of_year']].groupby( 'week_of_year').nunique().reset_index()
    # Unindo 2 dataframes
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
    # Divisão da entregas por semana pelo entregadores unicos por semana
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
            
    # Desenhar gráfico de linha
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )

    return fig


def order_by_week( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de linha
        Tipos de ações:
        1. Dataframe - Quantidade de pedidos por semana
        2. Criar a coluna de semana 'week_of_year'
        3. Filtra as colunas 'ID', 'week_of_year'
        4. Agrupar por 'week_of_year'
        5. Contar as linhas
        6. Desenhar e plotar um gráfico de linhas
                      
        Input: Dataframe
        Output: Gráfico de linhas         
    """
    # Criar a coluna de semana. Quantidade de pedidos por semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()              
    # Desenhar gráfico de linha
    fig = px.line( df_aux, x='week_of_year', y='ID' )

    return fig


def traffic_order_city( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de scatter
        Tipos de ações:
        1. Dataframe - Comparar volume de pedidos por cidade e tipo de trafego
        2. Filtra as colunas 'ID', 'City', 'Road_traffic_density'
        3. Agrupar por 'City' e 'Road_traffic_density'
        4. Contar as linhas
        5. Desenhar e plotar um gráfico de scatter
                      
        Input: Dataframe
        Output: Gráfico de scatter         
    """
    # Comparação do volume de pedidos por cidade e tipo de tráfego
    df_aux = ( df1[['ID', 'City', 'Road_traffic_density']].groupby(['City', 'Road_traffic_density'])                                                                                   .count()
                                                          .reset_index() )           
    # Desenhar gráfico scatter
    fig = px.scatter(df_aux, x='City', y='Road_traffic_density', size='ID', color='City')
    
    return fig        


def traffic_order_density( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de pizza
        Tipos de ações:
        1. Dataframe - Distribuição dos pedidos por tipo de tráfego
        2. Filtra as colunas 'ID', 'City', 'Road_traffic_density'
        3. Agrupar por 'Road_traffic_density'
        4. Contar as linhas
        5. Transfornmar em percentual
        6. Desenhar e plotar um gráfico de pizza
                      
        Input: Dataframe
        Output: Gráfico de pizza         
    """
    # Distribuição dos pedidos por tipo de tráfego
    df_aux = df1[['ID', 'Road_traffic_density']].groupby('Road_traffic_density').count().reset_index()
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()       
    # Desenhar gráfico de pizza
    fig = px.pie(df_aux, values='entregas_perc', names='Road_traffic_density')
    
    return fig
    

def order_metric( df1 ):
    """ Esta função tem a responsabilidade de plotar um gráfico de barras
        Tipos de ações:
        1. Dataframe - Quantidade de entregas por dia
        2. Filtra as colunas 'ID', 'Order_Date'
        3. Agrupar por 'Order_Date'
        4. Contar as linhas
        5. Desenhar e plotar um gráfico de barras
                      
        Input: Dataframe
        Output: Gráfico de barras         
    """
    cols = ['ID', 'Order_Date']
    # Seleção de linhas
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()            
    # Desenhar gráfico de barras
    fig = px.bar( df_aux, x='Order_Date', y='ID' )

    return fig
    
    
def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe
        Tipos de limpeza:
        1. Remoção dos dados NaN
        2. Mudança do tipo da coluna de dados
        3. Remoção dos espaços da variáveis de texto
        4. Formatação da coluna de datas
        5. Limpeza da coluna de tempo (remoção do texto da variável numérica)

        Input: Dataframe
        Output: Dataframe        
    """
    # 1. limpando linhas 'NaN' das colunas identificadas
    linhas_selecionadas = (df1['Delivery_person_Age'] != 'NaN ') 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Road_traffic_density'] != 'NaN ') 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['City'] != 'NaN ') 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['Festival'] != 'NaN ') 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    linhas_selecionadas = (df1['multiple_deliveries'] != 'NaN ')
    df1 = df1.loc[linhas_selecionadas, :].copy()
    
    # 2. convertando a colunas de texto para numero inteiro
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( 'int64' )
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( 'int64' )
    
    # 3. convertando a coluna Ratings de texto para numero decimal ( float )
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )
    
    # 4. convertando a coluna order_date de texto para data
    df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )    
      
    # 5. Removendo os espacos dentro de strings/texto/object
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    # 6. Limpando a coluna de time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype( 'int64' )

    return df1

# ====================================Inicio da estrutura lógica do código==============================
    
# ======================================
# Import dataset
# ======================================
df = pd.read_csv( 'train.csv' )

# ======================================
#Limpando os dados
# ======================================
df1 = clean_code( df )


# =======================================
# Barra Lateral
# =======================================
st.title( 'Marketplace - Visão Empresa' )

#image_path = 'pngwing.com.png'
image = Image.open( 'pngwing.com.png' )
st.sidebar.image( image, width=230 )

st.sidebar.markdown( '# La Place Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Selecione uma data limite' )

date_slider = st.sidebar.slider( 
    'Até qual valor?',
    value=pd.datetime( 2022, 4, 13 ),
    min_value=pd.datetime(2022, 2, 11 ),
    max_value=pd.datetime( 2022, 4, 6 ),
    format='DD-MM-YYYY' )

st.sidebar.markdown( """---""" )


traffic_options = st.sidebar.multiselect( 
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'], 
    default=['Low', 'Medium', 'High', 'Jam'] )

st.sidebar.markdown( """---""" )
st.sidebar.markdown( '### Powered by Wagner Sobrinho and Comunidade DS' )

# Filtro de data
linhas_selecionadas = df1['Order_Date'] <  date_slider 
df1 = df1.loc[linhas_selecionadas, :]

# Filtro de transito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]


# =======================================
# Layout no Streamlit
# =======================================
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográdica'] )

with tab1:
    with st.container():
        # Order Metric
        fig = order_metric( df1 )
        st.markdown( '### Order by Day' )
        st.plotly_chart(fig,use_container_width=True)        
            
    with st.container():
        # Order Metric
        col1, col2 = st.columns( 2 )
                    
        with col1:
            fig = traffic_order_density ( df1 )
            st.markdown('### Traffic Order Density')
            st.plotly_chart( fig, use_container_width=True )       
                                      
        with col2:
            fig = traffic_order_city ( df1 )
            st.markdown('### Traffic Order City')
            st.plotly_chart( fig, use_container_width=True )
            
with tab2:
    with st.container():
        # Order Metric
        fig = order_by_week ( df1 )
        st.markdown( '### Order by Week' )
        st.plotly_chart( fig, use_container_width=True )      
        
    with st.container():
        # Order Metric
        fig = order_share_by_week ( df1 )
        st.markdown( '### Order Share by Week' )
        st.plotly_chart( fig, use_container_width=True )        
        
with tab3:
    with st.container():
        st.markdown( '### Country Maps' )
        country_maps( df1 )
        