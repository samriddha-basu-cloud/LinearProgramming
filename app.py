import streamlit as st
from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, lpSum, value, LpStatus
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# ---------- Page Configuration ---------- #
st.set_page_config(page_title="🧮 LP Solver 3D++", layout="wide")

# ---------- Enhanced Styling with Gradients ---------- #
# Replace the existing st.markdown CSS section with this professional glassmorphic design

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* CSS Variables for Theme Support */
        :root {
            --bg-primary: #f8fafc;
            --bg-secondary: #e2e8f0;
            --glass-bg: rgba(255, 255, 255, 0.4);
            --glass-border: rgba(255, 255, 255, 0.3);
            --glass-shadow: rgba(0, 0, 0, 0.05);
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --accent-primary: #3b82f6;
            --accent-secondary: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
            --error: #ef4444;
            --surface-hover: rgba(255, 255, 255, 0.6);
        }

        /* Dark theme variables */
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-primary: #0f172a;
                --bg-secondary: #1e293b;
                --glass-bg: rgba(15, 23, 42, 0.6);
                --glass-border: rgba(255, 255, 255, 0.1);
                --glass-shadow: rgba(0, 0, 0, 0.3);
                --text-primary: #f1f5f9;
                --text-secondary: #cbd5e1;
                --text-muted: #94a3b8;
                --accent-primary: #60a5fa;
                --accent-secondary: #a78bfa;
                --success: #34d399;
                --warning: #fbbf24;
                --error: #f87171;
                --surface-hover: rgba(15, 23, 42, 0.8);
            }
        }

        /* Force dark theme support for Streamlit */
        [data-theme="dark"] {
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --glass-bg: rgba(15, 23, 42, 0.6);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: rgba(0, 0, 0, 0.3);
            --text-primary: #f1f5f9;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --accent-primary: #60a5fa;
            --accent-secondary: #a78bfa;
            --success: #34d399;
            --warning: #fbbf24;
            --error: #f87171;
            --surface-hover: rgba(15, 23, 42, 0.8);
        }

        /* Global font and base styling */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
        }

        /* Main background with professional gradient */
        .main {
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            min-height: 100vh;
            position: relative;
        }

        /* Professional background pattern */
        .main::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 25% 25%, var(--accent-primary)08 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, var(--accent-secondary)08 0%, transparent 50%),
                linear-gradient(135deg, transparent 25%, var(--glass-shadow) 25%, var(--glass-shadow) 50%, transparent 50%);
            background-size: 100px 100px, 100px 100px, 40px 40px;
            opacity: 0.3;
            pointer-events: none;
            z-index: -1;
        }

        /* Professional sidebar design */
        .css-1d391kg {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            border-right: 1px solid var(--glass-border) !important;
            box-shadow: 
                4px 0 24px var(--glass-shadow),
                inset -1px 0 0 var(--glass-border) !important;
        }

        /* Main content container */
        .block-container {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(32px) saturate(180%) !important;
            border-radius: 16px !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: 
                0 24px 48px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            margin: 1rem !important;
            padding: 2rem !important;
        }

        /* Professional button styling */
        div.stButton > button:first-child {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            padding: 12px 24px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 4px 12px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            width: 100% !important;
            letter-spacing: 0.025em !important;
            text-transform: none !important;
            position: relative !important;
            overflow: hidden !important;
        }

        div.stButton > button:first-child::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
            transition: left 0.6s ease;
        }

        div.stButton > button:first-child:hover {
            transform: translateY(-1px) !important;
            background: var(--surface-hover) !important;
            border-color: var(--accent-primary)40 !important;
            box-shadow: 
                0 8px 24px var(--glass-shadow),
                0 0 0 1px var(--accent-primary)20,
                inset 0 1px 0 var(--glass-border) !important;
            color: var(--accent-primary) !important;
        }

        div.stButton > button:first-child:hover::before {
            left: 100%;
        }

        div.stButton > button:first-child:active {
            transform: translateY(0) scale(0.98) !important;
        }

        /* Professional download button */
        div.stDownloadButton > button {
            background: var(--accent-primary)15 !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid var(--accent-primary)30 !important;
            border-radius: 10px !important;
            color: var(--accent-primary) !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            transition: all 0.3s ease !important;
            box-shadow: 
                0 4px 12px var(--accent-primary)10,
                inset 0 1px 0 var(--accent-primary)20 !important;
        }

        div.stDownloadButton > button:hover {
            transform: translateY(-1px) !important;
            background: var(--accent-primary)25 !important;
            border-color: var(--accent-primary)50 !important;
            box-shadow: 
                0 8px 20px var(--accent-primary)20,
                inset 0 1px 0 var(--accent-primary)30 !important;
        }

        /* Professional input fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(16px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 8px !important;
            padding: 10px 12px !important;
            transition: all 0.3s ease !important;
            box-shadow: 
                0 2px 8px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            color: var(--text-primary) !important;
            font-size: 14px !important;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            background: var(--surface-hover) !important;
            border-color: var(--accent-primary)60 !important;
            box-shadow: 
                0 0 0 2px var(--accent-primary)20,
                0 4px 12px var(--accent-primary)15,
                inset 0 1px 0 var(--glass-border) !important;
            outline: none !important;
        }

        /* Professional select boxes */
        .stSelectbox > div > div > div {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(16px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 8px !important;
            box-shadow: 
                0 2px 8px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
        }

        /* Professional sliders */
        .stSlider > div > div > div > div {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(12px) !important;
            border-radius: 12px !important;
            border: 1px solid var(--glass-border) !important;
        }

        .stSlider > div > div > div > div > div[role="slider"] {
            background: var(--accent-primary) !important;
            border: 2px solid white !important;
            box-shadow: 0 2px 8px var(--accent-primary)40 !important;
        }

        /* Professional radio buttons */
        .stRadio > div {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(16px) saturate(180%) !important;
            border-radius: 12px !important;
            padding: 16px !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: 
                0 4px 12px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
        }

        /* Professional section cards */
        .section-card {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(32px) saturate(180%) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            margin: 20px 0 !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: 
                0 12px 32px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        .section-card:hover {
            transform: translateY(-2px) !important;
            box-shadow: 
                0 16px 40px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
        }

        /* Professional title styling */
        h1 {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            font-weight: 800 !important;
            text-align: center !important;
            font-size: 3rem !important;
            margin-bottom: 8px !important;
            letter-spacing: -0.025em !important;
            line-height: 1.1 !important;
        }

        /* Professional subheaders */
        .stApp h2, .stApp h3 {
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            margin-top: 24px !important;
            margin-bottom: 12px !important;
            position: relative !important;
            font-size: 1.5rem !important;
        }

        .stApp h2::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 32px;
            height: 2px;
            background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
            border-radius: 1px;
        }

        /* Professional alerts */
        .stAlert {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            box-shadow: 
                0 8px 24px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            color: var(--text-primary) !important;
        }

        .stSuccess {
            background: var(--success)10 !important;
            border-color: var(--success)30 !important;
            color: var(--success) !important;
        }

        .stInfo {
            background: var(--accent-primary)10 !important;
            border-color: var(--accent-primary)30 !important;
            color: var(--accent-primary) !important;
        }

        .stError {
            background: var(--error)10 !important;
            border-color: var(--error)30 !important;
            color: var(--error) !important;
        }

        .stWarning {
            background: var(--warning)10 !important;
            border-color: var(--warning)30 !important;
            color: var(--warning) !important;
        }

        /* Professional metrics */
        [data-testid="metric-container"] {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            padding: 16px !important;
            box-shadow: 
                0 8px 20px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        [data-testid="metric-container"]:hover {
            transform: translateY(-2px) scale(1.01) !important;
            box-shadow: 
                0 12px 28px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
        }

        [data-testid="metric-container"] > div:first-child {
            color: var(--text-secondary) !important;
            font-size: 0.875rem !important;
            font-weight: 500 !important;
        }

        [data-testid="metric-container"] > div:last-child {
            color: var(--text-primary) !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }

        /* Professional tables */
        .stDataFrame {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            box-shadow: 
                0 8px 24px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            border: 1px solid var(--glass-border) !important;
        }

        /* Professional sidebar labels */
        .css-1d391kg .stTextInput label,
        .css-1d391kg .stSlider label,
        .css-1d391kg .stRadio label,
        .css-1d391kg .stSelectbox label,
        .css-1d391kg .stNumberInput label {
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 0.875rem !important;
            margin-bottom: 4px !important;
        }

        /* Professional sidebar header */
        .css-1d391kg h2 {
            color: var(--text-primary) !important;
            text-align: center !important;
            font-weight: 700 !important;
            margin-bottom: 20px !important;
            font-size: 1.25rem !important;
        }

        /* Professional code blocks */
        .stCode {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(16px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 8px !important;
            box-shadow: 
                0 4px 12px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            color: var(--text-primary) !important;
            font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace !important;
        }

        /* Professional spinner */
        .stSpinner > div {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border-radius: 12px !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: 
                0 8px 24px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
        }

        /* Professional plotly charts */
        .js-plotly-plot {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            border-radius: 16px !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: 
                0 12px 32px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            padding: 12px !important;
        }

        /* Professional dividers */
        hr {
            border: none !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--glass-border), transparent) !important;
            margin: 20px 0 !important;
        }

        /* Professional scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: var(--glass-bg);
            border-radius: 3px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--glass-border);
            border-radius: 3px;
            backdrop-filter: blur(8px);
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-primary)40;
        }

        /* Professional focus states */
        *:focus-visible {
            outline: 2px solid var(--accent-primary)60 !important;
            outline-offset: 2px !important;
            border-radius: 4px !important;
        }

        /* Professional loading animation */
        @keyframes professional-pulse {
            0%, 100% { 
                opacity: 0.8;
                transform: scale(1);
            }
            50% { 
                opacity: 1;
                transform: scale(1.01);
            }
        }

        .loading {
            animation: professional-pulse 2s ease-in-out infinite;
        }

        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .block-container {
                margin: 0.5rem !important;
                padding: 1.5rem 1rem !important;
                border-radius: 12px !important;
            }

            h1 {
                font-size: 2rem !important;
            }

            .section-card {
                padding: 16px !important;
                margin: 12px 0 !important;
                border-radius: 12px !important;
            }

            [data-testid="metric-container"] {
                padding: 12px !important;
                border-radius: 10px !important;
            }
        }

        /* Professional typography hierarchy */
        .stMarkdown p {
            color: var(--text-secondary);
            line-height: 1.6;
            font-size: 0.9rem;
        }

        .stMarkdown strong {
            color: var(--text-primary);
            font-weight: 600;
        }

        /* Professional status indicators */
        .status-optimal {
            color: var(--success) !important;
            font-weight: 600 !important;
        }

        .status-infeasible {
            color: var(--error) !important;
            font-weight: 600 !important;
        }

        .status-unbounded {
            color: var(--warning) !important;
            font-weight: 600 !important;
        }

        /* Enhanced interaction feedback */
        button:active,
        input:active,
        select:active {
            transform: scale(0.98) !important;
        }

        /* Professional tooltip styling */
        [data-baseweb="tooltip"] {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 8px !important;
            box-shadow: 
                0 8px 24px var(--glass-shadow),
                inset 0 1px 0 var(--glass-border) !important;
            color: var(--text-primary) !important;
            font-size: 0.85rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Functions ---------- #
def get_user_input():
    with st.sidebar:
        st.markdown('<h2>⚙️ Configure Problem</h2>', unsafe_allow_html=True)

        # Add some spacing and visual separators
        st.markdown("---")

        problem_heading = st.text_input("🎯 Problem Heading", value="Linear Programming Problem")

        st.markdown("---")
        st.markdown("**📝 Variable Names**")
        variable_names = []
        for i in range(3):
            var_name = st.text_input(f"Variable x{i + 1}", value=f"x{i + 1}", key=f"varname_{i}")
            variable_names.append(var_name)

        st.markdown("---")
        st.markdown("**🔧 Problem Configuration**")
        num_vars = st.slider("🔢 Number of Decision Variables", 2, 3, 2, help="Choose between 2D or 3D optimization")
        num_constraints = st.slider("📊 Number of Constraints", 1, 5, 2,
                                    help="More constraints = more realistic problems")
        problem_type = st.radio("🎯 Optimization Type", ("Maximize", "Minimize"), help="Choose your objective")

        st.markdown("---")
        solve = st.button("🚀 SOLVE PROBLEM")

    return problem_heading, variable_names[:num_vars], num_vars, num_constraints, problem_type, solve


def get_objective_function(num_vars, variable_names):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🎯 Objective Function")
    st.markdown("*Define what you want to optimize (maximize profit, minimize cost, etc.)*")

    obj_coeffs = []
    cols = st.columns(num_vars)

    for i in range(num_vars):
        with cols[i]:
            coeff = st.number_input(
                f"Coefficient of {variable_names[i]}",
                value=1.0,
                key=f"obj_{i}",
                help=f"How much {variable_names[i]} contributes to your objective"
            )
            obj_coeffs.append(coeff)

    # Display the objective function formula
    formula = " + ".join([f"{coeff}×{var}" for coeff, var in zip(obj_coeffs, variable_names)])
    st.info(f"📐 **Current Objective Function:** {formula}")

    st.markdown('</div>', unsafe_allow_html=True)
    return obj_coeffs


def get_constraints(num_constraints, num_vars, variable_names):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📉 Constraints")
    st.markdown("*Set the limitations and boundaries for your optimization problem*")

    constraints = []

    for j in range(num_constraints):
        st.markdown(f"### 🔒 Constraint {j + 1}")

        col1, col2 = st.columns([1, 3])
        with col1:
            name = st.text_input(f"Name", key=f"name_{j}", value=f"Constraint_{j + 1}")

        # Constraint equation inputs
        row = st.columns(num_vars + 2)
        coeffs = []

        for i in range(num_vars):
            with row[i]:
                coeff = st.number_input(
                    f"{variable_names[i]}",
                    key=f"c{j}_{i}",
                    value=1.0,
                    help=f"Coefficient for {variable_names[i]}"
                )
                coeffs.append(coeff)

        with row[-2]:
            ineq = st.selectbox("Operator", ["≤", "=", "≥"], key=f"ineq_{j}")

        with row[-1]:
            rhs = st.number_input("Value", key=f"rhs_{j}", value=10.0)

        # Convert symbols back to PuLP format
        ineq_map = {"≤": "<=", "=": "=", "≥": ">="}
        ineq_pulp = ineq_map[ineq]

        # Display the constraint formula
        constraint_formula = " + ".join([f"{coeff}×{var}" for coeff, var in zip(coeffs, variable_names)])
        st.success(f"📋 **{name}:** {constraint_formula} {ineq} {rhs}")

        constraints.append((name, coeffs, ineq_pulp, rhs))

        if j < num_constraints - 1:
            st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)
    return constraints


def solve_lp(num_vars, obj_coeffs, constraints, problem_type):
    prob = LpProblem("LP", LpMaximize if problem_type == "Maximize" else LpMinimize)
    vars_lp = [LpVariable(f"x{i + 1}", lowBound=0) for i in range(num_vars)]
    prob += lpSum([obj_coeffs[i] * vars_lp[i] for i in range(num_vars)])

    for name, coeffs, ineq, rhs in constraints:
        expr = lpSum([coeffs[i] * vars_lp[i] for i in range(num_vars)])
        if ineq == "<=":
            prob += expr <= rhs, name
        elif ineq == "=":
            prob += expr == rhs, name
        else:
            prob += expr >= rhs, name

    prob.solve()
    return prob, vars_lp


def show_solution(prob, vars_lp, variable_names):
    # Status with color coding
    status = LpStatus[prob.status]
    if status == "Optimal":
        st.success(f"✅ Problem Solved Successfully: {status}")
    else:
        st.error(f"❌ Solution Status: {status}")

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🎉 Optimization Results")

    # Create metrics for each variable
    cols = st.columns(len(vars_lp) + 1)
    solution_data = {}

    for i, var in enumerate(vars_lp):
        with cols[i]:
            value_rounded = round(var.varValue, 3)
            st.metric(
                label=f"🎯 {variable_names[i]}",
                value=f"{value_rounded}",
                help=f"Optimal value for {variable_names[i]}"
            )
            solution_data[variable_names[i]] = var.varValue

    # Objective value
    with cols[-1]:
        obj_value = round(value(prob.objective), 3)
        st.metric(
            label="🏆 Objective Value",
            value=f"{obj_value}",
            help="The optimized result of your objective function"
        )
        solution_data['Objective Value'] = value(prob.objective)

    # Detailed table
    st.markdown("### 📊 Detailed Results")
    results_df = pd.DataFrame([solution_data])
    st.dataframe(results_df, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)
    return solution_data


def show_constraints(prob):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📜 Problem Formulation")
    st.markdown("*Here's how your problem was interpreted:*")

    for name, c in prob.constraints.items():
        st.code(f"{name}: {c}", language="text")

    st.markdown('</div>', unsafe_allow_html=True)


def plot_2d(constraints, vars_lp):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📊 2D Feasible Region Visualization")
    st.markdown("*Visual representation of constraints and optimal solution*")

    x_vals = np.linspace(0, 20, 400)
    fig = go.Figure()

    # Color palette for constraints
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

    for i, (name, (coeffs, ineq, rhs)) in enumerate([(n, (c, i, r)) for n, c, i, r in constraints]):
        if coeffs[1] != 0:
            y_vals = (rhs - coeffs[0] * x_vals) / coeffs[1]
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                name=name,
                line=dict(color=colors[i % len(colors)], width=3)
            ))

    # Optimal point
    x_opt, y_opt = vars_lp[0].varValue, vars_lp[1].varValue
    fig.add_trace(go.Scatter(
        x=[x_opt],
        y=[y_opt],
        mode='markers+text',
        marker=dict(color='red', size=15, symbol='star'),
        text=[f"Optimal Point<br>({x_opt:.2f}, {y_opt:.2f})"],
        name="Optimal Solution",
        textposition="top center"
    ))

    fig.update_layout(
        xaxis_title="x₁",
        yaxis_title="x₂",
        template="plotly_white",
        title="Feasible Region and Optimal Solution",
        showlegend=True,
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def plot_3d(vars_lp):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📈 3D Solution Visualization")
    st.markdown("*Three-dimensional representation of your optimal solution*")

    x, y, z = vars_lp[0].varValue, vars_lp[1].varValue, vars_lp[2].varValue
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=[x],
        y=[y],
        z=[z],
        mode='markers+text',
        marker=dict(size=12, color='red', symbol='diamond'),
        text=[f"Optimal Solution<br>({x:.2f}, {y:.2f}, {z:.2f})"],
        name="Optimal Point"
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='x₁',
            yaxis_title='x₂',
            zaxis_title='x₃',
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        template="plotly_white",
        title="3D Optimal Solution",
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def show_breakeven_and_eos(obj_coeffs, vars_lp):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📘 Economic Analysis")
    st.markdown("*Break-even analysis and economies of scale insights*")

    total_cost = sum([obj_coeffs[i] * vars_lp[i].varValue for i in range(len(obj_coeffs))])
    total_units = sum([vars_lp[i].varValue for i in range(len(vars_lp))])
    avg_cost = total_cost / total_units if total_units else 0

    # Create metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💰 Total Cost", f"{total_cost:.2f}")

    with col2:
        st.metric("📦 Total Units", f"{total_units:.2f}")

    with col3:
        st.metric("📊 Average Cost/Unit", f"{avg_cost:.2f}")

    st.info(
        "💡 **Insight:** Economies of Scale occur when average cost decreases as output increases. Monitor this ratio as you scale your operations.")

    st.markdown('</div>', unsafe_allow_html=True)


def export_solution_to_csv(solution_data):
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("💾 Export Results")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("**Download your optimization results for further analysis or reporting.**")

    with col2:
        st.download_button(
            label="📥 Download CSV",
            data=pd.DataFrame([solution_data]).to_csv(index=False),
            file_name=f"lp_solution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- Main Application ---------- #
def main():
    # Header with enhanced styling
    st.markdown("""
        <div style='text-align: center; padding: 20px; margin-bottom: 30px;'>
            <h1>🧮 LP Solver 3D++</h1>
            <p style='font-size: 1.2em; color: #666; font-weight: 300;'>
                Advanced Linear Programming Solver with Interactive Visualization
            </p>
            <p style='font-size: 1em; color: #888;'>
                Solve <strong>Maximization/Minimization</strong> problems • 2D/3D visualization • Break-even analysis • Downloadable solutions
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Get user inputs
    problem_heading, variable_names, num_vars, num_constraints, problem_type, solve = get_user_input()

    # Main content
    st.title(f"🎯 {problem_heading}")

    # Get problem definition
    obj_coeffs = get_objective_function(num_vars, variable_names)
    constraints = get_constraints(num_constraints, num_vars, variable_names)

    # Solve and display results
    if solve:
        with st.spinner('🔄 Optimizing your problem...'):
            prob, vars_lp = solve_lp(num_vars, obj_coeffs, constraints, problem_type)

        solution_data = show_solution(prob, vars_lp, variable_names)
        show_constraints(prob)
        show_breakeven_and_eos(obj_coeffs, vars_lp)
        export_solution_to_csv(solution_data)

        # Visualizations
        if num_vars == 2:
            plot_2d(constraints, vars_lp)
        elif num_vars == 3:
            plot_3d(vars_lp)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
            <p>Built with ❤️ using Streamlit & PuLP | Enhanced UI with Modern Design</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()