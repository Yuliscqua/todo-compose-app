import os
import time

import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "todo_db")
DB_USER = os.environ.get("DB_USER", "todo_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "todo_password")
DB_PORT = os.environ.get("DB_PORT", "5432")

app = FastAPI()

# Autoriser les appels venant du frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Task(BaseModel):
    title: str


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )


def init_db():
    """Crée la table tasks si elle n'existe pas encore.
    Réessaie plusieurs fois au cas où PostgreSQL ne serait pas encore prêt."""
    retries = 10
    while retries > 0:
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL
                );
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            print("Base de données initialisée avec succès.")
            return
        except psycopg2.OperationalError as e:
            retries -= 1
            print(f"PostgreSQL non disponible, nouvelle tentative... ({e})")
            time.sleep(3)
    raise Exception("Impossible de se connecter à PostgreSQL après plusieurs tentatives.")


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    tasks = [{"id": row[0], "title": row[1]} for row in rows]
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title) VALUES (%s) RETURNING id;",
        (task.title,),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {"id": new_id, "title": task.title}