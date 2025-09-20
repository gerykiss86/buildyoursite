#!/usr/bin/env python3
"""
Automated bolt.new site generator and exporter for Linux
Using the logged-in Chromium profile
"""

import os
import sys
import time
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Linux profile path - same as used in test-login-status.py
PROFILE_DIR = Path('/git/buildyoursite/bolt-playwright/chromium-profile-linux')

def wait_for_page_stable(page, timeout=3000, check_interval=500):
    """
    Wait for page to stabilize by checking content hash
    """
    stable_count = 0
    last_hash = ""
    max_checks = timeout // check_interval
    
    for _ in range(max_checks):
        try:
            # Get current page content hash
            content = page.content()
            current_hash = hashlib.md5(content.encode()).hexdigest()
            
            if current_hash == last_hash:
                stable_count += 1
                if stable_count >= 2:  # Page stable for 2 consecutive checks
                    return True
            else:
                stable_count = 0
                last_hash = current_hash
            
            page.wait_for_timeout(check_interval)
        except:
            pass
    
    return False

def generate_bolt_site(prompt, headless=True, output_dir="output"):
    """
    Generate and export a bolt.new site with the given prompt

    Args:
        prompt: The prompt to use for site generation
        headless: Whether to run in headless mode (default: True)
        output_dir: Directory to save downloads (default: "output")

    Returns:
        tuple: (success: bool, folder_path: str) - True if successful and the output folder path
    """

    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Create timestamped subfolder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    subfolder_name = f"bolt_{timestamp}"
    downloads_path = output_path / subfolder_name
    downloads_path.mkdir(exist_ok=True)
    downloads_path = downloads_path.absolute()
    
    with sync_playwright() as p:
        print(f"\n{'='*60}")
        print(f"Starting bolt.new site generation")
        print(f"Prompt: {prompt}")
        print(f"Using profile: {PROFILE_DIR}")
        print(f"{'='*60}\n")
        
        try:
            # Launch browser with persistent context
            print("Launching Chromium with persistent profile...")
            print(f"Downloads will be saved to: {downloads_path}")
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(PROFILE_DIR),
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-background-timer-throttling',
                    '--disable-renderer-backgrounding',
                    '--disable-features=TranslateUI',
                ],
                ignore_https_errors=True,
                timeout=60000,
                accept_downloads=True,
                downloads_path=str(downloads_path),
                viewport={'width': 1920, 'height': 1080}
            )
            
            # Get or create page
            pages = browser.pages
            if pages:
                page = pages[0]
            else:
                page = browser.new_page()
            
            # Navigate to bolt.new
            print("Step 1: Navigating to bolt.new...")
            page.goto("https://bolt.new", wait_until="domcontentloaded", timeout=60000)
            
            # Wait for page to stabilize
            print("Step 2: Waiting for page to stabilize...")
            wait_for_page_stable(page)
            
            # Check for "Not now" popup
            try:
                if page.locator('button:has-text("Not now")').is_visible():
                    print("  - Dismissing popup...")
                    page.locator('button:has-text("Not now")').click()
                    wait_for_page_stable(page)
            except:
                pass  # No popup, continue
            
            # Enter the prompt
            print("Step 3: Entering prompt...")
            textarea = page.locator('textarea')
            textarea.click()
            textarea.fill(prompt)
            
            # Submit the prompt
            print("Step 4: Submitting prompt...")
            textarea.press("Enter")
            
            # Use smart wait for page to stabilize after submission
            print("Step 5: Waiting for page to stabilize and checking for dialogs...")
            wait_for_page_stable(page)
            
            # Check for "Not now" popup that can appear after prompt submission
            try:
                if page.locator('button:has-text("Not now")').is_visible():
                    print("  - Dismissing 'Not now' popup...")
                    page.locator('button:has-text("Not now")').click()
                    wait_for_page_stable(page)
            except:
                pass
            
            # Wait for generation to complete
            print("Step 6: Waiting for AI to generate the site and preview to load...")
            
            # First wait for basic generation (at least 15 seconds)
            print("  - Initial generation phase...")
            page.wait_for_timeout(15000)
            
            # Now wait until "Your preview will appear here" disappears - no timeout, wait as long as needed
            print("  - Waiting for preview to load...")
            seconds_waited = 15
            
            while True:
                # Check if the preview placeholder text element still EXISTS in the DOM
                preview_placeholder = page.locator('div:has-text("Your preview will appear here")')
                element_count = preview_placeholder.count()
                
                if element_count > 0:
                    # Element still exists, preview not ready yet
                    if seconds_waited % 10 == 0:
                        print(f"    Still waiting for preview... ({seconds_waited}s elapsed)")
                    page.wait_for_timeout(1000)
                    seconds_waited += 1
                else:
                    # Element doesn't exist anymore, preview is loaded!
                    print(f"  - Preview loaded after {seconds_waited} seconds total!")
                    break
            
            # Final stabilization wait
            print("  - Waiting for page to stabilize...")
            wait_for_page_stable(page, timeout=5000)
            
            # Open project dropdown menu
            print("Step 7: Opening project menu...")
            # Try to find the project name button in the header
            project_buttons = page.locator('header button').all_text_contents()
            project_name = None
            for btn_text in project_buttons:
                if btn_text and btn_text not in ['View history', '', 'Integrations', 'Publish']:
                    project_name = btn_text
                    break
            
            if project_name:
                print(f"  - Found project: {project_name}")
                # Use first visible button with the project name to avoid duplicates
                page.locator(f'button:has-text("{project_name}"):visible').first.click()
            else:
                # Fallback: try clicking the second button in header
                print("  - Using fallback method to open dropdown...")
                page.locator('header button').nth(1).click()
            
            wait_for_page_stable(page)
            
            # Click Export option
            print("Step 8: Clicking Export option...")
            page.locator('[role="menuitem"]:has-text("Export")').click()
            wait_for_page_stable(page)
            
            # Click Download button and wait for download
            print("Step 9: Starting download...")
            
            # Get project name for filename
            project_name = "bolt_project"
            try:
                project_buttons = page.locator('header button').all_text_contents()
                for btn_text in project_buttons:
                    if btn_text and btn_text not in ['View history', '', 'Integrations', 'Publish']:
                        project_name = btn_text.replace(' ', '_').replace('/', '-')
                        break
            except:
                pass
            
            # Start waiting for download before clicking
            with page.expect_download() as download_info:
                page.locator('button:has-text("Download")').click()
                print("  - Download button clicked, waiting for file...")
            
            # Get the download object
            download = download_info.value
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{project_name}_{timestamp}.zip"
            save_path = downloads_path / filename
            
            # Save the download
            print(f"Step 10: Saving download as {filename}...")
            download.save_as(str(save_path))
            
            print(f"  - File saved to: {save_path}")

            print("\n[SUCCESS] Site generated and exported.")
            print(f"Output folder: {downloads_path}")
            print(f"{'='*60}\n")

            # Close browser
            browser.close()
            return True, str(downloads_path)
            
        except PlaywrightTimeoutError as e:
            print(f"\n[ERROR] Timeout error: {str(e)}")
            browser.close()
            return False, None

        except Exception as e:
            print(f"\n[ERROR] Error: {str(e)}")
            browser.close()
            return False, None

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate and export a bolt.new site automatically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Use default prompt (Tic-Tac-Toe game)
  %(prog)s "Create a todo list app"          # Custom prompt
  %(prog)s --headless "Build a calculator"   # Run in headless mode
        """
    )
    
    parser.add_argument(
        'prompt',
        nargs='?',
        default="Build a tic-tac-toe game with React",
        help='The prompt for site generation (default: "Build a tic-tac-toe game with React")'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run browser in headless mode (no visible window)'
    )
    
    parser.add_argument(
        '--output',
        default='output',
        help='Output directory for downloads (default: "output")'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print("\n" + "="*60)
    print("Bolt.new Site Generator (Linux)")
    print("="*60)
    
    # Generate the site
    success, folder_path = generate_bolt_site(args.prompt, args.headless, args.output)

    if success:
        print(f"\nGenerated site saved in: {folder_path}")

    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()