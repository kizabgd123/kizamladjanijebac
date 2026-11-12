---
trigger: glob
globs:
  - "**/*.py"
---

# Python Code Quality & Type Safety Rule

1. **Type Annotations:** All functions, methods, and classes must include explicit type hints.
2. **Data Validation:** Use Pydantic `BaseModel` for configuration schemas, query payloads, and structured responses.
3. **Error Handling:** Avoid bare `except:`. Catch explicit exceptions and wrap with descriptive context.
4. **Clean Code:** Adhere to PEP 8 style conventions, modular design, and clear function responsibilities.
