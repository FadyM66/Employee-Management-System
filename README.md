# Employee Management System

A full-stack application for managing companies, departments, and employees with JWT authentication and role-based access control.

---

## 📊 Implementation Status

### **Backend (Django REST Framework)**  
**✅ Models**  
- `User`, `Company`, `Department`, and `Employee` models implemented  

**✅ Validations**  
1. Required field validation for all incoming requests - **Done**  
2. Auto-calculation of departments/employees per company - **Done**  
3. Auto-calculation of employees per department - **Done**  
4. Days-employed calculation based on hire date - **Done**  
5. Error handling - **🚧 In Progress**  

**✅ Workflow**  
- Hiring process transition order enforced (Application → Interview → Hired/Not Accepted)  

**✅ Security**  
- JWT authentication implemented  

**🔑 Role-Based System**  
- User role permissions - **Done**  
- Company/Department/Employee permissions - **🚧 In Progress**  

**🌐 API Endpoints**  
| Resource | Status | 
|----------|--------|
| User API | ✅ Done | 
| Company API | 🚧 In Progress | 
| Department API | 🚧 In Progress |  
| Employee API | 🚧 In Progress |  
| RESTful conventions | ✅ Done |

**📝 Logging System**  
- Basic implementation - **🚧 In Progress**

---

### **Frontend (React)**  
**🔐 Authentication**  
- Login/Logout - ✅ Done (Formik + Yup validation)  

**🏢 Management Pages**  
| Feature | Status |  
|---------|--------|  
| Company Management | 🚧 In Progress |  
| Department Management | 🚧 In Progress |  
| Employee Management | 🚧 In Progress |  
| User Management | 🚧 In Progress |  
| Summary Dashboard | 🚧 In Progress |  

**🛠️ Validations**  
- Login form - ✅ Done  
- Other forms - 🚧 In Progress  

**🔗 Context-Aware Data**  
- Department filtering by company - 🚧 In Progress  

**⚠️ Error Handling**  
- Basic implementation - 🚧 In Progress  

---

### **API Integration**  
**🔄 General Progress**  
- Data exchange setup - 🚧 In Progress  
- Authentication integration - ✅ Done  
- Authorization headers - ✅ Done  
- Error feedback UX - 🚧 In Progress  
- Loading states - 🚧 In Progress  

---

## 🔒 Security Features  
- JWT token authentication  
- Role-based access for user operations  
- Password hashing via Django auth  
- Secure API endpoints  

---

## ⚙️ Installation & Setup

### Option 1: Automated Setup (Recommended)
Run the project with the automation script:
```bash
python run_project.py

### Option 1: Automated Setup (Recommended)

### Backend
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/MacOS
# .venv\Scripts\activate  # Windows
git clone https://github.com/FadyM66/Employee-Management-System.git
cd backend/ems
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

### Frontend
```bash
cd ../../frontend
npm install
npm start

Frontend: http://localhost:5173
Backend API: http://localhost:8000/

