{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {
    "id": "4nAd0K5yOAPP"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "%pip install -U --quiet langchain-google-genai langchainhub langgraph google-ai-generativelanguage==0.6.15"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {
    "id": "OYItAbnaPA6f"
   },
   "outputs": [],
   "source": [
    "import os\n",
    "import getpass\n",
    "from langgraph.graph import StateGraph,END\n",
    "from langchain_google_genai import ChatGoogleGenerativeAI\n",
    "from langchain_core.messages import HumanMessage"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "Od9CLvABPmu_",
    "outputId": "cb135c59-cf4e-40f2-8b53-019d0e2fb806"
   },
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Enter the gemini Gemini API key:  ········\n"
     ]
    }
   ],
   "source": [
    "os.environ['GOOGLE_API_KEY']=getpass.getpass(\"Enter the gemini Gemini API key: \")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {
    "id": "Gc_iwr_RQK3Q"
   },
   "outputs": [],
   "source": [
    "llm=ChatGoogleGenerativeAI(model=\"models/gemini-1.5-flash-latest\",temperature=0.2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 21,
   "metadata": {
    "id": "fJiMKo1vQ3EI"
   },
   "outputs": [],
   "source": [
    "def get_input(state:dict)->dict:\n",
    "  val=input(\"Enter input:\")\n",
    "  state[\"val\"]=val\n",
    "  return state"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {
    "id": "5_7MFQ9HSqah"
   },
   "outputs": [],
   "source": [
    "def input_classifier(state:dict)->dict:\n",
    "  prompt=(\n",
    "      f\"Classify the given input {state['val']} into one of the categories: \\n1.Product (e.g., plastic bottle)\\n2.Activity (e.g., long showers)\\n3.Transport (e.g., daily car commute)\\n4.Energy use (e.g., incandescent bulbs)Respond only with\"f\" one word, Product,Activity,Energy use,Transport\")\n",
    "  response=llm.invoke([HumanMessage(content=prompt)])\n",
    "  category=response.content.strip()\n",
    "  print(f\"Category is {category}\")\n",
    "  state[\"category\"]=category.lower()\n",
    "  return state"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {
    "id": "HvkAS9kTT-dd"
   },
   "outputs": [],
   "source": [
    "def input_router(state:dict)->dict:\n",
    "    cat=state[\"category\"]\n",
    "    print(cat)\n",
    "    if(\"product\" in cat ):\n",
    "        return \"Product\"\n",
    "    elif(\"activity\" in cat ):\n",
    "        return \"Activity\"\n",
    "    elif(\"transport\" in cat ):\n",
    "        return \"Transport\"\n",
    "    elif(\"energy use\" in cat):\n",
    "      return \"Energy use\"\n",
    "    else:\n",
    "        print(\"Try Again\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {
    "id": "RvuOXPGIUvhE"
   },
   "outputs": [],
   "source": [
    "def impact_assessor(state:dict)->dict:\n",
    "  prompt=(\n",
    "      f\"Give a couple of the environmental impacts of using {state['val']} \")\n",
    "  response=llm.invoke([HumanMessage(content=prompt)])\n",
    "  res1=response.content.strip()\n",
    "  print(f\"{res1}\")\n",
    "  #print(type(state))\n",
    "  state[\"res1\"]=res1\n",
    "  return state"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {
    "id": "4ZyppUXjZ41N"
   },
   "outputs": [],
   "source": [
    "def alternative(state:dict)->dict:\n",
    "  prompt=(\n",
    "      f\"Give a couple of environmental friendly alternatives for {state['val']} \")\n",
    "  response=llm.invoke([HumanMessage(content=prompt)])\n",
    "  res=response.content.strip()\n",
    "  print(f\"{res}\")\n",
    "  state[\"res\"]=res\n",
    "  return state"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "Q05EQGS_aJVr",
    "outputId": "cac57c46-2a79-478b-8351-f97b992c505e"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<langgraph.graph.state.StateGraph at 0x1ddfe234da0>"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "builder=StateGraph(dict)\n",
    "builder.set_entry_point(\"get_input\")\n",
    "builder.add_node(\"get_input\",get_input)\n",
    "builder.add_node(\"input_classifier\",input_classifier)\n",
    "builder.add_node(\"input_router\",input_router)\n",
    "builder.add_node(\"impact_assessor\",impact_assessor)\n",
    "builder.add_node(\"alternative\",alternative)\n",
    "\n",
    "builder.add_edge(\"get_input\",\"input_classifier\")\n",
    "builder.add_edge(\"input_classifier\",\"impact_assessor\")\n",
    "#builder.add_edge(\"input_router\",\"impact_assessor\")\n",
    "builder.add_edge(\"impact_assessor\",\"alternative\")\n",
    "builder.add_edge(\"alternative\",END)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "0AJBmSkOcZiG",
    "outputId": "42d70dac-5a7b-4e58-83b3-a3dc0c64a016"
   },
   "outputs": [],
   "source": [
    "def get_graph():\n",
    "    return builder.compile()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "colab": {
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python [conda env:bot]",
   "language": "python",
   "name": "conda-env-bot-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
