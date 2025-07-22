import streamlit as st
from pulp import LpProblem, LpVariable, LpMaximize, LpMinimize, lpSum, value, LpStatus
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime

# ---------- Page Configuration ---------- #
st.set_page_config(page_title="🧮 LP Solver 3D++", layout="wide")

# ---------- Enhanced Styling with Gradients ---------- #
st.markdown("""
    <style>
        /* Main background with gradient */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }

        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #2D1B69 0%, #11998e 100%);
        }

        /* Main content area */
        .block-container {
            padding-top: 2rem;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            margin: 1rem;
            backdrop-filter: blur(10px);
        }

        /* Enhanced button styling */
        div.stButton > button:first-child {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            border: none;
            border-radius: 25px;
            font-weight: bold;
            font-size: 16px;
            padding: 15px 30px;
            transition: all 0.3s ease;
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
            width: 100%;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        div.stButton > button:first-child:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 25px rgba(0, 0, 0, 0.2);
            background: linear-gradient(45deg, #4ECDC4, #FF6B6B);
        }

        /* Download button styling */
        div.stDownloadButton > button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 20px;
            font-weight: bold;
            padding: 12px 25px;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        div.stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.6);
        }

        /* Input field styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 12px 16px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            background: white;
        }

        /* Number input styling */
        .stNumberInput > div > div > input {
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 10px 14px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .stNumberInput > div > div > input:focus {
            border-color: #4ECDC4;
            box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1);
        }

        /* Select box styling */
        .stSelectbox > div > div > select {
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 10px 14px;
            transition: all 0.3s ease;
        }

        /* Card-like sections */
        .section-card {
            background: linear-gradient(145deg, #ffffff, #f0f0f0);
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 
                20px 20px 60px #d9d9d9,
                -20px -20px 60px #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Title styling */
        h1 {
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            text-align: center;
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        /* Subheader styling */
        .stApp h2, .stApp h3 {
            background: linear-gradient(45deg, #11998e, #38ef7d);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
            margin-top: 30px;
        }

        /* Success message styling */
        .stSuccess {
            background: linear-gradient(90deg, #56ab2f, #a8edea);
            border-radius: 15px;
            padding: 15px;
            border: none;
        }

        /* Metric styling */
        [data-testid="metric-container"] {
            background: linear-gradient(145deg, #ffffff, #f8f9fa);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }

        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }

        /* Table styling */
        table {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        /* Sidebar header styling */
        .css-1d391kg h2 {
            color: white;
            text-align: center;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        /* Sidebar text styling */
        .css-1d391kg .stTextInput label,
        .css-1d391kg .stSlider label,
        .css-1d391kg .stRadio label {
            color: white !important;
            font-weight: 500;
        }

        /* Code block styling */
        .stCode {
            border-radius: 15px;
            border: 2px solid #e0e0e0;
            background: linear-gradient(145deg, #f8f9fa, #ffffff);
        }

        /* Animation for loading */
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        .loading {
            animation: pulse 2s ease-in-out infinite;
        }

        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .block-container {
                margin: 0.5rem;
                border-radius: 15px;
            }

            h1 {
                font-size: 2rem;
            }
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