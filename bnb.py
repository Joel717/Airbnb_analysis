#importing the necessary packages 
import streamlit as st 
import pandas as pd
import plotly.express as px 
import seaborn as sns
import matplotlib.pyplot as plt 
from streamlit_option_menu import option_menu
import os

#setting page configuration 
st.set_page_config(page_title='Airbnb Data Visualization',
                   layout='wide',
                   initial_sidebar_state='expanded')
st.title('Airbnb Data Visualization')

#creating a dataframe the csv 
df=pd.read_csv('C:\\Users\\devli\\airbnb\\airbnb.csv')

#setting a background
def setting_bg():
    local_image_path = "https://i.imgur.com/QuHF6NH.png"
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("{local_image_path}");
                background-size: cover;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

setting_bg()

#configuring a topbar
topbar=option_menu(
    menu_title=None,
    options=['Top Charts','Data Exploration','About'],
     icons=['house','file-bar-graph','search','exclamation-circle'],
    orientation='horizontal',
    default_index=0,
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f0f0", "color": "blue"},
        "icon": {"color": "yellow", "font-size": "16.5px"},
        "nav-link": {"font-size": "16.5px", "text-align": "left", "margin": "0px", "color": "black", "--hover-color": "#FF5A5F"},
        "nav-link-selected": {"background-color": "#fd5c63"},
    }
)
#creating EDA visualizations 
if topbar=='Top Charts':
    
    st.subheader('_Given below are few of the most insightful charts that can be derived from the Airbnb data_')
    st.divider()
    col1,col2=st.columns([1,1],gap="small")

    with col1:
        with st.container():

            st.markdown(''' <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                        <p style="font-size: 18px;">The below barchart shows the types and count of the Top 10 properties </div>''',unsafe_allow_html=True)
        property_type_counts = df['Property_type'].value_counts().head(10)
        fig = px.bar(property_type_counts, 
                    orientation='h', 
                    labels={'index': 'Property Type', 'value': 'Count'},
                    color=property_type_counts.index,
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    title="Top 10 Property Types available",
                    category_orders={"Property Type": 'additional_x_values'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        with st.container():

            st.markdown(''' <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                        <p style="font-size: 18px;">The below barchart shows the Types and count of the different room types available </div>''',unsafe_allow_html=True)
        room_type_counts=df['Room_type'].value_counts()
        fig1 = px.bar(room_type_counts,
                    title='Room Type Count',
                    color=room_type_counts.index,
                    labels={'index': 'Room_type', 'value': 'Count'}, 
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    st.divider()
    col3,col4=st.columns([1,1],gap="small")

    with col3:
        numeric_columns = df.select_dtypes(include=['int', 'float'])
        dfx = df[numeric_columns.columns]
        correlation_matrix = dfx.corr()
        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title('Correlation Heatmap')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    with col4:
        st.markdown('Correlation Heatmap')
        with st.container():

            st.markdown(''' <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                        <p style="font-size: 18px;">The heatmap visually represents the strength and direction of correlations between numerical features in the dataset.
                        <p style="font-size: 18px;">Darker colors signify stronger correlations, aiding quick identification of significant relationships.
                        <p style="font-size: 18px;">By examining the heatmap, you may identify features that are highly correlated. In some cases, highly correlated features might be candidates for feature selection or further investigation to avoid multicollinearity in statistical models.
                        </div>''',unsafe_allow_html=True)



    st.divider()

    col5,col6,col7=st.columns([1,1,1],gap='small')

    with col5:
        
        with st.container():

            st.markdown(''' <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                        <p style="font-size: 18px;">The table shows the hosts with the highest revenue and the number of propeties owned by them.
                        <p style="font-size: 18px;">It is also interesting to see through howmany listings that the host generate the revenue
                        <p style="font-size: 18px;">The pie chart visually represents the distribution of total prices among the top 10 hosts, highlighting the proportion of each host's contribution to the overall sum of prices in the dataset.
                        </div>''',unsafe_allow_html=True)

    with col6:
        top_hosts_count = df.groupby('Host_name').agg({'Price': 'sum', 'Property_type': 'count'}).reset_index().nlargest(10, 'Price')
        top_hosts_count = top_hosts_count.rename(columns={'Price': 'Total_Price', 'Property_type': 'Property_Count'})
        
        st.markdown(top_hosts_count.to_html(index=False), unsafe_allow_html=True)
    with col7:
        
        top_hosts_groupby = df.groupby('Host_name')['Price'].sum().reset_index().nlargest(10, 'Price')

        
        fig = px.pie(top_hosts_groupby, names='Host_name', values='Price', title='Top Hosts Total Price',
                    color='Host_name', color_discrete_sequence=px.colors.qualitative.Set3)

        
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    col8,col9=st.columns([1,1],gap='small')

    with col8:
        with st.container():

            st.markdown(''' <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                            <p style="font-size: 18px;">The pie chart shows the distribution of the cancellation policies  </div>''',unsafe_allow_html=True)
            
            cancellation_counts = df['Cancellation_policy'].value_counts().reset_index()
            cancellation_counts.columns = ['Cancellation_policy', 'Count']

            fig = px.pie(cancellation_counts, 
                        names='Cancellation_policy', 
                        values='Count', 
                        title='Distribution of Cancellation Policies')
            st.plotly_chart(fig, use_container_width=True)

    with col9:
        with st.container():

            st.markdown(''' <div style="background-color: #f0f0f0; padding: 15px; border-radius: 10px;">
                            <p style="font-size: 18px;">The 3D scatter plot visualizes the relationship between accommodation capacity ('Accomodates'), total bedrooms ('Total_bedrooms'), and price ('Price'), with each point representing a data entry in a three-dimensional space, and color indicating the price value.  </div>''',unsafe_allow_html=True)
            
            df1=df.drop(df[df['Price'] == 48842.0].index)
            fig = px.scatter_3d(df1, x='Accomodates', y='Total_bedrooms', z='Price',color='Price',
                                title='3D Scatter Plot: Accommodates, Total Bedrooms, and Price',
                                labels={'Accomodates': 'Accommodates', 'Total_bedrooms': 'Total Bedrooms', 'Price': 'Price'})
            st.plotly_chart(fig, use_container_width=True)

#creating interactive visualizations 
if topbar=='Data Exploration':
        st.markdown(" Explore more about the Airbnb data")
        
        
        country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))

        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    
        st.subheader("Price Analysis")
        
    
        col1,col2 = st.columns(2,gap='small')
            
        with col1:
                
            
            pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
            fig = px.bar(data_frame=pr_df,
                        x='Room_type',
                        y='Price',
                        color='Price',
                        title='Avg Price in each Room type'
                        )
            st.plotly_chart(fig,use_container_width=True)
            
            
            st.subheader("Availability Analysis")
            st.divider()        
            
            fig = px.box(data_frame=df.query(query),
                        x='Room_type',
                        y='Availability_365',
                        color='Room_type',
                        title='Availability by Room_type'
                        )
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
                
                
                country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
                fig = px.scatter_geo(data_frame=country_df,
                                            locations='Country',
                                            color= 'Price', 
                                            hover_data=['Price'],
                                            locationmode='country names',
                                            size='Price',
                                            title= 'Avg Price in each Country',
                                            color_continuous_scale='agsunset'
                                    )
                col2.plotly_chart(fig,use_container_width=True)
                
                
                st.markdown("#   ")
                st.markdown("#   ")
                st.divider()
        
                country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
                country_df.Availability_365 = country_df.Availability_365.astype(int)
                fig = px.scatter_geo(data_frame=country_df,
                                            locations='Country',
                                            color= 'Availability_365', 
                                            hover_data=['Availability_365'],
                                            locationmode='country names',
                                            size='Availability_365',
                                            title= 'Avg Availability in each Country',
                                            color_continuous_scale='agsunset'
                                    )
                st.plotly_chart(fig,use_container_width=True)
#creating an about section 

if topbar=='About': 
            st.subheader('About the creator:')
            st.markdown('The app is created by: Joel Gracelin ')
            st.markdown('This app is created as a part of Guvi Master Data Science course')
            st.markdown('Domain: Travel and Real Estate')
            st.markdown("Inspired from MongoDB sample data ")
            st.markdown("[Ghithub](https://github.com/Joel717)")