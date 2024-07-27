import tempfile

def plot_to_temp_file(fig):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
        fig.write_image(tmpfile.name)
        return tmpfile.name
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json


def create_charts(data):
    # Load the JSON data

    # Extract workshop metrics
    metrics = data['workshopMetrics']

    # Dictionary to store all graphs
    graphs = {}

    # 1. Time and Cost Comparison Chart
    fig1 = go.Figure(data=[
        go.Bar(name='Estimated', x=['Time(in hrs)', 'Cost(in 100s)'], y=[14, metrics['costMetrics']['estimatedCost']]),
        go.Bar(name='Actual', x=['Time(in hrs)', 'Cost(in 100s)'], y=[20, metrics['costMetrics']['actualCost']])
    ])
    fig1.update_layout(title='Estimated vs Actual Time and Cost', barmode='group')
    graphs['time_cost_comparison'] = fig1

    # 2. Quality Metrics Radar Chart
    fig2 = go.Figure(data=go.Scatterpolar(
        r=[100 - float(metrics['qualityMetrics']['reworkRate'][:-1]), 
           100 - float(metrics['qualityMetrics']['defectRate'][:-1]), 
           float(metrics['qualityMetrics']['customerSatisfaction'].split('/')[0]) * 20],
        theta=['Rework Rate', 'Defect Rate', 'Customer Satisfaction'],
        fill='toself'
    ))
    fig2.update_layout(title='Quality Metrics')
    graphs['quality_metrics'] = fig2

    # 3. Resource Utilization Gauge Charts
    fig3 = go.Figure()
    fig3.add_trace(go.Indicator(
        mode = "gauge+number",
        value = float(metrics['resourceUtilizationMetrics']['equipmentUtilization'][:-1]),
        title = {'text': "Equipment Utilization"},
        domain = {'x': [0, 0.5], 'y': [0, 1]}
    ))
    fig3.add_trace(go.Indicator(
        mode = "gauge+number",
        value = float(metrics['resourceUtilizationMetrics']['laborUtilization'][:-1]),
        title = {'text': "Labor Utilization"},
        domain = {'x': [0.5, 1], 'y': [0, 1]}
    ))
    fig3.update_layout(title='Resource Utilization')
    graphs['resource_utilization'] = fig3

    # 4. Productivity and Employee Metrics
    fig4 = go.Figure(data=[
        go.Bar(name='Value', x=['Task Completion Rate', 'Work Output', 'Employee Productivity', 'Employee Attendance', 'Employee Satisfaction'],
               y=[80, 100, 73, 95, 85])
    ])
    fig4.update_layout(title='Productivity and Employee Metrics')
    graphs['productivity_employee_metrics'] = fig4

    # 5. Financial Metrics Pie Chart
    fig5 = px.pie(values=[5000, 650], names=['Profit', 'Estimated Cost'],
                  title='Financial Overview')
    graphs['financial_overview'] = fig5

    # 6. Workshop Schedule Gantt Chart
    df = pd.DataFrame([
        dict(Task="Vehicle Servicing", Start='2024-07-01', Finish='2024-07-07', Resource="T001"),
        dict(Task="Street Lamp Installation", Start='2024-07-05', Finish='2024-07-10', Resource="T002"),
        dict(Task="Road Repair", Start='2024-07-08', Finish='2024-07-13', Resource="T003")
    ])
    fig6 = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource",
                       title="Workshop Schedule")
    # Adjust x-axis range to better visualize data
    # fig6.update_layout(xaxis_range=['2024-06-30', '2024-07-03'])

    # # Increase figure size for better visibility
    # fig6.update_layout(width=800, height=400)
    fig6.update_yaxes(autorange="reversed")
    graphs['workshop_schedule'] = fig6

    return graphs


"""
if all_metrics:
    metrics=all_metrics["workshopMetrics"]

fig1 = go.Figure(data=[
    go.Bar(name='Estimated', x=['Time', 'Cost'], y=[4, metrics['costMetrics']['estimatedCost']]),
    go.Bar(name='Actual', x=['Time', 'Cost'], y=[4.17, metrics['costMetrics']['actualCost']])
])
fig1.update_layout(title='Estimated vs Actual Time and Cost', barmode='group')

# 2. Quality Metrics Radar Chart
fig2 = go.Figure(data=go.Scatterpolar(
    r=[100 - float(metrics['qualityMetrics']['reworkRate'][:-1]), 
       100 - float(metrics['qualityMetrics']['defectRate'][:-1]), 
       float(metrics['qualityMetrics']['customerSatisfaction'].split('/')[0]) * 20],
    theta=['Rework Rate', 'Defect Rate', 'Customer Satisfaction'],
    fill='toself'
))
fig2.update_layout(title='Quality Metrics')

# 3. Resource Utilization Gauge Charts
fig3 = go.Figure()
fig3.add_trace(go.Indicator(
    mode = "gauge+number",
    value = float(metrics['resourceUtilizationMetrics']['equipmentUtilization'][:-1]),
    title = {'text': "Equipment Utilization"},
    domain = {'x': [0, 0.5], 'y': [0, 1]}
))
fig3.add_trace(go.Indicator(
    mode = "gauge+number",
    value = float(metrics['resourceUtilizationMetrics']['laborUtilization'][:-1]),
    title = {'text': "Labor Utilization"},
    domain = {'x': [0.5, 1], 'y': [0, 1]}
))
fig3.update_layout(title='Resource Utilization')

# 4. Productivity and Employee Metrics
fig4 = go.Figure(data=[
    go.Bar(name='Value', x=['Task Completion Rate', 'Work Output', 'Employee Productivity', 'Employee Attendance', 'Employee Satisfaction'],
           y=[20, 100, 5, 95, 4])
])
fig4.update_layout(title='Productivity and Employee Metrics')

# 5. Financial Metrics Pie Chart
fig5 = px.pie(values=[5000, 650], names=['Profit', 'Estimated Cost'],
              title='Financial Overview')

# 6. Workshop Schedule Gantt Chart
df = pd.DataFrame([
    dict(Task="Vehicle Servicing", Start='2024-07-01', Finish='2024-07-01', Resource="T001"),
    dict(Task="Gaddha Repairment", Start='2024-07-02', Finish='2024-07-02', Resource="T002"),
])
fig6 = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource",
                   title="Workshop Schedule")
fig6.update_yaxes(autorange="reversed")

# To display these charts in Streamlit, you would use:
# st.plotly_chart(fig1)
# st.plotly_chart(fig2)
# st.plotly_chart(fig3)
# st.plotly_chart(fig4)
# st.plotly_chart(fig5)
# st.plotly_chart(fig6)



"""
