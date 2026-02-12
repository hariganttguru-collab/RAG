# Fix: RAG site not loading on Azure

Your app: **https://ganttguru-rag-b6hrgugvgte0hebk.southindia-01.azurewebsites.net/**

If the page times out or shows an error, do these in **Azure Portal** → your Web App.

---

## 1. Set Startup Command

Go to **Configuration** → **General settings** → **Startup Command**.

Use **exactly** one of these (copy-paste).

**If your deployed code has `manage.py` at the root of the app (recommended):**
```bash
python manage.py collectstatic --noinput --no-color 2>/dev/null || true; gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 2 config.wsgi:application
```

**If your deployed code has the app inside a `RAG` folder (so you see `RAG/manage.py`):**
```bash
cd RAG && python manage.py collectstatic --noinput --no-color 2>/dev/null || true && gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 2 config.wsgi:application
```

Click **Save** at the top, then **Restart** the app.

---

## 2. Set Application Settings

Go to **Configuration** → **Application settings** → **New application setting**. Add:

| Name | Value |
|------|--------|
| `SECRET_KEY` | Any long random string (e.g. run: `python -c "import secrets; print(secrets.token_urlsafe(50))"`) |
| `DJANGO_DEBUG` | `False` |
| `ALLOWED_HOSTS` | `ganttguru-rag-b6hrgugvgte0hebk.southindia-01.azurewebsites.net` |
| `CSRF_TRUSTED_ORIGINS` | `https://ganttguru-rag-b6hrgugvgte0hebk.southindia-01.azurewebsites.net` |
| `OPENAI_API_KEY` | Your OpenAI API key (needed for RAG features) |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |

Save and **Restart** again.

---

## 3. Check Deployment / Project Root

- In **Deployment Center**, ensure the branch and repo are correct and the **last deployment succeeded**.
- The folder that Azure uses as the app root must contain:
  - `manage.py`
  - `config/` (with `settings.py`, `wsgi.py`)
  - `requirements.txt`
  - `apps/`
- If your repo has the Django app inside a subfolder (e.g. `RAG/`), either:
  - Configure the deployment so that the **deployed root** is that folder (so `manage.py` is at root), or  
  - Use the **second** startup command above (with `cd RAG && ...`).

---

## 4. Check Logs

- **Log stream**: **Monitoring** → **Log stream**. Reproduce the issue and look for Python tracebacks or “ModuleNotFoundError”.
- **Advanced Tools** → **SSH**: connect and run:
  ```bash
  cd /home/site/wwwroot
  ls -la
  # If you see RAG/manage.py:
  cd RAG
  python -c "import django; print(django.get_version())"
  python manage.py check
  ```

If `manage.py check` or imports fail, the error message will point to the fix (e.g. missing env var, wrong path).

---

## 5. Summary checklist

- [ ] Startup command set (one of the two above) and saved
- [ ] App restarted after changing Startup Command and Application settings
- [ ] `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` set
- [ ] `SCM_DO_BUILD_DURING_DEPLOYMENT` = `true`
- [ ] Deployed root contains `manage.py` and `config/` (or startup uses `cd RAG`)
- [ ] Log stream or SSH used to confirm no startup errors

After this, **https://ganttguru-rag-b6hrgugvgte0hebk.southindia-01.azurewebsites.net/** should load (login page or redirect to login).
