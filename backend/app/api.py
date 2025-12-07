from fastapi import APIRouter, HTTPException
from .schemas import SymptomRequest, SymptomResponse, Condition
from .llm_client import query_llm
from .safety import contains_red_flag

router = APIRouter()

# ----------------------------
# List of ALL symptoms for UI
# ----------------------------
SYMPTOM_LIST = [
    "Fever", "Cough", "Cold", "Sore throat", "Runny nose",
    "Headache", "Migraine", "Fatigue", "Weakness",
    "Chest pain", "Shortness of breath", "Wheezing",
    "Back pain", "Joint pain", "Neck pain",
    "Stomach pain", "Abdominal cramps", "Nausea",
    "Vomiting", "Diarrhea", "Constipation",
    "Dizziness", "Fainting", "Numbness", "Tingling",
    "Blurred vision", "Eye pain",
    "Skin rash", "Itching", "Redness",
    "Anxiety", "Stress", "Insomnia",
    "Loss of appetite", "Weight loss", "Weight gain",
    "Body aches", "Chills", "Sweating",
    "Rapid heartbeat", "Slow heartbeat",
    "Frequent urination", "Burning urination",
    "Swelling in legs", "Swelling in hands",
    "Hair loss", "Dry skin", "Acne",
    "Allergy", "Sneezing", "Sinus pressure",
    "Ear pain", "Hearing loss",
    "Difficulty swallowing",
    "Memory loss", "Confusion",
    "Mood swings"
]


# ----------------------------
# GET — Return all symptoms
# ----------------------------
@router.get("/symptoms/list")
async def get_symptom_list():
    return {"symptoms": SYMPTOM_LIST}


# ----------------------------
# POST — Analyze symptoms
# ----------------------------
@router.post("/symptoms", response_model=SymptomResponse)
async def analyze_symptoms(req: SymptomRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(400, "Empty symptoms text")

    # Safety check for red-flag symptoms
    if contains_red_flag(text):
        return SymptomResponse(
            conditions=[
                Condition(
                    name="Potential emergency condition",
                    likelihood=0.95,
                    rationale="Contains red-flag symptoms"
                )
            ],
            recommendations=["Seek emergency medical care immediately"],
            disclaimer="Educational only. If you have severe symptoms, call emergency services."
        )

    # Call LLM
    try:
        out = await query_llm(text)
    except Exception as e:
        raise HTTPException(500, f"LLM error: {e}")

  
    conditions = [
        Condition(
            name=c.get("name", "Unknown"),
            likelihood=float(c.get("likelihood", 0)),
            rationale=c.get("rationale")
        )
        for c in out.get("conditions", [])
    ]

    recs = out.get("recommendations", [])
    disc = out.get("disclaimer", "Not medical advice; consult a healthcare professional.")

    return SymptomResponse(
        conditions=conditions,
        recommendations=recs,
        disclaimer=disc
    )
