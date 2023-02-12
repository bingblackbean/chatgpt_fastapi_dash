from textwrap import dedent
from dash.exceptions import PreventUpdate
from dash import dcc,html
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import openai


def Header(name, app):
    title = html.H1(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("data_amber.png"), style={"float": "right", "height": 60}
    )
    return dbc.Row([dbc.Col(title, md=8), dbc.Col(logo, md=4)])


def textbox(text, box="AI", name="DataAmber"):
    text = text.replace(f"{name}:", "").replace("You:", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return dbc.Card(text, style=style, body=True, color="primary", inverse=True)

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=app.get_asset_url("data_amber.png"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox = dbc.Card(text, style=style, body=True, color="light", inverse=False)

        return html.Div([thumbnail, textbox])

    else:
        raise ValueError("Incorrect option for `box`.")


description = """
和chatgpt聊聊天。
"""

# Authentication
openai.api_key = "your key"

# Define app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# Load images
IMAGES = {"DataAmber": app.get_asset_url("data_amber.png")}


# Define Layout
conversation = html.Div(
    html.Div(id="display-conversation"),
    style={
        "overflow-y": "auto",
        "display": "flex",
        "height": "calc(90vh - 132px)",
        "flex-direction": "column-reverse",
    },
)

controls = dbc.InputGroup(
    children=[
        dbc.Input(id="user-input", placeholder="随便写点什么", type="text"),
        dbc.InputGroupText(dbc.Button("Submit", id="submit")),
    ]
)

app.layout = dbc.Container(
    fluid=False,
    children=[
        Header("Dash ChatGPT- DataAmber", app),
        html.Hr(),
        dcc.Store(id="store-conversation", data=""),
        conversation,
        controls,
        dbc.Spinner(html.Div(id="loading-component")),
    ],
)


@app.callback(
    [Output("store-conversation", "data"), Output("loading-component", "children")],
    [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    [State("user-input", "value"), State("store-conversation", "data")],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history):
    if user_input is None or user_input == "":
        raise PreventUpdate
    else:
        name = "DataAmber"
        # First add the user input to the chat history
        chat_history += f"You: {user_input}<split>{name}:"
        model_input = chat_history.replace("<split>", "\n")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=model_input,
            max_tokens=250,
            temperature=0.6,
        )
        model_output = response.choices[0].text + '<split>'
        chat_history += f"{model_output}"
        return [chat_history, None]

@app.callback(
    Output("display-conversation", "children"), [Input("store-conversation", "data")]
)
def update_display(chat_history):
    return [
        textbox(x, box="user") if i % 2 == 0 else textbox(x, box="AI")
        for i, x in enumerate(chat_history.split("<split>")[:-1])
    ]


if __name__ == "__main__":
    app.run_server(debug=True)