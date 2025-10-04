import asyncio
import aiohttp
import os
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import urllib.parse
from pathlib import Path

class ImageDownloader:
    def __init__(self, download_dir=None):
        if download_dir is None:
            # Default to backend/generateImages/downloaded_images folder
            self.download_dir = Path(__file__).parent / "downloaded_images"
        else:
            self.download_dir = Path(download_dir)
        
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.images = []  # Store objects: { src, position }
        self.SCROLL_STEP = 200
        self.MAX_SCROLL = 4000
        self.driver = None
        
    def setup_driver(self):
        """Setup Chrome WebDriver to connect to existing Chrome instance with remote debugging"""
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            print("✅ Connected to existing Chrome instance with remote debugging")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to Chrome with remote debugging: {e}")
            print("Make sure Chrome is running with: --remote-debugging-port=9222")
            print('Command: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\ChromeDebug"')
            return False
    
    async def delay(self, ms):
        """Async delay function similar to JavaScript setTimeout"""
        await asyncio.sleep(ms / 1000)
    
    def scroll_window_and_divs(self):
        """Scroll the window and all scrollable divs"""
        # Scroll the main window
        self.driver.execute_script(f"window.scrollBy({{top: {self.SCROLL_STEP}, behavior: 'smooth'}});")
        
        # Find and scroll all scrollable divs
        scrollable_divs = self.driver.execute_script("""
            return Array.from(document.querySelectorAll('div'))
                .filter(div => div.scrollHeight > div.clientHeight);
        """)
        
        for div in scrollable_divs:
            try:
                self.driver.execute_script(f"arguments[0].scrollTop += {self.SCROLL_STEP};", div)
            except Exception as e:
                # Some divs might not be scrollable anymore
                continue
    
    def collect_images_from_container(self, scrolled_position):
        """Collect images from the .PTre container"""
        try:
            container = self.driver.find_element(By.CSS_SELECTOR, '.PTre')
            imgs = container.find_elements(By.TAG_NAME, 'img')
            
            collected_count = 0
            for idx, img in enumerate(imgs):
                try:
                    src = img.get_attribute('src')
                    if src:
                        self.images.append({
                            'src': src,
                            'position': scrolled_position + idx
                        })
                        collected_count += 1
                except Exception as e:
                    continue
            
            print(f"📌 Scrolled to {scrolled_position}px, collected {collected_count} images so far")
            return collected_count
            
        except NoSuchElementException:
            print(f"⚠️ Container '.PTre' not found at scroll position {scrolled_position}")
            return 0
    
    async def scroll_and_collect(self, url=None):
        """Main function to scroll through page and collect images"""
        if not self.setup_driver():
            return False
        
        try:
            if url:
                print(f"🌐 Loading URL: {url}")
                self.driver.get(url)
                # Wait for page to load
                await self.delay(2000)
            else:
                print("🌐 Using current page in existing Chrome session")
                print(f"📍 Current URL: {self.driver.current_url}")
            
            # 1️⃣ Scroll in chunks and collect images
            for scrolled in range(0, self.MAX_SCROLL + self.SCROLL_STEP, self.SCROLL_STEP):
                # Scroll the window and divs
                self.scroll_window_and_divs()
                
                # Wait for images to load
                await self.delay(800)
                
                # Collect images from container
                self.collect_images_from_container(scrolled)
            
            return True
            
        except Exception as e:
            print(f"❌ Error during scrolling and collection: {e}")
            return False
        finally:
            # Don't quit the driver since we're using an existing Chrome session
            print("🔗 Keeping Chrome session open (not closing browser)")
            pass
    
    def remove_duplicates_and_sort(self):
        """Remove duplicates and sort by position"""
        # 2️⃣ Remove duplicates and sort by position
        unique_images_map = {}
        for img in self.images:
            if img['src'] not in unique_images_map:
                unique_images_map[img['src']] = img['position']
        
        unique_images = [
            {'src': src, 'position': position} 
            for src, position in unique_images_map.items()
        ]
        
        # Sort by position
        unique_images.sort(key=lambda x: x['position'])
        
        print(f"🗂 Total unique images: {len(unique_images)}")
        
        # 3️⃣ Print unique image links in order
        for i, img in enumerate(unique_images):
            print(f"{i + 1}: {img['src']}")
        
        return unique_images
    
    def download_image_via_browser(self, src, filename):
        """Download a single image using browser JavaScript (converts blob to base64)"""
        try:
            # JavaScript code compatible with older browsers and Selenium
            script = f"""
            var callback = arguments[arguments.length - 1];
            
            fetch('{src}')
                .then(function(response) {{
                    return response.blob();
                }})
                .then(function(blob) {{
                    var reader = new FileReader();
                    reader.onloadend = function() {{
                        callback(reader.result);
                    }};
                    reader.onerror = function() {{
                        callback('ERROR: Failed to read blob');
                    }};
                    reader.readAsDataURL(blob);
                }})
                .catch(function(error) {{
                    callback('ERROR: ' + error.message);
                }});
            """
            
            # Execute the script to get base64 data
            base64_data = self.driver.execute_async_script(script)
            
            if base64_data and not base64_data.startswith('ERROR:'):
                # Remove the data URL prefix (e.g., "data:image/png;base64,")
                if ',' in base64_data:
                    base64_content = base64_data.split(',', 1)[1]
                    
                    # Decode and save the image
                    image_data = base64.b64decode(base64_content)
                    
                    filepath = self.download_dir / filename
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    
                    print(f"💾 Downloaded {filename}")
                    return True
                else:
                    print(f"⚠️ Invalid base64 data for {src}")
                    return False
            else:
                error_msg = base64_data if base64_data else "Unknown error"
                print(f"⚠️ Failed to download {src}: {error_msg}")
                return False
                
        except Exception as e:
            print(f"⚠️ Failed to download {src}: {e}")
            return False
    
    async def download_all_images(self, unique_images):
        """Download all unique images using browser JavaScript"""
        if not unique_images:
            print("❌ No images to download")
            return
        
        print(f"🚀 Starting download of {len(unique_images)} images...")
        print(f"📁 Saving directly to: {self.download_dir.absolute()}")
        
        for i, img in enumerate(unique_images):
            src = img['src']
            
            # Generate filename with .png extension for consistency with creator
            filename = f"image_{i + 1}.png"
            
            # Download image using browser
            self.download_image_via_browser(src, filename)
            
            # Delay between downloads
            await self.delay(300)
        
        print(f"✅ Download complete! Images saved to: {self.download_dir.absolute()}")

async def main():
    """Main async function"""
    print("🔗 Connecting to existing Chrome session...")
    print("Make sure Chrome is running with:")
    print('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\ChromeDebug"')
    print()
    
    # Ask user if they want to navigate to a new URL or use current page
    choice = input("Use current page in Chrome (c) or navigate to new URL (n)? [c/n]: ").strip().lower()
    
    url = None
    if choice == 'n':
        url = input("Enter the URL to navigate to: ").strip()
        if not url:
            print("❌ Please provide a valid URL")
            return
    
    # Create downloader instance
    downloader = ImageDownloader()
    
    # Scroll and collect images
    success = await downloader.scroll_and_collect(url)
    
    if not success:
        print("❌ Failed to collect images")
        return
    
    # Remove duplicates and sort
    unique_images = downloader.remove_duplicates_and_sort()
    
    if not unique_images:
        print("❌ No images found")
        return
    
    # Ask user if they want to download
    download_choice = input(f"\nFound {len(unique_images)} unique images. Download them? (y/n): ").strip().lower()
    
    if download_choice in ['y', 'yes']:
        await downloader.download_all_images(unique_images)
    else:
        print("📋 Image collection complete. Download skipped.")

if __name__ == "__main__":
    print("🚀 Image Downloader Script")
    print("=" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Script interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
