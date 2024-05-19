import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import mysql.connector
import requests
import json

#DATAFRAME CREATION
mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='phonepe',
    )
mycursor = mydb.cursor(buffered=True)


#aggre_transaction_df
mycursor.execute('SELECT * FROM aggregated_transaction')
mydb.commit()
table1=mycursor.fetchall()

Aggre_transaction = pd.DataFrame(table1, columns=('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count', 'Transaction_amount'))

#aggre_user_df
mycursor.execute('SELECT * FROM aggregated_user')
mydb.commit()
table2 = mycursor.fetchall()

Aggre_user = pd.DataFrame(table2, columns=('States','Years','Quarter','Brands','Transaction_count','Percentage'))

#map_transaction_df
mycursor.execute('SELECT * FROM map_transaction')
mydb.commit()
table3=mycursor.fetchall()

map_transaction= pd.DataFrame(table3,columns=('States','Years','Quarter','Districts','Transaction_count','Transaction_amount'))

#map_user_df
mycursor.execute('SELECT * FROM map_user')
mydb.commit()
table4=mycursor.fetchall()

map_user=pd.DataFrame(table4,columns=('States','Years','Quarter','Districts','RegisteredUsers','AppOpens'))

#top_transaction_df
mycursor.execute('SELECT * FROM top_transaction')
mydb.commit()
table5 = mycursor.fetchall()
map_user = pd.DataFrame(table5, columns=('States','Years','Quarter','Pincodes','Transaction_count','Transaction_amount'))

#map_user_df
mycursor.execute('SELECT * FROM top_user')
mydb.commit()
table6 = mycursor.fetchall()
top_user = pd.DataFrame(table6, columns=('States','Years','Quarter','Pincodes','RegisteredUsers'))

#TRANSACTION YEAR BASED FUNCTION

def Transaction_amount_count_Y(df, year):
    
    tacy = df[df["Years"] == year]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1, col2 = st.columns(2)
    with col1:

        fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(fig_count)      
        
    col1,col2= st.columns(2)
    with col1:   
        
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1= json.loads(response.content)
        states_name=[]
        for feature in data1['features']:
            states_name.append(feature['properties']['ST_NM'])
            
        states_name.sort()
    
        fig_india_1= px.choropleth(tacyg, geojson=data1, locations= 'States', featureidkey= 'properties.ST_NM',
                              color='Transaction_amount', color_continuous_scale= 'rainbow',
                              range_color=(tacyg['Transaction_amount'].min(),tacyg['Transaction_amount'].max()),
                              hover_name='States', title=f'{year} TRANSACTION AMOUNT', fitbounds= 'locations',
                              height= 600, width= 600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
        
    with col2:

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations= 'States', featureidkey= 'properties.ST_NM',
                                color='Transaction_count', color_continuous_scale= 'rainbow',
                                range_color=(tacyg['Transaction_count'].min(),tacyg['Transaction_count'].max()),
                                hover_name='States', title=f'{year} TRANSACTION COUNT', fitbounds= 'locations',
                                height= 600, width= 600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
    
        return tacy
        
# TRANSACTION QUARTER BASED FUNCTION

def Transaction_amount_count_Y_Q(df, quarter):
        
    tacy = df[df['Quarter'] == quarter]
    tacy.reset_index(drop= True, inplace=True)

    tacyg= tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2= st.columns(2)

    with col1:
        
        fig_amount=px.bar(tacyg, x='States', y='Transaction_amount', title=f'{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT',
                        color_discrete_sequence=px.colors.sequential.Bluered)
        st.plotly_chart(fig_amount)
        
    with col2:
        fig_count= px.bar(tacyg, x='States', y='Transaction_count',title=f'{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT',
                        color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)
        
        col1,col2=st.columns(2)
    
    with col1:
                
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1=json.loads(response.content)
        states_name= []
        for feature in data1['features']:
            states_name.append(feature['properties']['ST_NM'])
            
        states_name.sort()

        
    col1,col2=st.columns(2)
   
    with col1:
        
        fig_india_1=px.choropleth(tacyg, geojson=data1, locations= 'States', featureidkey= 'properties.ST_NM',
                                color='Transaction_amount', color_continuous_scale= 'rainbow',
                                range_color=(tacyg['Transaction_amount'].min(),tacyg['Transaction_amount'].max()),
                                hover_name='States', title=f'{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT', fitbounds= 'locations',
                                height= 600, width= 600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations= 'States', featureidkey= 'properties.ST_NM',
                                color='Transaction_count', color_continuous_scale= 'rainbow',
                                range_color=(tacyg['Transaction_count'].min(),tacyg['Transaction_count'].max()),
                                hover_name='States', title=f'{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT', fitbounds= 'locations',
                                height= 600, width= 600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)
        
    return tacy
        
#TRANSACTION TYPE        
def Aggre_Tran_Transaction_type(df, state):
    
    tacy =df[df['States'] == state]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby('Transaction_type')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    
    with col1:
        fig_pie_1=px.pie(data_frame=tacyg, names='Transaction_type', values='Transaction_amount',
                        width= 600,title=f'{state.upper()} TRANSACTION AMOUNT', hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame=tacyg, names='Transaction_type', values='Transaction_count',
                        width= 600,title=f'{state.upper()} TRANSACTION COUNT', hole= 0.5)
        st.plotly_chart(fig_pie_2)

#AGGREGATED USER ANALYSIS_1
def Aggre_user_plot_1(df, year):
    aguy= df[df['Years']== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg=pd.DataFrame(aguy.groupby('Brands')['Transaction_count'].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x='Brands', y='Transaction_count', title= f'{year}   BRANDS AND TRANSACTION COUNT',
                    width= 900, color_discrete_sequence=px.colors.sequential.Bluered_r, hover_name='Brands')
    st.plotly_chart(fig_bar_1)
    
    return aguy

#AGGREGATED USER ANALYSIS_1
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df['Quarter']== quarter]
    aguyq.reset_index(drop= True, inplace= True)
    
    aguyqg=pd.DataFrame(aguyq.groupby('Brands')['Transaction_count'].sum())
    aguyqg.reset_index(inplace= True)


    fig_bar_1=px.bar(aguyqg, x='Brands', y='Transaction_count', title= f'{quarter} QUARTER, BRANDS AND TRANSACTION COUNT',
                        width=900, color_discrete_sequence=px.colors.sequential.Bluered_r, hover_name='Brands')
    st.plotly_chart(fig_bar_1)

    return aguyq

#AGGRE_USER_ANALYSIS_3
def Aggre_user_plot_3(df, state):
    auyqs=df[df['States'] == state]
    auyqs.reset_index(drop= True, inplace= True)
    
    fig_line_1=px.line(auyqs, x= 'Brands', y='Transaction_count', hover_name= 'Percentage',
                    title=f'{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE', width= 1000, markers=True)
    st.plotly_chart(fig_line_1)

#
#
def map_tran_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_tran_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

    

#streamlit part
st.set_page_config(layout='wide')
st.title('PHONEPE DATA VISUALIZATION AND EXPLORATION')

with st.sidebar:
    
    select = option_menu('Main Menu',['HOME','DATA EXPLORATION','TOP CHARTS'])
    
if select == 'HOME':
    pass
elif select == 'DATA EXPLORATION':
    
    tab1, tab2, tab3 = st.tabs(['Aggregated Analysis', 'Map Analysis', 'Top Analysis'])
    
    with tab1:
        
        method = st.radio('Select The Method',['Transaction Analysis', 'User Analysis'])
        
        if method == 'Transaction Analysis':
            
            col1,col2= st.columns(2)
            with col1:
                            
                years = st.slider('Select The Year', Aggre_transaction['Years'].min(),Aggre_transaction['Years'].max(),Aggre_transaction['Years'].min())
            Aggre_tran_tac_Y = Transaction_amount_count_Y(Aggre_transaction, years)
            
            
            
            col1,col2=st.columns(2)
            
            with col1:
                quarters= st.slider("Select the Quarter:",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y, quarters)      
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State",Aggre_tran_tac_Y["States"].unique())
                
            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y, states)
    
                
                
        elif method == 'User Analysis':
            
            col1,col2= st.columns(2)
            with col1:
                            
                years = st.slider('Select The Year', Aggre_user['Years'].min(),Aggre_user['Years'].max(),Aggre_user['Years'].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)
            
            col1,col2=st.columns(2)
            
            with col1:
                quarters= st.slider("Select the Quarter:",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y, quarters)      
            
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)
    
   
            
    with tab2:
        method_2=st.radio('Select The Method',['Map Transaction','Map User'])
        if method_2 == 'Map Transaction':
            # col1,col2= st.columns(2)
            # with col1:
                            
            #     years = st.slider('Select The Year', map_transaction['Years'].min(),map_transaction['Years'].max(),map_transaction['Years'].min())
            # map_tran_tac_Y = Transaction_amount_count_Y(map_transaction, years)
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.slider("**Select the Year_mi**", map_transaction["Years"].min(), map_transaction["Years"].max(),map_transaction["Years"].min())

            df_map_tran_Y= Transaction_amount_count_Y(map_transaction, years_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

            map_tran_plot_1(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.slider("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(),df_map_tran_Y["Quarter"].min())

            df_map_tran_Y_Q= Transaction_amount_count_Y_Q(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())            
            
            map_tran_plot_2(df_map_tran_Y_Q, state_m4)

            
        elif method_2 == 'Map User':
            pass
            
    with tab3:
        method_3=st.radio('Select The Method',['Top Transaction','Top User'])
        if method_3 == 'Top Transaction':
            pass

        elif method_3 =='Top User':
            pass

elif select =='TOP CHARTS':
    pass