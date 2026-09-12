import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "tarefas"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(120) NOT NULL,
            descricao TEXT,
            prioridade VARCHAR(20) NOT NULL DEFAULT 'Média',
            concluida BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def index():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM tarefas ORDER BY concluida, id DESC")
    tarefas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tarefas=tarefas)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/adicionar", methods=["POST"])
def adicionar():
    titulo = request.form["titulo"].strip()
    descricao = request.form.get("descricao", "").strip()
    prioridade = request.form.get("prioridade", "Média")
    if titulo:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tarefas (titulo, descricao, prioridade) VALUES (%s, %s, %s)",
            (titulo, descricao, prioridade)
        )
        conn.commit()
        cur.close()
        conn.close()
    return redirect(url_for("index"))

@app.route("/concluir/<int:tarefa_id>", methods=["POST"])
def concluir(tarefa_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tarefas SET concluida = NOT concluida WHERE id = %s", (tarefa_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))

@app.route("/excluir/<int:tarefa_id>", methods=["POST"])
def excluir(tarefa_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tarefas WHERE id = %s", (tarefa_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
