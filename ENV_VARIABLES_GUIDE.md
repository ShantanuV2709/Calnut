# Quick Reference: Environment Variables

## 📝 Current Environment Variables

| Variable | Purpose | Current Value | Required |
|----------|---------|---------------|----------|
| `DJANGO_SECRET_KEY` | Django's secret key for cryptographic signing | Set in `.env` | ✅ Yes |
| `DEBUG` | Enable/disable debug mode | `True` (default) | No |

## 🔧 How to Add More Environment Variables

### 1. Add to `.env` file
```env
NEW_VARIABLE=value_here
```

### 2. Add to `.env.example` file (for documentation)
```env
NEW_VARIABLE=example_value
```

### 3. Use in `settings.py`
```python
# For strings
MY_VAR = env('NEW_VARIABLE')

# For booleans
MY_BOOL = env.bool('BOOL_VARIABLE', default=False)

# For integers
MY_INT = env.int('INT_VARIABLE', default=100)

# For lists (comma-separated)
MY_LIST = env.list('LIST_VARIABLE', default=[])

# With fallback
MY_VAR = env('OPTIONAL_VAR', default='fallback_value')
```

## 📚 Common Use Cases

### Database URL
```python
# In .env
DATABASE_URL=mongodb://localhost:27017/Calnut

# In settings.py
DATABASES = {
    'default': env.db_url('DATABASE_URL')
}
```

### Allowed Hosts
```python
# In .env
ALLOWED_HOSTS=localhost,127.0.0.1,example.com

# In settings.py
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
```

### Email Settings
```python
# In .env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# In settings.py
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
```

## 🚨 Important Rules

1. ✅ **DO**: Keep `.env` in `.gitignore`
2. ✅ **DO**: Update `.env.example` when adding new variables
3. ✅ **DO**: Use different values for dev/staging/production
4. ✅ **DO**: Provide sensible defaults for optional variables
5. ❌ **DON'T**: Commit `.env` to Git
6. ❌ **DON'T**: Share `.env` files publicly
7. ❌ **DON'T**: Hardcode secrets in `settings.py`

## 🔄 Different Environments

### Development (.env)
```env
DEBUG=True
DJANGO_SECRET_KEY=dev-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production (.env)
```env
DEBUG=False
DJANGO_SECRET_KEY=super-secure-production-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 🆘 Troubleshooting

### Error: "Environment variable not found"
**Solution**: Add the variable to `.env` or provide a default:
```python
MY_VAR = env('MY_VAR', default='default_value')
```

### Error: "No module named 'environ'"
**Solution**: Install django-environ:
```bash
pip install django-environ
```

### Settings not updating
**Solution**: 
1. Restart the Django development server
2. Check `.env` file syntax (no spaces around `=`)
3. Ensure `.env` is in the project root

## 📖 Documentation

- django-environ docs: https://django-environ.readthedocs.io/
- Django settings best practices: https://docs.djangoproject.com/en/stable/topics/settings/
