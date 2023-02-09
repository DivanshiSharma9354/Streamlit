import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer


df = pd.read_csv("HR.csv", parse_dates=['DateofHire', 'DateofTermination', 'LastPerformanceReview_Date'])
df.rename(columns={'DateofHire': 'Date of Hire', 'DateofTermination': 'Date of Termination',
                   "MaritalDesc": 'Marital Status', 'RaceDesc': 'Race', 'RecruitmentSource': 'Recruitment Source'},
          inplace=True)
df["Sex"] = df["Sex"].replace(['F', 'M '], ['Female', 'Male'])

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.sidebar.header("HR Analytics")

st.sidebar.subheader('Map Parameters')
map_params = st.sidebar.selectbox('Sort By', ('EngagementSurvey', 'Salary', 'Absences'))

st.sidebar.subheader('Donut Chart Parameters')
donut_theta = st.sidebar.selectbox('Select Parameter', ('Sex', 'Marital Status', 'Race', 'Department', 'Recruitment Source', 'Position'))

st.sidebar.subheader('Yearly Data Parameters')
plot_data = st.sidebar.selectbox('Select Parameter', ('Date of Hire',  'Date of Termination'))

st.sidebar.markdown('''
---
Created with ❤️ by [Divanshi Sharma](https://www.linkedin.com/in/divanshi-sharma-676401210/).
''')

# Row A
st.title   (' HR ANALYTICS DASHBOARD')


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Salary Expenditure")
    st.image('images/impression.png',use_column_width='Auto')
    department = st.selectbox("Select Department", options=df.Department.unique())
    dep_df = df.groupby("Department")['Salary'].sum()
    st.metric(label="Expense" , value="$" + "{:,}".format(dep_df[department]))

with col2:
    st.markdown("#### Employee Satisfaction Rate")
    st.image('images/tap.png',use_column_width='Auto')
    gender = st.selectbox("Select Gender", options=df.Sex.unique()[::-1])
    gender_df = df.groupby("Sex")["EmpSatisfaction"].sum()
    total_satisfaction = df.Sex.value_counts() * 5
    st.metric(label="Satisfaction %", value="{}%".format(round((gender_df[gender]/total_satisfaction[gender])*100,1)))

with col3:
    st.markdown("#### Employees Absence")
    st.image('images/hand.png',use_column_width='Auto')
    department2 = st.selectbox("Select Department ", options=df.Department.unique())
    dep_df2 = df.groupby("Department")['Absences'].sum()
    st.metric(label="Total Absence", value="{:,}".format(dep_df2[department2]))

# Row B
c1, c2 = st.columns((6, 4))
with c1:
    st.markdown('### State Wise Analysis')
    fig1 = px.choropleth(df, locations='State', locationmode="USA-states",
                        scope="usa", color=map_params, color_continuous_scale="viridis")
    st.plotly_chart(fig1)

with c2:
    st.markdown('### Donut chart')
    fig2 = px.pie(df, names=donut_theta, height=300, width=500, hole=0.4)
    fig2.update_layout(plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                      legend=dict(y=-0.5, xanchor="center", x=-0.1))
    st.plotly_chart(fig2)

# Row C

cl1, cl2 = st.columns((6,4))
with cl1:
    st.markdown('### Yearly Data')
    df_date = df.set_index(plot_data).resample('MS').size()
    fig3 = px.bar(df_date, labels={"value": "Total"}, width=500)
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3)

with cl2:
    st.markdown("### Employee Status")
    emp_df = df[['EmpID', 'EmploymentStatus', 'Date of Hire', 'Date of Termination', 'TermReason']]
    emp_df = emp_df.set_index('EmpID')
    ID = st.selectbox("Select Employee ID ", options=df.EmpID.unique())
    check = emp_df.loc[ID, 'EmploymentStatus']
    if check == 'Active':
        st.header("ACTIVE ✅")
    else:
        tenure = emp_df.loc[ID, 'Date of Termination'] - emp_df.loc[ID, 'Date of Hire']
        st.header("Terminated! ❌")
        st.markdown(f'Worked for {"%d days" % tenure.days}')
        st.markdown(emp_df.loc[ID, 'TermReason'].capitalize())


#Row D
st.markdown("### Data Filter")
dum_df = df[['Employee_Name', 'Salary', 'Date of Hire', 'Position']]
filtered_df = dataframe_explorer(dum_df)
st.dataframe(filtered_df, width=700)
