import os
import pytest

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)

def file_exists(path):
    return os.path.isfile(os.path.join(ROOT, path))

def file_not_empty(path):
    full = os.path.join(ROOT, path)
    return os.path.isfile(full) and os.path.getsize(full) > 0

def test_readme_exists_and_not_empty():
    assert file_not_empty('README.md'), "README.md missing or empty"

def test_authors_exists():
    assert file_not_empty('AUTHORS'), "AUTHORS missing or empty"

def test_license_exists():
    assert file_not_empty('LICENSE'), "LICENSE missing or empty"

def test_gitignore_has_venv():
    path = os.path.join(ROOT, '.gitignore')
    content = open(path).read()
    assert 'venv/' in content or '.venv/' in content, ".gitignore must include venv/"

def test_no_venv_in_repo():
    """venv/ และ .venv/ ต้องไม่มีใน repo"""
    assert not os.path.isdir(os.path.join(ROOT, 'venv')), "venv/ must not be committed"
    assert not os.path.isdir(os.path.join(ROOT, '.venv')), ".venv/ must not be committed"

def test_required_route_files_exist():
    routes = ['app/routes/auth.py', 'app/routes/account.py',
              'app/routes/products.py']
    for r in routes:
        assert file_not_empty(r), f"{r} missing or empty"

def test_required_templates_exist():
    templates = ['app/templates/base.html', 'app/templates/login.html',
                 'app/templates/home.html', 'app/templates/edit_profile.html']
    for t in templates:
        assert file_not_empty(t), f"{t} missing or empty"

def test_evil_html_exists():
    assert file_exists('evil.html'), "evil.html missing"

def test_document_md_has_csrf_section():
    path = os.path.join(ROOT, 'document.md')
    content = open(path).read()
    assert 'CSRF' in content, "document.md must contain CSRF section"
