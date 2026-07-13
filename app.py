import os
import sys
import json
import webview
import io
import threading
import shutil
from pathlib import Path

# Import backend logic
from main import main
from config import PROCESSED_DIR, DUPLICATES_DIR, REPORTS_DIR, REVIEW_DIR

class Api:
    def __init__(self):
        self.window = None
        self.current_screen = 'system_overview'
        self.is_processing = False
        # Accumulate all results so we can replay them when navigating back
        self.activity_log = []
        self.batch_total = 0
        self.batch_done = 0
        self.current_image = None

    def start_batch(self):
        """Opens folder dialog, then kicks off processing in a background thread."""
        folder_paths = self.window.create_file_dialog(
            webview.FOLDER_DIALOG,
            allow_multiple=False,
            directory=''
        )

        if not folder_paths:
            return False  # User cancelled

        selected_folder = folder_paths[0]

        # Count images up front for the progress bar
        from pathlib import Path as P
        target = P(selected_folder)
        images = list(target.glob("*.png")) + list(target.glob("*.jpg")) + list(target.glob("*.jpeg"))
        self.batch_total = len(images)
        self.batch_done = 0
        self.activity_log = []
        self.current_image = None
        self.is_processing = True

        # Auto-navigate to the live processing dashboard
        self.navigate('live_processing_dashboard')

        def ui_callback(result):
            """Called from the background thread after each receipt — thread-safe via evaluate_js."""
            self.batch_done += 1
            
            # Pop image_data out so we don't store 1000s of base64 images in memory history
            result_log = result.copy()
            self.current_image = result_log.pop('image_data', None)
            self.activity_log.append(result_log)
            
            if self.window:
                pct = round((self.batch_done / self.batch_total) * 100, 1) if self.batch_total else 0
                payload = {
                    "done": self.batch_done,
                    "total": self.batch_total,
                    "pct": pct,
                    "log": result_log,
                    "image_data": self.current_image,
                    "confidence": result_log.get('confidence', 0),
                    "needs_review": len(list(REVIEW_DIR.glob("*.*")))
                }
                
                json_str = json.dumps(payload)
                self.window.evaluate_js(f'if(window.onReceiptProcessed) window.onReceiptProcessed({json_str});')

        def run_thread():
            main(ui_callback=ui_callback, source_dir=selected_folder)
            self.is_processing = False
            if self.window:
                self.window.evaluate_js('if(window.onBatchComplete) window.onBatchComplete();')

        threading.Thread(target=run_thread, daemon=True).start()
        return True

    def export_report(self):
        """Opens a save dialog and copies the Excel report to the chosen path."""
        save_path = self.window.create_file_dialog(
            webview.SAVE_DIALOG,
            save_filename='Receipts_Report.xlsx'
        )

        if save_path:
            source_file = REPORTS_DIR / "Receipts.xlsx"
            if source_file.exists():
                shutil.copy2(source_file, save_path[0] if isinstance(save_path, tuple) else save_path)
            else:
                self.window.evaluate_js('alert("No report exists yet. Please process some receipts first.");')
        return bool(save_path)

    def get_stats(self):
        """Returns current file counts from the output directories."""
        processed = len(list(PROCESSED_DIR.rglob("*.*")))
        duplicates = len(list(DUPLICATES_DIR.glob("*.*")))
        needs_review = len(list(REVIEW_DIR.glob("*.*")))
        return {
            "processed": processed,
            "duplicates": duplicates,
            "needs_review": needs_review
        }

    def get_current_state(self):
        """Returns accumulated state so a page can hydrate itself on load."""
        return {
            "is_processing": self.is_processing,
            "batch_total": self.batch_total,
            "batch_done": self.batch_done,
            "activity_log": self.activity_log,
            "current_image": self.current_image
        }

    def navigate(self, screen_folder):
        """Loads a different HTML screen into the window."""
        global base_path
        self.current_screen = screen_folder
        html_path = os.path.join(base_path, 'ui_design', screen_folder, 'code.html')
        self.window.load_url(f'file://{html_path}')


def on_closing():
    return api.window.create_confirmation_dialog('Quit', 'Are you sure you want to exit?')


if __name__ == '__main__':
    # Only redirect when genuinely headless (PyInstaller --noconsole sets these to None)
    if sys.stdout is None:
        sys.stdout = io.StringIO()
    if sys.stderr is None:
        sys.stderr = io.StringIO()

    api = Api()

    global base_path
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    html_path = os.path.join(base_path, 'ui_design', 'system_overview', 'code.html')

    api.window = webview.create_window(
        title='Receipt Pro Dashboard',
        url=f'file://{html_path}',
        js_api=api,
        width=1200,
        height=800,
        text_select=False
    )

    api.window.events.closing += on_closing

    webview.start()
