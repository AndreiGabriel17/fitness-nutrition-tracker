import plotly.graph_objects as go
import plotly.express as px

def create_macro_pie_chart(macros):
    labels = ['Protein', 'Carbs', 'Fat']
    values = [macros['protein'], macros['carbs'], macros['fat']]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3
    )])
    
    fig.update_layout(
        title="Macronutrient Distribution",
        showlegend=True,
        height=400
    )
    
    return fig

def create_progress_chart(progress_data):
    fig = px.line(
        progress_data,
        x='date',
        y='weight',
        title='Weight Progress Over Time'
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Weight (kg)",
        height=400
    )
    
    return fig

def create_workout_summary(workout_data):
    fig = px.bar(
        workout_data,
        x='exercise',
        y='sets',
        title='Workout Summary'
    )
    
    fig.update_layout(
        xaxis_title="Exercise",
        yaxis_title="Sets Completed",
        height=400
    )
    
    return fig
