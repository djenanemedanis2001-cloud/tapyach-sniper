import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading
import sys
import os
import time
import random
import pandas as pd
from datetime import datetime

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class PrintRedirector:
    """Redirects stdout to a tkinter text widget."""
    def __init__(self, text_widget, app_instance):
        self.text_widget = text_widget
        self.app_instance = app_instance

    def write(self, string):
        # Schedule the update on the main thread
        self.app_instance.after(0, self._append_text, string)

    def _append_text(self, string):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", string)
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")

    def flush(self):
        pass

class BotWorker:
    """Handles the selenium bot logic."""
    def __init__(self, data_file, link, limit, rest_time):
        self.data_file = data_file
        self.link = link
        self.limit = int(limit)
        self.rest_time = int(rest_time)
        self.running = False
        self.driver = None

    def stop(self):
        """Signals the bot to stop."""
        self.running = False
        print("\n🛑 Stopping bot request received...")

    def run(self):
        self.running = True
        
        # --- 1. تحديد مكان ملف السجل ---
        current_folder = os.path.dirname(os.path.abspath(__file__))
        log_file_path = os.path.join(current_folder, "success_log.txt")
        
        if not os.path.exists(log_file_path):
            with open(log_file_path, "w", encoding="utf-8") as f:
                f.write(f"--- بداية السجل: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        
        print(f"\n📂 ملف التسجيل (Log) راهو هنا:\n👉 {log_file_path}")

        # --- 2. تحميل الداتا ---
        print(f"⏳ جاري تحميل {self.data_file}...")
        try:
            df = pd.read_csv(self.data_file)
            print(f"✅ تم تحميل {len(df)} طلبية.")
        except Exception as e:
            print(f"❌ خطأ في تحميل ملف البيانات: {e}")
            return

        if not self.running: return

        # --- 3. تشغيل المتصفح ---
        print("🚀 تشغيل المحرك...")
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        try:
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
             print(f"❌ Failed to start driver: {e}")
             return

        orders_counter = 0

        try:
            for index, row in df.iterrows():
                if not self.running:
                    break

                try:
                    print(f"\n=============================================")
                    print(f"📦 محاولة الطلب رقم [{index+1}] للزبون: {row['nom']}")
                    
                    self.driver.get(self.link)
                    
                    if self.driver.current_url != self.link:
                         print("⚠️ السيت رجعني للبداية! نعاود ندخل...")
                         self.driver.get(self.link)

                    # Chunked sleep for responsiveness
                    for _ in range(20): # 2 seconds total
                        if not self.running: break
                        time.sleep(0.1)
                    if not self.running: break

                    self.driver.execute_script("window.scrollTo(0, 600);")

                    # Filling forms
                    self.driver.find_element(By.NAME, "first_name").clear()
                    self.driver.find_element(By.NAME, "first_name").send_keys(row['nom'])
                    
                    self.driver.find_element(By.NAME, "phone").clear()
                    self.driver.find_element(By.NAME, "phone").send_keys(str(row['telephone']))
                    
                    self.driver.find_element(By.NAME, "city").clear()
                    self.driver.find_element(By.NAME, "city").send_keys(row['adresse'])

                    try:
                        self.driver.find_element(By.CSS_SELECTOR, ".product-option-item").click()
                        time.sleep(0.5)
                    except:
                        pass

                    if not self.running: break

                    # Submit
                    try:
                        submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button.single-submit")
                        self.driver.execute_script("arguments[0].click();", submit_btn)
                        print("🚀 كليكيت! جاري التحقق...")
                    except:
                        print("❌ الزر مالقيتوش!")

                    # Verification wait
                    for _ in range(40): # 4 seconds
                        if not self.running: break
                        time.sleep(0.1)

                    if not self.running: break

                    # Check success
                    is_success = False
                    if "thank_you" in self.driver.current_url or "success" in self.driver.current_url:
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"✅✅✅ كفو! الطلبية دخلت: {now}")
                        
                        with open(log_file_path, "a", encoding="utf-8") as log:
                            log.write(f"[{now}] ✅ OK: {row['nom']} | {row['telephone']}\n")
                        
                        is_success = True
                        orders_counter += 1
                    else:
                        print("⚠️ ما فاتتش (CAPTCHA أو Home Page Redirect).")

                    # Cleanup
                    self.driver.delete_all_cookies()
                    self.driver.execute_script("window.localStorage.clear();")
                    self.driver.execute_script("window.sessionStorage.clear();")

                    # Cool-down logic
                    if is_success and orders_counter > 0 and orders_counter % self.limit == 0:
                        print(f"\n🛑 كملنا {self.limit} طلبيات ناجحة.")
                        print(f"😴 استراحة لمدة {self.rest_time} دقيقة...")
                        
                        seconds = self.rest_time * 60
                        for i in range(seconds, 0, -1):
                            if not self.running: break
                            if i % 10 == 0 or i < 10: # Print every 10s or last 10s to avoid spam
                                print(f"⏳ باقي للعودة: {i} ثانية ...")
                            time.sleep(1)
                        print("\n🚀 صايي الوقت فات! عودة للعمل.")
                    else:
                        wait_t = random.randint(4, 7)
                        print(f"Waiting {wait_t} seconds...")
                        for _ in range(wait_t * 10):
                            if not self.running: break
                            time.sleep(0.1)

                except Exception as e:
                    print(f"❌ خطأ: {e}")
                    if self.driver:
                        self.driver.refresh()

        except Exception as e:
            print(f"❌ مشكل كبير: {e}")

        finally:
            print("👋 كملنا.")
            if self.driver:
                self.driver.quit()
                self.driver = None


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouCan Order Bot 3.0")
        self.geometry("700x650")
        
        # Grid layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1) # Log area expands

        # 1. Header
        self.header_label = ctk.CTkLabel(self, text="YouCan Order Bot 3.0", font=("Roboto", 24, "bold"))
        self.header_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # 2. File Selection
        self.file_frame = ctk.CTkFrame(self)
        self.file_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.select_file_btn = ctk.CTkButton(self.file_frame, text="Select Data File (CSV)", command=self.select_file)
        self.select_file_btn.pack(side="left", padx=10, pady=10)
        
        self.file_path_label = ctk.CTkLabel(self.file_frame, text="No file selected", text_color="gray")
        self.file_path_label.pack(side="left", padx=10, pady=10)
        self.file_path = None

        # 3. Settings Section
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.settings_frame.grid_columnconfigure(1, weight=1)

        # Product Link
        ctk.CTkLabel(self.settings_frame, text="Product Link:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.link_entry = ctk.CTkEntry(self.settings_frame, placeholder_text="https://...")
        self.link_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.link_entry.insert(0, "https://libyaworld.youcan.store/products/alsaaa-alrkmy-hsrya-fy-lybya")

        # Orders Limit
        ctk.CTkLabel(self.settings_frame, text="Orders Limit:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.limit_entry = ctk.CTkEntry(self.settings_frame)
        self.limit_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.limit_entry.insert(0, "2")

        # Rest Time
        ctk.CTkLabel(self.settings_frame, text="Rest Time (Min):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.rest_entry = ctk.CTkEntry(self.settings_frame)
        self.rest_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.rest_entry.insert(0, "5")

        # 4. Control Buttons
        self.controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.controls_frame.grid(row=3, column=0, padx=20, pady=10)

        self.start_btn = ctk.CTkButton(self.controls_frame, text="START", command=self.start_bot, 
                                       fg_color="green", hover_color="darkgreen", width=150, height=40)
        self.start_btn.pack(side="left", padx=10)

        self.stop_btn = ctk.CTkButton(self.controls_frame, text="STOP", command=self.stop_bot, 
                                      fg_color="red", hover_color="darkred", width=150, height=40, state="disabled")
        self.stop_btn.pack(side="left", padx=10)

        # 5. Status Label
        self.status_label = ctk.CTkLabel(self, text="Status: Idle", text_color="silver")
        self.status_label.grid(row=4, column=0, padx=20, pady=(5, 0))

        # 6. Console/Log Area
        self.log_box = ctk.CTkTextbox(self, font=("Consolas", 12))
        self.log_box.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.log_box.configure(state="disabled")

        # Redirect stdout
        sys.stdout = PrintRedirector(self.log_box, self)
        
        self.bot_worker = None
        self.bot_thread = None

    def select_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.file_path = filename
            self.file_path_label.configure(text=os.path.basename(filename), text_color="white")

    def start_bot(self):
        if not self.file_path:
            print("⚠️ Please select a CSV file first!")
            return
        
        link = self.link_entry.get()
        limit = self.limit_entry.get()
        rest = self.rest_entry.get()
        
        if not link or not limit or not rest:
             print("⚠️ Please fill all settings fields.")
             return

        self.toggle_inputs(False)
        self.status_label.configure(text="Status: Running", text_color="#00FF00")
        
        self.bot_worker = BotWorker(self.file_path, link, limit, rest)
        self.bot_thread = threading.Thread(target=self._run_wrapper, daemon=True)
        self.bot_thread.start()

    def _run_wrapper(self):
        self.bot_worker.run()
        # When finished (or stopped)
        self.after(0, self._on_bot_finished)

    def _on_bot_finished(self):
        self.toggle_inputs(True)
        self.status_label.configure(text="Status: Idle", text_color="silver")
        print("ℹ️ Process finished.")

    def stop_bot(self):
        if self.bot_worker:
            self.bot_worker.stop()
            self.status_label.configure(text="Status: Stopping...", text_color="orange")
            self.stop_btn.configure(state="disabled")

    def toggle_inputs(self, enable):
        state = "normal" if enable else "disabled"
        self.select_file_btn.configure(state=state)
        self.link_entry.configure(state=state)
        self.limit_entry.configure(state=state)
        self.rest_entry.configure(state=state)
        self.start_btn.configure(state=state)
        
        # Stop button is opposite
        self.stop_btn.configure(state="normal" if not enable else "disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()
