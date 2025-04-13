from langchain_core.tools import tool
import scipy
import numpy as np
import sympy as sp


@tool
def scipy_general_solver(query: str) -> str:
    """
    This tool allows the agent to use any SciPy function (optimize, integrate, stats, etc.)
    Example prompts:
    - "Integrate sin(x) from 0 to pi"
    - "Minimize x**2 + 3*x + 2"
    - "Find the cumulative probability for normal distribution with mean=0, std=1 at x=1.96"
    """
    try:
        # Step 1: Convert expression to Python-executable code
        # Replace common math names with numpy
        replacements = {
            "sin": "np.sin", "cos": "np.cos", "tan": "np.tan",
            "log": "np.log", "exp": "np.exp", "sqrt": "np.sqrt",
            "pi": "np.pi", "^": "**"
        }
        for k, v in replacements.items():
            query = query.replace(k, v)

        # Step 2: Handle known cases
        if "integrate" in query:
            # Example: "Integrate np.sin(x) from 0 to np.pi"
            match = re.search(r"integrate (.*?) from (.*?) to (.*)", query, re.IGNORECASE)
            if match:
                expr = match.group(1).strip()
                a = eval(match.group(2).strip())
                b = eval(match.group(3).strip())
                f = eval(f"lambda x: {expr}")
                from scipy.integrate import quad
                val, err = quad(f, a, b)
                return f"✅ Integral result: {val:.6f} with error {err:.2e}"

        if "minimize" in query:
            # Example: "Minimize x**2 + 3*x + 2"
            expr = re.search(r"minimize (.*)", query, re.IGNORECASE).group(1)
            f = eval(f"lambda x: {expr}")
            from scipy.optimize import minimize
            res = minimize(f, x0=[0])
            return f"✅ Minimum value: {res.fun:.4f} at x = {res.x[0]:.4f}"

        if "normal" in query and ("pdf" in query or "cdf" in query):
            from scipy.stats import norm
            match = re.search(r"mean\s*=\s*([-+]?[0-9.]+).*?std\s*=\s*([-+]?[0-9.]+).*?x\s*=\s*([-+]?[0-9.]+)", query)
            if match:
                mu, sigma, x = map(float, match.groups())
                if "pdf" in query:
                    val = norm.pdf(x, loc=mu, scale=sigma)
                    return f"📈 PDF at x={x}: {val:.5f}"
                elif "cdf" in query:
                    val = norm.cdf(x, loc=mu, scale=sigma)
                    return f"📊 CDF at x={x}: {val:.5f}"

        return "❌ Query not recognized. Try phrasing like: 'integrate x**2 from 0 to 1'"
    except Exception as e:
        return f"❌ Error while solving: {str(e)}"
