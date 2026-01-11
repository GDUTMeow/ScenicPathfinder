import streamlit.web.cli as cli
import sys
import os

if __name__ == "__main__":
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    os.chdir(base)
    app = os.path.join(base, "app.py")
    if not os.path.exists(app):
        raise FileNotFoundError(f"Cannot find app.py at {app}")
    sys.argv = ["streamlit", "run", app, "--global.developmentMode=false", "--client.toolbarMode=viewer"]
    sys.exit(cli.main())