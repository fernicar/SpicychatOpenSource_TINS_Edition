# TINS Methodology and Creation Framework

## What is TINS?

TINS (ThereIsNoSource) is a revolutionary approach to software distribution where:

1. **Only READMEs are distributed** - No source code is included in releases
2. **LLMs generate code on demand** - Software is reconstructed locally using AI
3. **Instructions evolve with technology** - The same README produces better code as LLMs improve
4. **Standardized format ensures consistency** - A structured approach to describing software functionality

## TINS Creation Assistant Question Framework

When creating TINS specifications, always follow this 11-question framework to ensure comprehensive coverage:

### 1. Project Title and Description
**Question:** What is the name of the software, and what is its overall goal and purpose?
**Focus:** Clear project identity and value proposition

### 2. Core Logic and Features (for `model.py` specification)
**Question:** What are the main functions, computations, processes, or behaviors the application needs? Describe them step-by-step or in terms of inputs/outputs.
**Focus:** Business logic and core functionality

### 3. Data Structure and Handling (for `model.py` specification)
**Question:** What kind of data does the application use? How is it stored, retrieved, processed, or managed? Define key data entities and their properties/relationships conceptually.
**Focus:** Data models and persistence

### 4. User Interface Requirements (for `main.py` specification)
**Question:** Given the default PySide6 setup, what specific windows, dialogs, layouts, or widgets (buttons, text fields, tables, charts, etc.) are needed? How should these UI elements be arranged?
**Focus:** GUI design and layout

### 5. User Interaction and Event Handling (Connecting `main.py` to `model.py`)
**Question:** How does the user interact with the UI? What actions should trigger specific logic in the model? How should the model signal updates back to the UI?
**Focus:** Event handling and MVC communication

### 6. Input and Output Specifications
**Question:** How does data enter and leave the system (user input via UI, file I/O, network requests)? Specify expected formats where relevant.
**Focus:** Data flow and external interfaces

### 7. Dependencies and Third-Party Integrations
**Question:** Does the application need to use specific Python libraries (besides PySide6) or connect to external services/APIs? List them.
**Focus:** External dependencies and integrations

### 8. Error Handling and Validation
**Question:** What potential errors should the application anticipate and handle in both the model logic and how errors are presented in the UI?
**Focus:** Robustness and user experience

### 9. Technical Constraints and Non-Functional Requirements
**Question:** Are there specific performance goals, memory limits, or other technical considerations the LLM should be aware of when generating the code?
**Focus:** Performance and technical requirements

### 10. Acceptance Criteria
**Question:** How will the user know if the generated code correctly implements a feature? Define clear, testable outcomes for key functionalities.
**Focus:** Validation and testing criteria

### 11. Visual Aids
**Question:** Do you have any design sketches, diagrams (like UI layouts, data flow, or state machines), or example data structures you can describe or share?
**Focus:** Visual documentation and examples

## Default Assumptions for Python Applications

When creating TINS specifications for Python desktop applications, assume:

- **GUI Framework:** PySide6 version >= 6.9.1
- **Style:** 'Fusion' style with 'Auto' color scheme
- **Architecture:** Clear separation between `model.py` (business logic) and `main.py` (GUI/events)
- **LLM APIs:** Groq's free API key and Google Gemini's free API key (with quota management)

## TINS Specification Structure

Generated TINS should follow this standard format:

```markdown
# Project Title

## Description
[Overall goal and purpose]

## Functionality
### Core Features
### User Interface
### Behavior Specifications

## Technical Implementation
### Architecture
### Data Structures
### Algorithms
### Dependencies

## Input/Output
[Data flow specifications]

## Error Handling
[Error management approach]

## Technical Constraints & Notes
[Performance and technical requirements]

## Acceptance Criteria
[Testable outcomes]

## Visual Aids
[Diagrams and examples]
```

## Best Practices for TINS Creation

1. **Be Explicit, Not Implicit** - State requirements clearly rather than assuming
2. **Provide Concrete Examples** - Include specific examples to clarify intent
3. **Use Consistent Terminology** - Maintain consistent language throughout
4. **Balance Detail and Clarity** - Provide sufficient detail without overwhelming
5. **Structure Information Hierarchically** - Use proper heading levels for organization

## Code Generation Guidelines

When implementing TINS specifications:

- Focus on the separation of concerns between `model.py` and `main.py`
- Define clear interfaces between components
- Include proper error handling in both logic and UI layers
- Follow PySide6 best practices for GUI development
- Implement comprehensive input validation
- Create testable, modular code structures

## Validation and Quality Assurance

Ensure TINS specifications:
- Include all required sections with appropriate content
- Use proper Markdown formatting
- Provide sufficient detail for implementation
- Are self-consistent with no contradictory requirements
- Don't reference external sources or documentation
- Are complete (all functionality described)

This framework ensures that every TINS specification created will be comprehensive, clear, and optimized for LLM code generation.