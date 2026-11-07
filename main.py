import streamlit as st  # type: ignore[reportMissingImports]
import json
import os
import time
import random
import hashlib
import hmac
import secrets
import pandas as pd
from datetime import datetime
try:
    st_autorefresh = getattr(
        __import__("streamlit_autorefresh"), "st_autorefresh"
    )
except ImportError:
    # Keep the app usable when the optional auto-refresh package is absent.
    def st_autorefresh(*, interval, key=None):
        return None

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="PlacementPro | Mock Placement Test",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# 2. FILE CONFIGURATION
# =====================================================

DATA_DIR = "data"

STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")
RESULTS_FILE = os.path.join(DATA_DIR, "results.json")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin@12345"

EXAM_DURATION = 90 * 60
CORRECT_MARKS = 4
NEGATIVE_MARKS = 1
TOTAL_QUESTIONS = 60

os.makedirs(DATA_DIR, exist_ok=True)


def load_json(path, default):
    try:
        if not os.path.exists(path):
            save_json(path, default)
            return default

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    except (json.JSONDecodeError, OSError):
        return default


def save_json(path, data):
    temp_path = path + ".tmp"

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    os.replace(temp_path, path)


# =====================================================
# 3. PASSWORD SECURITY
# =====================================================

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        200000
    )

    return salt + ":" + hashed.hex()


def verify_password(password, stored):
    try:
        salt, old_hash = stored.split(":")
        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            200000
        ).hex()

        return hmac.compare_digest(new_hash, old_hash)

    except (ValueError, AttributeError):
        return False


# =====================================================
# 4. ADVANCED QUESTION BANK - 60 QUESTIONS
# =====================================================

def make_q(category, question, options, correct, explanation):
    return {
        "id": secrets.token_hex(5),
        "category": category,
        "question": question,
        "options": options,
        "correct": correct,
        "explanation": explanation
    }


SEED_QUESTIONS = [

# QUANTITATIVE APTITUDE

make_q("Quantitative Aptitude",
"A sum becomes Rs. 13,310 in 3 years at 10% compound interest. Find the principal.",
["10000", "11000", "12000", "9000"], 0,
"13310 / 1.1^3 = 10000."),

make_q("Quantitative Aptitude",
"A 180 m train crosses a pole in 9 seconds. Find its speed.",
["60 km/h", "72 km/h", "80 km/h", "90 km/h"], 1,
"180/9 = 20 m/s = 72 km/h."),

make_q("Quantitative Aptitude",
"A completes work in 12 days and B in 18 days. Together?",
["6 days", "7.2 days", "8 days", "9 days"], 1,
"Combined rate is 1/12 + 1/18 = 5/36."),

make_q("Quantitative Aptitude",
"Two numbers are in ratio 5:7 and their HCF is 9. Find their LCM.",
["315", "280", "350", "405"], 0,
"Numbers are 45 and 63. LCM is 315."),

make_q("Quantitative Aptitude",
"Cost price is Rs. 900. Profit is 20%, discount is 10%. Find marked price.",
["1100", "1200", "1250", "1350"], 1,
"SP = 1080; MP = 1080/0.9 = 1200."),

make_q("Quantitative Aptitude",
"Average of 8 numbers is 24. Replace 18 with 34. New average?",
["25", "26", "27", "28"], 1,
"New average = (192-18+34)/8 = 26."),

make_q("Quantitative Aptitude",
"40 litres mixture has milk:water = 7:3. How much water to add for 7:5?",
["6 L", "8 L", "10 L", "12 L"], 1,
"Milk 28 L, water 12 L. Add 8 L."),

make_q("Quantitative Aptitude",
"Find compound interest on Rs. 8000 at 5% for 2 years.",
["800", "820", "840", "860"], 1,
"Amount = 8820. Interest = 820."),

make_q("Quantitative Aptitude",
"Boat covers 30 km downstream in 2 hours and upstream in 3 hours. Stream speed?",
["2", "2.5", "3", "3.5"], 1,
"Downstream 15, upstream 10. Stream = 2.5 km/h."),

make_q("Quantitative Aptitude",
"If x + 1/x = 5, find x² + 1/x².",
["21", "23", "25", "27"], 1,
"Square and subtract 2. Answer 23."),

make_q("Quantitative Aptitude",
"Two dice are thrown. Probability that their sum is 8?",
["1/6", "5/36", "1/9", "7/36"], 1,
"Five favourable outcomes out of 36."),

make_q("Quantitative Aptitude",
"Income increases 20%, expenditure increases 10%. Original savings are 25% of income. Increase in savings?",
["40%", "45%", "50%", "60%"], 2,
"Take income 100: new savings = 37.5 versus 25. Increase 50%."),

make_q("Quantitative Aptitude",
"Number of distinct arrangements of LEVEL?",
["20", "30", "60", "120"], 1,
"5!/(2! x 2!) = 30."),

make_q("Quantitative Aptitude",
"One pipe fills in 15 minutes, another empties in 20 minutes. Together?",
["45 min", "50 min", "60 min", "75 min"], 2,
"Net rate = 1/60 tank per minute."),

make_q("Quantitative Aptitude",
"Find sum of first 20 terms: 3, 7, 11, 15...",
["800", "820", "840", "860"], 1,
"S20 = 10 x (6 + 76) = 820."),

# LOGICAL REASONING

make_q("Logical Reasoning",
"Find next: 2, 6, 12, 20, 30, 42, ?",
["48", "54", "56", "60"], 2,
"Pattern n(n+1). Next 7x8 = 56."),

make_q("Logical Reasoning",
"Find next: AZ, BY, CX, DW, ?",
["EV", "FU", "EW", "FV"], 0,
"First letters increase and second decrease."),

make_q("Logical Reasoning",
"If TABLE is coded UBCMF, how is CHAIR coded?",
["DIBJS", "DIBIR", "DHBJS", "DICJS"], 0,
"Every letter shifts forward by one."),

make_q("Logical Reasoning",
"A is brother of B. B is mother of C. A is C's?",
["Father", "Uncle", "Brother", "Grandfather"], 1,
"Mother's brother is maternal uncle."),

make_q("Logical Reasoning",
"Walk 10 km north, 6 km east, 10 km south. Final position?",
["6 km east", "6 km west", "10 km north", "16 km east"], 0,
"North and south cancel."),

make_q("Logical Reasoning",
"All programmers are logical. Some logical people are artists. Are some programmers artists?",
["Definitely true", "Definitely false", "Cannot be determined", "Both"], 2,
"The overlap is not established."),

make_q("Logical Reasoning",
"Find the odd one: 27, 64, 125, 196.",
["27", "64", "125", "196"], 3,
"First three are perfect cubes."),

make_q("Logical Reasoning",
"If 1 January is Monday in a non-leap year, 1 March is?",
["Wednesday", "Thursday", "Friday", "Saturday"], 1,
"59 days shift gives Thursday."),

make_q("Logical Reasoning",
"Five people: D is left of A, A left of B, B left of C, C left of E. Who is middle?",
["A", "B", "C", "D"], 1,
"Order D-A-B-C-E."),

make_q("Logical Reasoning",
"Find next: 3, 8, 18, 38, 78, ?",
["148", "156", "158", "168"], 2,
"Multiply by 2 and add 2."),

make_q("Logical Reasoning",
"Rank 12th from top and 19th from bottom. Total students?",
["29", "30", "31", "32"], 1,
"12 + 19 - 1 = 30."),

make_q("Logical Reasoning",
"If + means multiplication and x means subtraction, evaluate 8 + 3 x 4.",
["20", "28", "32", "36"], 0,
"8 x 3 - 4 = 20."),

make_q("Logical Reasoning",
"Find next: 121, 144, 169, 196, ?",
["210", "215", "225", "256"], 2,
"Squares of 11,12,13,14,15."),

make_q("Logical Reasoning",
"A is taller than B. C is taller than A. D is shorter than B. Tallest?",
["A", "B", "C", "D"], 2,
"C is tallest."),

make_q("Logical Reasoning",
"Complete: AB, DE, GH, JK, ?",
["LM", "MN", "NO", "OP"], 1,
"Each pair advances three letters."),

# VERBAL ABILITY

make_q("Verbal Ability",
"Choose correct sentence.",
["Neither boys are present.", "Neither of the boys is present.", "Neither boys is present.", "Neither of boys are present."], 1,
"Neither takes a singular verb."),

make_q("Verbal Ability",
"Synonym of Meticulous?",
["Careless", "Precise", "Hasty", "Casual"], 1,
"Meticulous means very careful."),

make_q("Verbal Ability",
"Antonym of Obsolete?",
["Outdated", "Ancient", "Modern", "Useless"], 2,
"Obsolete means outdated."),

make_q("Verbal Ability",
"Had I known, I ____ attended.",
["will have", "would have", "would", "had"], 1,
"Third conditional uses would have."),

make_q("Verbal Ability",
"Passive voice: The team completed the project.",
["The project completed by team.", "The project was completed by the team.", "The project is completed.", "The team was completed."], 1,
"Past simple passive: was + past participle."),

make_q("Verbal Ability",
"Correct spelling?",
["Accomodation", "Accommodation", "Acommodation", "Accommadation"], 1,
"Accommodation is correct."),

make_q("Verbal Ability",
"Find the error: Each of the students have submitted their assignment.",
["Each of", "the students", "have submitted", "their assignment"], 2,
"Each is singular: has submitted."),

make_q("Verbal Ability",
"Meaning of Burn the midnight oil?",
["Waste electricity", "Work late at night", "Start fire", "Sleep early"], 1,
"It means working late at night."),

make_q("Verbal Ability",
"She is proficient ____ Python.",
["at", "in", "on", "with"], 1,
"Proficient in is the standard expression."),

make_q("Verbal Ability",
"Indirect speech: He said, I am busy.",
["He said I am busy.", "He said that he was busy.", "He says he is busy.", "He said he busy."], 1,
"Present changes to past in reported speech."),

make_q("Verbal Ability",
"A person who speaks many languages?",
["Linguist", "Polyglot", "Orator", "Translator"], 1,
"Polyglot speaks multiple languages."),

make_q("Verbal Ability",
"Choose correct sentence.",
["Despite of rain, we played.", "Despite the rain, we played.", "Although the rain, we played.", "In spite rain, we played."], 1,
"Despite is followed directly by a noun phrase."),

make_q("Verbal Ability",
"Meaning of Pragmatic?",
["Idealistic", "Practical", "Emotional", "Uncertain"], 1,
"Pragmatic means practical."),

make_q("Verbal Ability",
"Doctor : Hospital :: Teacher : ?",
["Court", "School", "Laboratory", "Bank"], 1,
"Teacher commonly works in a school."),

make_q("Verbal Ability",
"No sooner ____ the train left than it started raining.",
["has", "had", "was", "did"], 1,
"No sooner had...than."),

# TECHNICAL KNOWLEDGE

make_q("Technical Knowledge",
"Binary search time complexity?",
["O(n)", "O(log n)", "O(n log n)", "O(1)"], 1,
"Search space is halved each iteration."),

make_q("Technical Knowledge",
"Java class acquires properties of another class using?",
["Encapsulation", "Inheritance", "Polymorphism", "Abstraction"], 1,
"Inheritance supports code reuse."),

make_q("Technical Knowledge",
"Which SQL clause filters groups?",
["WHERE", "ORDER BY", "HAVING", "DISTINCT"], 2,
"HAVING filters aggregated groups."),

make_q("Technical Knowledge",
"Data structure used in recursive calls?",
["Queue", "Stack", "Heap", "Graph"], 1,
"Function calls are maintained in call stack."),

make_q("Technical Knowledge",
"Which normal form removes partial dependencies?",
["1NF", "2NF", "3NF", "BCNF"], 1,
"Second Normal Form removes partial dependencies."),

make_q("Technical Knowledge",
"Reliable connection-oriented protocol?",
["UDP", "IP", "TCP", "ARP"], 2,
"TCP provides reliable ordered communication."),

make_q("Technical Knowledge",
"Python type of []?",
["tuple", "dict", "list", "set"], 2,
"Square brackets create a list."),

make_q("Technical Knowledge",
"Which OOP concept hides implementation complexity?",
["Inheritance", "Encapsulation", "Abstraction", "Overloading"], 2,
"Abstraction hides unnecessary implementation details."),

make_q("Technical Knowledge",
"Average hash table search complexity?",
["O(1)", "O(log n)", "O(n)", "O(n log n)"], 0,
"Average lookup is constant time."),

make_q("Technical Knowledge",
"SQL command that removes a table structure?",
["DELETE", "REMOVE", "DROP", "TRUNCATE"], 2,
"DROP removes the table."),

make_q("Technical Knowledge",
"Which scheduling algorithm may cause starvation?",
["FCFS", "Round Robin", "Priority Scheduling", "FIFO"], 2,
"Low priority processes may wait indefinitely."),

make_q("Technical Knowledge",
"Binary 1010 AND 1100?",
["1000", "1110", "0110", "1010"], 0,
"Bitwise AND gives 1000."),

make_q("Technical Knowledge",
"HTTP status code for Not Found?",
["200", "301", "403", "404"], 3,
"404 indicates resource not found."),

make_q("Technical Knowledge",
"Which ACID property ensures all-or-nothing?",
["Consistency", "Isolation", "Atomicity", "Durability"], 2,
"Atomicity ensures complete execution or rollback."),

make_q("Technical Knowledge",
"Quick Sort worst-case complexity?",
["O(n)", "O(n log n)", "O(n²)", "O(log n)"], 2,
"Highly unbalanced partitions result in O(n²).")
]


# =====================================================
# 5. INITIALIZE DATA
# =====================================================

if not os.path.exists(STUDENTS_FILE):
    save_json(STUDENTS_FILE, {})

if not os.path.exists(RESULTS_FILE):
    save_json(RESULTS_FILE, [])

if not os.path.exists(QUESTIONS_FILE):
    save_json(QUESTIONS_FILE, SEED_QUESTIONS)

students = load_json(STUDENTS_FILE, {})
questions = load_json(QUESTIONS_FILE, SEED_QUESTIONS)
results = load_json(RESULTS_FILE, [])


# =====================================================
# 6. SESSION STATE
# =====================================================

defaults = {
    "logged_in": False,
    "username": "",
    "role": "",
    "exam_active": False,
    "exam_questions": [],
    "exam_answers": {},
    "exam_start": None,
    "exam_index": 0,
    "exam_submitted": False,
    "exam_result": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# 7. DESIGN CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background: #f4f6fc;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.nav-title {
    background: linear-gradient(110deg,#172554,#4f46e5,#9333ea);
    padding: 24px;
    border-radius: 16px;
    color: white;
    margin-bottom: 18px;
}

.nav-title h1 {
    color: white;
    margin: 0;
}

.nav-title p {
    color: #e0e7ff;
    margin: 5px 0 0;
}

div[role="radiogroup"] {
    background: white;
    padding: 12px;
    border-radius: 14px;
    border: 1px solid #dce3f1;
    gap: 8px;
}

div[role="radiogroup"] label {
    background: #eef2ff;
    border-radius: 9px;
    padding: 8px 13px;
    font-weight: 600;
}

div[role="radiogroup"] label:hover {
    background: #c7d2fe;
}

div.stButton > button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 40px;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color: white;
    border: none;
}

.card {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 3px 12px rgba(0,0,0,.04);
    min-height: 120px;
}

.card h2 {
    margin: 0;
    color: #4338ca;
}

.hero {
    background: linear-gradient(120deg,#172554,#2563eb,#9333ea);
    color: white;
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 20px;
}

.hero h1 {
    color: white;
}

.small-note {
    color: #64748b;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 8. HEADER AND HORIZONTAL NAVIGATION
# =====================================================

st.markdown("""
<div class="nav-title">
    <h1>🎓 PlacementPro</h1>
    <p>Advanced Mock Placement Test & Career Preparation Portal</p>
</div>
""", unsafe_allow_html=True)

menu = [
    "🏠 Home",
    "🔐 Student Login",
    "📝 Register",
    "👨‍🎓 Student Dashboard",
    "📚 Take Test",
    "📊 My Results",
    "🏆 Leaderboard",
    "🔑 Admin Login",
    "⚙️ Admin Panel"
]

col_nav, col_logout = st.columns([5, 1])

with col_nav:
    page = st.radio(
        "Navigation",
        menu,
        horizontal=True,
        label_visibility="collapsed",
        key="top_navigation"
    )

with col_logout:
    if st.session_state.logged_in:
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

st.divider()


# =====================================================
# 9. COMMON FUNCTIONS
# =====================================================

def reload_data():
    global students, questions, results
    students = load_json(STUDENTS_FILE, {})
    questions = load_json(QUESTIONS_FILE, [])
    results = load_json(RESULTS_FILE, [])


def require_student():
    return (
        st.session_state.logged_in
        and st.session_state.role == "student"
    )


def require_admin():
    return (
        st.session_state.logged_in
        and st.session_state.role == "admin"
    )


def reset_exam():
    st.session_state.exam_active = False
    st.session_state.exam_questions = []
    st.session_state.exam_answers = {}
    st.session_state.exam_start = None
    st.session_state.exam_index = 0
    st.session_state.exam_submitted = False
    st.session_state.exam_result = None


def finish_exam():
    if st.session_state.exam_submitted:
        return

    qs = st.session_state.exam_questions
    answers = st.session_state.exam_answers

    correct = 0
    wrong = 0
    unanswered = 0
    details = []
    section_stats = {}

    for i, q in enumerate(qs):
        selected = answers.get(str(i))
        right = q["correct"]

        if q["category"] not in section_stats:
            section_stats[q["category"]] = {
                "correct": 0,
                "wrong": 0,
                "unanswered": 0
            }

        if selected is None:
            status = "Unanswered"
            marks = 0
            unanswered += 1
            section_stats[q["category"]]["unanswered"] += 1

        elif selected == right:
            status = "Correct"
            marks = 4
            correct += 1
            section_stats[q["category"]]["correct"] += 1

        else:
            status = "Incorrect"
            marks = -1
            wrong += 1
            section_stats[q["category"]]["wrong"] += 1

        details.append({
            "question": q["question"],
            "category": q["category"],
            "your_answer": (
                q["options"][selected]
                if selected is not None else "Not Answered"
            ),
            "correct_answer": q["options"][right],
            "status": status,
            "marks": marks,
            "explanation": q["explanation"]
        })

    score = correct * 4 - wrong
    percentage = score / (len(qs) * 4) * 100 if qs else 0

    duration = int(time.time() - st.session_state.exam_start)

    result = {
        "username": st.session_state.username,
        "name": students[st.session_state.username]["name"],
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "score": score,
        "maximum": len(qs) * 4,
        "percentage": round(percentage, 2),
        "correct": correct,
        "wrong": wrong,
        "unanswered": unanswered,
        "duration_seconds": duration,
        "details": details,
        "section_stats": section_stats
    }

    results = load_json(RESULTS_FILE, [])
    results.append(result)
    save_json(RESULTS_FILE, results)

    st.session_state.exam_result = result
    st.session_state.exam_submitted = True
    st.session_state.exam_active = False


def start_exam():
    available = load_json(QUESTIONS_FILE, [])

    if len(available) < 60:
        st.error("Admin must add questions until there are at least 60.")
        return

    selected = random.sample(available, 60)

    st.session_state.exam_questions = selected
    st.session_state.exam_answers = {}
    st.session_state.exam_index = 0
    st.session_state.exam_start = time.time()
    st.session_state.exam_active = True
    st.session_state.exam_submitted = False
    st.session_state.exam_result = None


# =====================================================
# 10. HOME PAGE
# =====================================================

if page == "🏠 Home":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to PlacementPro 🚀</h1>
        <h3>Prepare Today. Get Placed Tomorrow.</h3>
        <p>Practise company-level placement examinations
        and improve your technical skills.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    for col, number, label in [
        (c1, "60", "Questions per Test"),
        (c2, "90", "Minutes"),
        (c3, "240", "Maximum Marks"),
        (c4, "4", "Test Sections")
    ]:
        with col:
            st.markdown(
                f'<div class="card"><h2>{number}</h2><b>{label}</b></div>',
                unsafe_allow_html=True
            )

    st.write("")

    st.subheader("📚 Examination Categories")

    categories = [
        ("📊", "Quantitative Aptitude", "Mathematical ability and calculations."),
        ("🧠", "Logical Reasoning", "Patterns, puzzles and analytical thinking."),
        ("📖", "Verbal Ability", "English grammar and vocabulary."),
        ("💻", "Technical Knowledge", "Python, Java, SQL, DBMS, OS and DSA.")
    ]

    cols = st.columns(4)

    for col, (icon, name, description) in zip(cols, categories):
        with col:
            st.markdown(
                f'<div class="card"><h2>{icon}</h2>'
                f'<b>{name}</b><p>{description}</p></div>',
                unsafe_allow_html=True
            )

    st.write("")
    st.subheader("⭐ Why Choose PlacementPro?")

    st.markdown("""
    - Real examination-style interface.
    - Advanced placement-level questions.
    - Timer and negative marking.
    - Performance reports and explanations.
    - Student leaderboard.
    - Personal examination history.
    """)

    if st.session_state.logged_in:
        st.success(
            f"Welcome back, {st.session_state.username}!"
        )
    else:
        st.info("Register or login from the navigation bar to begin.")


# =====================================================
# 11. STUDENT REGISTRATION
# =====================================================

elif page == "📝 Register":

    st.subheader("📝 Create Student Account")

    with st.form("register_form"):

        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        username = st.text_input("Choose Username")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button(
            "Create Account",
            type="primary",
            use_container_width=True
        )

        if submitted:

            reload_data()

            if not all([name, email, username, password, confirm]):
                st.error("Please fill in all fields.")

            elif "@" not in email:
                st.error("Enter a valid email address.")

            elif len(password) < 8:
                st.error("Password must contain at least 8 characters.")

            elif password != confirm:
                st.error("Passwords do not match.")

            elif username.lower() == ADMIN_USERNAME:
                st.error("This username is reserved.")

            elif username in students:
                st.error("Username already exists.")

            elif any(
                s["email"].lower() == email.lower()
                for s in students.values()
            ):
                st.error("Email already registered.")

            else:

                students[username] = {
                    "name": name,
                    "email": email,
                    "password": hash_password(password),
                    "role": "student",
                    "created": datetime.now().strftime("%d-%m-%Y")
                }

                save_json(STUDENTS_FILE, students)

                st.success("Registration successful! Please login.")


# =====================================================
# 12. STUDENT LOGIN
# =====================================================

elif page == "🔐 Student Login":

    st.subheader("🔐 Student Login")

    with st.form("student_login"):

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        login = st.form_submit_button(
            "Login",
            type="primary",
            use_container_width=True
        )

        if login:

            reload_data()

            if (
                username in students
                and verify_password(
                    password,
                    students[username]["password"]
                )
            ):

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = "student"

                st.success("Login successful!")
                st.rerun()

            else:
                st.error("Invalid username or password.")


# =====================================================
# 13. STUDENT DASHBOARD
# =====================================================

elif page == "👨‍🎓 Student Dashboard":

    if not require_student():
        st.warning("Please login as a student first.")

    else:

        reload_data()

        user = students[st.session_state.username]

        user_results = [
            r for r in results
            if r["username"] == st.session_state.username
        ]

        st.subheader("👨‍🎓 Student Dashboard")

        st.markdown(
            f"### Welcome, {user['name']} 👋"
        )

        a, b, c = st.columns(3)

        a.metric("Tests Completed", len(user_results))

        best = max(
            [r["score"] for r in user_results],
            default=0
        )

        b.metric("Best Score", f"{best}/240")

        average = (
            sum(r["percentage"] for r in user_results)
            / len(user_results)
            if user_results else 0
        )

        c.metric("Average Percentage", f"{average:.1f}%")

        st.divider()

        st.write("**Student Information**")
        st.write("Name:", user["name"])
        st.write("Email:", user["email"])
        st.write("Username:", st.session_state.username)
        st.write("Joined:", user["created"])


# =====================================================
# 14. TAKE TEST
# =====================================================

elif page == "📚 Take Test":

    if not require_student():

        st.warning("Please login as a student first.")

    else:

        if st.session_state.exam_active:

            st_autorefresh(
                interval=1000,
                key="placement_timer"
            )

            elapsed = time.time() - st.session_state.exam_start
            remaining = max(0, EXAM_DURATION - int(elapsed))

            if remaining <= 0:
                finish_exam()
                st.rerun()

            mins, secs = divmod(remaining, 60)

            qs = st.session_state.exam_questions
            idx = st.session_state.exam_index
            q = qs[idx]

            st.markdown("""
            <div class="hero">
                <h2>📝 Live Examination</h2>
                <p>Advanced Mock Placement Test</p>
            </div>
            """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)

            c1.metric("Time Remaining", f"{mins:02d}:{secs:02d}")
            c2.metric("Question", f"{idx+1}/60")
            c3.metric("Answered", len(st.session_state.exam_answers))

            st.progress((idx + 1) / 60)

            st.markdown(f"### {q['category']}")
            st.markdown(f"**Q{idx+1}. {q['question']}**")

            previous = st.session_state.exam_answers.get(str(idx))

            choices = ["-- Not Answered --"] + q["options"]

            selected = st.radio(
                "Choose your answer",
                choices,
                index=previous + 1 if previous is not None else 0,
                key=f"exam_radio_{idx}"
            )

            if selected == "-- Not Answered --":
                st.session_state.exam_answers.pop(str(idx), None)
            else:
                st.session_state.exam_answers[str(idx)] = q["options"].index(selected)

            st.divider()

            p, n, submit_col = st.columns(3)

            with p:
                if st.button("⬅ Previous", disabled=idx == 0):
                    st.session_state.exam_index -= 1
                    st.rerun()

            with n:
                if st.button("Next ➡", disabled=idx == 59):
                    st.session_state.exam_index += 1
                    st.rerun()

            with submit_col:
                if st.button("🏁 Submit Exam", type="primary"):
                    finish_exam()
                    st.rerun()

            st.divider()
            st.subheader("Question Navigator")

            nav_cols = st.columns(10)

            for i in range(60):

                with nav_cols[i % 10]:

                    if i == idx:
                        label = f"🔵 {i+1}"
                    elif str(i) in st.session_state.exam_answers:
                        label = f"🟢 {i+1}"
                    else:
                        label = f"⚪ {i+1}"

                    if st.button(label, key=f"exam_nav_{i}"):
                        st.session_state.exam_index = i
                        st.rerun()

        elif st.session_state.exam_submitted:

            st.success("Your examination has already been submitted.")

            if st.button("Start Another Test"):
                reset_exam()
                st.rerun()

        else:

            st.subheader("📚 Start Your Examination")

            st.info("""
            Examination rules:

            - 60 questions.
            - 90 minutes.
            - Correct answer: +4 marks.
            - Wrong answer: -1 mark.
            - Unanswered: 0 marks.
            - Total marks: 240.
            - Questions are randomly selected.
            """)

            if st.button(
                "🚀 Start Advanced Test",
                type="primary",
                use_container_width=True
            ):

                reload_data()
                start_exam()
                st.rerun()


# =====================================================
# 15. MY RESULTS
# =====================================================

elif page == "📊 My Results":

    if not require_student():

        st.warning("Please login first.")

    else:

        reload_data()

        my_results = [
            r for r in results
            if r["username"] == st.session_state.username
        ]

        st.subheader("📊 My Examination History")

        if not my_results:

            st.info("You have not attempted any examination yet.")

        else:

            df = pd.DataFrame([
                {
                    "Date": r["date"],
                    "Score": r["score"],
                    "Percentage": r["percentage"],
                    "Correct": r["correct"],
                    "Wrong": r["wrong"],
                    "Unanswered": r["unanswered"]
                }
                for r in my_results
            ])

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Performance Trend")

            st.line_chart(
                df.set_index("Date")["percentage"]
            )

            st.download_button(
                "Download My Results CSV",
                df.to_csv(index=False).encode("utf-8"),
                "my_placement_results.csv",
                "text/csv"
            )


# =====================================================
# 16. LEADERBOARD
# =====================================================

elif page == "🏆 Leaderboard":

    reload_data()

    st.subheader("🏆 Top Student Leaderboard")

    if not results:

        st.info("No examination results available yet.")

    else:

        best_results = {}

        for r in results:

            username = r["username"]

            if (
                username not in best_results
                or r["score"] > best_results[username]["score"]
            ):
                best_results[username] = r

        ranking = sorted(
            best_results.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        leaderboard = []

        for rank, r in enumerate(ranking[:10], start=1):

            leaderboard.append({
                "Rank": rank,
                "Student": r["name"],
                "Score": f"{r['score']}/{r['maximum']}",
                "Percentage": f"{r['percentage']}%",
                "Date": r["date"]
            })

        st.dataframe(
            pd.DataFrame(leaderboard),
            use_container_width=True,
            hide_index=True
        )

        st.caption("Ranking is based on each student's best score.")


# =====================================================
# 17. ADMIN LOGIN
# =====================================================

elif page == "🔑 Admin Login":

    st.subheader("🔑 Administrator Login")

    with st.form("admin_login"):

        username = st.text_input("Admin Username")
        password = st.text_input("Admin Password", type="password")

        login = st.form_submit_button(
            "Admin Login",
            type="primary",
            use_container_width=True
        )

        if login:

            if (
                username == ADMIN_USERNAME
                and hmac.compare_digest(password, ADMIN_PASSWORD)
            ):

                st.session_state.logged_in = True
                st.session_state.username = ADMIN_USERNAME
                st.session_state.role = "admin"

                st.success("Admin login successful.")
                st.rerun()

            else:
                st.error("Invalid admin credentials.")

    st.caption("Demo admin username: admin")
    st.caption("Demo admin password: Admin@12345")
    st.warning("Change the default password before deploying publicly.")


# =====================================================
# 18. ADMIN PANEL
# =====================================================

elif page == "⚙️ Admin Panel":

    if not require_admin():

        st.warning("Admin login required.")

    else:

        reload_data()

        st.markdown("""
        <div class="hero">
            <h2>⚙️ Admin Control Panel</h2>
            <p>Manage students, questions and examination records.</p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([
            "📊 Overview",
            "➕ Manage Questions",
            "👥 Students & Results"
        ])

        # ADMIN OVERVIEW

        with tab1:

            c1, c2, c3 = st.columns(3)

            c1.metric("Total Students", len(students))
            c2.metric("Total Questions", len(questions))
            c3.metric("Total Tests", len(results))

            if results:

                score_data = pd.DataFrame([
                    {
                        "Student": r["name"],
                        "Score": r["score"],
                        "Percentage": r["percentage"]
                    }
                    for r in results
                ])

                st.subheader("Recent Test Records")
                st.dataframe(
                    score_data.tail(10),
                    use_container_width=True,
                    hide_index=True
                )

        # QUESTION MANAGEMENT

        with tab2:

            st.subheader("➕ Add New Question")

            with st.form("add_question"):

                category = st.selectbox(
                    "Category",
                    [
                        "Quantitative Aptitude",
                        "Logical Reasoning",
                        "Verbal Ability",
                        "Technical Knowledge"
                    ]
                )

                question = st.text_area("Question")

                o1 = st.text_input("Option A")
                o2 = st.text_input("Option B")
                o3 = st.text_input("Option C")
                o4 = st.text_input("Option D")

                correct = st.selectbox(
                    "Correct Answer",
                    ["A", "B", "C", "D"]
                )

                explanation = st.text_area("Explanation")

                add = st.form_submit_button(
                    "Add Question",
                    type="primary"
                )

                if add:

                    if not all([question, o1, o2, o3, o4, explanation]):
                        st.error("Fill all question fields.")

                    else:

                        questions.append(
                            make_q(
                                category,
                                question,
                                [o1, o2, o3, o4],
                                ["A", "B", "C", "D"].index(correct),
                                explanation
                            )
                        )

                        save_json(QUESTIONS_FILE, questions)
                        st.success("Question added successfully.")
                        st.rerun()

            st.divider()

            st.subheader("Existing Questions")

            if questions:

                question_labels = {
                    q["id"]: f"{i+1}. {q['category']} - {q['question'][:65]}"
                    for i, q in enumerate(questions)
                }

                selected_id = st.selectbox(
                    "Select a question to delete",
                    list(question_labels.keys()),
                    format_func=lambda x: question_labels[x]
                )

                if st.button("🗑️ Delete Selected Question"):

                    questions = [
                        q for q in questions
                        if q["id"] != selected_id
                    ]

                    save_json(QUESTIONS_FILE, questions)
                    st.success("Question deleted.")
                    st.rerun()

                st.caption(f"Total available questions: {len(questions)}")

        # STUDENT MANAGEMENT

        with tab3:

            st.subheader("👥 Registered Students")

            if students:

                student_rows = []

                for username, user in students.items():

                    student_rows.append({
                        "Name": user["name"],
                        "Username": username,
                        "Email": user["email"],
                        "Joined": user["created"]
                    })

                st.dataframe(
                    pd.DataFrame(student_rows),
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.info("No students registered.")

            st.divider()

            st.subheader("📊 All Examination Results")

            if results:

                all_results = pd.DataFrame([
                    {
                        "Name": r["name"],
                        "Username": r["username"],
                        "Date": r["date"],
                        "Score": r["score"],
                        "Percentage": r["percentage"]
                    }
                    for r in results
                ])

                st.dataframe(
                    all_results,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "Download All Results",
                    all_results.to_csv(index=False).encode("utf-8"),
                    "all_student_results.csv",
                    "text/csv"
                )

            else:
                st.info("No results available.")


# =====================================================
# 19. FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:15px; color:#64748b;">
    <b>🎓 PlacementPro</b><br>
    Advanced Mock Placement Test Portal<br>
    Built with Python + Streamlit
    <br><br>
    © 2026 PlacementPro. All Rights Reserved.
</div>
""", unsafe_allow_html=True)
