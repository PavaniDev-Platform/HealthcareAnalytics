import sys
from pathlib import Path
from dash import Dash,dcc,html,Input,Output
import plotly.express as px
import pandas as pd

project_root=Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# Import your config paths
from core.config import CSV_DIR, DB_PATH
print(CSV_DIR)
print (DB_PATH)
from dal.emergency_department_dal import EmergencyDepartmentDAL
from biz.emergency_department_analyzer import EmergencyDepartmentAnalyzer

objERDatabaseManager=EmergencyDepartmentDAL()
objEDAnalyzer=EmergencyDepartmentAnalyzer(objERDatabaseManager)
dfEmergencyDeptData=objEDAnalyzer.fetchData() #Using for raw exploration
# KPI Cards Emergency Department
total_admissions = dfEmergencyDeptData["visit_id"].nunique()
door_to_doc = (
    dfEmergencyDeptData["wait_time_doctor_min"] + 
    dfEmergencyDeptData["wait_time_triage_min"]
).mean().round(2)
avg_satisfaction_score = dfEmergencyDeptData["satisfaction_score"].mean().round(2)
readmission_rate_30d = 100.0 * dfEmergencyDeptData["readmitted_30d"].sum() / dfEmergencyDeptData["visit_id"].nunique()
total_revenue = dfEmergencyDeptData["billed_amount_usd"].sum()
# Operation
admissions_cnt = total_admissions
physician_cnt = dfEmergencyDeptData["attending_physician"].nunique()
critical_admissions_cnt = len(dfEmergencyDeptData.loc[dfEmergencyDeptData["triage_level"].isin([1, 2])])
avg_length_of_stay_hrs = dfEmergencyDeptData["length_of_stay_hrs"].mean().round(2)
# Demographic KPI
demoAgeView_admission_cnt = total_admissions
demoAgeView_rate_of_readmission_30d = readmission_rate_30d
demoAgeView_avg_satisfaction_score = avg_satisfaction_score
month_dict = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',6:"Jun",7:"Jul",8:"Aug",9:"Sept",10:"Oct",11:"Nov",12:"Dec"}
#Executive Overview With Insurance Mix
dfExecutiveDeptOverview=objEDAnalyzer.getEDExecutiveOverview()
dfInsuranceOverview=objEDAnalyzer.getEDInsuranceOverview()
#Operation Overview With Critical Emergency vs General Emergency
dfMonthlyEDAdmissionTrends=objEDAnalyzer.getMonthlyEDAdmissionTrends()
dfBusiestMonthED=dfMonthlyEDAdmissionTrends.loc[dfMonthlyEDAdmissionTrends["rnk_highest_emergency"]==1,["department","arrival_month","emergency_admissions"]]
dfEDOperations=objEDAnalyzer.getEDOperationOverview()
dfEDOperationOverview=dfEDOperations.merge(
    dfBusiestMonthED,on="department",how="left"
)
dfEDOperationOverview['arrival_month'] = dfEDOperationOverview['arrival_month'].map(month_dict)
dfEDOperationOverview=dfEDOperationOverview.rename(columns=({"arrival_month":"busiest_month"}))
#Demographic Overview
dfDemographicOverviewByAge=objEDAnalyzer.getEDDemographicOverviewByAge()
min_age=dfDemographicOverviewByAge["patient_age"].min()
max_age=dfDemographicOverviewByAge["patient_age"].max()
grpSize= ((max_age - min_age) / 5).round()
bins = [min_age - 1, min_age + grpSize, min_age + 2 * grpSize, 
        min_age + 3 * grpSize, min_age + 4 * grpSize, max_age]
labels = [
    f"Age {int(min_age)}-{int(bins[1])}",
    f"Age {int(bins[1])}-{int(bins[2])}",
    f"Age {int(bins[2])}-{int(bins[3])}",
    f"Age {int(bins[3])}-{int(bins[4])}",
    f"Age {int(bins[4])}-{int(max_age)}"
]

dfDemographicOverviewByAge["age_group"] = pd.cut(
    dfDemographicOverviewByAge["patient_age"], 
    bins=bins, 
    labels=labels
)
#dfDemographicOverviewByAge=dfDemographicOverviewByAge.loc[dfDemographicOverviewByAge["department"]=="Cardiology"]
demoAgeView_chief_complaint_cnt=dfDemographicOverviewByAge["critical_admissions"].sum()
AgeGroupOptions=dfDemographicOverviewByAge["age_group"].unique()
# Reusable style constants for cleaner code
CARD_STYLE = {
    "flex": "1",
    "minWidth": "220px",
    "backgroundColor": "white",
    "padding": "20px",
    "margin": "10px",
    "borderRadius": "10px",
    "border": "1px solid lightgray",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",  # Optional: Adds a subtle, modern shadow
}
GRAPH_CONTAINER_STYLE={
    "backgroundColor": "white",
    "border": "1px solid lightgray",
    "borderRadius": "10px",
    "padding": "10px",
    "margin": "10px",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
    "flex": "1",  # <--- Ensures the card stretches across the flex row
}
HTML_LABEL_STYLE={"color": "#666", "margin": "0 0 10px 0","white-space":"no-wrap"}
HTML_LABEL_VALUE_STYLE={"color": "#111", "margin": "0"}
TAB_STYLE={
    "backgroundColor": "#ffffff",
    "border": "1px solid #e0e0e0",
    "borderTop": "3px solid transparent",
    "padding": "12px 24px",
    "fontWeight": "500",
    "color": "#666666",
    "borderRadius": "6px 6px 0 0",
}
TAB_SELECTED_STYLE={
    "backgroundColor": "#ffffff",
    "border": "1px solid #e0e0e0",
    "borderTop": "3px solid #007bff",  # Professional primary blue accent
    "borderBottom": "1px solid #ffffff",  # Blends into content area
    "padding": "14px 28px",
    "fontWeight": "700",
    "color": "#007bff",
    "borderRadius": "6px 6px 0 0"
}
insurance_color_bar={
    "Private":"#0078D4",
    "Medicare":"#5B9BD5",
    "Medicaid":"#70AD47",
    "Self-Pay":"#A19F9D"

}
admission_color_bar={
    "non-critical": "#0078D4",
    "critical": "#C0504D"
}
operation_overview_layout=html.Div(
    [
        # KPI Cards Row
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Total Physicians",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{physician_cnt}",
                            id="physician_cnt-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Admissions",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{admissions_cnt:,}",
                            id="admissions_cnt-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Critical Admissions",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{critical_admissions_cnt:,}",
                            id="critical_admissions_cnt-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Door to Doc",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{door_to_doc} min",
                            id="op_door_to_doc_min-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Length Of Stay",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{avg_length_of_stay_hrs} hrs",
                            id="avg_length_of_stay_hrs-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Patient Satisfaction",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{avg_satisfaction_score}",
                            id="opv_avg_satisfaction_score-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
            ],
            style={"display": "flex","flexWrap":"wrap","marginBottom": "20px"},
        ),
        # Dropdowns Row
        html.Div(
            [
                 html.H4(
                    "Department Metric Selector:",
                    style=HTML_LABEL_STYLE,
                ),
                dcc.Dropdown(
                    options=[
                        {"label":"Physicians","value":"physicians"},
                        {"label":"Admissions","value":"admissions"},
                        {"label":"Satisfaction","value":"satisfaction"},
                        {"label":"Wait Time","value":"wait_time"},
                        {"label":"Length Of Stay","value":"length_of_stay"},
                    ],
                    id="drpd-departmentOperationMetrics",
                    value="physicians",
                    clearable=False  #default
                ),
            ],
            style={"display": "flex","gap":"10px","marginBottom": "20px","alignItems": "center"},
        ),
        # Graphs Row 1 (Dynamic Graph for Selected Operation Metric)
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="fig-departmentOperationMetrics", figure={},config={'displayModeBar': False})],
                    style=GRAPH_CONTAINER_STYLE,
                )
            ],
            style={"display": "flex","width": "100%"},
        ),
    ],
    style={
            "backgroundColor": "#f8f9fa",
            "padding": "30px",
            "fontFamily": "sans-serif",
    }
)

executive_overview_layout=html.Div(
    [
        # KPI Cards Row
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Total Visits",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{total_admissions:,}",
                            id="total_visits-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Door to Doc",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{door_to_doc} min",
                            id="ex_door_to_doc_min-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Patient Satisfaction",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{avg_satisfaction_score}",
                            id="avg_satisfaction_score-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Readmission Rate",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{readmission_rate_30d}%",
                            id="readmission_rate_30d-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Total Revenue",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"${total_revenue:,.0f}",
                            id="total_revenue-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
            ],
            style={"display": "flex", "marginBottom": "20px"},
        ),
        # Dropdowns Row
        html.Div(
            [
                 html.H4(
                    "Department Metric Selector:",
                    style=HTML_LABEL_STYLE,
                ),
                dcc.Dropdown(
                    options=[
                        {"label":"Admissions","value":"Admissions"},
                        {"label":"Wait Time","value":"Wait-Time"},
                        {"label":"Satisfaction","value":"Satisfaction"},
                        {"label":"Readmission Rate","value":"Readmission Rate"},
                        {"label":"Revenue","value":"Revenue"},
                    ],
                    id="drpd-departmentMetrics",
                    value="Admissions",
                    clearable=False  #default
                ),
            ],
            style={"display": "flex","gap":"10px","marginBottom": "20px","alignItems": "center"},
        ),
        # Graphs Row 1 (Dynamic Graph for Selected Metric)
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="fig-departmentMetrics", figure={},config={'displayModeBar': False})],
                    style=GRAPH_CONTAINER_STYLE,
                )
            ],
            style={"display": "flex","width": "100%"},
        ),
        # Graphs Row 2 (Dynamic Graph for Selected Metric Insurance View)
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="fig-deptInsuranceMetrics", figure={},config={'displayModeBar': False})],
                    style=GRAPH_CONTAINER_STYLE,
                )
            ],
            style={"display": "flex","width": "100%"},
        ),
    ],
    style={
            "backgroundColor": "#f8f9fa",
            "padding": "30px",
            "fontFamily": "sans-serif",
    }
)
demographic_overview_layout=html.Div(
    [
        # KPI Cards Row
        html.Div(
            [
                html.Div(
                    [
                        html.H4(
                            "Total Admissions",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{demoAgeView_admission_cnt:,}",
                            id="demoAgeView_admission_cnt-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "30-Day Readmission Rate",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{demoAgeView_rate_of_readmission_30d}%",
                            id="demoAgeView_rate_of_readmission_30d-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
                html.Div(
                    [
                        html.H4(
                            "Patient Satisfaction",
                            style=HTML_LABEL_STYLE,
                        ),
                        html.H2(
                            f"{demoAgeView_avg_satisfaction_score}",
                            id="demoAgeView_avg_satisfaction_score-kpi",
                            style=HTML_LABEL_VALUE_STYLE,
                        ),
                    ],
                    style=CARD_STYLE,
                ),
            ],
            style={"display": "flex", "marginBottom": "20px"},
        ),
        # Dropdowns Row
        html.Div(
            [
                 html.H4(
                    "Age Group Selector:",
                    style=HTML_LABEL_STYLE,
                ),
                dcc.Dropdown(
                    options=AgeGroupOptions,
                    id="drpd-agegroup",
                    value=AgeGroupOptions[0],  #default
                    clearable=False 
                ),
                html.H4(
                    "Department Metric Selector:",
                    style=HTML_LABEL_STYLE,
                ),
                dcc.Dropdown(
                    options=[
                        {"label":"Admissions","value":"Admissions"},
                        {"label":"Satisfaction","value":"Satisfaction"},
                        {"label":"Readmission Rate","value":"Readmission Rate"},
                    ],
                    id="drpd-demographicAgeMetrics",
                    value="Admissions",
                    clearable=False  #default
                ),
            ],
            style={"display": "flex","gap":"10px","marginBottom": "20px","alignItems": "center"},
        ),
        # Graphs Row 1 (Dynamic Graph for Selected Age Group)
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="fig-demographicAgeMetrics", figure={},config={'displayModeBar': False})],
                    style=GRAPH_CONTAINER_STYLE,
                )
            ],
            style={"display": "flex","width": "100%"},
        ),
    ],
    style={
            "backgroundColor": "#f8f9fa",
            "padding": "30px",
            "fontFamily": "sans-serif",
    }
)
app=Dash(__name__)
app.layout=html.Div(
    [
        html.H1(
           "Emergency Department Analytics Dashboard",
            style={
                "textAlign": "center",
                "marginBottom": "30px",
                "color": "#333333",
            },
        ),
        dcc.Tabs(
            [
                dcc.Tab(
                    label="Executive Overview",
                    children=[executive_overview_layout],
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE
                ),
                dcc.Tab(
                    label="Operation Overview",
                    children=[operation_overview_layout],
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE
                ),
                dcc.Tab(
                    label="Demographic Overview",
                    children=[demographic_overview_layout],
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED_STYLE
                ),
            ],
            # Styling for the overall tabs container bar
            style={
                "borderBottom": "1px solid #e0e0e0",
                "marginBottom": "20px",
            },
        )
    ],
    style={
        "backgroundColor": "#f8f9fa",
        "padding": "30px",
        "fontFamily": "sans-serif",
    }
)
#Callback Implementations
#Callback Demographic Overview Implementation
@app.callback(
    Output("fig-demographicAgeMetrics", "figure"),
    Input("drpd-agegroup", "value"),
    Input("drpd-demographicAgeMetrics", "value"),
)
def drpd_demographicMetrics_callback(
    selected_age_group, selected_demographic_metric):
    strY = "department"
    strYTitle = "Department"
    dfSelectedAgeGroup = dfDemographicOverviewByAge.loc[dfDemographicOverviewByAge["age_group"] == selected_age_group ]
    number_0f_admissions=dfSelectedAgeGroup.groupby('department')['number_0f_admissions'].sum()
    critical_admissions=dfSelectedAgeGroup.groupby('department')['critical_admissions'].sum()
    total_readmission_30d=dfSelectedAgeGroup.groupby('department')['readmission_30d'].sum()
    rate_of_readmission_30d=(100.0 * total_readmission_30d)/number_0f_admissions
    total_critical_readmission_30d = dfSelectedAgeGroup.groupby('department')['critical_readmission_30d'].sum()
    critical_rate_of_readmission_30d=(100.0 * total_critical_readmission_30d)/critical_admissions
    satisfaction_score=dfSelectedAgeGroup.groupby('department')['satisfaction_score'].sum()/number_0f_admissions
    critical_satisfaction_score=dfSelectedAgeGroup.groupby('department')['critical_satisfaction_score'].sum()/critical_admissions
    dfSelectedAgeGroupOverview=pd.DataFrame({
        "number_0f_admissions":number_0f_admissions,
        "critical_admissions":critical_admissions,
        "rate_of_readmission_30d":rate_of_readmission_30d.round(2),
        "critical_rate_of_readmission_30d":critical_rate_of_readmission_30d.round(2),
        "satisfaction_score":satisfaction_score.round(2),
        "critical_satisfaction_score":critical_satisfaction_score.round(2)
    })
    dfSelectedAgeGroupOverview=dfSelectedAgeGroupOverview.reset_index()
    #dfSelectedAgeGroupOverview
    match selected_demographic_metric:
        case "Admissions":
            strX = "number_0f_admissions"
            strCCX = "critical_admissions"
            strTitle = f"Admissions for {selected_age_group} by Department"
            strXTitle = "Total Admissions"
        case "Readmission Rate":
            strX = "rate_of_readmission_30d"
            strCCX = "critical_rate_of_readmission_30d"
            strTitle = f"30-Day Readmission Rate for {selected_age_group} by Department"
            strXTitle = "30-Day Readmission Rate"
        case "Satisfaction":  # Updated case name to match dropdown value
            strX = "satisfaction_score"
            strCCX = "critical_satisfaction_score"
            strTitle = f"Patient Satisfaction for {selected_age_group} by Department"
            strXTitle = "Patient Satisfaction"

    legend_names = {
            strX: "Non-Critical",
            strCCX: "Critical Care"
    }

    figDemoAgeGroupMetric = px.bar(
        data_frame=dfSelectedAgeGroupOverview,
        x=[strX,strCCX],
        y=strY,
        #color=strCCX,
        title=strTitle,
        orientation="h",
        barmode="stack",
        color_discrete_map={
            strX: "#0078D4",  
            strCCX: "#C0504D"  
        },
            labels={
                "variable": strXTitle,
            },
        text_auto=True
    )
    # Added clean text formatting for floats
    #figDemoAgeGroupMetric.update_traces(
        #texttemplate="%{text:.1f}", textposition="outside"
    #)
    figDemoAgeGroupMetric.update_layout(
        xaxis_title=strXTitle,
        yaxis_title=strYTitle,
        yaxis={"categoryorder": "total ascending"},
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
    )
     # 3. Clean up the legend labels (optional, otherwise it uses the raw column names)
    figDemoAgeGroupMetric.for_each_trace(
            lambda t: t.update(name=legend_names.get(t.name, t.name))
    )

    #Updating the X-axis as Paitent Satisfaction has min=1.000000 and max=9.500000
    if selected_demographic_metric == "Satisfaction":
        figDemoAgeGroupMetric.update_xaxes(range=[0, 10])

    return figDemoAgeGroupMetric

#Callback Operation Overview Implementation
@app.callback(
    Output("fig-departmentOperationMetrics","figure"),
    Input("drpd-departmentOperationMetrics","value")
)
def drpd_departmentOperationMetrics_callback(selected_operation_metric):
    strY = "department" # dfEDOperationOverview["department"]
    strYTitle = "Department"
    match selected_operation_metric:
        case "physicians":
            strX = "general_physicians" #dfEDOperationOverview["general_physicians"]
            strCCX="criticalcare_physicians" #dfEDOperationOverview["criticalcare_physicians"]
            strTitle = "Physicians Distribution by Department"
            strXTitle = "Total Physicians"
        case "admissions":
            strX = "number_of_admissions"  #dfEDOperationOverview["number_of_admissions"]
            strCCX="number_of_critical_admissions" #dfEDOperationOverview["number_of_critical_admissions"]
            strTitle = "Admissions by Department"
            strXTitle = "Total Admissions"
        case "wait_time":
            strX = "avg_doortodoc_wait_time"  #dfEDOperationOverview["avg_doortodoc_wait_time"]
            strCCX = "avg_critical_doortodoc_wait_time"  #dfEDOperationOverview["avg_critical_doortodoc_wait_time"]
            strTitle = "Door-to-Doctor Journey by Patient Acuity"
            strXTitle = "Wait-Time (Min)"
        case "length_of_stay":
            strX = "avg_length_of_stay_hrs"  #dfEDOperationOverview["avg_length_of_stay_hrs"]
            strCCX = "avg_critical_length_of_stay_hrs"  #dfEDOperationOverview["avg_critical_length_of_stay_hrs"]
            strTitle = "Length Of Stay by Department"
            strXTitle = "Length Of Stay (Hrs)"
        case "satisfaction":
            strX = "satisfaction"  #dfEDOperationOverview["satisfaction"]
            strCCX = "critical_satisfaction_score"  #dfEDOperationOverview["critical_satisfaction_score"]
            strTitle = "Patient Satisfaction by Department"
            strXTitle = "Patient Satisfaction"
    # 1. Create a mapping to give the legend clean, readable names
    legend_names = {
        strX: "Non-Critical",
        strCCX: "Critical Care"
    }

    figDeptOperationMetric = px.bar(
            data_frame=dfEDOperationOverview,
            x=[strX, strCCX],
            y=strY,
            #color=strCCX,
            title=strTitle,
            orientation='h',
            barmode="stack",
            color_discrete_map={
                strX: "#0078D4",  
                strCCX: "#C0504D"  
            },
            labels={
                "variable": strXTitle,
            },
            text_auto=True # Automatically displays values for BOTH stacked segments
    )
    # 3. Clean up the legend labels (optional, otherwise it uses the raw column names)
    figDeptOperationMetric.for_each_trace(
        lambda t: t.update(name=legend_names.get(t.name, t.name))
    )
    figDeptOperationMetric.update_layout(
        xaxis_title=strXTitle,
        yaxis_title=strYTitle,        
        yaxis={'categoryorder':'total ascending'}, # Automatically sorts bars from shortest to longest
        plot_bgcolor='white', 
        paper_bgcolor="white",
        height=500,  
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
     #Updating the X-axis as Paitent Satisfaction has min=1.000000 and max=9.500000
    if selected_operation_metric == "satisfaction":
        figDeptOperationMetric.update_xaxes(range=[0, 10])

    return figDeptOperationMetric
#Callback Executive Overview Implementation  
@app.callback(
    Output("fig-departmentMetrics","figure"),
    Output("fig-deptInsuranceMetrics","figure"),
    Input("drpd-departmentMetrics","value")
)
def drpd_departmentMetrics_callback(selected_metric):
    strY = "department" # dfExecutiveDeptOverview["department"]/dfInsuranceOverview["department"]
    strYTitle = "Department"
    match selected_metric:
        case "Admissions":
            strX = "total_admissions" #dfExecutiveDeptOverview["total_admissions"]
            strTitle = "Total Admissions by Department"
            strXTitle = "Total Admissions"
            strInsuranceX="total_admissions" #dfInsuranceOverview["total_admissions"]
            strInsuranceTitle = "Total Admissions by Insurance"
        case "Wait-Time":
            strX = "avg_doortodoc_wait_time"  #dfExecutiveDeptOverview["avg_doortodoc_wait_time"]
            strTitle = "Door-to-Doctor Wait-Time (Min)"
            strXTitle = "Wait Time (Min)"
            strInsuranceX="avg_doortodoc_wait_time" #dfInsuranceOverview["avg_doortodoc_wait_time"]
            strInsuranceTitle = "Insurance Type Impact on Patient Wait Times"
        case "Satisfaction":
            strX = "avg_satisfaction_score" #dfExecutiveDeptOverview["avg_satisfaction_score"]
            strTitle = "Patient Satisfaction Score by Department"
            strXTitle = "Patient Satisfaction"
            strInsuranceX="avg_satisfaction_score" #dfInsuranceOverview["avg_satisfaction_score"]
            strInsuranceTitle = "Insurance Type Impact On Patient Satisfaction"
        case "Readmission Rate":
            strX = "readmission_rate_30d"  #dfExecutiveDeptOverview["readmission_rate_30d"]
            strTitle = "30-Day Readmission Rate by Department"
            strXTitle = "30-Day Readmission Rate"
            strInsuranceX="rate_of_readmission_30d" #dfInsuranceOverview["rate_of_readmission_30d"]
            strInsuranceTitle = "30-Day Readmission Rate by Insurance"
        case "Revenue":
            strX = "total_deptrevenue"  #dfExecutiveDeptOverview["total_deptrevenue"]
            strTitle = "Revenue by Department"
            strXTitle = "Revenue"
            strInsuranceX="total_deptrevenue" #dfInsuranceOverview["total_deptrevenue"]
            strInsuranceTitle = "Revenue by Insurance"
            
    figDeptMetric = px.bar(
            data_frame=dfExecutiveDeptOverview,
            x=strX,
            y=strY,
            title=strTitle,
            orientation='h',
            text=strX #Displays the exact number on the bar
    )
    figDeptMetric.update_layout(
        xaxis_title=strXTitle,
        yaxis_title=strYTitle,        
        yaxis={'categoryorder':'total ascending'}, # Automatically sorts bars from shortest to longest
        plot_bgcolor='white',  
        paper_bgcolor="white",
        height=500, 
        margin=dict(l=20, r=20, t=40, b=20)
    )
    figDeptInsuranceMetric = px.bar(
        data_frame=dfInsuranceOverview,
        x=strInsuranceX,
        y=strY,
        title=strInsuranceTitle,
        color='insurance_type',
        orientation='h',
        barmode='stack',
        color_discrete_map=insurance_color_bar,
        text=strInsuranceX #Displays the exact number on the bar
    )
    figDeptInsuranceMetric.update_layout(
        xaxis_title=strXTitle,
        yaxis_title=strYTitle,        
        yaxis={'categoryorder':'total ascending'}, # Automatically sorts bars from shortest to longest
        plot_bgcolor='white', 
        paper_bgcolor="white",
        height=500,  
        margin=dict(l=20, r=20, t=40, b=20)
    )
    #Updating the X-axis as Paitent Satisfaction has min=1.000000 and max=9.500000
    if selected_metric == "Satisfaction":
        figDeptMetric.update_xaxes(range=[0, 10])
        #figDeptInsuranceMetric.update_xaxes(range=[0, 10])

    return figDeptMetric , figDeptInsuranceMetric  

if(__name__)=="__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=8050,
        use_reloader=False
    )