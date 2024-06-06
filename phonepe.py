import streamlit as st
import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from PIL import Image

#DataFrame Creation

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

#aggre_insurance_df

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()
Aggregated_insurance=pd.DataFrame(table1,columns= ("States","Years","Quarter","TransactionType",
                                                   "TransactionCount","TransactionAmount"))



#aggre_transaction_df

#DataFrame Creation

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()
Aggregated_transaction=pd.DataFrame(table2,columns= ("States","Years","Quarter","TransactionType",
                                                       "TransactionCount","TransactionAmount"))

#aggre_user_df

#DataFrame Creation

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()
Aggregated_user=pd.DataFrame(table3,columns= ("States","Years","Quarter","Brands",
                                                       "TransactionCount","Percentage"))



#map insurance df

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

cursor.execute("SELECT * FROM map_insur_details")
mydb.commit()
table4=cursor.fetchall()
Map_insurance=pd.DataFrame(table4,columns= ("States","Years","Quarter","Districts",
                                                       "TransactionCount","TransactionAmount"))


#map transaction df

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()
Map_transaction=pd.DataFrame(table5,columns= ("States","Years","Quarter","Districts",
                                                       "TransactionCount","TransactionAmount"))

#map user df

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()
Map_user=pd.DataFrame(table6,columns= ("States","Years","Quarter","Districts",
                                                       "RegisteredUsers","AppOpens"))


#top insurance df

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

cursor.execute("SELECT * FROM top_insur_details")
mydb.commit()
table7=cursor.fetchall()
Top_insurance=pd.DataFrame(table7,columns= ("States","Years","Quarter","Pincodes",
                                                       "TransactionCount","TransactionAmount"))

#top transaction

mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

cursor.execute("SELECT * FROM top_trans_details")
mydb.commit()
table8=cursor.fetchall()
Top_transaction=pd.DataFrame(table8,columns= ("States","Years","Quarter","Pincodes",
                                                       "TransactionCount","TransactionAmount"))


#top User df
mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_details",
                      password="srmukhi15")

cursor=mydb.cursor()

cursor.execute("SELECT * FROM top_user_details")
mydb.commit()
table9=cursor.fetchall()
Top_user=pd.DataFrame(table9,columns= ("States","Years","Quarter","Pincodes",
                                                       "RegisteredUsers"))



def Transaction_Amount_Count_Year(df,year):

    trac_year=df[df["Years"]==year]
    trac_year.reset_index(drop=True,inplace=True)
    
    trans_gr=trac_year.groupby("States")[["TransactionCount","TransactionAmount"]].sum()
    trans_gr.reset_index(inplace=True)
           
    fig_amount=px.bar(trans_gr,x="States",y="TransactionAmount",title=f"{year} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=700,width=600)

    st.plotly_chart(fig_amount)    

    fig_count=px.bar(trans_gr,x="States",y="TransactionCount",title=f"{year}TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Burg,height=650,width=600)

    st.plotly_chart(fig_count)
    
    url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response= requests.get(url)
    data1= json.loads(response.content)
    states_name= []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
        
    states_name.sort()    

    
    fig_india_1= px.choropleth(trans_gr, geojson= data1, locations= "States",featureidkey= "properties.ST_NM",
                            color= "TransactionAmount", color_continuous_scale= "Rainbow",
                            range_color= (trans_gr["TransactionAmount"].min(),trans_gr["TransactionAmount"].max()),
                            hover_name= "States", title= f"{year} TRANSACTIONAMOUNT", fitbounds= "locations",
                            height= 700)

    fig_india_1.update_geos(visible=False)

    st.plotly_chart(fig_india_1)
    
    fig_india_2= px.choropleth(trans_gr, geojson= data1, locations= "States",featureidkey= "properties.ST_NM",
                            color= "TransactionCount", color_continuous_scale= "Rainbow",
                            range_color= (trans_gr["TransactionCount"].min(),trans_gr["TransactionCount"].max()),
                            hover_name= "States", title= f"{year} TRANSACTIONCOUNT", fitbounds= "locations",height=700
                            )
    
    fig_india_2.update_geos(visible=False)

    st.plotly_chart(fig_india_2)
    
    return trac_year

def Transaction_Amount_Count_Year_Quarter(df,quarter):

    trac_year=df[df["Quarter"]==quarter]
    trac_year.reset_index(drop=True,inplace=True)

    trans_gr=trac_year.groupby("States")[["TransactionCount","TransactionAmount"]].sum()
    trans_gr.reset_index(inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:
    
        fig_amount=px.bar(trans_gr,x="States",y="TransactionAmount",title=f"{trac_year['Years'].min()}YEAR{quarter}QUARTER TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600)

        st.plotly_chart(fig_amount)
        
    with col2:    

        fig_count=px.bar(trans_gr,x="States",y="TransactionCount",title=f"{trac_year['Years'].min()}YEAR{quarter}QUARTER TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Cividis_r,height=600,width=600)

        st.plotly_chart(fig_count)
        
    col1,col2 = st.columns(2)
    
    with col1:
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
            
        states_name.sort()    

        fig_india_1= px.choropleth(trans_gr, geojson= data1, locations= "States",featureidkey= "properties.ST_NM",
                                color= "TransactionAmount", color_continuous_scale= "Rainbow",
                                range_color= (trans_gr["TransactionAmount"].min(),trans_gr["TransactionAmount"].max()),
                                hover_name= "States", title= f"{trac_year['Years'].min()} YEAR{quarter}QUARTER TRANSACTIONAMOUNT", fitbounds= "locations",
                                height= 500)
        
        fig_india_1.update_geos(visible=False)

        st.plotly_chart(fig_india_1)
    with col2:
            
        
        fig_india_2= px.choropleth(trans_gr, geojson= data1, locations= "States",featureidkey= "properties.ST_NM",
                                color= "TransactionCount", color_continuous_scale= "Rainbow",
                                range_color= (trans_gr["TransactionCount"].min(),trans_gr["TransactionCount"].max()),
                                hover_name= "States", title= f"{trac_year['Years'].min()}YEAR {quarter}QUARTER TRANSACTIONCOUNT", fitbounds= "locations",
                                height= 500)
        
        fig_india_2.update_geos(visible=False)

        st.plotly_chart(fig_india_2)
        
    return trac_year
        

def Aggre_Trans_Type(df,state):

    trac_year=aggs_year[aggs_year["States"] == state]
    trac_year.reset_index(drop=True,inplace=True)

    trans_gr=trac_year.groupby("TransactionType")[["TransactionCount","TransactionAmount"]].sum()
    trans_gr.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        fig_pie1 = px.pie(data_frame=trans_gr,names="TransactionType",values="TransactionAmount",
                    width=600,title=f"{state.upper()} TARANSACTION AMOUNT",hole=0.5)

    st.plotly_chart(fig_pie1)
    
    with col2:

        fig_pie2 = px.pie(data_frame=trans_gr,names="TransactionType",values="TransactionCount",
                    width=600,title=f"{state.upper()} TARANSACTION COUNT",hole=0.5)

    st.plotly_chart(fig_pie2)
    

def agg_user_year_plot1(df,year):

    agg_user_year = df[df["Years"] == year]
    agg_user_year.reset_index(drop=True,inplace=True)

    agg_user_group=pd.DataFrame(agg_user_year.groupby("Brands")[["TransactionCount","Percentage"]].sum())
    agg_user_group.reset_index(inplace=True)

    fig_bar_1 = px.bar(agg_user_group,x="Brands",y="TransactionCount",title=f"{year} BRANDS AND TRANSACTIONCOUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.Turbo_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return agg_user_year


def Aggre_user_plot2_quarter(df,quarter):
    
    agg_user_year_Q = df[df["Quarter"] == quarter]
    agg_user_year_Q.reset_index(drop=True,inplace=True)
    agguyq = pd.DataFrame(agg_user_year_Q.groupby("Brands")["TransactionCount"].sum())
    agguyq.reset_index(inplace=True)

    fig_bar_Q = px.bar(agguyq,x="Brands",y="TransactionCount",title= f"{quarter} QUARTER BRANDS AND TRANSACTIONCOUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.Turbo_r)
    st.plotly_chart(fig_bar_Q)
    
    return agg_user_year_Q


def Aggre_user_plot3(df,state):
    auyqstate =df[df["States"] == state]
    auyqstate.reset_index(drop=True,inplace=True)
    fig_line_1=px.line(auyqstate,x= "Brands",y= "TransactionCount",hover_data="Percentage",
                    title=f"{state}BRANDS,TRANSACTION COUNT,PERCENTAGE",width=1000,markers=True)
    st.plotly_chart(fig_line_1)
    
#Map_insurance_districts
def Map_insur_District(df,state):

    trac_year=df[df["States"] == state]
    trac_year.reset_index(drop=True,inplace=True)

    trans_gr=trac_year.groupby("Districts")[["TransactionCount","TransactionAmount"]].sum()
    trans_gr.reset_index(inplace=True)

    fig_bar1 = px.bar(trans_gr, x="TransactionAmount", y="Districts",orientation='h',height=600,
                      title= f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT",color_discrete_sequence= px.colors.sequential.Mint_r)

    st.plotly_chart(fig_bar1)

    fig_bar2=px.bar(trans_gr, x="TransactionAmount", y="Districts",orientation='h',height=600,
                      title= f"{state.upper()} DISTRICTS AND TRANSACTION AMOUNT",color_discrete_sequence= px.colors.sequential.Greens_r)
    st.plotly_chart(fig_bar2)
    
def map_user_plot_1(df,year):
    map_user_year=df[df["Years"] == 2020]
    map_user_year.reset_index(drop=True,inplace=True)
    map_user_group=map_user_year.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    map_user_group.reset_index(inplace=True)
    fig_line_1=px.line(map_user_group,x= "States",y= ["RegisteredUsers","AppOpens"],
                        title=f"{year} REGISTEREDUSERS APPOPENS",width=1000,height= 800,markers=True)
    st.plotly_chart(fig_line_1)
    return map_user_year

#Map_user_plot_2
def map_user_plot_2(df,quarter):
    map_user_quarter=df[df["Quarter"] == quarter]
    map_user_quarter.reset_index(drop=True,inplace=True) 
    map_user_qg=map_user_quarter.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    map_user_qg.reset_index(inplace=True)
    fig_line_2=px.line(map_user_qg,x= "States",y= ["RegisteredUsers","AppOpens"],
                        title=f"{df['Years'].min()} YEAR {quarter} REGISTEREDUSERS APPOPENS",width=800,height= 800,markers=True,
                        color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_2)
    
    return map_user_quarter


# Map_user_analysis_plot3

def map_user_plot3(df,states):   
    map_user_states = df[df["States"] == states]
    map_user_states.reset_index(drop=True,inplace=True)
    
    col1,col2 = st.columns(2)
    with col1:       

        fig_map_user_bar1=px.bar(map_user_states,x="RegisteredUsers",y="Districts",orientation='h',
                                title=f"{states.upper()} REGISTRED USER",height=800,color_discrete_sequence= px.colors.sequential.Jet)
        st.plotly_chart(fig_map_user_bar1)
        
        
    with col2:
        
        fig_map_user_bar2=px.bar(map_user_states,x="AppOpens",y="Districts",orientation='h',
                                title=f"{states.upper()} AppOpens",height=800,color_discrete_sequence= px.colors.sequential.Emrld)
        st.plotly_chart(fig_map_user_bar2)

#Top_Insurance_plot1
def Top_insur_plot1(df,state):
    Top_insur_quarter=df[df["States"] == state]
    Top_insur_quarter.reset_index(drop=True,inplace=True)
    
    col1,col2= st.columns(2)
    with col1:
        
        fig_top_insur_bar1=px.bar(Top_insur_quarter,x= "Quarter",y="TransactionAmount",hover_data="Pincodes",
                                    title="TRANSACTION_AMOUNT",height=800,color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar1)
    with col2:    
        
        fig_top_insur_bar2=px.bar(Top_insur_quarter,x= "Quarter",y="TransactionCount",hover_data="Pincodes",
                                    title="TRANSACTION_COUNT",height=800,color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar2)
        
def Top_user_plot1(df,year):
    Top_user_year = Top_user[Top_user["Years"] == 2020]
    Top_user_year.reset_index(drop=True,inplace=True)


    Top_user_group=pd.DataFrame(Top_user_year.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    Top_user_group.reset_index(inplace=True)
    
    fig_top_plot_1 = px.bar(Top_user_group,x="States",y="RegisteredUsers",color="Quarter",
                            width=1000,height=800,color_discrete_sequence=px.colors.sequential.Darkmint_r,hover_name="States",
                            title=f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)
    
    return Top_user_year
    
def top_u_plot2(df,state):
    topuy=df[df["States"] == state]
    topuy.reset_index(drop=True,inplace=True)

    fig_top_user_plot2=px.bar(topuy,x="Quarter",y="RegisteredUsers",title="REGISTEREDUSERS,PINCODE,QUARTER",
                            width=1000,height=800,color="RegisteredUsers",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Oranges)
    st.plotly_chart(fig_top_user_plot2)
        
#Top chart Queries


def topcharts_trans(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_details",
                        password="srmukhi15")
    cursor=mydb.cursor()

    #plot1
    query1=f'''select states,sum(transactionamount)as transactionamount from 
                {table_name}
                group by states
                order by transactionamount desc
                limit 10;'''
    cursor.execute(query1)     

    table_1=cursor.fetchall()
    mydb.commit()


    df_1=pd.DataFrame(table_1,columns=("States","TransactionAmount")) 
    
    col1,col2=st.columns(2)
    with col1:

        fig_que1=px.bar(df_1,x="States",y="TransactionAmount",title="TOP 10 STATES OF TRANSACTION AMOUNT",hover_name="States",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600)

        st.plotly_chart(fig_que1)


    #plot2

    query2=f'''select states,sum(transactionamount)as transactionamount from 
                {table_name}
                group by states
                order by transactionamount 
                limit 10;'''
    cursor.execute(query2)     

    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("States","TransactionAmount")) 
    
    with col2:

        fig_que2=px.bar(df_2,x="States",y="TransactionAmount",title="LAST 10 STATES OF TRANSACTION AMOUNT",hover_name="States",color_discrete_sequence=px.colors.sequential.Oranges_r,
                        height=600,width=600)

        st.plotly_chart(fig_que2)
        
    #plot3
    query3=f'''select states,avg(transactionamount)as transactionamount from 
                {table_name}
                group by states
                order by transactionamount ;'''
    cursor.execute(query3)     

    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("States","TransactionAmount")) 

    fig_que3=px.bar(df_3,x="TransactionAmount",y="States",title="AVERAGE OF TRANSACTION AMOUNT",hover_name="States",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=800,width=1000)

    st.plotly_chart(fig_que3)
    
 #TRANSACTION COUNT   
    
def topcharts_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_details",
                        password="srmukhi15")
    cursor=mydb.cursor()

    #plot1
    query1=f'''select states,sum(transactioncount)as transactioncount from 
                {table_name}
                group by states
                order by transactioncount desc
                limit 10;'''
    cursor.execute(query1)     

    table_1=cursor.fetchall()
    mydb.commit()


    df_1=pd.DataFrame(table_1,columns=("States","Transactioncount")) 

    fig_que1=px.bar(df_1,x="States",y="Transactioncount",title="TOP 10 STATES OF TRANSACTION COUNT",hover_name="States",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600)

    st.plotly_chart(fig_que1)


    #plot2

    query2=f'''select states,sum(transactioncount)as transactioncount from 
                {table_name}
                group by states
                order by transactioncount 
                limit 10;'''
    cursor.execute(query2)     

    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("States","TransactionCount")) 

    fig_que2=px.bar(df_2,x="States",y="TransactionCount",title="LAST 10 STATES OF TRANSACTION COUNT",hover_name="States",color_discrete_sequence=px.colors.sequential.Oranges_r,height=600,width=600)

    st.plotly_chart(fig_que2)
    
    #plot3
    query3=f'''select states,avg(transactioncount)as transactioncount from 
                {table_name}
                group by states
                order by transactioncount ;'''
    cursor.execute(query3)     

    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("States","TransactionCount")) 

    fig_que3=px.bar(df_3,x="TransactionCount",y="States",title="AVERAGE OF TRANSACTION COUNT",hover_name="States",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=600,width=600)

    st.plotly_chart(fig_que3)
    
#registered users

def topcharts_registeredusers(table_name,state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_details",
                        password="srmukhi15")
    cursor=mydb.cursor()

    #plot1
    query1=f'''select districts, sum(registeredusers) as registeredusers from {table_name}
                where states = '{state}'
                group by districts
                order by registeredusers desc
                limit 10;'''
                
    cursor.execute(query1)     

    table_1=cursor.fetchall()
    mydb.commit()


    df_1=pd.DataFrame(table_1,columns=("districts","registeredusers")) 

    fig_que1=px.bar(df_1,x="districts",y="registeredusers",title="TOP 10 REGISTEREDUSERS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600)

    st.plotly_chart(fig_que1)


    #plot2
    
    query2=f'''select districts, sum(registeredusers) as registeredusers from {table_name}
                where states = '{state}'
                group by districts
                order by registeredusers 
                limit 10;'''
                
    cursor.execute(query2)     

    table_2=cursor.fetchall()
    mydb.commit()


    df_2=pd.DataFrame(table_2,columns=("districts","registeredusers")) 

    fig_que2=px.bar(df_2,x="districts",y="registeredusers",title="LAST 10 REGISTEREDUSERS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600)

    st.plotly_chart(fig_que2)

    #plot3
    query3=f'''select districts, avg(registeredusers) as registeredusers from {table_name}
                where states = '{state}'
                group by districts
                order by registeredusers;'''
    cursor.execute(query3)     

    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("districts","registeredusers")) 

    fig_que3=px.bar(df_3,x="registeredusers",y="districts",title="AVERAGE OF REGISTEREDUSERS",hover_name="districts",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=600,width=600)

    st.plotly_chart(fig_que3)
    
    
#APPOPENS    
def topcharts_appopens(table_name,state):
    
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_details",
                        password="srmukhi15")
    cursor=mydb.cursor()

    #plot1
    query1=f'''select districts, sum(appopens) as appopens from {table_name}
                where states = '{state}'
                group by districts
                order by appopens desc
                limit 10;'''
                
    cursor.execute(query1)     

    table_1=cursor.fetchall()
    mydb.commit()


    df_1=pd.DataFrame(table_1,columns=("districts","appopens")) 

    fig_que1=px.bar(df_1,x="districts",y="appopens",title="TOP 10 APPOPENS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600)

    st.plotly_chart(fig_que1)


    #plot2

    query2=f'''select districts, sum(appopens) as appopens from {table_name}
                where states = '{state}'
                group by districts
                order by appopens 
                limit 10;'''
                
    cursor.execute(query2)     

    table_2=cursor.fetchall()
    mydb.commit()


    df_2=pd.DataFrame(table_2,columns=("districts","appopens")) 

    fig_que2=px.bar(df_2,x="districts",y="appopens",title="LAST 10 REGISTEREDUSERS",hover_name="districts",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600)

    st.plotly_chart(fig_que2)

    #plot3
    query3=f'''select districts, avg(appopens) as appopens from {table_name}
                where states = '{state}'
                group by districts
                order by appopens;'''
    cursor.execute(query3)     

    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("districts","appopens")) 

    fig_que3=px.bar(df_3,x="appopens",y="districts",title="AVERAGE OF REGISTEREDUSERS",hover_name="districts",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=600,width=600)

    st.plotly_chart(fig_que3)

#topuser

def topcharts_users(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_details",
                        password="srmukhi15")
    cursor=mydb.cursor()

    #plot1
    query1=f'''select states,sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10; '''
    cursor.execute(query1)     

    table_1=cursor.fetchall()
    mydb.commit()


    df_1=pd.DataFrame(table_1,columns=("States","registeredusers")) 

    fig_que1=px.bar(df_1,x="States",y="registeredusers",title="TOP 10 REGISTEREDUSERS",hover_name="States",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=600,width=600)

    st.plotly_chart(fig_que1)


    #plot2

    query2=f''' select states,sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers 
                limit 10;'''
    cursor.execute(query2)     

    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2,columns=("States","registeredusers")) 

    fig_que2=px.bar(df_2,x="States",y="registeredusers",title="LAST 10 REGISTEREDUSERS",hover_name="States",color_discrete_sequence=px.colors.sequential.Oranges_r,height=600,width=600)

    st.plotly_chart(fig_que2)
    
    #plot3
    query3=f'''select states,avg(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers;'''
                
    cursor.execute(query3)     

    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3,columns=("States","registeredusers")) 

    fig_que3=px.bar(df_3,x="registeredusers",y="States",title="AVERAGE OF REGISTEREDUSERS",hover_name="States",orientation="h",
                    color_discrete_sequence=px.colors.sequential.Darkmint_r,height=600,width=600)

    st.plotly_chart(fig_que3)

    
    
    


#Streamlit Part

st.set_page_config(page_title="PhonePe Visualization",layout="wide")
page_bg_img='''
<style>
[data-testid="stAppViewContainer"]{
        background-color:#645F5F;   
}
</style>'''
st.markdown(page_bg_img,unsafe_allow_html=True)
st.title(":blue[PhonePe Pulse Data Insights]")
st.subheader(":white[This is a User-Friendly Tool to know the insights about PhonePe]")

select = option_menu(
            menu_title = None,
            options = ["About","Analysis","Insights"],
            icons =["house","map","bar-chart"],
            default_index=0,
            orientation="horizontal",
            styles={"container": {"padding": "0!important", "background-color": "black","size":"cover", "width": "100%"},
                    "icon": {"color": "#FF5733", "font-size": "20px"},
                    "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#60645F"},
                    "nav-link-selected": {"background-color": "#C70039"}})

if select=="About" :
    col1, col2 = st.columns(2)
    with col1:
                st.header("**PhonePe**")
                st.subheader("_India's Best Transaction App_")
                st.write("""_PhonePe is a digital wallet and mobile payment platform in India.It uses the Unified Payment Interface (UPI) system to allow users to send and receive money recharge mobile, DTH, data cards,make utility payments,pay at shops,invest in tax saving funds,buy insurance, mutual funds and digital gold._""")
                st.write("****FEATURES****")
                st.write("   **- Fund Transfer**")
                st.write("   **- Payment to Merchant**")
                st.write("   **- Recharge and Bill payments**")
                st.write("   **- Autopay of Bills**")
                st.write("   **- Cashback and Rewards and much more**")
                st.link_button(":violet[**DOWNLOAD THE APP NOW**]", "https://www.phonepe.com/app-download/")
        
    with col2:
                st.subheader("Video about PhonePe")
                st.video("https://youtu.be/aXnNA4mv1dU?si=HnSu_ETm4X29Lrvf")
                st.write("***To know more about PhonePe click below***")
                st.link_button(":violet[**PhonePe**]", "https://www.phonepe.com/")

elif select=="Analysis":
    
    tab1,tab2,tab3=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"]) 
    
    with tab1:
        
        method=st.radio("SELECT THE METHOD",["Insurance Analysis","Transaction Analysis","User Analysis"])
        
        if method=="Insurance Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                
               years=st.slider("Select the Year",Aggregated_insurance["Years"].min(),Aggregated_insurance["Years"].max(),Aggregated_insurance["Years"].min())
            tac_year=Transaction_Amount_Count_Year(Aggregated_insurance,years)
            col1,col2 = st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter",tac_year["Quarter"].min(),tac_year["Quarter"].max(),tac_year["Quarter"].min())
                 
            Transaction_Amount_Count_Year_Quarter(tac_year,quarters)
                                         
            
        elif method=="Transaction Analysis":
            
            col1,col2=st.columns(2)
            with col1:
                
               years=st.slider("Select the Year",Aggregated_transaction["Years"].min(),Aggregated_transaction["Years"].max(),Aggregated_insurance["Years"].min())
            aggs_year=Transaction_Amount_Count_Year(Aggregated_transaction,years)
            
            col1,col2=st.columns(2)
            
            with col1:
                states1=st.selectbox("Select the States", aggs_year["States"].unique())
            Aggre_Trans_Type(aggs_year,states1)
    

           
            col1,col2 = st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter",aggs_year["Quarter"].min(),aggs_year["Quarter"].max(),aggs_year["Quarter"].min())
                 
            aggs_year_quarter=Transaction_Amount_Count_Year_Quarter(aggs_year,quarters)
            
            col1,col2=st.columns(2)
            
            with col1:
                states1=st.selectbox("Select the States_Type", aggs_year_quarter["States"].unique())
            Aggre_Trans_Type(aggs_year_quarter,states1)     
            
        elif method=="User Analysis":
            col1,col2=st.columns(2)
            with col1:
                
               years=st.slider("Select the Year",Aggregated_user["Years"].min(),Aggregated_user["Years"].max(),Aggregated_user["Years"].min())
            Aggre_User_Year=agg_user_year_plot1(Aggregated_user,years)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter",Aggre_User_Year["Quarter"].min(),Aggre_User_Year["Quarter"].max(),Aggre_User_Year["Quarter"].min())
                 
            aggs_user_quarter=Aggre_user_plot2_quarter(Aggre_User_Year,quarters)
            
            
            col1,col2=st.columns(2)
            
            
            with col1:
                stat1 = st.selectbox("Select the Type_state", aggs_user_quarter['States'].unique())
            Aggre_user_plot3(aggs_user_quarter,stat1)            
            
            
    with tab2:
    
        method2 =st.radio("SELECT THE METHOD",["MAP INSURANCE","MAP TRANSACTION","MAP USER"])    
    
        if method2=="MAP INSURANCE" :
            
            col1,col2=st.columns(2)
            with col1:
                
               mapyear=st.slider("Select the map_year",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            map_insur_trac_Y=Transaction_Amount_Count_Year(Map_insurance,mapyear)
            
            col1,col2=st.columns(2)
            
            with col1:
                states1=st.selectbox("Select the Type",map_insur_trac_Y["States"].unique())
            Map_insur_District(map_insur_trac_Y,states1)
            
  
            col1,col2 = st.columns(2)
            with col1:
                quartersmap=st.slider("Select the Map_Quaters",map_insur_trac_Y["Quarter"].min(),map_insur_trac_Y["Quarter"].max(),map_insur_trac_Y["Quarter"].min())
            map_insur_quarter=Transaction_Amount_Count_Year_Quarter(map_insur_trac_Y,quartersmap)
            
            col1,col2=st.columns(2)
            
            with col1:
                states1=st.selectbox("Select the States", map_insur_quarter["States"].unique())
            Map_insur_District(map_insur_quarter,states1)     
            
              
            
        elif method2=="MAP TRANSACTION":
            col1,col2=st.columns(2)
            with col1:
                
               mapyear=st.slider("Select the Map_Year",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            map_tran_trac_Y=Transaction_Amount_Count_Year(Map_transaction,mapyear)
            
            col1,col2=st.columns(2)
            
            with col1:
                states1=st.selectbox("Select ",map_tran_trac_Y["States"].unique())
            Map_insur_District(map_tran_trac_Y,states1)
            
  
            col1,col2 = st.columns(2)
            with col1:
                quarters=st.slider("Select the Map_Quarter",map_tran_trac_Y["Quarter"].min(),map_tran_trac_Y["Quarter"].max(),map_tran_trac_Y["Quarter"].min())
            map_trans_quarter=Transaction_Amount_Count_Year_Quarter(map_tran_trac_Y,quarters)
            
            col1,col2=st.columns(2)
            
            with col1:
                states1=st.selectbox("Select the Map_State", map_trans_quarter["States"].unique())
            Map_insur_District(map_trans_quarter,states1)     
            
        elif method2=="MAP USER":
            col1,col2=st.columns(2)
            with col1:
                
               mapyear=st.slider("Select the Map_Year",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_year=map_user_plot_1(Map_user,mapyear)
            
            col1,col2 = st.columns(2)
            with col1:
                quarters=st.slider("Select the Map_User_Quarter",map_user_year["Quarter"].min(),map_user_year["Quarter"].max(),map_user_year["Quarter"].min())
            map_user_quarter=map_user_plot_2(map_user_year,quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("select the state_mapuser",map_user_quarter["States"].unique())
            map_user_plot3(map_user_quarter,states)    
            
            
            
    with tab3:
    
        method3 =st.radio("SELECT THE METHOD",["TOP INSURANCE","TOP TRANSACTION","TOP USER"])    
    
        if method3=="TOP INSURANCE" :
            col1,col2=st.columns(2)
            with col1:
                
               topyear=st.slider("Select the top_year",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            top_insur_trac_Y=Transaction_Amount_Count_Year(Top_insurance,topyear)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("select the state_Topinsur",top_insur_trac_Y["States"].unique())
            Top_insur_plot1(top_insur_trac_Y,states)    
            
            col1,col2 = st.columns(2)
            with col1:
                quarters=st.slider("Select the Top_Quarter",top_insur_trac_Y["Quarter"].min(),top_insur_trac_Y["Quarter"].max(),top_insur_trac_Y["Quarter"].min())
            Tpp_insur_Q_Y=Transaction_Amount_Count_Year_Quarter(top_insur_trac_Y,quarters)
             
            
        
        elif method3=="TOP TRANSACTION":
            
            col1,col2=st.columns(2)
            with col1:
                
               topyear=st.slider("Select the Top_trans",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            top_trans_Y=Transaction_Amount_Count_Year(Top_transaction,topyear)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("select the state Top_trans",top_trans_Y["States"].unique())
            Top_insur_plot1(top_trans_Y,states)    
            
            col1,col2 = st.columns(2)
            with col1:
                quarters=st.slider("Select the Quarter_tt",top_trans_Y["Quarter"].min(),top_trans_Y["Quarter"].max(),top_trans_Y["Quarter"].min())
            Top_tran_Q_Y=Transaction_Amount_Count_Year_Quarter(top_trans_Y,quarters)

            
             
        elif method3=="TOP USER":
            
            col1,col2=st.columns(2)
            with col1:
                
               topyear=st.slider("Select the top_Year",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            top_user_Y=Top_user_plot1(Top_user,topyear)
            
            col1,col2= st.columns(2)
            with col1:
                states = st.selectbox("select the state Top_user",top_user_Y["States"].unique())
            top_u_plot2(top_user_Y,states)

        
elif select == "Insights":    
            
        question = st.selectbox("Select the Questions",["1.Transaction Amount and Count of Aggregated Insurance",
                                                            "2.Transaction Amount and Count of Map_insurance",
                                                            "3.Transaction Amount and Count of Top_insurance",
                                                            "4.Transaction Amount and Count of Aggregated Transaction_Amount_Count_Year",
                                                            "5.Transaction Amount and count od Map Transaction_Amount_Count_Year",
                                                            "6.Transaction Amount and Count of Top Transaction_Amount_Count_Year",
                                                            "7.Transaction Count of Aggregated user",
                                                            "8.Registered Users of Map User",
                                                            "9.App Opens Map User",
                                                            "10.Registered Users of Top User",
                                                            ])

        if question == "1.Transaction Amount and Count of Aggregated Insurance":
            
            st.subheader("TRANSACTION AMOUNT")
            topcharts_trans("aggregated_insurance")
            
            st.subheader("TRANSACTION COUNT")
            topcharts_count("aggregated_insurance")
            
        elif question == "2.Transaction Amount and Count of Map_insurance":

            
            st.subheader("TRANSACTION AMOUNT")
            topcharts_trans("map_insur_details")
            
            st.subheader("TRANSACTION COUNT")
            topcharts_count("map_insur_details")
            
        elif question == "3.Transaction Amount and Count of Top_insurance":

            
            st.subheader("TRANSACTION AMOUNT")
            topcharts_trans("top_insur_details")
            
            st.subheader("TRANSACTION COUNT")
            topcharts_count("top_insur_details")
                
        elif question == "4.Transaction Amount and Count of Aggregated Transaction_Amount_Count_Year":

            st.subheader("TRANSACTION AMOUNT")
            topcharts_trans("aggregated_transaction")
            
            st.subheader("TRANSACTION COUNT")
            topcharts_count("aggregated_transaction")
            
        elif question == "5.Transaction Amount and count od Map Transaction_Amount_Count_Year":
            
            st.subheader("TRANSACTION AMOUNT")
            topcharts_trans("map_transaction")
            
            st.subheader("TRANSACTION COUNT")
            topcharts_count("map_transaction")
            
        elif question == "6.Transaction Amount and Count of Top Transaction_Amount_Count_Year":
            
            st.subheader("TRANSACTION AMOUNT")
            topcharts_trans("top_trans_details")
            
            st.subheader("TRANSACTION COUNT")
            topcharts_count("top_trans_details")
        
        elif question == "7.Transaction Count of Aggregated user":
             
            st.subheader("TRANSACTION COUNT")
            topcharts_count("aggregated_user")
            
        elif question == "8.Registered Users of Map User":
            
            states=st.selectbox("select the States",Map_user["States"].unique()) 
            st.subheader("REGISTEREDUSERS")
            topcharts_registeredusers("map_user",states)
        
        elif question == "9.App Opens Map User":
            
            states=st.selectbox("select the States",Map_user["States"].unique()) 
            st.subheader("APPOPENS")
            topcharts_appopens("map_user",states)
            
        elif question == "10.Registered Users of Top User":
            st.subheader("REGISTEREDUSERS")
            topcharts_users("top_user_details")
            
                
                  
            
        

