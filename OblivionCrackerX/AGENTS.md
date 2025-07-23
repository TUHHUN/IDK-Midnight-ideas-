## OblivionCrackerX Agent Instructions

This file provides instructions for AI agents contributing to the OblivionCrackerX project.

### Project Structure

- `oblivion.py`: The main entry point for the application.
- `modules/`: Contains decryption modules for different file types.
- `attacks/`: Contains different attack strategies (e.g., brute-force, dictionary).
- `utils/`: Contains utility functions used across the project.
- `wordlists/`: Contains wordlists for dictionary attacks.

### Development Guidelines

1.  **Modularity:** Keep modules self-contained and focused on a single file type or attack method.
2.  **Cross-Platform Compatibility:** Ensure that all code is compatible with Windows, macOS, and Linux. Avoid platform-specific libraries where possible.
3.  **Extensibility:** Design modules and a core framework that are easy to extend with new file formats and attack methods.
4.  **Performance:** For performance-critical code, consider implementing it in Rust or C++ and calling it from Python.
5.  **Testing:** Add unit tests for all new functionality.

### Running Tests

Before submitting any changes, please run the test suite to ensure that everything is working correctly.

```bash
python -m unittest discover
```
