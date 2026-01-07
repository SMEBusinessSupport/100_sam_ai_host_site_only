# AI Assistant Teaching Prompts

**Generated:** 2025-10-08 19:46:51

---

## Lesson 1: Code Quality Issues Detected [MEDIUM]

**Detected Instances:** 69


**LESSON: Code Quality Best Practices**

Senior developer review found 69 code quality issues in your recent code.

**Common issues found:**
- Long functions (>100 lines) - hard to maintain and test
- Missing type hints - reduces code clarity
- Duplicate code patterns - should be extracted to functions
- Missing docstrings - reduces code understandability

**Best Practices:**
1. Keep functions under 50 lines when possible
2. Add type hints: `def func(param: str) -> int:`
3. Extract repeated code into helper functions
4. Document all public functions with docstrings

**AI SAM Environment Standards:**
- ALL public functions MUST have docstrings
- Use Python 3.10+ type hints
- Follow PEP 8 style guide
- Extract duplicated code (DRY principle)


---

