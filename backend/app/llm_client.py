
import json

async def query_llm(symptoms: str):
    
    s = symptoms.lower()
    disclaimer = "."

   
    conditions = []
    recommendations = []

   
    if any(x in s for x in ["chest pain", "severe shortness of breath", "loss of consciousness", "sudden weakness"]):
        conditions.append({
            "name": "Possible emergency condition",
            "likelihood": 0.9,
            "rationale": "Contains red-flag symptoms requiring urgent evaluation."
        })
        recommendations = [
            "Seek emergency medical care immediately.",
            "Do not ignore severe or worsening symptoms."
        ]
        return {
            "conditions": conditions,
            "recommendations": recommendations,
            "disclaimer": disclaimer
        }

 
    if "fever" in s and ("cough" in s or "sore throat" in s):
        conditions.append({
            "name": "Viral respiratory infection",
            "likelihood": 0.7,
            "rationale": "Fever + cough/sore throat commonly indicates viral illness."
        })
        recommendations = [
            "Rest and drink plenty of fluids.",
            "Monitor symptoms for 48 hours.",
            "Seek medical help if fever persists or breathing becomes difficult."
        ]

    elif any(x in s for x in ["runny nose", "sneezing", "itchy eyes"]):
        conditions.append({
            "name": "Allergic rhinitis",
            "likelihood": 0.5,
            "rationale": "Runny nose and sneezing often indicate allergies."
        })
        recommendations = [
            "Avoid dust or allergens.",
            "Use antihistamines if needed.",
            "Consult a doctor if symptoms persist."
        ]
    else:
        conditions.append({
            "name": "Non-specific symptoms",
            "likelihood": 0.3,
            "rationale": "Symptoms do not match a specific condition clearly."
        })
        recommendations = [
            "Rest and stay hydrated.",
            "Observe symptoms for 1–2 days.",
            "Consult a healthcare professional if symptoms worsen."
        ]

    return {
        "conditions": conditions,
        "recommendations": recommendations,
        "disclaimer": disclaimer
    }
