import streamlit as st
import re
from datetime import datetime

# -------------------------------------------------
# Rule-Based System Components
# -------------------------------------------------

class FAQRuleBasedSystem:
    def __init__(self):
        self.rules = self._initialize_rules()
        self.faqs = self._initialize_faqs()
    
    def _initialize_faqs(self):
        """Initialize FAQ knowledge base"""
        return {
            "How do I book an appointment with the Dean?":
                "Appointments are booked through the school office or official university email.",
            "What should I do if I have an academic complaint?":
                "First consult your lecturer or Head of Department. If unresolved, escalate through formal university channels.",
            "How can I get my academic transcript?":
                "Ensure you have completed all assessments and cleared any outstanding fees.",
            "What is the procedure for deferment of studies?":
                "Submit a deferment request form through your department with supporting documents.",
            "Who do I contact for examination issues?":
                "Contact your department examination coordinator or HOD.",
            "How do I appeal exam results?":
                "Appeals must be submitted in writing through your department within the stipulated time.",
            "Can I change my course or program?":
                "Course changes are subject to university policies and approval by the relevant offices.",
            "What happens if I miss an examination?":
                "You must provide valid reasons and supporting evidence to your department immediately.",
            "How do I apply for special examinations?":
                "Apply through your department with medical or other valid documentation.",
            "Where can I get academic advising?":
                "Academic advising is offered by your assigned academic advisor or Head of Department."
        }
    
    def _initialize_rules(self):
        """Initialize keyword-based rules for question matching"""
        return {
            "appointment": {
                "keywords": ["appointment", "meet", "schedule", "see dean", "meeting"],
                "response": "Appointments are booked through the school office or official university email. Contact the Dean's secretary at ext. 2000."
            },
            "transcript": {
                "keywords": ["transcript", "academic record", "results", "grades"],
                "response": "To get your academic transcript, ensure you have completed all assessments and cleared any outstanding fees. Visit the Registrar's office or apply online through the student portal."
            },
            "exam_appeal": {
                "keywords": ["appeal", "contest", "dispute", "exam result", "grade appeal"],
                "response": "Appeals must be submitted in writing through your department within 14 days of result publication. Include your registration number and specific grounds for appeal."
            },
            "missed_exam": {
                "keywords": ["missed exam", "absent", "didn't sit", "couldn't take exam"],
                "response": "If you miss an examination, provide valid reasons with supporting evidence (medical certificate, etc.) to your department immediately. Special exams may be arranged based on approval."
            },
            "deferment": {
                "keywords": ["defer", "postpone", "take break", "pause studies"],
                "response": "Submit a deferment request form through your department with supporting documents (medical, financial hardship proof, etc.). Maximum deferment period is typically 2 semesters."
            },
            "course_change": {
                "keywords": ["change course", "transfer program", "switch major", "change program"],
                "response": "Course changes are subject to university policies and require approval from both departments and the Academic Board. Apply through the Registrar's office with valid academic reasons."
            },
            "complaint": {
                "keywords": ["complaint", "issue", "problem", "unfair", "grievance"],
                "response": "First consult your lecturer or Head of Department. If unresolved, escalate to the Dean's office through formal university channels with documented evidence."
            },
            "special_exam": {
                "keywords": ["special exam", "supplementary", "makeup exam"],
                "response": "Apply for special examinations through your department with medical or other valid documentation. Applications must be submitted within the specified deadline."
            },
            "advising": {
                "keywords": ["advisor", "academic advice", "guidance", "counseling"],
                "response": "Academic advising is offered by your assigned academic advisor or Head of Department. Schedule appointments through your department office."
            },
            "fees": {
                "keywords": ["fees", "payment", "tuition", "financial"],
                "response": "For fee-related inquiries, visit the Finance Office or check the student portal. Payment deadlines and methods are communicated each semester."
            }
        }
    
    def match_question(self, question):
        """Match question to rules using keyword detection"""
        question_lower = question.lower()
        matched_rules = []
        
        # Check each rule for keyword matches
        for rule_name, rule_data in self.rules.items():
            for keyword in rule_data["keywords"]:
                if keyword in question_lower:
                    matched_rules.append({
                        "rule": rule_name,
                        "response": rule_data["response"],
                        "confidence": self._calculate_confidence(question_lower, rule_data["keywords"])
                    })
                    break
        
        # Sort by confidence and return best match
        if matched_rules:
            matched_rules.sort(key=lambda x: x["confidence"], reverse=True)
            return matched_rules[0]
        
        return None
    
    def _calculate_confidence(self, question, keywords):
        """Calculate confidence score based on keyword matches"""
        matches = sum(1 for keyword in keywords if keyword in question)
        return (matches / len(keywords)) * 100

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Dean FAQ System | DeKUT",
    page_icon="🎓",
    layout="centered"
)

# Initialize session state
if 'faq_system' not in st.session_state:
    st.session_state.faq_system = FAQRuleBasedSystem()
if 'submitted_questions' not in st.session_state:
    st.session_state.submitted_questions = []
if 'admin_faqs' not in st.session_state:
    st.session_state.admin_faqs = {}

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #0aae28f6;'>
        Dedan Kimathi University of Technology
    </h1>
    <h3 style='text-align: center;'>Dean's Frequently Asked Questions Portal</h3>
    <p style='text-align: center; color: #666;'>🤖 Powered by Rule-Based AI System</p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# Navigation Tabs
# -------------------------------------------------
tabs = st.tabs(["📘 Student FAQs", "✍ Ask a Question", "🛠 Dean / Admin Panel", "📊 System Info"])

# -------------------------------------------------
# TAB 1: STUDENT FAQs
# -------------------------------------------------
with tabs[0]:
    st.subheader("Frequently Asked Questions (Students)")
    
    # Combine default FAQs with admin-added ones
    all_faqs = {**st.session_state.faq_system.faqs, **st.session_state.admin_faqs}
    
    # Search functionality
    search_query = st.text_input("🔍 Search FAQs", placeholder="Type keywords to search...")
    
    if search_query:
        filtered_faqs = {q: a for q, a in all_faqs.items() 
                        if search_query.lower() in q.lower() or search_query.lower() in a.lower()}
        if filtered_faqs:
            st.info(f"Found {len(filtered_faqs)} matching FAQ(s)")
            for question, answer in filtered_faqs.items():
                with st.expander(question):
                    st.write(answer)
        else:
            st.warning("No matching FAQs found. Try different keywords.")
    else:
        for question, answer in all_faqs.items():
            with st.expander(question):
                st.write(answer)

# -------------------------------------------------
# TAB 2: ASK A QUESTION
# -------------------------------------------------
with tabs[1]:
    st.subheader("Ask a Question (Students)")
    st.write("Submit your question and get an instant answer from our rule-based system.")
    
    with st.form("student_question_form"):
        reg_no = st.text_input("Registration Number", placeholder="e.g., S13/12345/20")
        student_question = st.text_area("Your Question", height=120, 
                                       placeholder="Type your question here...")
        submit = st.form_submit_button("Submit Question")
        
        if submit:
            if reg_no and student_question:
                # Try to match question using rule-based system
                match = st.session_state.faq_system.match_question(student_question)
                
                if match:
                    st.success("✅ Question submitted successfully!")
                    st.markdown("### 🤖 Automated Response")
                    st.info(match["response"])
                    st.progress(match["confidence"] / 100)
                    st.caption(f"Confidence: {match['confidence']:.1f}% | Rule: {match['rule']}")
                    
                    # Save to submitted questions
                    st.session_state.submitted_questions.append({
                        "reg_no": reg_no,
                        "question": student_question,
                        "answer": match["response"],
                        "rule": match["rule"],
                        "confidence": match["confidence"],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "answered"
                    })
                else:
                    st.warning("⚠ No automated answer found. Your question has been forwarded to the Dean's office.")
                    st.session_state.submitted_questions.append({
                        "reg_no": reg_no,
                        "question": student_question,
                        "answer": None,
                        "rule": None,
                        "confidence": 0,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "status": "pending"
                    })
            else:
                st.warning("⚠ Please fill in all fields before submitting.")

# -------------------------------------------------
# TAB 3: ADMIN PANEL
# -------------------------------------------------
with tabs[2]:
    st.subheader("Dean / Admin Panel")
    st.info("This section is restricted to authorized staff only.")
    
    admin_tabs = st.tabs(["Add FAQ", "View Submissions", "Manage Rules"])
    
    # Add FAQ
    with admin_tabs[0]:
        st.markdown("#### Add New FAQ")
        with st.form("admin_form"):
            admin_question = st.text_input("Question")
            admin_answer = st.text_area("Answer", height=120)
            save = st.form_submit_button("Save Answer")
            
            if save:
                if admin_question and admin_answer:
                    st.session_state.admin_faqs[admin_question] = admin_answer
                    st.success("✅ Answer saved successfully.")
                else:
                    st.warning("⚠ Please provide both question and answer.")
    
    # View Submissions
    with admin_tabs[1]:
        st.markdown("#### Student Question Submissions")
        if st.session_state.submitted_questions:
            for i, submission in enumerate(reversed(st.session_state.submitted_questions)):
                with st.expander(f"{submission['reg_no']} - {submission['timestamp']} ({submission['status']})"):
                    st.write(f"**Question:** {submission['question']}")
                    if submission['answer']:
                        st.write(f"**Automated Answer:** {submission['answer']}")
                        st.write(f"**Rule Used:** {submission['rule']}")
                        st.write(f"**Confidence:** {submission['confidence']:.1f}%")
                    else:
                        st.write("**Status:** Awaiting manual response")
        else:
            st.info("No questions submitted yet.")
    
    # Manage Rules
    with admin_tabs[2]:
        st.markdown("#### Current Rules")
        for rule_name, rule_data in st.session_state.faq_system.rules.items():
            with st.expander(f"Rule: {rule_name}"):
                st.write(f"**Keywords:** {', '.join(rule_data['keywords'])}")
                st.write(f"**Response:** {rule_data['response']}")

# -------------------------------------------------
# TAB 4: SYSTEM INFO
# -------------------------------------------------
with tabs[3]:
    st.subheader("Rule-Based System Information")
    
    st.markdown("""
    ### How the System Works
    
    This FAQ system uses a **rule-based approach** to automatically answer student questions:
    
    1. **Keyword Matching**: Questions are analyzed for specific keywords
    2. **Rule Matching**: Keywords trigger predefined rules
    3. **Confidence Scoring**: System calculates how well the question matches each rule
    4. **Best Answer Selection**: The highest-confidence match is returned
    
    ### System Statistics
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rules", len(st.session_state.faq_system.rules))
    with col2:
        st.metric("Total FAQs", len(st.session_state.faq_system.faqs) + len(st.session_state.admin_faqs))
    with col3:
        answered = sum(1 for q in st.session_state.submitted_questions if q['status'] == 'answered')
        st.metric("Questions Answered", answered)
    
    st.markdown("""
    ### Available Rules
    The system can automatically respond to questions about:
    - Appointments with the Dean
    - Academic transcripts
    - Exam appeals
    - Missed examinations
    - Study deferment
    - Course changes
    - Academic complaints
    - Special examinations
    - Academic advising
    - Fees and payments
    """)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.divider()
st.markdown(
    "<p style='text-align: center;'>© 2025 Dedan Kimathi University of Technology</p>",
    unsafe_allow_html=True
)