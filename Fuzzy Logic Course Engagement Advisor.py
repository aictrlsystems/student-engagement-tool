import streamlit as st
import numpy as np

# Fuzzy membership functions

def gaussian(x, c, sigma):
    return np.exp(-0.5 * ((x - c) / sigma) ** 2)

def trapezoid(x, a, b, c, d):
    return np.maximum(np.minimum(np.minimum((x - a)/(b - a + 1e-6), 1), (d - x)/(d - c + 1e-6)), 0)

# Defuzzify using centroid method with fallback
def defuzzify(x, mf, default=5.0):
    return np.sum(x * mf) / np.sum(mf) if np.sum(mf) != 0 else default

# Output space
x_output = np.linspace(0, 10, 200)

def main():
    st.title("Fuzzy Logic Course Engagement Advisor")

    st.header("Student Inputs")
    interest = st.slider("Interest Level (0 = Low, 10 = High)", 0.0, 10.0, 5.0)
    experience = st.slider("Prior Experience (0 = None, 10 = Extensive)", 0.0, 10.0, 5.0)
    course_type_label = st.selectbox("Course Type", ["Core", "Elective"])

    course_type_map = {"Core": 1.0, "Elective": 9.0}
    course_type = course_type_map[course_type_label]

    # Gaussian membership degrees
    μ_interest_low = gaussian(interest, 2, 1.5)
    μ_interest_medium = gaussian(interest, 5, 1.5)
    μ_interest_high = gaussian(interest, 8, 1.5)

    μ_experience_none = gaussian(experience, 1, 1.5)
    μ_experience_some = gaussian(experience, 5, 1.5)
    μ_experience_extensive = gaussian(experience, 9, 1.5)

    μ_course_core = gaussian(course_type, 1, 1.5)
    μ_course_elective = gaussian(course_type, 9, 1.5)

    # Define fuzzy rules (difficulty/support pairs)
    rule1 = np.fmin(np.fmin(μ_interest_low, μ_experience_none), μ_course_core)
    rule2 = np.fmin(np.fmin(μ_interest_medium, μ_experience_none), μ_course_core)
    rule3 = np.fmin(np.fmin(μ_interest_low, μ_experience_some), μ_course_core)
    rule4 = np.fmin(np.fmin(μ_interest_high, μ_experience_extensive), μ_course_elective)
    rule5 = np.fmin(np.fmin(μ_interest_low, μ_experience_none), μ_course_elective)
    rule6 = np.fmin(np.fmin(μ_interest_high, μ_experience_none), μ_course_core)
    rule7 = np.fmin(np.fmin(μ_interest_medium, μ_experience_extensive), μ_course_elective)
    rule8 = np.fmin(np.fmin(μ_interest_high, μ_experience_some), μ_course_core)
    rule9 = np.fmin(np.fmin(μ_interest_high, μ_experience_none), μ_course_elective)

    rule_activations = [
        ("Rule 1 (Easy/High)", rule1),
        ("Rule 2 (Moderate/High)", rule2),
        ("Rule 3 (Moderate/High)", rule3),
        ("Rule 4 (Challenging/Low)", rule4),
        ("Rule 5 (Easy/Medium)", rule5),
        ("Rule 6 (Moderate/Medium)", rule6),
        ("Rule 7 (Challenging/Medium)", rule7),
        ("Rule 8 (Challenging/Medium)", rule8),
        ("Rule 9 (Moderate/Medium)", rule9)
    ]

    # Output fuzzy sets (trapezoidal)
    difficulty_easy = trapezoid(x_output, 0, 0, 2, 4)
    difficulty_moderate = trapezoid(x_output, 3, 4.5, 5.5, 7)
    difficulty_challenging = trapezoid(x_output, 6, 8, 10, 10)

    support_high = trapezoid(x_output, 6, 8, 10, 10)
    support_medium = trapezoid(x_output, 3, 4.5, 5.5, 7)
    support_low = trapezoid(x_output, 0, 0, 2, 4)

    # Aggregate difficulty
    difficulty_agg = np.fmax.reduce([
        rule1 * difficulty_easy,
        rule2 * difficulty_moderate,
        rule3 * difficulty_moderate,
        rule4 * difficulty_challenging,
        rule5 * difficulty_easy,
        rule6 * difficulty_moderate,
        rule7 * difficulty_challenging,
        rule8 * difficulty_challenging,
        rule9 * difficulty_moderate
    ])

    # Aggregate support
    support_agg = np.fmax.reduce([
        rule1 * support_high,
        rule2 * support_high,
        rule3 * support_high,
        rule4 * support_low,
        rule5 * support_medium,
        rule6 * support_medium,
        rule7 * support_medium,
        rule8 * support_low,
        rule9 * support_medium
    ])

    # Defuzzify
    difficulty_score = defuzzify(x_output, difficulty_agg)
    support_score = defuzzify(x_output, support_agg)

    # Output
    st.header("System Recommendation")
    st.write(f"**Assignment Difficulty Score:** {difficulty_score:.2f} (0 = Easy, 10 = Challenging)")
    st.write(f"**Support Level Score:** {support_score:.2f} (0 = None, 10 = Maximum Support)")

    st.subheader("Rule Activation Levels")
    for label, activation in rule_activations:
        st.write(f"{label}: {activation:.3f}")

    if all(activation < 0.01 for _, activation in rule_activations):
        st.warning("⚠️ None of the rules activated. Your input combination may fall outside all rule coverage.")

    st.text("\nPress Ctrl+C in terminal to exit this app.")

if __name__ == "__main__":
    main()
