from flask import Flask, render_template, request
import os
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyCiibAhs0tssOL8uVHPaCQcB9ddQt3CsmA"

llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest", temperature=0.2)

app = Flask(__name__)

# ------- LangGraph Node Functions --------

def get_input(state: dict) -> dict:
    # This just returns the state, input is already inside
    return state

def input_classifier(state: dict) -> dict:
    prompt = (
        f"Classify the given input {state['val']} into one of the categories: \n"
        "1. Product (e.g., plastic bottle)\n"
        "2. Activity (e.g., long showers)\n"
        "3. Transport (e.g., daily car commute)\n"
        "4. Energy use (e.g., incandescent bulbs)\n"
        "Respond only with one word: Product, Activity, Energy use, Transport"
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    category = response.content.strip()
    state["category"] = category.lower()
    return state

def input_router(state: dict) -> str:
    cat = state["category"]
    if "product" in cat:
        return "Product"
    elif "activity" in cat:
        return "Activity"
    elif "transport" in cat:
        return "Transport"
    elif "energy use" in cat:
        return "Energy use"
    else:
        return END  # fallback

def impact_assessor(state: dict) -> dict:
    prompt = f"Give a couple of the environmental impacts of using {state['val']}."
    response = llm.invoke([HumanMessage(content=prompt)])
    state["res1"] = response.content.strip()
    return state

def alternative(state: dict) -> dict:
    prompt = f"Give a couple of environmental friendly alternatives for {state['val']}."
    response = llm.invoke([HumanMessage(content=prompt)])
    state["res"] = response.content.strip()
    return state

# --------- Build LangGraph ---------

def get_graph():
    builder = StateGraph(dict)
    builder.set_entry_point("get_input")
    builder.add_node("get_input", get_input)
    builder.add_node("input_classifier", input_classifier)
    builder.add_node("input_router", input_router)
    builder.add_node("impact_assessor", impact_assessor)
    builder.add_node("alternative", alternative)

    builder.add_edge("get_input", "input_classifier")
    builder.add_edge("input_classifier", "impact_assessor")
    builder.add_edge("impact_assessor", "alternative")
    builder.add_edge("alternative", END)

    return builder.compile()

graph = get_graph()

# -------- Flask Route --------

@app.route('/home', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        user_input = request.form.get("input")
        initial_state = {"val": user_input}
        result = graph.invoke(initial_state)  # dict with res1 and res
        print(result)
    return render_template('app.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
