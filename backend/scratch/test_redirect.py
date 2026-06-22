import os
import sys

# Ensure backend directory is in the import path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("--- Testing localhost:8000 ---")
# 1. Test Google Login
response_google = client.get("/auth/google/login", headers={"Host": "localhost:8000"}, follow_redirects=False)
print("Google redirect location:", response_google.headers.get("location"))

# 2. Test GitHub Login
response_github = client.get("/auth/github/login", headers={"Host": "localhost:8000"}, follow_redirects=False)
print("GitHub redirect location:", response_github.headers.get("location"))

print("\n--- Testing production domain ---")
# 3. Test Google Login (Production)
response_prod_google = client.get("/auth/google/login", headers={"Host": "interleet-backend.sharexpress.in"}, follow_redirects=False)
print("Google redirect location (prod):", response_prod_google.headers.get("location"))

# 4. Test GitHub Login (Prod)
response_prod_github = client.get("/auth/github/login", headers={"Host": "interleet-backend.sharexpress.in"}, follow_redirects=False)
print("GitHub redirect location (prod):", response_prod_github.headers.get("location"))
