# SpicyChat Desktop GUI - Design Document

## Overview

The SpicyChat Desktop GUI is a PySide6-based desktop application that provides the same functionality as the existing web interface. It allows users to chat with AI characters through a native desktop interface while connecting to the same backend database and AI services. The application follows a model-view-controller architecture with clear separation between business logic (`gui/model.py`) and user interface (`gui/main.py`).

## Architecture

### High-Level Architecture

```mermaid
graph TD
    A[gui/main.py - PySide6 GUI] --> B[gui/model.py - Business Logic]
    B --> C[app/api/bs.py - Database Layer]
    B --> D[app/api/ai.py - AI Communication]
    B --> E[Session Management]
    C --> F[PostgreSQL Database]
    C --> G[Redis Session Store]
    D --> H[Ollama AI Models]
    E --> I[User Sessions & Chat Rooms]
```

### Component Separation

**gui/main.py (GUI/Controller):**
- PySide6 main window and UI components
- Character list display and selection
- AI model selection dropdown
- Chat history display (QTextEdit)
- Message input and send functionality
- Event handling for user interactions
- Threading for AI communication

**gui/model.py (Business Logic):**
- Chat session management
- Integration with existing app.api.bs functions
- AI communication using app.api.ai.AI class
- User session handling
- Database operations coordination
- Error handling and recovery

## Components and Interfaces

### Core Classes

#### SpicyChatModel
```python
class SpicyChatModel(QObject):
    # Signals for UI updates
    characters_loaded = pyqtSignal(list)
    models_loaded = pyqtSignal(list)
    message_received = pyqtSignal(str, str, str)  # sender, content, timestamp
    message_stream = pyqtSignal(str)  # streaming content
    error_occurred = pyqtSignal(str)  # error message
    
    def __init__(self):
        super().__init__()
        self.user_id: str = ""
        self.current_character_id: str = ""
        self.current_model: str = ""
        self.current_room_id: str = ""
        self.ai_instance: Optional[AI] = None
        self.chat_thread: Optional[QThread] = None
    
    def load_characters(self) -> None
    def load_models(self) -> None
    def select_character(self, character_id: str) -> None
    def select_model(self, model_name: str) -> None
    def send_message(self, message: str) -> None
    def load_chat_history(self) -> List[Dict]
    def clear_chat_history(self) -> None
    def create_or_get_user_session(self) -> str
```

#### ChatWorker (QThread)
```python
class ChatWorker(QThread):
    message_chunk = pyqtSignal(str)
    message_complete = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, ai_instance: AI, message: str, history: List[Dict]):
        super().__init__()
        self.ai_instance = ai_instance
        self.message = message
        self.history = history
    
    def run(self) -> None:
        # Async AI communication in separate thread
        # Emit signals for UI updates
```

#### DatabaseManager
```python
class DatabaseManager:
    def __init__(self):
        # Reuse existing database connection from app.storage.db
        pass
    
    def get_characters(self) -> List[Dict]:
        # Wrapper around app.api.bs.get_characters()
    
    def get_models(self) -> List[Dict]:
        # Wrapper around app.api.bs.get_models()
    
    def get_or_create_room(self, user_id: str, character_id: str) -> Dict:
        # Wrapper around app.api.bs.get_or_create_room()
    
    def save_message(self, room_id: str, from_id: str, from_bot: bool, 
                    content: str, content_type: str, timestamp: datetime) -> None:
        # Wrapper around app.api.bs.save_message()
```

### UI Components

#### MainWindow
```python
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = SpicyChatModel()
        self.setup_ui()
        self.connect_signals()
        
        # UI Components
        self.character_list: QListWidget
        self.model_combo: QComboBox
        self.chat_display: QTextEdit
        self.message_input: QLineEdit
        self.send_button: QPushButton
        self.clear_button: QPushButton
    
    def setup_ui(self) -> None
    def connect_signals(self) -> None
    def on_character_selected(self, character_id: str) -> None
    def on_model_selected(self, model_name: str) -> None
    def on_send_message(self) -> None
    def on_message_received(self, sender: str, content: str, timestamp: str) -> None
    def on_clear_history(self) -> None
```

#### CharacterListWidget
```python
class CharacterListWidget(QListWidget):
    character_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def populate_characters(self, characters: List[Dict]) -> None
    def on_item_clicked(self, item: QListWidgetItem) -> None
```

#### ChatDisplayWidget
```python
class ChatDisplayWidget(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setup_formatting()
    
    def add_user_message(self, message: str, timestamp: str) -> None
    def add_ai_message(self, message: str, timestamp: str, character_name: str) -> None
    def add_streaming_text(self, text: str) -> None
    def clear_history(self) -> None
    def setup_formatting(self) -> None
```

## Data Models

### Database Schema Integration
The desktop application integrates with the existing database schema:

```sql
-- Characters table
CREATE TABLE character (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    settings TEXT,  -- JSON containing character personality/instructions
    created_at TIMESTAMP DEFAULT NOW()
);

-- AI Models table  
CREATE TABLE ai_model (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    model VARCHAR NOT NULL,  -- Model identifier for API
    api VARCHAR NOT NULL,    -- API endpoint URL
    api_key VARCHAR,         -- Optional API key
    extra_args JSONB,        -- Additional model parameters
    ordinal INTEGER DEFAULT 0
);

-- Users table
CREATE TABLE "user" (
    id VARCHAR PRIMARY KEY,
    nickname VARCHAR NOT NULL,
    avatar VARCHAR,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Chat rooms table
CREATE TABLE room (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES "user"(id),
    character_id VARCHAR REFERENCES character(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Messages table
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES room(id),
    from_id VARCHAR NOT NULL,
    from_bot BOOLEAN NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR DEFAULT 'text',
    created_at TIMESTAMP NOT NULL,
    send_to VARCHAR NOT NULL
);
```

### Application State Structure
```python
# Application configuration
app_config = {
    "database_url": "postgres://nsfw:nsfw@localhost:5433/nsfw",
    "redis_host": "localhost",
    "redis_port": 6379,
    "default_model": "QWen 2.5 1m 14b",
    "window_geometry": {
        "width": 1200,
        "height": 800,
        "x": 100,
        "y": 100
    },
    "ui_settings": {
        "style": "Fusion",
        "color_scheme": "Auto"
    }
}

# Chat session state
chat_session = {
    "user_id": "uuid-string",
    "current_character": {
        "id": "character_id",
        "name": "Character Name",
        "settings": "Character personality instructions..."
    },
    "current_model": "QWen 2.5 1m 14b",
    "room_id": 123,
    "message_history": [
        {
            "id": 1,
            "from_id": "user_id",
            "from_bot": False,
            "content": "Hello!",
            "timestamp": "2025-01-14T10:30:00Z"
        }
    ]
}
```

### Message Flow Architecture
```mermaid
sequenceDiagram
    participant UI as MainWindow
    participant Model as SpicyChatModel
    participant Worker as ChatWorker
    participant AI as AI Instance
    participant DB as Database
    
    UI->>Model: send_message("Hello")
    Model->>DB: save_message(user_message)
    Model->>Worker: start_chat_thread(message, history)
    Worker->>AI: chat(message, history)
    
    loop Streaming Response
        AI-->>Worker: stream_chunk
        Worker-->>Model: message_chunk signal
        Model-->>UI: message_stream signal
        UI->>UI: update_chat_display
    end
    
    AI-->>Worker: complete_response
    Worker-->>Model: message_complete signal
    Model->>DB: save_message(ai_response)
    Model-->>UI: message_received signal
    UI->>UI: finalize_message_display
```

## Error Handling

### Validation System
- Real-time input validation using configurable rules
- User-friendly error messages with suggestions
- Visual indicators for validation status
- Prevention of navigation with incomplete required fields

### File Operations
- Graceful handling of file I/O errors
- Automatic backup creation before save operations
- Recovery mechanisms for corrupted project files
- Clear error messages with actionable solutions

### Application Recovery
- Auto-save functionality every 30 seconds
- Session recovery on application restart
- Graceful degradation when components fail
- Logging system for debugging issues

## Testing Strategy

### Unit Testing
- Model classes with comprehensive test coverage
- Validation logic testing with edge cases
- TINS generation testing with various input combinations
- File I/O operations testing

### Integration Testing
- UI component interaction testing
- Model-view communication testing
- End-to-end workflow testing
- File format compatibility testing

### User Acceptance Testing
- Complete question workflow testing
- Export functionality validation
- Project save/load cycle testing
- Error recovery scenario testing

## Performance Considerations

### Responsive UI
- Asynchronous operations for file I/O
- Progressive loading of large content
- Efficient preview updates
- Smooth navigation between questions

### Memory Management
- Efficient data structures for question/response storage
- Lazy loading of help content and examples
- Proper cleanup of UI resources
- Optimized markdown rendering

### Scalability
- Extensible question framework
- Pluggable validation system
- Configurable TINS templates
- Support for custom question sets