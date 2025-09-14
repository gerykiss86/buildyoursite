#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
from pathlib import Path
import time

profile_dir = Path('/git/buildyoursite/bolt-playwright/chromium-profile-linux')
print(f'Using profile: {profile_dir}')
print('='*60)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir),
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox'],
        viewport={'width': 1920, 'height': 1080}
    )
    
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    print('Navigating to bolt.new...')
    page.goto('https://bolt.new')
    time.sleep(5)
    
    # Take screenshot
    page.screenshot(path='login_status.png')
    
    # Check for sign in button
    sign_in = page.locator('button:has-text("Sign in"):visible, button:has-text("Sign In"):visible').count()
    
    if sign_in > 0:
        print('? NOT LOGGED IN - Sign in button found')
    else:
        print('? SUCCESSFULLY LOGGED IN!')
        
        # Look for user menu or avatar
        user_indicators = [
            'button[aria-label*="user"]',
            'button[aria-label*="account"]',
            'button[aria-label*="menu"]',
            'img[alt*="avatar"]',
            '[data-testid*="user"]'
        ]
        
        for selector in user_indicators:
            if page.locator(selector).count() > 0:
                print(f'  ? Found user element: {selector}')
                break
    
    browser.close()
    print('='*60)
