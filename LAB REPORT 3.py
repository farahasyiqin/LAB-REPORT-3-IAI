import streamlit as st

rules = [
    {
        "name": "Top merit candidate", "priority": 100,
        "conditions": [ 
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship", 
        "priority": 80,
        "conditions": [ 
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
            "decision": "AWARD_PARTIAL",
            "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review", 
        "priority": 70, 
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": { 
            "decision": "REVIEW",
            "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible", 
        "priority": 95,
        "conditions": [ 
            ["cgpa", "<", 2.5]
        ],
        "action": { 
            "decision": "REJECT",
            "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [ 
            ["disciplinary_actions", ">=", 2]
        ],
        "action": { 
            "decision": "REJECT",
            "reason": "Too many disciplinary records"
        }
    }
]

st.title("🎓 Scholarship Decision System (Rule-Based)")

st.write("Enter the student details below:")

# User inputs
cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, step=0.01)
co_curricular_score = st.number_input("Co-curricular Score", min_value=0, max_value=100)
family_income = st.number_input("Family Income (RM)", min_value=0)
disciplinary_actions = st.number_input("Number of Disciplinary Actions", min_value=0)

# Helper function to evaluate rules
def check_condition(field_value, operator, condition_value):
    if operator == ">=": return field_value >= condition_value
    if operator == "<=": return field_value <= condition_value
    if operator == ">":  return field_value > condition_value
    if operator == "<":  return field_value < condition_value
    if operator == "==": return field_value == condition_value
    return False

if st.button("Evaluate Scholarship Decision"):
    student = {
        "cgpa": cgpa,
        "co_curricular_score": co_curricular_score,
        "family_income": family_income,
        "disciplinary_actions": disciplinary_actions
    }

    matched = []

    # Evaluate your rules exactly
    for rule in rules:
        conditions_met = True
        for field, operator, value in rule["conditions"]:
            if not check_condition(student[field], operator, value):
                conditions_met = False
                break
        if conditions_met:
            matched.append(rule)

    if matched:
        # Pick highest priority rule
        best_rule = sorted(matched, key=lambda x: x["priority"], reverse=True)[0]

        st.success(f"Decision: {best_rule['action']['decision']}")
        st.info(f"Reason: {best_rule['action']['reason']}")
        st.write(f"Matched Rule: **{best_rule['name']}** (Priority {best_rule['priority']})")

    else:
        st.error("No rule matched. Student does not qualify for any scholarship.")
