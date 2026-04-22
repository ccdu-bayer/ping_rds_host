# --- CONFIGURATION ---
# Use your RDS Private Endpoint and Port
# RDS_HOST =os.environ.get("DB_HOST", "ht-workflow.c9hukjucdlzt.us-east-1.rds.amazonaws.com")
# RDS_PORT = 5432  # 5432 for Postgres, 3306 for MySQL/Aurora

import dash
from dash import html, dcc, Input, Output, State
import socket
import datetime

# --- CONFIGURATION ---
# Replace these with your actual RDS details
DEFAULT_RDS_HOST = "ht-workflow.c9hukjucdlzt.us-east-1.rds.amazonaws.com"
DEFAULT_RDS_PORT = 5432  # 5432 for Postgres, 3306 for MySQL

app = dash.Dash(__name__)
server = app.server  # Crucial for Posit Connect!

app.layout = html.Div(style={'fontFamily': 'sans-serif', 'padding': '40px'}, children=[
    html.H2("RDS Connectivity Diagnostic Tool"),
    html.P("This tool tests the TCP connection from this Posit Connect host to your RDS instance."),
    
    html.Div(style={'marginBottom': '20px'}, children=[
        html.Label("RDS Hostname:"),
        dcc.Input(id='input-host', value=DEFAULT_RDS_HOST, type='text', style={'width': '100%', 'padding': '8px'}),
    ]),
    
    html.Div(style={'marginBottom': '20px'}, children=[
        html.Label("Port:"),
        dcc.Input(id='input-port', value=DEFAULT_RDS_PORT, type='number', style={'width': '100px', 'padding': '8px'}),
    ]),
    
    html.Button('Test Connection', id='btn-test', n_clicks=0, 
                style={'backgroundColor': '#007bff', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 'cursor': 'pointer'}),
    
    html.Hr(),
    
    dcc.Loading(id="loading-1", type="default", children=[
        html.Div(id='result-output', style={'marginTop': '20px', 'fontSize': '18px', 'fontWeight': 'bold'})
    ]),
    
    html.Div(id='debug-log', style={'marginTop': '20px', 'color': '#666', 'fontSize': '12px'})
])

@app.callback(
    [Output('result-output', 'children'),
     Output('result-output', 'style'),
     Output('debug-log', 'children')],
    Input('btn-test', 'n_clicks'),
    [State('input-host', 'value'), State('input-port', 'value')]
)
def run_test(n_clicks, host, port):
    if n_clicks == 0:
        return "", {}, ""
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # --- Step 1: Try DNS Resolution ---
    try:
        resolved_ip = socket.gethostbyname(host)
        dns_status = f"DNS Status: Resolved {host} to {resolved_ip}"
    except Exception as e:
        dns_status = f"DNS Status: FAILED to resolve {host}. Error: {str(e)}"
        return "❌ DNS FAILURE", {'color': 'red'}, dns_status

    # --- Step 2: Try TCP Connection ---
    try:
        with socket.create_connection((host, int(port)), timeout=5):
            return "✅ SUCCESS", {'color': 'green'}, dns_status
    except Exception as e:
        # If DNS worked but this fails, it's a firewall/routing issue
        return "❌ TIMED OUT", {'color': 'red'}, f"{dns_status} | Connection Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

 