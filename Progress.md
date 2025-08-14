# GUI Implementation Plan

This plan outlines the steps to create a new desktop GUI for the application using PySide6, as specified in the project guidelines.

## Phase 1: Setup and Basic Structure

- [ ] **1.1: Install Dependencies:** Add `PySide6==6.9.1` to `requirements.txt` and install it. (Note: using 6.7.0 as it's a recent stable version, will upgrade to >=6.9.1 if specific features are needed as per docs).
- [ ] **1.2: Create `gui` directory:** Create a new directory named `gui` to house the new GUI code.
- [ ] **1.3: Create `gui/model.py`:** Create the `model.py` file. This will contain the application's business logic, state management, and interaction with the existing `app/api` and `app/storage` modules.
- [ ] **1.4: Create `gui/main.py`:** Create the `main.py` file. This will contain the PySide6 application setup, main window, UI components, and event handling.
- [ ] **1.5: Basic Window:** Implement a basic, empty main window in `gui/main.py` that uses the 'Fusion' style and 'Auto' color scheme.

## Phase 2: Character and Model Selection

- [ ] **2.1: Character List View:** In `gui/main.py`, implement a UI component (e.g., a `QListWidget` or `QTableView`) to display the list of available characters.
- [ ] **2.2: Model Logic for Characters:** In `gui/model.py`, add a function to fetch the list of characters by calling `app.api.bs.get_characters()`.
- [ ] **2.3: Connect Character UI to Logic:** In `gui/main.py`, call the model's function to populate the character list view.
- [ ] **2.4: Model Selection UI:** In `gui/main.py`, add a `QComboBox` to display the available AI models.
- [ ] **2.5: Model Logic for AI Models:** In `gui/model.py`, add a function to fetch the AI models using `app.api.bs.get_models()`.
- [ ] **2.6: Connect Model UI to Logic:** In `gui/main.py`, populate the model selection `QComboBox`.

## Phase 3: Chat Interface

- [ ] **3.1: Chat History View:** In `gui/main.py`, add a `QTextEdit` or a similar widget to display the chat history. It should be read-only.
- [ ] **3.2: Message Input:** In `gui/main.py`, add a `QLineEdit` or `QTextEdit` for the user to type their messages, and a "Send" button.
- [ ] **3.3: Layout:** Arrange the character list, model selection, chat history, and message input into a user-friendly layout (e.g., using `QHBoxLayout` and `QVBoxLayout`).
- [ ] **3.4: Model Logic for Chat:** In `gui/model.py`, create a class to manage the chat state. This class will:
    - Hold the current character, model, and room ID.
    - Have a method to send a message and receive a response. This will involve adapting the WebSocket logic from `app/api/chat.py` to work with the GUI. This might require creating a separate thread (`QThread`) for the WebSocket communication to avoid blocking the GUI.
- [ ] **3.5: Connect Chat UI to Logic:**
    - When the "Send" button is clicked in `gui/main.py`, it should call the chat method in `gui/model.py`.
    - The model should emit signals (`pyqtSignal`) to update the chat history view in the main window as new messages (user's and AI's) are processed.

## Phase 4: Integration and Refinement

- [ ] **4.1: Session Management:** Integrate session handling. The GUI will need to get or create a user session. This may involve reusing or adapting logic from `app.api.session.py`.
- [ ] **4.2: Error Handling:** Implement dialog boxes or status bar messages in `gui/main.py` to display errors that might occur (e.g., network issues, API errors), based on signals from `gui/model.py`.
- [ ] **4.3: Clear History:** Add a "Clear History" button to the UI and connect it to the `clear_room_history` function in `app.api.bs`.
- [ ] **4.4: Final Polish:** Review the UI for usability, fix any layout issues, and ensure the 'Fusion' style is applied correctly.
- [ ] **4.5: Create Launcher:** Create a new script, e.g., `run_gui.py`, at the root level to launch the new PySide6 application.
