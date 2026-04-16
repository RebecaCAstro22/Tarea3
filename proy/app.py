import os
import pandas as pd
from flask import Flask, request, jsonify, render_template
from openai import OpenAI

app = Flask(__name__)
# Leer Excel
# Agrega esto antes de leer el excel:
ruta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_excel = os.path.join(ruta_actual, "data.xlsx")

# Inicializar cliente OpenAI

import os
# Ahora el código buscará la clave en el sistema, no en el archivo
api_key = os.getenv("GROQ_API_KEY")


# Ruta principal (UI)
@app.route("/")
def home():
    return render_template("index.html")

# Endpoint chatbot
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_question = request.json.get("question")

        

# Cambia tu línea de lectura por esta:
        df = pd.read_excel(ruta_excel)

        # Convertir a contexto
        context = df.to_string(index=False)

        # Prompt
        prompt = f"""
        You are a helpful assistant. Answer ONLY using this data:

        {context}

        Question: {user_question}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        answer = response.choices[0].message.content

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
