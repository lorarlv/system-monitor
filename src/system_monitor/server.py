import threading
import time
import webbrowser

import uvicorn

from .api import app

def open_browser() -> None:
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:8000")

def main() -> None:
    threading.Thread(
        target=open_browser,
        daemon=True,
    ).start()

    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_config=None,
        access_log=False,
    )

    server = uvicorn.Server(config)

    app.state.shutdown_callback = lambda: setattr(
        server,
        "should_exit",
        True,
    )

    server.run()

if __name__ == "__main__":
    main()