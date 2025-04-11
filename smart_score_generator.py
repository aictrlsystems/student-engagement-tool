# Import Libraries
import streamlit as st
from textblob import TextBlob

# Define motivation-related keywords
motivation_keywords = [
    "apply", "build", "curious", "improve", "learn", "master", "solve", 
    "real-world", "understand", "design", "hands-on", "explore", "develop", "experiment"
]

# Confidence phrases to boost score
confidence_phrases = [
    "real-world", "apply", "confident", "ready", "build on", "prior experience"
]

def keyword_score(response):
    score = 0
    for word in motivation_keywords:
        if word.lower() in response.lower():
            score += 1
    return min(score / 5.0, 1.0)  # normalize to 0–1

def confidence_boost(response):
    boost = 0
    for phrase in confidence_phrases:
        if phrase.lower() in response.lower():
            boost += 0.1
    return min(boost, 0.5)

def analyze_response(response, manual_boost=False):
    sentiment = TextBlob(response).sentiment.polarity
    length_score = min(len(response.split()) / 20.0, 1.0)
    keyword_weight = keyword_score(response)
    confidence = confidence_boost(response)
    base_total = (sentiment + length_score + keyword_weight) / 3
    adjusted_total = base_total + confidence
    if manual_boost:
        adjusted_total += 0.5
    return min(adjusted_total * 2, 2)  # scale and cap at 2

def main():
    st.title("Student Engagement Index")

    st.write("Answer the following questions to assess your motivational readiness.")

    q1 = st.text_area("1. What motivated you to enroll in this course?")
    q2 = st.text_area("2. What do you hope to gain from this course?")
    q3 = st.text_area("3. Have you had any prior experience with this subject or related topics?")
    q4 = st.text_area("4. What challenges do you anticipate facing in this course?")
    q5 = st.text_area("5. How do you plan to stay engaged and motivated throughout the semester?")

    booster = st.checkbox("I feel confident and ready to engage in this course.")

    if st.button("Generate Score"):
        scores = []
        for response in [q1, q2, q3, q4, q5]:
            scores.append(analyze_response(response, manual_boost=booster))

        total = sum(scores)
        final_score = round((total / 10) * 10, 2)

        st.markdown(f"### Motivational Readiness Score: {final_score} / 10")

        if final_score >= 8:
            st.success("Highly motivated and prepared!")
        elif final_score >= 5:
            st.info("Moderately motivated with some readiness.")
        else:
            st.warning("Motivational readiness appears low—may need support.")

if __name__ == "__main__":
    main()
