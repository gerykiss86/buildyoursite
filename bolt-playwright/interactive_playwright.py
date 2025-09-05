"""
Interactive Playwright debugger using the test base class
Execute Playwright commands one at a time by editing command_to_feed.txt
Includes automatic logging, screenshots, and HTML report generation
Now with persistent session support for stored credentials
"""

import os
import sys
import time
import json
import shutil
from datetime import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_base import PlaywrightTestBase

# Set browser path - check common locations
if 'PLAYWRIGHT_BROWSERS_PATH' not in os.environ:
    # Try user's AppData first
    ms_playwright = os.path.expanduser(r'~\AppData\Local\ms-playwright')
    if os.path.exists(ms_playwright):
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = ms_playwright
    else:
        # Try local browsers folder
        local_browsers = os.path.join('playwright-env', 'browsers')
        if os.path.exists(local_browsers):
            os.environ['PLAYWRIGHT_BROWSERS_PATH'] = local_browsers


class InteractivePlaywright(PlaywrightTestBase):
    """Interactive debugger with automatic reporting and persistent session support"""
    
    def __init__(self, use_persistent_session=True):
        super().__init__("interactive_debug")
        self.command_file = Path("command_to_feed.txt")
        self.last_command = None
        self.command_history = []
        self.manual_screenshots = 0
        self.use_persistent_session = use_persistent_session
        
        # Profile paths for persistent session
        self.chrome_user_data = r"C:\Users\info\AppData\Local\Google\Chrome\User Data"
        self.chromium_user_data = r"C:\Users\info\chromium-playwright-profile"
        
    def setup_persistent_profile(self):
        """Setup Chromium profile with Chrome's saved data"""
        if not self.use_persistent_session:
            return
            
        print("Setting up Chromium with Chrome profile data...")
        
        # Create chromium profile directory if it doesn't exist
        if not os.path.exists(self.chromium_user_data):
            os.makedirs(self.chromium_user_data)
        
        # Copy the Default profile directory structure
        default_src = os.path.join(self.chrome_user_data, "Default")
        default_dst = os.path.join(self.chromium_user_data, "Default")
        
        if not os.path.exists(default_dst):
            print("Creating initial profile copy (this may take a moment)...")
            try:
                shutil.copytree(default_src, default_dst)
            except Exception as e:
                print(f"Warning during copy: {e}")
            
            # Also copy Local State for account info
            local_state_src = os.path.join(self.chrome_user_data, "Local State")
            local_state_dst = os.path.join(self.chromium_user_data, "Local State")
            if os.path.exists(local_state_src):
                try:
                    shutil.copy2(local_state_src, local_state_dst)
                except Exception as e:
                    print(f"Warning copying Local State: {e}")
            print("✓ Profile copy complete")
        else:
            print("✓ Using existing Chromium profile")
    
    def setup_interactive_session(self):
        """Setup interactive session files"""
        # Setup persistent profile if enabled
        if self.use_persistent_session:
            self.setup_persistent_profile()
            
        # Create or clear command file
        self.command_file.write_text("# Interactive Playwright Session\n# Edit this file and save to execute commands\n# Last non-comment line will be executed\n\n")
        
        # Setup report directory (from base class)
        self.setup_report_directory()
        
        # Initialize command output log
        self.command_log_path = self.report_dir / "command_output.log"
        with open(self.command_log_path, 'w', encoding='utf-8') as log_file:
            log_file.write(f"Interactive Playwright Session - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            if self.use_persistent_session:
                log_file.write("Using persistent session with stored credentials\n")
            log_file.write("="*80 + "\n\n")
            
        print(f"\nSession directory: {self.report_dir}")
        print(f"Command file: {self.command_file}")
        if self.use_persistent_session:
            print("✓ Persistent session enabled - your cookies and credentials are available")
        print("\nEdit command_to_feed.txt and save to execute commands.")
        print("Type 'exit()' to quit.\n")
        
    def log_output(self, output):
        """Log output to file and console"""
        print(output)
        with open(self.command_log_path, 'a', encoding='utf-8') as log_file:
            log_file.write(output + "\n")
            
    def read_command(self):
        """Read the last non-comment line from command file"""
        try:
            with open(self.command_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Find last non-empty, non-comment line
            for line in reversed(lines):
                line = line.strip()
                if line and not line.startswith('#'):
                    return line
                    
        except Exception as e:
            self.log_output(f"Error reading command file: {e}")
            
        return None
        
    def execute_command(self, command):
        """Execute a command and handle errors"""
        try:
            # Special handling for common commands
            if command == "exit()":
                return False
                
            elif command.startswith("screenshot("):
                # Extract screenshot name if provided
                import re
                match = re.match(r'screenshot\((.*?)\)', command)
                if match and match.group(1):
                    name = match.group(1).strip('"\'')
                else:
                    self.manual_screenshots += 1
                    name = f"manual_{self.manual_screenshots}"
                    
                filename = self.screenshot(name, f"Manual screenshot: {name}")
                self.log_output(f"Screenshot saved: {filename}")
                
            elif command == "wait()" or command == "wait_for_stable()":
                # Use hash-based waiting
                self.wait_for_stable()
                self.log_output("Page stabilized")
                
            elif command.startswith("wait("):
                # Parse wait time (for backwards compatibility in interactive mode only)
                import re
                match = re.match(r'wait\((\d+)\)', command)
                if match:
                    # Just use wait_for_stable instead
                    self.wait_for_stable()
                    self.log_output(f"Page stabilized (requested {match.group(1)}ms wait)")
                    
            elif command.startswith("page."):
                # Direct page commands - execute and log
                method = command[5:].split('(')[0]
                result = eval(f"self.{command}")
                self.log_output(f"Executed: {command}")
                if result is not None:
                    self.log_output(f"Result: {result}")
                    
            else:
                # Try to execute as a method on self (which wraps page methods)
                result = eval(f"self.{command}")
                if result is not None:
                    self.log_output(f"Result: {result}")
                    
            return True
            
        except PlaywrightTimeoutError as e:
            self.log_output(f"Timeout Error: {str(e)}")
            error_screenshot = self.screenshot("timeout_error", "Timeout error occurred")
            self.log_output(f"Error screenshot: {error_screenshot}")
            return True
            
        except Exception as e:
            self.log_output(f"Error executing command: {type(e).__name__}: {str(e)}")
            error_screenshot = self.screenshot("error", "Error occurred")
            self.log_output(f"Error screenshot: {error_screenshot}")
            return True
            
    def run_interactive(self):
        """Run the interactive session"""
        self.setup_interactive_session()
        
        # Use the base class execute method to setup browser
        with sync_playwright() as p:
            try:
                if self.use_persistent_session:
                    # Use persistent context with saved credentials
                    print("Launching Chromium with persistent profile...")
                    self.browser = p.chromium.launch_persistent_context(
                        user_data_dir=self.chromium_user_data,
                        headless=False,
                        args=[
                            '--disable-blink-features=AutomationControlled',
                            '--start-maximized',
                            '--enable-features=SyncDisabled',
                            '--disable-background-timer-throttling',
                            '--disable-renderer-backgrounding',
                            '--disable-features=TranslateUI',
                            '--password-store=basic',
                            '--ignore-certificate-errors'
                        ],
                        ignore_https_errors=True,
                        timeout=60000,
                        accept_downloads=True,
                        viewport={'width': 1920, 'height': 1080}
                    )
                    
                    # Get the default page from persistent context
                    pages = self.browser.pages
                    if pages:
                        self.page = pages[0]
                    else:
                        self.page = self.browser.new_page()
                    
                    # The browser itself acts as the context in persistent mode
                    self.context = self.browser
                    
                else:
                    # Regular non-persistent browser
                    self.browser = p.chromium.launch(
                        headless=False,
                        args=['--ignore-certificate-errors']
                    )
                    
                    self.context = self.browser.new_context(
                        viewport={'width': 1920, 'height': 1080},
                        ignore_https_errors=True
                    )
                    
                    self.page = self.context.new_page()
                
                # Take initial screenshot
                initial_screenshot = self.screenshot("initial", "Session started")
                self.log_output(f"Initial screenshot: {initial_screenshot}")
                
                # Main interactive loop
                while True:
                    try:
                        # Check for new command
                        command = self.read_command()
                        
                        if command and command != self.last_command:
                            self.last_command = command
                            self.command_history.append(command)
                            
                            self.log_output(f"\n[{datetime.now().strftime('%H:%M:%S')}] Executing: {command}")
                            
                            if not self.execute_command(command):
                                break
                                
                        time.sleep(0.5)  # Check for new commands every 500ms
                        
                    except KeyboardInterrupt:
                        self.log_output("\nSession interrupted by user")
                        break
                        
            except Exception as e:
                self.log_output(f"Fatal error: {e}")
                
            finally:
                # Generate HTML report
                self._generate_html_report()
                
                # Cleanup
                if self.use_persistent_session:
                    # For persistent context, only close browser
                    if self.browser:
                        self.browser.close()
                else:
                    # For regular context, close both
                    if self.context:
                        self.context.close()
                    if self.browser:
                        self.browser.close()
                    
                self.log_output("\nSession ended")
                print(f"\nHTML report generated: {self.report_dir / 'report.html'}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Interactive Playwright debugger with optional persistent session")
    parser.add_argument('--no-persist', action='store_true', 
                        help='Disable persistent session (use regular browser without saved credentials)')
    args = parser.parse_args()
    
    # Create session with or without persistence
    use_persistent = not args.no_persist
    session = InteractivePlaywright(use_persistent_session=use_persistent)
    
    if use_persistent:
        print("🔐 Starting interactive session with persistent profile (credentials saved)")
        print("   Use --no-persist flag to disable persistent session\n")
    else:
        print("Starting interactive session without persistent profile")
        print("   Remove --no-persist flag to enable credential storage\n")
    
    session.run_interactive()


if __name__ == "__main__":
    main()