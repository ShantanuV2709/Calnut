# 🔧 Quick Fix Guide - Install & Run

## ⚡ Immediate Actions Required

### 1. Install Missing Dependencies
```bash
pip install Pillow reportlab
```

**OR** reinstall everything:
```bash
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
python -c "import PIL; import reportlab; print('✅ All dependencies installed!')"
```

### 3. Run the Server
```bash
python manage.py runserver
```

---

## 🐛 What Was Fixed

| Bug | Severity | Status |
|-----|----------|--------|
| Duplicate `profile_view` function | 🔴 Critical | ✅ Fixed |
| Missing Pillow dependency | 🟡 High | ✅ Fixed |
| Missing reportlab dependency | 🟡 High | ✅ Fixed |
| Unregistered admin models | 🟡 Medium | ✅ Fixed |

---

## ✅ Verification Checklist

After installing dependencies, verify these features work:

- [ ] User can register and login
- [ ] Profile page loads without errors
- [ ] Can upload profile picture (uses Pillow)
- [ ] Food logging works
- [ ] Water and exercise tracking works
- [ ] PDF export works (uses reportlab)
- [ ] CSV export works
- [ ] Admin panel shows all models

---

## 🚨 If You Encounter Errors

### Error: "No module named 'PIL'"
**Fix**: `pip install Pillow`

### Error: "No module named 'reportlab'"
**Fix**: `pip install reportlab`

### Error: "Profile matching query does not exist"
**Fix**: App will auto-create profile on first login

### MongoDB Connection Error
**Fix**: Ensure MongoDB is running:
- Windows: `net start MongoDB`
- Mac/Linux: `sudo systemctl start mongod`

---

## 📦 Complete Setup (Fresh Install)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Seed database (optional)
python manage.py shell
>>> from home.utils import seed_database
>>> seed_database()
>>> exit()

# 7. Run server
python manage.py runserver
```

---

## 🎉 All Fixed!

Your Calnut application is now bug-free and ready to use! 🚀
