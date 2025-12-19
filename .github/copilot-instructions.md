- [x] Verify that the copilot-instructions.md file in the .github directory is created. (created file)

- [x] Clarify Project Requirements
  - Build an image background removal tool in Python with FastAPI API, CLI, and minimal web UI.

- [x] Scaffold the Project
  - Created README, requirements, Dockerfile, Makefile, src package, and tests directories.

- [x] Customize the Project
  - Implemented FastAPI API, CLI, background removal service, and minimal web UI.

- [x] Install Required Extensions
  - No extensions required (get_project_setup_info returned none).

- [x] Compile the Project
  - Ran get_errors diagnostics; no issues reported. Installed dependencies via python3 -m pip.

- [x] Create and Run Task
  - Added .vscode/tasks.json task `api (uvicorn)` (PYTHONPATH=src python3 -m uvicorn background_removal.api:app --host 0.0.0.0 --port 8000 --reload`).

- [x] Launch the Project
  - Started `api (uvicorn)` task on http://0.0.0.0:8000 with reload enabled.

- [x] Ensure Documentation is Complete
  - README present and current; this instructions file cleaned of HTML comments and updated.
