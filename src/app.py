"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Club de Ajedrez": {
        "description": "Aprende estrategias y compite en torneos de ajedrez",
        "schedule": "Viernes, 15:30 - 17:00",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Clase de Programación": {
        "description": "Aprende fundamentos de programación y desarrolla proyectos de software",
        "schedule": "Martes y Jueves, 15:30 - 16:30",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Clase de Gimnasia": {
        "description": "Educación física y actividades deportivas",
        "schedule": "Lunes, Miércoles y Viernes, 14:00 - 15:00",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Básquetbol": {
        "description": "Juegos y entrenamientos competitivos de básquetbol",
        "schedule": "Lunes y Miércoles, 16:00 - 17:30",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Club de Fútbol": {
        "description": "Práctica de fútbol y partidos amistosos",
        "schedule": "Martes y Jueves, 16:00 - 17:30",
        "max_participants": 18,
        "participants": ["sarah@mergington.edu", "james@mergington.edu"]
    },
    "Estudio de Arte": {
        "description": "Técnicas de pintura, dibujo y escultura",
        "schedule": "Miércoles, 15:30 - 17:00",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu"]
    },
    "Banda de Música": {
        "description": "Aprende y toca música en conjunto",
        "schedule": "Lunes y Viernes, 15:30 - 16:30",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
    },
    "Equipo de Debate": {
        "description": "Desarrolla habilidades de oratoria y argumentación",
        "schedule": "Martes, 16:00 - 17:30",
        "max_participants": 12,
        "participants": ["rachel@mergington.edu"]
    },
    "Club de Ciencias": {
        "description": "Explora experimentos y descubrimientos científicos",
        "schedule": "Jueves, 15:30 - 17:00",
        "max_participants": 20,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate student is not already signed up for the activity
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
