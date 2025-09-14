#!/usr/bin/env python3
"""
Script to open Chromium for manual login to bolt.new
Run this in VNC session to create/update the logged-in profile
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
import time

profile_dir = Path('/git/buildyoursite/bolt-playwright/chromium-profile-linux')
profile_dir.mkdir(exist_ok=True)

print('Starting Chromium with persistent profile...')
print(f'Profile directory: {profile_dir}')
print('='*60)
print('Please log in to bolt.new manually in the browser')
print('When done, close the browser to save the session')
print('='*60)

with sync_playwright() as p:
    # Launch with GUI for manual login
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=False,  # Show browser window
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--start-maximized'
        ],
        ignore_https_errors=True,
        viewport={'width': 1920, 'height': 1080}
    )
    
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    # Navigate to bolt.new
    print('Navigating to bolt.new...')
    page.goto('https://bolt.new')
    
    print('\nBrowser opened. Please log in manually.')
    print('Press Ctrl+C or close the browser when done...')
    
    try:
        # Keep browser open until user closes it
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\nClosing browser and saving session...')
    
    browser.close()
    print('Session saved to:', profile_dir)
