# 📋 TaskFlow 

-**Deployed link :** https://azentrix-fullstack-task2-rho.vercel.app
-used vercel to deploy 

## 🎯 What is This?

TaskFlow is a complete task management application (like Trello) built with:
- **Backend**: Python Flask (simple!)
- **Frontend**: HTML, CSS, JavaScript (no frameworks!)
- **Database**: SQLite (automatic!)
---

## ✨ Features

✅ **User Accounts** - Register and login
✅ **Demo Workspace** - Automatically created with sample data
✅ **Kanban Board** - To Do, In Progress, Done columns
✅ **Drag & Drop** - Move tasks between columns
✅ **Comments** - Add comments to tasks
✅ **Task Management** - Create, edit, delete tasks
✅ **Beautiful UI** - Modern gradient design
✅ **Progress Tracking** - Track task completion
✅ **Priority Levels** - High, Medium, Low
✅ **Responsive** - Works on desktop and mobile

---

## 📁 File Structure

```
taskflow/
├── app.py                    (Main application - 300 lines)
└── templates/
    ├── auth.html            (Login/Signup page)
    └── dashboard.html       (Kanban board)
```

## 👤 Create Account & Explore

1. Click "Sign Up"
2. Fill in name, username, email, password
3. **Boom!** 💥 You get a demo workspace with sample tasks
4. Drag tasks, add comments, create new tasks
5. Try all features!

---

## 🎁 Demo Workspace

New users automatically get:
- ✅ Sample board with real tasks
- ✅ 10 tasks across 3 columns
- ✅ Team member assignments
- ✅ Comments on tasks
- ✅ Different priorities
- ✅ Due dates

Perfect for testing all features instantly!

---

## 🎨 Code Quality

The code is:
- ✅ **Simple**: Easy to understand
- ✅ **Commented**: Explanations in code
- ✅ **Organized**: Clear structure
- ✅ **Modular**: Easy to modify
- ✅ **Beautiful**: No dependencies bloat

Perfect for learning!

---

## 🔧 What You'll Learn

By studying this code, you'll learn:

1. **Flask Basics**
   - Routes and views
   - Request/response handling
   - RESTful API design

2. **Database with SQLAlchemy**
   - Models and relationships
   - CRUD operations
   - Foreign keys

3. **Frontend Development**
   - HTML structure
   - CSS styling (gradients, animations)
   - JavaScript (async/fetch, DOM manipulation)
   - Drag and drop

4. **Web Architecture**
   - Client-server model
   - JSON APIs
   - Session management

---

## 📊 Project Stats

| Metric | Value |
|--------|-------|
| Backend Lines | 300 |
| Frontend HTML | 250 |
| Frontend CSS | 400 |
| Frontend JavaScript | 200 |
| Total Code | 1,150 lines |
| Database Tables | 4 |
| API Endpoints | 12 |
| Setup Time | 5 minutes |
| Dependencies | 2 |
| Complexity | ⭐ Very Easy |

---

## 💡 Key Concepts Demonstrated

### Backend (app.py)
```python
# 1. Flask app initialization
# 2. SQLAlchemy ORM models
# 3. User authentication
# 4. RESTful API routes
# 5. Database relationships
# 6. Error handling
# 7. Session management
```

### Frontend (HTML + JavaScript)
```javascript
// 1. Fetch API for HTTP requests
// 2. DOM manipulation
// 3. Event listeners
// 4. Drag and drop
// 5. Modal dialogs
// 6. Form validation
// 7. Real-time UI updates
```

### Database
```
Users → Boards → Tasks → Comments
```

Proper relationships and foreign keys!

---


## 📚 Learning Resources

### Understanding the Code
1. **Models** (app.py lines 20-60) - Database structure
2. **Routes** (app.py lines 80-150) - API endpoints
3. **Frontend** (templates) - User interface

### Code Comments
Every important section has comments explaining what it does.

### Clear Function Names
Functions like `create_demo_workspace()` are self-explanatory.

---

## ⚙️ Installation & Setup

### Prerequisites

* Python 3.14+
* pip

### Clone Repository

```bash
git clone <https://github.com/MeloniJQ/azentrix-fullstack-task2.git>
cd azentrix-fullstack-task2
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

### Open Browser

```text
http://localhost:5000
```
---


## 📖 Code Overview

### app.py (300 lines)

**Part 1: Imports & Setup (Lines 1-20)**
```python
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
# ... setup code
```

**Part 2: Database Models (Lines 30-120)**
```python
class User(db.Model):
class Board(db.Model):
class Task(db.Model):
class Comment(db.Model):
```

**Part 3: API Routes (Lines 130-250)**
```python
@app.route('/api/register')
@app.route('/api/login')
@app.route('/api/boards')
@app.route('/api/tasks')
# ... 12 API endpoints total
```

**Part 4: Demo Data (Lines 260-300)**
```python
def create_demo_workspace(user_id):
    # Creates sample board with tasks
```

---


## 📝 License

Free to use, modify, and share. Perfect for learning!

---

## 💪 Built With

- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Simple database
- **HTML5** - Markup
- **CSS3** - Styling with modern features
- **Vanilla JavaScript** - No frameworks!

---

## 🎓 Perfect For

- 🎓 Students learning web development
- 👨‍💻 Beginners starting their coding journey
- 📚 Portfolio project
- 🔍 Understanding full-stack architecture
- 🎯 Teaching concepts like REST APIs, databases, forms

---
Below are the screen shots of websites attached 
<br>
<img width="1888" height="847" alt="Screenshot 2026-06-30 092025" src="https://github.com/user-attachments/assets/0949fcd5-60e5-45a3-a94b-3f7dd9741c31" />

<img width="1897" height="857" alt="Screenshot 2026-06-30 092045" src="https://github.com/user-attachments/assets/57d009d5-b09c-4adb-abfe-834d2d2d0c5d" />

<img width="1895" height="848" alt="Screenshot 2026-06-30 101314" src="https://github.com/user-attachments/assets/63021c96-1517-4532-91f5-c3a01d4d33bf" />

<img width="1098" height="757" alt="Screenshot 2026-06-30 101331" src="https://github.com/user-attachments/assets/b19dbae6-bc9a-4219-9e94-33dd2d0d63b0" />

<img width="772" height="821" alt="Screenshot 2026-06-30 101355" src="https://github.com/user-attachments/assets/79cb27f4-e071-449c-bf79-2530c3745a39" />

<img width="1317" height="750" alt="image" src="https://github.com/user-attachments/assets/033d6a92-eb0c-4b29-8dc1-0dbcf000bc3b" />

---
Below is the screen recording of the working website 
<br>
https://www.loom.com/share/15a8373391a04a98b26307b009a4c20f



**Made simple. Made powerful for learning. Made beautiful for users.** 

🚀 **Happy coding!**
