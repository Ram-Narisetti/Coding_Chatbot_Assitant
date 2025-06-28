import streamlit as st
import re
import time
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="CodeCraft AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: #e0e0e0;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    .chat-container {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #404040;
    }
    
    .user-message {
        background-color: #4a90e2;
        color: white;
        padding: 1rem;
        border-radius: 10px 10px 0 10px;
        margin: 0.5rem 0;
        margin-left: 2rem;
    }
    
    .bot-message {
        background-color: #3d3d3d;
        color: #ffffff;
        padding: 1rem;
        border-radius: 10px 10px 10px 0;
        margin: 0.5rem 0;
        margin-right: 2rem;
        border-left: 4px solid #667eea;
    }
    
    .code-block {
        background-color: #1a1a1a;
        border: 1px solid #404040;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
    }
    
    .sidebar-content {
        background-color: #2d2d2d;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .stTextInput > div > div > input {
        background-color: #3d3d3d;
        color: white;
        border: 1px solid #555;
        border-radius: 8px;
    }
    
    .stSelectbox > div > div > select {
        background-color: #3d3d3d;
        color: white;
        border: 1px solid #555;
    }
    
    .example-card {
        background-color: #3d3d3d;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .example-card:hover {
        background-color: #4a4a4a;
        transform: translateX(5px);
    }
    
    .stats-card {
        background-color: #3d3d3d;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_count' not in st.session_state:
    st.session_state.conversation_count = 0
if 'code_examples_generated' not in st.session_state:
    st.session_state.code_examples_generated = 0

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("## 🤖 CodeCraft AI")
    st.markdown("**Your Coding Assistant**")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### About")
    st.markdown("""
    A smart assistant to help you with:
    - **Python** 🐍
    - **JavaScript** 🌐
    - **C++** ⚡
    - **HTML/CSS** 🎨
    - **SQL** 🗃️
    - **And more!** 🚀
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Language selection
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 🔧 Settings")
    selected_language = st.selectbox(
        "Preferred Language:",
        ["Python", "JavaScript", "C++", "Java", "HTML/CSS", "SQL", "React", "Node.js"]
    )
    
    difficulty_level = st.selectbox(
        "Difficulty Level:",
        ["Beginner", "Intermediate", "Advanced"]
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Example prompts
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 💡 Quick Examples")
    
    example_prompts = [
        "Write a Python function to calculate factorial",
        "Create a JavaScript array sorting function",
        "Build a simple HTML form with validation",
        "Write a SQL query to join two tables",
        "Create a C++ class for a basic calculator",
        "Build a React component for a todo list"
    ]
    
    for prompt in example_prompts:
        if st.button(prompt, key=f"example_{prompt[:20]}"):
            st.session_state.current_input = prompt
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Stats
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stats-card"><div class="stats-number">{st.session_state.conversation_count}</div><div>Questions</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stats-card"><div class="stats-number">{st.session_state.code_examples_generated}</div><div>Code Examples</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Reset button
    if st.button("🔄 Reset Chat", type="secondary"):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.session_state.code_examples_generated = 0
        st.rerun()

# Main content
st.markdown("""
<div class="main-header">
    <h1>🤖 CodeCraft AI</h1>
    <p>Your Advanced Coding Assistant</p>
</div>
""", unsafe_allow_html=True)

# Code generation functions
def generate_code_response(prompt, language="Python"):
    """Generate code responses based on user prompts"""
    prompt_lower = prompt.lower()
    
    # Python examples
    if "factorial" in prompt_lower and language == "Python":
        return """Here's a Python function to calculate the factorial of a number:

```python
def factorial(n):
    # Calculate the factorial of a number recursively
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Alternative iterative approach
def factorial_iterative(n):
    # Calculate factorial using iteration
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

# Example usage
print(factorial(5))  # Output: 120
print(factorial_iterative(5))  # Output: 120
```

**Explanation:**
- The recursive version calls itself with `n-1` until it reaches the base case
- The iterative version uses a loop to multiply numbers from 2 to n
- Both handle the edge cases where n is 0 or 1 (factorial is 1)"""

    elif "sorting" in prompt_lower and "javascript" in prompt_lower:
        return """Here's a JavaScript function for array sorting with multiple algorithms:

```javascript
// Bubble Sort
function bubbleSort(arr) {
    const n = arr.length;
    for (let i = 0; i < n - 1; i++) {
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            }
        }
    }
    return arr;
}

// Quick Sort (more efficient)
function quickSort(arr) {
    if (arr.length <= 1) return arr;
    
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);
    
    return [...quickSort(left), ...middle, ...quickSort(right)];
}

// Using built-in sort
function customSort(arr, ascending = true) {
    return arr.sort((a, b) => ascending ? a - b : b - a);
}

// Example usage
const numbers = [64, 34, 25, 12, 22, 11, 90];
console.log("Original:", numbers);
console.log("Bubble Sort:", bubbleSort([...numbers]));
console.log("Quick Sort:", quickSort([...numbers]));
console.log("Built-in Sort:", customSort([...numbers]));
```"""

    elif "html" in prompt_lower and "form" in prompt_lower:
        return """Here's an HTML form with built-in validation:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form</title>
    <style>
        .form-container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: #f4f4f4;
            border-radius: 10px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        .btn {
            background: #007bff;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .btn:hover {
            background: #0056b3;
        }
        .error {
            color: red;
            font-size: 14px;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Contact Form</h2>
        <form id="contactForm" novalidate>
            <div class="form-group">
                <label for="name">Full Name *</label>
                <input type="text" id="name" name="name" required>
                <div class="error" id="nameError"></div>
            </div>
            
            <div class="form-group">
                <label for="email">Email Address *</label>
                <input type="email" id="email" name="email" required>
                <div class="error" id="emailError"></div>
            </div>
            
            <div class="form-group">
                <label for="phone">Phone Number</label>
                <input type="tel" id="phone" name="phone" pattern="[0-9]{10}">
                <div class="error" id="phoneError"></div>
            </div>
            
            <div class="form-group">
                <label for="subject">Subject *</label>
                <select id="subject" name="subject" required>
                    <option value="">Select a subject</option>
                    <option value="general">General Inquiry</option>
                    <option value="support">Technical Support</option>
                    <option value="feedback">Feedback</option>
                </select>
                <div class="error" id="subjectError"></div>
            </div>
            
            <div class="form-group">
                <label for="message">Message *</label>
                <textarea id="message" name="message" rows="5" required></textarea>
                <div class="error" id="messageError"></div>
            </div>
            
            <button type="submit" class="btn">Send Message</button>
        </form>
    </div>

    <script>
        document.getElementById('contactForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Clear previous errors
            document.querySelectorAll('.error').forEach(el => el.textContent = '');
            
            let isValid = true;
            
            // Validate name
            const name = document.getElementById('name').value.trim();
            if (!name) {
                document.getElementById('nameError').textContent = 'Name is required';
                isValid = false;
            }
            
            // Validate email
            const email = document.getElementById('email').value.trim();
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!email) {
                document.getElementById('emailError').textContent = 'Email is required';
                isValid = false;
            } else if (!emailRegex.test(email)) {
                document.getElementById('emailError').textContent = 'Please enter a valid email';
                isValid = false;
            }
            
            // Validate phone (optional but must be valid if provided)
            const phone = document.getElementById('phone').value.trim();
            if (phone && !/^[0-9]{10}$/.test(phone)) {
                document.getElementById('phoneError').textContent = 'Please enter a valid 10-digit phone number';
                isValid = false;
            }
            
            // Validate subject
            const subject = document.getElementById('subject').value;
            if (!subject) {
                document.getElementById('subjectError').textContent = 'Please select a subject';
                isValid = false;
            }
            
            // Validate message
            const message = document.getElementById('message').value.trim();
            if (!message) {
                document.getElementById('messageError').textContent = 'Message is required';
                isValid = false;
            } else if (message.length < 10) {
                document.getElementById('messageError').textContent = 'Message must be at least 10 characters long';
                isValid = false;
            }
            
            if (isValid) {
                alert('Form submitted successfully!');
                // Here you would typically send the data to a server
                this.reset();
            }
        });
    </script>
</body>
</html>
```

**Features:**
- Client-side validation with custom error messages
- Responsive design
- Required field indicators
- Email format validation
- Phone number pattern validation
- Message length validation"""

    elif "sql" in prompt_lower and "join" in prompt_lower:
        return """Here are various SQL JOIN examples:

```sql
-- Sample Tables
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    department_id INT
);

CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    manager_id INT
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    product_name VARCHAR(100),
    amount DECIMAL(10,2),
    order_date DATE
);

-- INNER JOIN - Returns only matching records
SELECT u.name, u.email, d.name as department_name
FROM users u
INNER JOIN departments d ON u.department_id = d.id;

-- LEFT JOIN - Returns all records from left table
SELECT u.name, u.email, d.name as department_name
FROM users u
LEFT JOIN departments d ON u.department_id = d.id;

-- RIGHT JOIN - Returns all records from right table
SELECT u.name, u.email, d.name as department_name
FROM users u
RIGHT JOIN departments d ON u.department_id = d.id;

-- FULL OUTER JOIN - Returns all records from both tables
SELECT u.name, u.email, d.name as department_name
FROM users u
FULL OUTER JOIN departments d ON u.department_id = d.id;

-- Multiple JOINs
SELECT 
    u.name as user_name,
    u.email,
    d.name as department_name,
    o.product_name,
    o.amount,
    o.order_date
FROM users u
INNER JOIN departments d ON u.department_id = d.id
LEFT JOIN orders o ON u.id = o.user_id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.order_date DESC;

-- Self JOIN - Joining table with itself
SELECT 
    u.name as employee_name,
    m.name as manager_name
FROM users u
LEFT JOIN users m ON u.manager_id = m.id;

-- Aggregate with JOIN
SELECT 
    d.name as department_name,
    COUNT(u.id) as employee_count,
    AVG(o.amount) as avg_order_amount
FROM departments d
LEFT JOIN users u ON d.id = u.department_id
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY d.id, d.name
ORDER BY employee_count DESC;
```

**JOIN Types Explained:**
- **INNER JOIN**: Only returns rows where there's a match in both tables
- **LEFT JOIN**: Returns all rows from the left table, matching rows from right
- **RIGHT JOIN**: Returns all rows from the right table, matching rows from left
- **FULL OUTER JOIN**: Returns all rows from both tables, whether matched or not"""

    elif "calculator" in prompt_lower and "c++" in prompt_lower:
        return """Here's a C++ calculator class with basic operations:

```cpp
#include <iostream>
#include <stdexcept>
#include <cmath>

class Calculator {
private:
    double lastResult;
    
public:
    // Constructor
    Calculator() : lastResult(0.0) {}
    
    // Basic arithmetic operations
    double add(double a, double b) {
        lastResult = a + b;
        return lastResult;
    }
    
    double subtract(double a, double b) {
        lastResult = a - b;
        return lastResult;
    }
    
    double multiply(double a, double b) {
        lastResult = a * b;
        return lastResult;
    }
    
    double divide(double a, double b) {
        if (b == 0) {
            throw std::invalid_argument("Division by zero is not allowed");
        }
        lastResult = a / b;
        return lastResult;
    }
    
    // Advanced operations
    double power(double base, double exponent) {
        lastResult = std::pow(base, exponent);
        return lastResult;
    }
    
    double squareRoot(double number) {
        if (number < 0) {
            throw std::invalid_argument("Cannot calculate square root of negative number");
        }
        lastResult = std::sqrt(number);
        return lastResult;
    }
    
    double percentage(double number, double percent) {
        lastResult = (number * percent) / 100.0;
        return lastResult;
    }
    
    // Utility functions
    double getLastResult() const {
        return lastResult;
    }
    
    void clearMemory() {
        lastResult = 0.0;
    }
    
    // Display menu
    void displayMenu() {
        std::cout << "\n=== Calculator Menu ===" << std::endl;
        std::cout << "1. Addition" << std::endl;
        std::cout << "2. Subtraction" << std::endl;
        std::cout << "3. Multiplication" << std::endl;
        std::cout << "4. Division" << std::endl;
        std::cout << "5. Power" << std::endl;
        std::cout << "6. Square Root" << std::endl;
        std::cout << "7. Percentage" << std::endl;
        std::cout << "8. Show Last Result" << std::endl;
        std::cout << "9. Clear Memory" << std::endl;
        std::cout << "0. Exit" << std::endl;
        std::cout << "=====================" << std::endl;
    }
};

// Main function to demonstrate usage
int main() {
    Calculator calc;
    int choice;
    double num1, num2;
    
    std::cout << "Welcome to Advanced Calculator!" << std::endl;
    
    do {
        calc.displayMenu();
        std::cout << "Enter your choice: ";
        std::cin >> choice;
        
        try {
            switch (choice) {
                case 1:
                    std::cout << "Enter two numbers: ";
                    std::cin >> num1 >> num2;
                    std::cout << "Result: " << calc.add(num1, num2) << std::endl;
                    break;
                    
                case 2:
                    std::cout << "Enter two numbers: ";
                    std::cin >> num1 >> num2;
                    std::cout << "Result: " << calc.subtract(num1, num2) << std::endl;
                    break;
                    
                case 3:
                    std::cout << "Enter two numbers: ";
                    std::cin >> num1 >> num2;
                    std::cout << "Result: " << calc.multiply(num1, num2) << std::endl;
                    break;
                    
                case 4:
                    std::cout << "Enter two numbers: ";
                    std::cin >> num1 >> num2;
                    std::cout << "Result: " << calc.divide(num1, num2) << std::endl;
                    break;
                    
                case 5:
                    std::cout << "Enter base and exponent: ";
                    std::cin >> num1 >> num2;
                    std::cout << "Result: " << calc.power(num1, num2) << std::endl;
                    break;
                    
                case 6:
                    std::cout << "Enter number: ";
                    std::cin >> num1;
                    std::cout << "Result: " << calc.squareRoot(num1) << std::endl;
                    break;
                    
                case 7:
                    std::cout << "Enter number and percentage: ";
                    std::cin >> num1 >> num2;
                    std::cout << "Result: " << calc.percentage(num1, num2) << std::endl;
                    break;
                    
                case 8:
                    std::cout << "Last result: " << calc.getLastResult() << std::endl;
                    break;
                    
                case 9:
                    calc.clearMemory();
                    std::cout << "Memory cleared!" << std::endl;
                    break;
                    
                case 0:
                    std::cout << "Thank you for using the calculator!" << std::endl;
                    break;
                    
                default:
                    std::cout << "Invalid choice! Please try again." << std::endl;
            }
        } catch (const std::exception& e) {
            std::cout << "Error: " << e.what() << std::endl;
        }
        
        std::cout << std::endl;
        
    } while (choice != 0);
    
    return 0;
}
```

**Features:**
- Basic arithmetic operations (add, subtract, multiply, divide)
- Advanced operations (power, square root, percentage)
- Memory functionality to store last result
- Error handling for division by zero and negative square roots
- Interactive menu system
- Exception handling for robust error management"""

    elif "react" in prompt_lower and "todo" in prompt_lower:
        return """Here's a React component for a Todo List:

```jsx
import React, { useState, useEffect } from 'react';
import './TodoList.css';

const TodoList = () => {
    const [todos, setTodos] = useState([]);
    const [inputValue, setInputValue] = useState('');
    const [filter, setFilter] = useState('all');
    const [editingId, setEditingId] = useState(null);
    const [editingText, setEditingText] = useState('');

    // Load todos from localStorage on component mount
    useEffect(() => {
        const savedTodos = localStorage.getItem('todos');
        if (savedTodos) {
            setTodos(JSON.parse(savedTodos));
        }
    }, []);

    // Save todos to localStorage whenever todos change
    useEffect(() => {
        localStorage.setItem('todos', JSON.stringify(todos));
    }, [todos]);

    // Add new todo
    const addTodo = () => {
        if (inputValue.trim() !== '') {
            const newTodo = {
                id: Date.now(),
                text: inputValue.trim(),
                completed: false,
                createdAt: new Date().toISOString()
            };
            setTodos([...todos, newTodo]);
            setInputValue('');
        }
    };

    // Toggle todo completion
    const toggleTodo = (id) => {
        setTodos(todos.map(todo =>
            todo.id === id ? { ...todo, completed: !todo.completed } : todo
        ));
    };

    // Delete todo
    const deleteTodo = (id) => {
        setTodos(todos.filter(todo => todo.id !== id));
    };

    // Start editing
    const startEditing = (id, text) => {
        setEditingId(id);
        setEditingText(text);
    };

    // Save edit
    const saveEdit = () => {
        if (editingText.trim() !== '') {
            setTodos(todos.map(todo =>
                todo.id === editingId ? { ...todo, text: editingText.trim() } : todo
            ));
        }
        setEditingId(null);
        setEditingText('');
    };

    // Cancel edit
    const cancelEdit = () => {
        setEditingId(null);
        setEditingText('');
    };

    // Clear completed todos
    const clearCompleted = () => {
        setTodos(todos.filter(todo => !todo.completed));
    };

    // Filter todos
    const filteredTodos = todos.filter(todo => {
        switch (filter) {
            case 'active':
                return !todo.completed;
            case 'completed':
                return todo.completed;
            default:
                return true;
        }
    });

    // Handle key press
    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            addTodo();
        }
    };

    const handleEditKeyPress = (e) => {
        if (e.key === 'Enter') {
            saveEdit();
        } else if (e.key === 'Escape') {
            cancelEdit();
        }
    };

    const completedCount = todos.filter(todo => todo.completed).length;
    const activeCount = todos.length - completedCount;

    return (
        <div className="todo-app">
            <header className="todo-header">
                <h1>📝 Todo List</h1>
                <div className="todo-input-container">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="What needs to be done?"
                        className="todo-input"
                    />
                    <button onClick={addTodo} className="add-button">
                        Add
                    </button>
                </div>
            </header>

            <div className="todo-filters">
                <button
                    className={filter === 'all' ? 'active' : ''}
                    onClick={() => setFilter('all')}
                >
                    All ({todos.length})
                </button>
                <button
                    className={filter === 'active' ? 'active' : ''}
                    onClick={() => setFilter('active')}
                >
                    Active ({activeCount})
                </button>
                <button
                    className={filter === 'completed' ? 'active' : ''}
                    onClick={() => setFilter('completed')}
                >
                    Completed ({completedCount})
                </button>
            </div>

            <ul className="todo-list">
                {filteredTodos.map(todo => (
                    <li key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                        <div className="todo-content">
                            <input
                                type="checkbox"
                                checked={todo.completed}
                                onChange={() => toggleTodo(todo.id)}
                                className="todo-checkbox"
                            />
                            
                            {editingId === todo.id ? (
                                <input
                                    type="text"
                                    value={editingText}
                                    onChange={(e) => setEditingText(e.target.value)}
                                    onKeyDown={handleEditKeyPress}
                                    onBlur={saveEdit}
                                    className="edit-input"
                                    autoFocus
                                />
                            ) : (
                                <span
                                    className="todo-text"
                                    onDoubleClick={() => startEditing(todo.id, todo.text)}
                                >
                                    {todo.text}
                                </span>
                            )}
                        </div>
                        
                        <div className="todo-actions">
                            {editingId === todo.id ? (
                                <>
                                    <button onClick={saveEdit} className="save-button">
                                        ✓
                                    </button>
                                    <button onClick={cancelEdit} className="cancel-button">
                                        ✕
                                    </button>
                                </>
                            ) : (
                                <>
                                    <button
                                        onClick={() => startEditing(todo.id, todo.text)}
                                        className="edit-button"
                                    >
                                        ✏️
                                    </button>
                                    <button
                                        onClick={() => deleteTodo(todo.id)}
                                        className="delete-button"
                                    >
                                        🗑️
                                    </button>
                                </>
                            )}
                        </div>
                    </li>
                ))}
            </ul>

            {todos.length > 0 && (
                <footer className="todo-footer">
                    <span className="todo-count">
                        {activeCount} item{activeCount !== 1 ? 's' : ''} left
                    </span>
                    {completedCount > 0 && (
                        <button onClick={clearCompleted} className="clear-completed">
                            Clear completed
                        </button>
                    )}
                </footer>
            )}

            {todos.length === 0 && (
                <div className="empty-state">
                    <p>No todos yet. Add one above!</p>
                </div>
            )}
        </div>
    );
};

export default TodoList;
```

**CSS File (TodoList.css):**
```css
.todo-app {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.todo-header {
    text-align: center;
    margin-bottom: 30px;
}

.todo-header h1 {
    color: #2c3e50;
    margin-bottom: 20px;
    font-size: 2.5rem;
}

.todo-input-container {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
}

.todo-input {
    flex: 1;
    padding: 12px 16px;
    font-size: 16px;
    border: 2px solid #e1e8ed;
    border-radius: 8px;
    outline: none;
    transition: border-color 0.2s;
}

.todo-input:focus {
    border-color: #3498db;
}

.add-button {
    padding: 12px 24px;
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.2s;
}

.add-button:hover {
    background-color: #2980b9;
}

.todo-filters {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 20px;
}

.todo-filters button {
    padding: 8px 16px;
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
}

.todo-filters button:hover {
    background-color: #f8f9fa;
}

.todo-filters button.active {
    background-color: #3498db;
    color: white;
    border-color: #3498db;
}

.todo-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.todo-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 15px;
    border: 1px solid #e1e8ed;
    border-radius: 8px;
    margin-bottom: 10px;
    background-color: white;
    transition: all 0.2s;
}

.todo-item:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.todo-item.completed {
    opacity: 0.7;
    background-color: #f8f9fa;
}

.todo-content {
    display: flex;
    align-items: center;
    flex: 1;
    gap: 12px;
}

.todo-checkbox {
    width: 18px;
    height: 18px;
    cursor: pointer;
}

.todo-text {
    font-size: 16px;
    cursor: pointer;
}

.todo-item.completed .todo-text {
    text-decoration: line-through;
    color: #6c757d;
}

.edit-input {
    flex: 1;
    padding: 6px 8px;
    font-size: 16px;
    border: 1px solid #3498db;
    border-radius: 4px;
    outline: none;
}

.todo-actions {
    display: flex;
    gap: 8px;
}

.todo-actions button {
    padding: 6px 8px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
}

.edit-button, .save-button {
    background-color: #f39c12;
    color: white;
}

.edit-button:hover, .save-button:hover {
    background-color: #e67e22;
}

.delete-button, .cancel-button {
    background-color: #e74c3c;
    color: white;
}

.delete-button:hover, .cancel-button:hover {
    background-color: #c0392b;
}

.todo-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 0;
    border-top: 1px solid #e1e8ed;
    margin-top: 20px;
}

.todo-count {
    color: #6c757d;
    font-size: 14px;
}

.clear-completed {
    padding: 6px 12px;
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.clear-completed:hover {
    background-color: #c82333;
}

.empty-state {
    text-align: center;
    padding: 40px 20px;
    color: #6c757d;
}

.empty-state p {
    font-size: 18px;
    margin: 0;
}

@media (max-width: 600px) {
    .todo-app {
        padding: 10px;
    }
    
    .todo-input-container {
        flex-direction: column;
    }
    
    .todo-filters {
        flex-wrap: wrap;
    }
    
    .todo-item {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
    }
    
    .todo-content {
        width: 100%;
    }
    
    .todo-footer {
        flex-direction: column;
        gap: 10px;
        text-align: center;
    }
}
```

**Key Features:**
- ✅ Add, edit, delete, and toggle todos
- 🔍 Filter by All, Active, or Completed
- 💾 Local storage persistence
- ✏️ Inline editing (double-click or edit button)
- 🧹 Clear completed todos
- 📱 Responsive design
- ⌨️ Keyboard shortcuts (Enter, Escape)
- 📊 Todo counters and statistics"""
    
    else:
        # Generic response
        return f"""I'd be happy to help you with {language} programming! Here are some general tips and a basic example:

**General Programming Best Practices:**
- Write clean, readable code with meaningful variable names
- Add comments to explain complex logic
- Handle errors gracefully
- Test your code thoroughly
- Follow language-specific conventions

**Basic {language} Structure:**
```{language.lower()}
// Example basic structure for {language}
// (This is a generic template - please provide more specific requirements)

function exampleFunction() {{
    // Your code here
    console.log("Hello from {language}!");
}}
```

**What would you like to build specifically?** I can help you with:
- Functions and algorithms
- Data structures
- Web development
- Database operations
- Object-oriented programming
- And much more!

Please provide more details about what you'd like to create, and I'll give you a detailed, working example."""

def get_ai_response(user_input, language):
    """Generate AI response based on user input"""
    st.session_state.conversation_count += 1
    
    # Check if the input contains code-related keywords
    code_keywords = ['function', 'class', 'algorithm', 'code', 'program', 'write', 'create', 'build', 'develop']
    if any(keyword in user_input.lower() for keyword in code_keywords):
        st.session_state.code_examples_generated += 1
        return generate_code_response(user_input, language)
    
    # General programming help
    return f"""Great question! I'm here to help you with {language} and other programming languages.

**For {language} specifically, I can help you with:**
- Basic syntax and structure
- Functions and methods
- Data types and variables
- Control structures (loops, conditionals)
- Object-oriented programming concepts
- Best practices and code optimization
- Debugging and error handling
- Popular libraries and frameworks

**How I can assist you:**
- 💡 Explain programming concepts
- 🔧 Write custom code solutions
- 🐛 Help debug existing code
- 📚 Provide learning resources
- 🚀 Suggest best practices

Could you provide more details about what specific programming challenge you're working on? I'd love to give you a detailed solution with working code examples!"""

# Chat interface
chat_container = st.container()

with chat_container:
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">🧑‍💻 <strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤖 <strong>CodeCraft AI:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)

# Input area
input_container = st.container()
with input_container:
    col1, col2 = st.columns([6, 1])
    
    with col1:
        # Check if there's a preset input from example buttons
        if 'current_input' in st.session_state:
            user_input = st.text_input("Ask anything about coding...", value=st.session_state.current_input, key="user_input")
            # Clear the preset input after using it
            del st.session_state.current_input
        else:
            user_input = st.text_input("Ask anything about coding...", key="user_input", placeholder="e.g., Write a Python function to reverse a string")
    
    with col2:
        send_button = st.button("Send 🚀", type="primary", use_container_width=True)

# Process user input
if send_button or user_input:
    if user_input.strip():
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate AI response
        with st.spinner("🤖 CodeCraft AI is thinking..."):
            time.sleep(1)  # Simulate processing time
            ai_response = get_ai_response(user_input, selected_language)
        
        # Add AI response to chat
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Clear input and rerun to show new messages
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>🤖 <strong>CodeCraft AI</strong> - Your Advanced Coding Assistant</p>
    <p>Built with ❤️ using Streamlit | Ready to help with Python, JavaScript, C++, HTML, SQL, and more!</p>
    <p><em>💡 Tip: Double-click any code example to select it for easy copying</em></p>
</div>
""", unsafe_allow_html=True)