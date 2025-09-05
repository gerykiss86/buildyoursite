"""
Base class for Playwright tests with automatic logging, screenshots, and HTML report generation
This can be imported and reused by all test cases for consistent logging and reporting
"""

import json
import time
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import traceback
from typing import Any, Optional, Dict, List
from dotenv import load_dotenv

# Enable Unicode output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class PlaywrightTestBase:
    """Base class for Playwright tests with automatic execution logging"""
    
    def __init__(self, test_name: str):
        # Load environment variables from .env file
        load_dotenv()
        
        self.test_name = test_name
        self.base_url = os.getenv('BASE_URL', 'https://bolt.new/')
        self.page: Optional[Page] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.report_dir: Optional[Path] = None
        self.execution_log: List[Dict[str, Any]] = []
        self.step_counter = 0
        self.session_started = datetime.now()
        self.max_wait_time = 30000  # Maximum time to wait for page to stabilize 
        self.hash_check_interval = 200  # Check hash interval
        
    def setup_report_directory(self):
        """Create report directory for this test run"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_dir = Path("reports") / f"{self.test_name}_{timestamp}"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        return self.report_dir
        
    def _take_screenshot(self, name: str, description: str = "") -> str:
        """Take a screenshot and save to report directory"""
        if self.page and self.report_dir:
            filename = f"{self.step_counter:03d}_{name}.png"
            filepath = self.report_dir / filename
            self.page.screenshot(path=str(filepath))
            return filename
        return ""
        
    def _log_command(self, command: str, method: str, args: tuple, kwargs: dict, 
                     result: Any = None, error: Exception = None):
        """Log command execution details"""
        self.step_counter += 1
        
        # Format command string
        if args or kwargs:
            arg_strs = [repr(arg) for arg in args]
            arg_strs.extend([f"{k}={repr(v)}" for k, v in kwargs.items()])
            command_str = f"{method}({', '.join(arg_strs)})"
        else:
            command_str = command
            
        # Take before screenshot
        before_screenshot = self._take_screenshot(f"before_{method}", f"Before {command_str}")
        
        # Create log entry
        log_entry = {
            "step": self.step_counter,
            "command": command_str,
            "timestamp": datetime.now().isoformat(),
            "before_screenshot": before_screenshot,
        }
        
        # Execute and capture result/error
        if error:
            log_entry["status"] = "ERROR"
            log_entry["error"] = str(error)
            log_entry["traceback"] = traceback.format_exc()
        else:
            log_entry["status"] = "SUCCESS"
            if result is not None:
                log_entry["output"] = f"Result: {result}"
                
        # Take after screenshot
        after_screenshot = self._take_screenshot(f"after_{method}", f"After {command_str}")
        log_entry["after_screenshot"] = after_screenshot
        
        self.execution_log.append(log_entry)
        self._save_execution_summary()
        
        # Print to console
        print(f"[Step {self.step_counter}] {command_str}")
        if error:
            print(f"  ERROR: {error}")
        elif result is not None:
            print(f"  Result: {result}")
            
    def _save_execution_summary(self):
        """Save execution summary to JSON file"""
        if self.report_dir:
            summary = {
                "test_name": self.test_name,
                "session_started": self.session_started.isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_commands": len(self.execution_log),
                "commands": self.execution_log
            }
            
            summary_path = self.report_dir / "execution_summary.json"
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2)
                
    def _generate_html_report(self):
        """Generate HTML report from execution log"""
        if not self.report_dir:
            return
            
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{self.test_name} - Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background-color: #333;
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .step {{
            background-color: white;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .step-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}
        .command {{
            font-family: 'Courier New', monospace;
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 3px;
            margin: 10px 0;
        }}
        .success {{
            color: #28a745;
            font-weight: bold;
        }}
        .error {{
            color: #dc3545;
            font-weight: bold;
        }}
        .screenshots {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }}
        .screenshot-container {{
            flex: 1;
            text-align: center;
        }}
        .screenshot {{
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 3px;
            cursor: pointer;
        }}
        .screenshot-label {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .error-details {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 10px;
            border-radius: 3px;
            margin-top: 10px;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 12px;
        }}
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
        }}
        .modal-content {{
            margin: auto;
            display: block;
            max-width: 90%;
            max-height: 90%;
            margin-top: 50px;
        }}
        .close {{
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{self.test_name} - Test Execution Report</h1>
        <p>Started: {self.session_started.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Total Steps: {len(self.execution_log)}</p>
    </div>
"""

        for step in self.execution_log:
            status_class = "success" if step["status"] == "SUCCESS" else "error"
            html_content += f"""
    <div class="step">
        <div class="step-header">
            <h3>Step {step['step']}</h3>
            <span class="{status_class}">{step['status']}</span>
        </div>
        <div class="command">{step['command']}</div>
        <small>Timestamp: {step['timestamp']}</small>
"""
            
            if step.get('output'):
                html_content += f"""
        <div style="margin-top: 10px;">
            <strong>Output:</strong> {step['output']}
        </div>
"""
            
            if step.get('error'):
                html_content += f"""
        <div class="error-details">
            <strong>Error:</strong> {step['error']}
            {step.get('traceback', '')}
        </div>
"""
            
            # Add screenshots
            if step.get('before_screenshot') or step.get('after_screenshot'):
                html_content += '<div class="screenshots">'
                
                if step.get('before_screenshot'):
                    html_content += f"""
            <div class="screenshot-container">
                <div class="screenshot-label">Before</div>
                <img class="screenshot" src="{step['before_screenshot']}" onclick="openModal(this.src)">
            </div>
"""
                
                if step.get('after_screenshot'):
                    html_content += f"""
            <div class="screenshot-container">
                <div class="screenshot-label">After</div>
                <img class="screenshot" src="{step['after_screenshot']}" onclick="openModal(this.src)">
            </div>
"""
                
                html_content += '</div>'
            
            html_content += '</div>'
            
        html_content += """
    <div id="imageModal" class="modal" onclick="closeModal()">
        <span class="close">&times;</span>
        <img class="modal-content" id="modalImage">
    </div>
    
    <script>
        function openModal(src) {
            var modal = document.getElementById('imageModal');
            var modalImg = document.getElementById('modalImage');
            modal.style.display = "block";
            modalImg.src = src;
        }
        
        function closeModal() {
            document.getElementById('imageModal').style.display = "none";
        }
    </script>
</body>
</html>
"""

        report_path = self.report_dir / "report.html"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"\nHTML report generated: {report_path}")
        
    # Wrapped Playwright methods that automatically log
    def goto(self, url: str, **kwargs):
        """Navigate to URL with logging"""
        try:
            result = self.page.goto(url, **kwargs)
            self._log_command(f"goto('{url}')", "goto", (url,), kwargs, result)
            # Wait for page to stabilize after navigation
            self._wait_for_page_stable()
            return result
        except Exception as e:
            self._log_command(f"goto('{url}')", "goto", (url,), kwargs, error=e)
            raise
            
    def _scroll_to_element(self, selector: str):
        """Scroll element into view before interacting with it"""
        try:
            # First check if element exists
            if self.page.locator(selector).count() > 0:
                # Scroll element into view using JavaScript
                self.page.evaluate("""
                    (selector) => {
                        const element = document.querySelector(selector);
                        if (element) {
                            element.scrollIntoView({
                                behavior: 'smooth',
                                block: 'center',
                                inline: 'center'
                            });
                        }
                    }
                """, selector)
                # Give a moment for smooth scroll to complete
                self.page.wait_for_timeout(300)
        except:
            # If scroll fails, continue anyway
            pass
            
    def _scroll_to_locator(self, locator):
        """Scroll locator element into view"""
        try:
            # Check if locator has any elements
            if locator.count() > 0:
                # Scroll the first element into view
                locator.first.evaluate("""
                    (element) => {
                        element.scrollIntoView({
                            behavior: 'smooth',
                            block: 'center',
                            inline: 'center'
                        });
                    }
                """)
                # Give a moment for smooth scroll to complete
                self.page.wait_for_timeout(300)
        except:
            # If scroll fails, continue anyway
            pass
            
    def _get_page_hash(self) -> str:
        """Calculate a hash of the current page state"""
        try:
            # Get page content including dynamic elements
            content = self.page.evaluate("""
                () => {
                    // Get HTML content
                    const html = document.documentElement.outerHTML;
                    // Get all input values
                    const inputs = Array.from(document.querySelectorAll('input, select, textarea')).map(el => ({
                        id: el.id || el.name || '',
                        value: el.value,
                        checked: el.checked,
                        selectedIndex: el.selectedIndex
                    }));
                    // Get visibility state of elements
                    const visibility = Array.from(document.querySelectorAll('*')).filter(el => {
                        const style = window.getComputedStyle(el);
                        return style.display === 'none' || style.visibility === 'hidden';
                    }).map(el => el.id || el.className || '');
                    
                    return JSON.stringify({
                        html: html.length,  // Use length to avoid huge strings
                        inputs: inputs,
                        visibility: visibility,
                        url: window.location.href,
                        scrollY: window.scrollY,
                        scrollX: window.scrollX
                    });
                }
            """)
            return hashlib.md5(content.encode()).hexdigest()
        except:
            # If hash calculation fails, return current timestamp
            return str(time.time())
            
    def _wait_for_page_stable(self, initial_hash: Optional[str] = None):
        """Wait for page to become stable by comparing hashes"""
        if initial_hash is None:
            initial_hash = self._get_page_hash()
            
        stable_count = 0
        stable_threshold = 3  # Page must be stable for 3 consecutive checks
        last_hash = initial_hash
        start_time = time.time()
        
        while (time.time() - start_time) * 1000 < self.max_wait_time:
            time.sleep(self.hash_check_interval / 1000)  # Convert to seconds
            current_hash = self._get_page_hash()
            
            if current_hash == last_hash:
                stable_count += 1
                if stable_count >= stable_threshold:
                    # Page has been stable, now wait 2 more seconds
                    time.sleep(2)
                    return
            else:
                stable_count = 0
                last_hash = current_hash
                
        # If we timeout, just continue
        time.sleep(2)  # Final 2 second wait
    
    def click(self, selector: str, **kwargs):
        """Click element with logging"""
        try:
            # Get initial page state
            initial_hash = self._get_page_hash()
            # Scroll to element first
            self._scroll_to_element(selector)
            self.page.click(selector, **kwargs)
            self._log_command(f"click('{selector}')", "click", (selector,), kwargs)
            # Wait for page to stabilize
            self._wait_for_page_stable(initial_hash)
        except Exception as e:
            self._log_command(f"click('{selector}')", "click", (selector,), kwargs, error=e)
            raise
            
    def fill(self, selector: str, value: str, **kwargs):
        """Fill input with logging"""
        try:
            # Get initial page state
            initial_hash = self._get_page_hash()
            # Scroll to element first
            self._scroll_to_element(selector)
            self.page.fill(selector, value, **kwargs)
            self._log_command(f"fill('{selector}', '{value}')", "fill", (selector, value), kwargs)
            # Wait for page to stabilize
            self._wait_for_page_stable(initial_hash)
        except Exception as e:
            self._log_command(f"fill('{selector}', '{value}')", "fill", (selector, value), kwargs, error=e)
            raise
            
    # Removed wait_for_timeout - use automatic hash-based waiting instead
            
    def wait_for_selector(self, selector: str, **kwargs):
        """Wait for selector with logging"""
        try:
            result = self.page.wait_for_selector(selector, **kwargs)
            self._log_command(f"wait_for_selector('{selector}')", "wait_for_selector", (selector,), kwargs, result)
            # Scroll to element after it appears
            self._scroll_to_element(selector)
            return result
        except Exception as e:
            self._log_command(f"wait_for_selector('{selector}')", "wait_for_selector", (selector,), kwargs, error=e)
            raise
            
    def locator(self, selector: str):
        """Get locator (not logged until action is performed)"""
        return self.page.locator(selector)
        
    def count(self, selector: str) -> int:
        """Count elements matching selector with logging"""
        try:
            count = self.page.locator(selector).count()
            self._log_command(f"count('{selector}')", "count", (selector,), {}, count)
            return count
        except Exception as e:
            self._log_command(f"count('{selector}')", "count", (selector,), {}, error=e)
            raise
        
    def evaluate(self, expression: str, *args):
        """Evaluate JavaScript with logging"""
        try:
            result = self.page.evaluate(expression, *args)
            self._log_command(f"evaluate('{expression[:50]}...')", "evaluate", (expression,), {}, result)
            return result
        except Exception as e:
            self._log_command(f"evaluate('{expression[:50]}...')", "evaluate", (expression,), {}, error=e)
            raise
            
    def screenshot(self, name: str, description: str = ""):
        """Take a screenshot with logging"""
        filename = self._take_screenshot(name, description)
        self._log_command(f"screenshot('{name}')", "screenshot", (name,), {"description": description}, filename)
        return filename
        
    def set_viewport_size(self, viewport: dict):
        """Set viewport size with logging"""
        try:
            self.page.set_viewport_size(viewport)
            self._log_command(f"set_viewport_size({viewport})", "set_viewport_size", (viewport,), {})
        except Exception as e:
            self._log_command(f"set_viewport_size({viewport})", "set_viewport_size", (viewport,), {}, error=e)
            raise
            
    def keyboard_press(self, key: str):
        """Press keyboard key with logging"""
        try:
            self.page.keyboard.press(key)
            self._log_command(f"keyboard.press('{key}')", "keyboard_press", (key,), {})
        except Exception as e:
            self._log_command(f"keyboard.press('{key}')", "keyboard_press", (key,), {}, error=e)
            raise
            
    def wait_for_stable(self):
        """Wait for page to become stable (for interactive debugging)"""
        try:
            self._wait_for_page_stable()
            self._log_command("wait_for_stable()", "wait_for_stable", (), {})
        except Exception as e:
            self._log_command("wait_for_stable()", "wait_for_stable", (), {}, error=e)
            raise
            
    def check(self, selector: str, **kwargs):
        """Check checkbox with logging"""
        try:
            # Get initial page state
            initial_hash = self._get_page_hash()
            # Scroll to element first
            self._scroll_to_element(selector)
            self.page.check(selector, **kwargs)
            self._log_command(f"check('{selector}')", "check", (selector,), kwargs)
            # Wait for page to stabilize
            self._wait_for_page_stable(initial_hash)
        except Exception as e:
            self._log_command(f"check('{selector}')", "check", (selector,), kwargs, error=e)
            raise
            
    def uncheck(self, selector: str, **kwargs):
        """Uncheck checkbox with logging"""
        try:
            # Get initial page state
            initial_hash = self._get_page_hash()
            # Scroll to element first
            self._scroll_to_element(selector)
            self.page.uncheck(selector, **kwargs)
            self._log_command(f"uncheck('{selector}')", "uncheck", (selector,), kwargs)
            # Wait for page to stabilize
            self._wait_for_page_stable(initial_hash)
        except Exception as e:
            self._log_command(f"uncheck('{selector}')", "uncheck", (selector,), kwargs, error=e)
            raise
            
    def get_by_role(self, role: str, **kwargs):
        """Get element by role with automatic interaction logging"""
        locator = self.page.get_by_role(role, **kwargs)
        return self._wrap_locator(locator, f"get_by_role('{role}', {kwargs})")
        
    def get_by_text(self, text: str, **kwargs):
        """Get element by text with automatic interaction logging"""
        locator = self.page.get_by_text(text, **kwargs)
        return self._wrap_locator(locator, f"get_by_text('{text}', {kwargs})")
        
    def get_by_label(self, text: str, **kwargs):
        """Get element by label with automatic interaction logging"""
        locator = self.page.get_by_label(text, **kwargs)
        return self._wrap_locator(locator, f"get_by_label('{text}', {kwargs})")
        
    def _wrap_locator(self, locator, description: str):
        """Wrap a locator to add automatic logging on interaction"""
        class LoggingLocator:
            def __init__(self, base_locator, base_instance, desc):
                self._locator = base_locator
                self._base = base_instance
                self._desc = desc
                
            def click(self, **kwargs):
                try:
                    initial_hash = self._base._get_page_hash()
                    self._base._scroll_to_locator(self._locator)
                    self._locator.click(**kwargs)
                    self._base._log_command(f"{self._desc}.click()", "click", (), kwargs)
                    self._base._wait_for_page_stable(initial_hash)
                except Exception as e:
                    self._base._log_command(f"{self._desc}.click()", "click", (), kwargs, error=e)
                    raise
                    
            def fill(self, value: str, **kwargs):
                try:
                    initial_hash = self._base._get_page_hash()
                    self._base._scroll_to_locator(self._locator)
                    self._locator.fill(value, **kwargs)
                    self._base._log_command(f"{self._desc}.fill('{value}')", "fill", (value,), kwargs)
                    self._base._wait_for_page_stable(initial_hash)
                except Exception as e:
                    self._base._log_command(f"{self._desc}.fill('{value}')", "fill", (value,), kwargs, error=e)
                    raise
                    
            def check(self, **kwargs):
                try:
                    initial_hash = self._base._get_page_hash()
                    self._base._scroll_to_locator(self._locator)
                    self._locator.check(**kwargs)
                    self._base._log_command(f"{self._desc}.check()", "check", (), kwargs)
                    self._base._wait_for_page_stable(initial_hash)
                except Exception as e:
                    self._base._log_command(f"{self._desc}.check()", "check", (), kwargs, error=e)
                    raise
                    
            def press(self, key: str, **kwargs):
                try:
                    self._locator.press(key, **kwargs)
                    self._base._log_command(f"{self._desc}.press('{key}')", "press", (key,), kwargs)
                except Exception as e:
                    self._base._log_command(f"{self._desc}.press('{key}')", "press", (key,), kwargs, error=e)
                    raise
                    
            def count(self):
                try:
                    count = self._locator.count()
                    self._base._log_command(f"{self._desc}.count()", "count", (), {}, count)
                    return count
                except Exception as e:
                    self._base._log_command(f"{self._desc}.count()", "count", (), {}, error=e)
                    raise
                    
            def first(self):
                return self._wrap_nth(0)
                
            def nth(self, index: int):
                return self._wrap_nth(index)
                
            def _wrap_nth(self, index: int):
                nth_locator = self._locator.nth(index)
                return self._base._wrap_locator(nth_locator, f"{self._desc}.nth({index})")
                
            def locator(self, selector: str):
                new_locator = self._locator.locator(selector)
                return self._base._wrap_locator(new_locator, f"{self._desc}.locator('{selector}')")
                
            def set_input_files(self, files, **kwargs):
                try:
                    initial_hash = self._base._get_page_hash()
                    self._locator.set_input_files(files, **kwargs)
                    files_str = files if isinstance(files, str) else ', '.join(files)
                    self._base._log_command(f"{self._desc}.set_input_files('{files_str}')", "set_input_files", (files,), kwargs)
                    self._base._wait_for_page_stable(initial_hash)
                except Exception as e:
                    files_str = files if isinstance(files, str) else ', '.join(files)
                    self._base._log_command(f"{self._desc}.set_input_files('{files_str}')", "set_input_files", (files,), kwargs, error=e)
                    raise
                
            # Delegate other methods to the original locator
            def __getattr__(self, name):
                return getattr(self._locator, name)
        
        return LoggingLocator(locator, self, description)
    
    def select_option(self, selector: str, value, **kwargs):
        """Select dropdown option with logging"""
        try:
            # Get initial page state
            initial_hash = self._get_page_hash()
            # Scroll to element first
            self._scroll_to_element(selector)
            self.page.select_option(selector, value, **kwargs)
            self._log_command(f"select_option('{selector}', {repr(value)})", "select_option", (selector, value), kwargs)
            # Wait for page to stabilize
            self._wait_for_page_stable(initial_hash)
        except Exception as e:
            self._log_command(f"select_option('{selector}', {repr(value)})", "select_option", (selector, value), kwargs, error=e)
            raise
            
    def type(self, selector: str, text: str, **kwargs):
        """Type text with logging"""
        try:
            # Scroll to element first
            self._scroll_to_element(selector)
            self.page.type(selector, text, **kwargs)
            self._log_command(f"type('{selector}', '{text}')", "type", (selector, text), kwargs)
        except Exception as e:
            self._log_command(f"type('{selector}', '{text}')", "type", (selector, text), kwargs, error=e)
            raise
            
    def hover(self, selector: str, **kwargs):
        """Hover over element with logging"""
        try:
            # Scroll to element first
            self._scroll_to_element(selector)
            self.page.hover(selector, **kwargs)
            self._log_command(f"hover('{selector}')", "hover", (selector,), kwargs)
        except Exception as e:
            self._log_command(f"hover('{selector}')", "hover", (selector,), kwargs, error=e)
            raise
            
    def set_input_files(self, selector: str, files, **kwargs):
        """Set input files with logging"""
        try:
            # Get initial page state
            initial_hash = self._get_page_hash()
            self.page.set_input_files(selector, files, **kwargs)
            files_str = files if isinstance(files, str) else ', '.join(files)
            self._log_command(f"set_input_files('{selector}', '{files_str}')", "set_input_files", (selector, files), kwargs)
            # Wait for page to stabilize
            self._wait_for_page_stable(initial_hash)
        except Exception as e:
            files_str = files if isinstance(files, str) else ', '.join(files)
            self._log_command(f"set_input_files('{selector}', '{files_str}')", "set_input_files", (selector, files), kwargs, error=e)
            raise
            
    def locator_click(self, locator_expression: str, index: int = 0):
        """Click on a locator element with logging and scrolling"""
        try:
            # Get initial page state
            initial_hash = self._get_page_hash()
            locator = self.page.locator(locator_expression)
            if index > 0:
                locator = locator.nth(index)
            # Scroll to the element
            self._scroll_to_locator(locator)
            locator.click()
            self._log_command(f"locator('{locator_expression}').nth({index}).click()", "locator_click", (locator_expression, index), {})
            # Wait for page to stabilize
            self._wait_for_page_stable(initial_hash)
        except Exception as e:
            self._log_command(f"locator('{locator_expression}').nth({index}).click()", "locator_click", (locator_expression, index), {}, error=e)
            raise
            
    def locator_fill(self, locator_expression: str, value: str, index: int = 0):
        """Fill a locator element with logging and scrolling"""
        try:
            # Get initial page state
            initial_hash = self._get_page_hash()
            locator = self.page.locator(locator_expression)
            if index > 0:
                locator = locator.nth(index)
            # Scroll to the element
            self._scroll_to_locator(locator)
            locator.fill(value)
            self._log_command(f"locator('{locator_expression}').nth({index}).fill('{value}')", "locator_fill", (locator_expression, value, index), {})
            # Wait for page to stabilize
            self._wait_for_page_stable(initial_hash)
        except Exception as e:
            self._log_command(f"locator('{locator_expression}').nth({index}).fill('{value}')", "locator_fill", (locator_expression, value, index), {}, error=e)
            raise
            
    def run_test(self):
        """Run the test (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement run_test()")
        
    def execute(self):
        """Execute the test with setup and teardown"""
        with sync_playwright() as p:
            try:
                # Setup
                self.setup_report_directory()
                
                # Initial log entry
                self.execution_log.append({
                    "step": 0,
                    "command": "Session initialized",
                    "timestamp": datetime.now().isoformat(),
                    "status": "INITIAL",
                    "output": "Browser started with Chromium"
                })
                
                # Launch browser
                self.browser = p.chromium.launch(
                    headless=False,
                    args=['--ignore-certificate-errors']
                )
                
                # Create context
                self.context = self.browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    ignore_https_errors=True
                )
                
                # Create page
                self.page = self.context.new_page()
                
                # Run the actual test
                self.run_test()
                
                print(f"\n{self.test_name} completed successfully!")
                
            except Exception as e:
                print(f"\n{self.test_name} failed with error: {e}")
                self.screenshot("error", "Test failed")
                raise
                
            finally:
                # Generate report
                self._generate_html_report()
                
                # Cleanup
                if self.context:
                    self.context.close()
                if self.browser:
                    self.browser.close()