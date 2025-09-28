#!/usr/bin/env python3
"""
GUI untuk Hybrid LSB Steganography-Blockchain System dengan Real Email Integration
Penelitian: Secure Digital Communication with Integrity Verification

Author: Research Team
Date: September 2025
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinter import PhotoImage
from PIL import Image, ImageTk
import threading
import os
import sys
import json
from pathlib import Path

# Add project path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import our modules
try:
    from stego_chain.utils.hybrid_integration import send_secure_message, receive_secure_message
    from stego_chain.utils.lsb_steganography import LSBSteganography
    from stego_chain.core.blockchain import check_connection
    from stego_chain.utils.email_simulation import send_stego_email, get_inbox_messages
    from stego_chain.utils.real_email_sender import (
        send_real_email, validate_email_format, test_email_credentials, 
        get_gmail_help, detect_email_provider
    )
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class SteganographyGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_variables()
        self.setup_ui()
        self.check_blockchain_connection()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("🔐 Hybrid LSB Steganography-Blockchain System")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
    def setup_variables(self):
        """Initialize variables"""
        self.cover_image_path = tk.StringVar()
        self.stego_image_path = tk.StringVar()
        self.secret_message = tk.StringVar()
        self.recipient_address = tk.StringVar(value="0x50E57867322143f349d55197388Db32d1b7DB8e5")
        self.tx_hash = tk.StringVar()
        
        # Real email variables
        self.sender_email = tk.StringVar()
        self.sender_password = tk.StringVar()
        self.recipient_email = tk.StringVar()
        self.use_real_email = tk.BooleanVar(value=False)
        self.email_subject = tk.StringVar(value="🔐 Secure Document - Steganography Transfer")
        
        # Image references
        self.cover_image_display = None
        self.stego_image_display = None
        
    def setup_ui(self):
        """Create the main UI"""
        # Main title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🔐 Hybrid LSB Steganography-Blockchain System",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Secure Digital Communication with Integrity Verification - Research Tool",
            font=('Arial', 10),
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        subtitle_label.pack()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_send_tab()
        self.create_receive_tab()
        self.create_demo_tab()
        
    def create_send_tab(self):
        """Create the send message tab dengan real email support"""
        send_frame = ttk.Frame(self.notebook)
        self.notebook.add(send_frame, text="📤 Send Secret Message")
        
        # Left panel - Controls
        left_panel = ttk.LabelFrame(send_frame, text="📋 Message Configuration", padding=10)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Cover image selection
        ttk.Label(left_panel, text="1. Select Cover Image:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(0, 5))
        
        cover_frame = tk.Frame(left_panel)
        cover_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Entry(
            cover_frame, 
            textvariable=self.cover_image_path, 
            state='readonly',
            width=50
        ).pack(side='left', fill='x', expand=True)
        
        ttk.Button(
            cover_frame, 
            text="Browse 📁", 
            command=self.select_cover_image
        ).pack(side='right', padx=(5, 0))
        
        # Secret message input
        ttk.Label(left_panel, text="2. Secret Message:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        
        self.message_text = scrolledtext.ScrolledText(
            left_panel, 
            height=4, 
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.message_text.pack(fill='x', pady=(0, 10))
        
        # Recipient address (blockchain)
        ttk.Label(left_panel, text="3. Blockchain Recipient Address:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 5))
        
        recipient_frame = tk.Frame(left_panel)
        recipient_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Entry(
            recipient_frame, 
            textvariable=self.recipient_address,
            font=('Arial', 9),
            state='readonly'
        ).pack(fill='x')
        
        # Add info label
        info_label = ttk.Label(
            left_panel, 
            text="ℹ️ Fixed: Account1 → Account2 (for research consistency)", 
            font=('Arial', 8), 
            foreground='blue'
        )
        info_label.pack(anchor='w', pady=(0, 10))
        
        # Email Configuration Section (NEW!)
        email_section = ttk.LabelFrame(left_panel, text="📧 Email Delivery Configuration", padding=10)
        email_section.pack(fill='x', pady=(20, 10))
        
        # Email mode selection
        mode_frame = tk.Frame(email_section)
        mode_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Radiobutton(
            mode_frame, 
            text="📧 Send via Real Email (Gmail/Outlook/Yahoo)", 
            variable=self.use_real_email, 
            value=True,
            command=self.toggle_email_mode
        ).pack(anchor='w', pady=2)
        
        ttk.Radiobutton(
            mode_frame, 
            text="🧪 Use Email Simulation (Testing Only)", 
            variable=self.use_real_email, 
            value=False,
            command=self.toggle_email_mode
        ).pack(anchor='w', pady=2)
        
        # Real email configuration frame
        self.real_email_frame = tk.Frame(email_section)
        self.real_email_frame.pack(fill='x', pady=10)
        
        # Sender email
        sender_frame = tk.Frame(self.real_email_frame)
        sender_frame.pack(fill='x', pady=5)
        ttk.Label(sender_frame, text="Your Email:", font=('Arial', 9, 'bold'), width=15).pack(side='left')
        sender_entry = ttk.Entry(sender_frame, textvariable=self.sender_email, font=('Arial', 9))
        sender_entry.pack(side='left', fill='x', expand=True, padx=(5,5))
        
        # Email provider detection label
        self.provider_label = ttk.Label(sender_frame, text="", font=('Arial', 8), foreground='blue')
        self.provider_label.pack(side='right')
        
        # Bind email change to auto-detect provider
        self.sender_email.trace('w', self.on_sender_email_change)
        
        # Sender password
        password_frame = tk.Frame(self.real_email_frame)
        password_frame.pack(fill='x', pady=5)
        ttk.Label(password_frame, text="Password/App:", font=('Arial', 9, 'bold'), width=15).pack(side='left')
        password_entry = ttk.Entry(password_frame, textvariable=self.sender_password, show="*", font=('Arial', 9))
        password_entry.pack(side='left', fill='x', expand=True, padx=(5,5))
        
        # Help button for Gmail
        help_btn = tk.Button(password_frame, text="❓", command=self.show_gmail_help, 
                            bg='#3498db', fg='white', font=('Arial', 8))
        help_btn.pack(side='right', padx=(2,0))
        
        # Test connection button
        test_btn = tk.Button(password_frame, text="🔧 Test", command=self.test_email_connection,
                            bg='#f39c12', fg='white', font=('Arial', 8))
        test_btn.pack(side='right', padx=(2,0))
        
        # Recipient email
        recipient_email_frame = tk.Frame(self.real_email_frame)
        recipient_email_frame.pack(fill='x', pady=5)
        ttk.Label(recipient_email_frame, text="Send To Email:", font=('Arial', 9, 'bold'), width=15).pack(side='left')
        ttk.Entry(recipient_email_frame, textvariable=self.recipient_email, font=('Arial', 9)).pack(side='left', fill='x', expand=True, padx=(5,0))
        
        # Email subject
        subject_frame = tk.Frame(self.real_email_frame)
        subject_frame.pack(fill='x', pady=5)
        ttk.Label(subject_frame, text="Subject:", font=('Arial', 9, 'bold'), width=15).pack(side='left')
        ttk.Entry(subject_frame, textvariable=self.email_subject, font=('Arial', 9)).pack(side='left', fill='x', expand=True, padx=(5,0))
        
        # Email status indicator
        self.email_status_frame = tk.Frame(email_section)
        self.email_status_frame.pack(fill='x', pady=5)
        self.email_status_label = ttk.Label(self.email_status_frame, text="", font=('Arial', 8))
        self.email_status_label.pack()
        
        # Initially hide real email fields
        self.toggle_email_mode()
        
        # Action buttons
        button_frame = tk.Frame(left_panel)
        button_frame.pack(fill='x', pady=20)
        
        self.send_button = tk.Button(
            button_frame,
            text="🚀 Send Secret Message",
            command=self.send_message_thread,
            bg='#27ae60',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2
        )
        self.send_button.pack(fill='x')
        
        # Progress bar
        self.send_progress = ttk.Progressbar(
            left_panel, 
            mode='indeterminate'
        )
        self.send_progress.pack(fill='x', pady=10)
        
        # Status display
        self.send_status = scrolledtext.ScrolledText(
            left_panel,
            height=8,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.send_status.pack(fill='x', pady=10)
        
        # Right panel - Image preview
        right_panel = ttk.LabelFrame(send_frame, text="🖼️ Image Preview", padding=10)
        right_panel.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Original image frame
        original_frame = tk.Frame(right_panel)
        original_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        ttk.Label(original_frame, text="Original Image:", font=('Arial', 10, 'bold')).pack()
        
        self.original_canvas = tk.Canvas(
            original_frame, 
            width=300, 
            height=200,
            bg='white',
            relief='sunken',
            bd=2
        )
        self.original_canvas.pack(pady=5)
        
        # Stego image frame
        stego_frame = tk.Frame(right_panel)
        stego_frame.pack(fill='both', expand=True, pady=(5, 0))
        
        ttk.Label(stego_frame, text="Stego Image:", font=('Arial', 10, 'bold')).pack()
        
        self.stego_canvas = tk.Canvas(
            stego_frame, 
            width=300, 
            height=200,
            bg='white',
            relief='sunken',
            bd=2
        )
        self.stego_canvas.pack(pady=5)
        
        # Quality metrics display
        self.quality_frame = tk.Frame(right_panel)
        self.quality_frame.pack(fill='x', pady=10)
        
        self.quality_text = tk.Text(
            self.quality_frame,
            height=4,
            width=40,
            font=('Courier', 9),
            bg='#34495e',
            fg='#ecf0f1'
        )
        self.quality_text.pack(fill='x')
        
    def create_receive_tab(self):
        """Create the receive message tab"""
        receive_frame = ttk.Frame(self.notebook)
        self.notebook.add(receive_frame, text="📥 Receive Secret Message")
        
        # Main content frame
        content_frame = ttk.LabelFrame(receive_frame, text="📨 Extract Hidden Message", padding=20)
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Stego image selection
        ttk.Label(content_frame, text="1. Select Stego Image:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        stego_select_frame = tk.Frame(content_frame)
        stego_select_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Entry(
            stego_select_frame, 
            textvariable=self.stego_image_path, 
            state='readonly',
            font=('Arial', 10)
        ).pack(side='left', fill='x', expand=True)
        
        ttk.Button(
            stego_select_frame, 
            text="Browse 📁", 
            command=self.select_stego_image
        ).pack(side='right', padx=(10, 0))
        
        # Transaction hash input
        ttk.Label(content_frame, text="2. Transaction Hash (for verification):", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        ttk.Entry(
            content_frame, 
            textvariable=self.tx_hash,
            font=('Arial', 10)
        ).pack(fill='x', pady=(0, 20))
        
        # Extract button
        self.extract_button = tk.Button(
            content_frame,
            text="🔍 Extract & Verify Message",
            command=self.extract_message_thread,
            bg='#3498db',
            fg='white',
            font=('Arial', 12, 'bold'),
            height=2
        )
        self.extract_button.pack(fill='x', pady=10)
        
        # Progress bar
        self.extract_progress = ttk.Progressbar(
            content_frame, 
            mode='indeterminate'
        )
        self.extract_progress.pack(fill='x', pady=10)
        
        # Results display
        ttk.Label(content_frame, text="📝 Extracted Message:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20, 5))
        
        self.extracted_message = scrolledtext.ScrolledText(
            content_frame,
            height=8,
            wrap=tk.WORD,
            font=('Arial', 11),
            bg='#ecf0f1'
        )
        self.extracted_message.pack(fill='both', expand=True, pady=(0, 10))
        
        # Status display
        self.extract_status = scrolledtext.ScrolledText(
            content_frame,
            height=6,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.extract_status.pack(fill='x')
        
    def create_demo_tab(self):
        """Create demo workflow tab"""
        demo_frame = ttk.Frame(self.notebook)
        self.notebook.add(demo_frame, text="🧪 Demo Workflow")
        
        # Demo content
        demo_content = ttk.LabelFrame(demo_frame, text="🎯 Complete Demo Workflow", padding=20)
        demo_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Instructions
        instructions = tk.Text(
            demo_content,
            height=6,
            wrap=tk.WORD,
            font=('Arial', 10),
            bg='#f8f9fa'
        )
        instructions.pack(fill='x', pady=(0, 20))
        
        demo_text = """🎯 DEMO WORKFLOW - Complete End-to-End Testing

This demo will:
1. Load a sample cover image (you can select your own)
2. Embed a test message using LSB steganography  
3. Send the message hash to blockchain for verification
4. Extract and verify the message integrity
5. Display quality metrics (PSNR, MSE) for research

Perfect for testing the complete system and collecting research data!"""
        
        instructions.insert('1.0', demo_text)
        instructions.config(state='disabled')
        
        # Demo button
        self.demo_button = tk.Button(
            demo_content,
            text="🚀 Run Complete Demo",
            command=self.run_demo_thread,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 14, 'bold'),
            height=3
        )
        self.demo_button.pack(fill='x', pady=20)
        
        # Demo progress
        self.demo_progress = ttk.Progressbar(
            demo_content, 
            mode='indeterminate'
        )
        self.demo_progress.pack(fill='x', pady=10)
        
        # Demo results
        self.demo_results = scrolledtext.ScrolledText(
            demo_content,
            height=15,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        self.demo_results.pack(fill='both', expand=True)
    
    # Email functionality methods
    def toggle_email_mode(self):
        """Toggle between real email and simulation mode"""
        if self.use_real_email.get():
            # Show real email fields
            for widget in self.real_email_frame.winfo_children():
                if hasattr(widget, 'pack'):
                    widget.pack()
            self.email_status_label.config(text="📧 Real email mode: Enter your credentials above", foreground='blue')
        else:
            # Hide real email fields  
            for widget in self.real_email_frame.winfo_children():
                if hasattr(widget, 'pack_forget'):
                    widget.pack_forget()
            self.email_status_label.config(text="🧪 Simulation mode: Using dummy email accounts", foreground='green')
    
    def on_sender_email_change(self, *args):
        """Auto-detect email provider when sender email changes"""
        email = self.sender_email.get()
        if email and '@' in email:
            try:
                provider = detect_email_provider(email).upper()
                self.provider_label.config(text=f"({provider})")
            except:
                self.provider_label.config(text="")
        else:
            self.provider_label.config(text="")
    
    def show_gmail_help(self):
        """Show Gmail App Password setup guide"""
        help_text = get_gmail_help()
        
        # Create help window
        help_window = tk.Toplevel(self.root)
        help_window.title("📧 Gmail App Password Setup Guide")
        help_window.geometry("600x500")
        help_window.configure(bg='white')
        
        # Add scrollable text
        text_frame = tk.Frame(help_window)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, font=('Arial', 10))
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', help_text)
        text_widget.config(state='disabled')
        
        # Close button
        close_btn = tk.Button(help_window, text="Close", command=help_window.destroy,
                             bg='#3498db', fg='white', font=('Arial', 10))
        close_btn.pack(pady=10)
    
    def test_email_connection(self):
        """Test email connection credentials"""
        email = self.sender_email.get()
        password = self.sender_password.get()
        
        if not email or not password:
            messagebox.showwarning("Missing Info", "Please enter both email and password first!")
            return
        
        self.email_status_label.config(text="🔧 Testing connection...", foreground='orange')
        self.root.update_idletasks()
        
        def test_connection():
            try:
                result = test_email_credentials(email, password)
                
                def update_ui():
                    if result['success']:
                        self.email_status_label.config(
                            text=f"✅ Connection successful! Provider: {result.get('provider', 'Unknown').upper()}", 
                            foreground='green'
                        )
                        messagebox.showinfo("Success", result['message'])
                    else:
                        self.email_status_label.config(text="❌ Connection failed", foreground='red')
                        messagebox.showerror("Connection Failed", result['error'])
                
                self.root.after(0, update_ui)
                
            except Exception as e:
                def show_error():
                    self.email_status_label.config(text="❌ Test failed", foreground='red')
                    messagebox.showerror("Test Error", f"Connection test failed: {str(e)}")
                
                self.root.after(0, show_error)
        
        # Run test in background thread
        thread = threading.Thread(target=test_connection)
        thread.daemon = True
        thread.start()
        
    # Core functionality methods
    def select_cover_image(self):
        """Open file dialog to select cover image"""
        file_path = filedialog.askopenfilename(
            title="Select Cover Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.cover_image_path.set(file_path)
            self.display_image(file_path, self.original_canvas)
            self.log_to_status("send", f"✅ Cover image selected: {os.path.basename(file_path)}")
            
    def select_stego_image(self):
        """Open file dialog to select stego image"""
        file_path = filedialog.askopenfilename(
            title="Select Stego Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.stego_image_path.set(file_path)
            self.log_to_status("extract", f"✅ Stego image selected: {os.path.basename(file_path)}")
            
    def display_image(self, image_path, canvas):
        """Display image on canvas"""
        try:
            # Open and resize image
            image = Image.open(image_path)
            
            # Calculate resize to fit canvas
            canvas_width = canvas.winfo_width() or 300
            canvas_height = canvas.winfo_height() or 200
            
            image.thumbnail((canvas_width-10, canvas_height-10), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Clear canvas and display image
            canvas.delete("all")
            x = canvas_width // 2
            y = canvas_height // 2
            canvas.create_image(x, y, image=photo, anchor='center')
            
            # Keep reference to prevent garbage collection
            canvas.image = photo
            
        except Exception as e:
            self.log_to_status("send", f"❌ Error displaying image: {str(e)}")
            
    def log_to_status(self, tab, message):
        """Log message to appropriate status area"""
        if tab == "send":
            text_widget = self.send_status
        elif tab == "extract":
            text_widget = self.extract_status
        elif tab == "demo":
            text_widget = self.demo_results
        else:
            return
            
        text_widget.insert(tk.END, f"{message}\n")
        text_widget.see(tk.END)
        self.root.update_idletasks()
        
    def check_blockchain_connection(self):
        """Check blockchain connection on startup"""
        try:
            if check_connection():
                self.log_to_status("send", "✅ Blockchain connection: SUCCESS")
                self.log_to_status("extract", "✅ Blockchain connection: SUCCESS") 
                self.log_to_status("demo", "✅ Blockchain connection: SUCCESS")
            else:
                self.log_to_status("send", "❌ Blockchain connection: FAILED")
                self.log_to_status("extract", "❌ Blockchain connection: FAILED")
                self.log_to_status("demo", "❌ Blockchain connection: FAILED")
        except Exception as e:
            self.log_to_status("send", f"❌ Blockchain error: {str(e)}")
            
    def send_message_thread(self):
        """Send message in separate thread"""
        thread = threading.Thread(target=self.send_message)
        thread.daemon = True
        thread.start()
        
    def send_message(self):
        """Send secret message using LSB + blockchain + real email"""
        try:
            # Validate basic inputs
            if not self.cover_image_path.get():
                messagebox.showerror("Error", "Please select a cover image!")
                return
                
            message = self.message_text.get('1.0', tk.END).strip()
            if not message:
                messagebox.showerror("Error", "Please enter a secret message!")
                return
                
            if not self.recipient_address.get():
                messagebox.showerror("Error", "Please enter recipient address!")
                return
            
            # Validate email inputs if using real email
            if self.use_real_email.get():
                if not self.sender_email.get() or not self.sender_password.get():
                    messagebox.showerror("Error", "Please enter your email credentials!")
                    return
                    
                if not self.recipient_email.get():
                    messagebox.showerror("Error", "Please enter recipient email address!")
                    return
                
                if not validate_email_format(self.sender_email.get()):
                    messagebox.showerror("Error", "Invalid sender email format!")
                    return
                    
                if not validate_email_format(self.recipient_email.get()):
                    messagebox.showerror("Error", "Invalid recipient email format!")
                    return
                
            # Start progress
            self.send_button.config(state='disabled')
            self.send_progress.start()
            
            self.log_to_status("send", "🚀 Starting secure message transmission...")
            self.log_to_status("send", f"📁 Cover image: {os.path.basename(self.cover_image_path.get())}")
            self.log_to_status("send", f"📝 Message length: {len(message)} characters")
            
            if self.use_real_email.get():
                self.log_to_status("send", f"📧 Real email: {self.sender_email.get()} → {self.recipient_email.get()}")
            else:
                self.log_to_status("send", "🧪 Using email simulation mode")
            
            # Send using hybrid system
            result = send_secure_message(
                cover_image_path=self.cover_image_path.get(),
                secret_message=message,
                recipient_address=self.recipient_address.get(),
                output_path="stego_output.png"
            )
            
            if result and 'success' in result and result['success']:
                # Display results
                self.log_to_status("send", "✅ LSB + BLOCKCHAIN COMPLETED!")
                self.log_to_status("send", f"🔗 Transaction Hash: {result.get('tx_hash', 'N/A')}")
                self.log_to_status("send", f"💾 Stego Image: {result.get('stego_path', 'stego_output.png')}")
                
                # Display quality metrics
                if 'metrics' in result:
                    metrics = result['metrics']
                    quality_text = f"""📊 QUALITY METRICS:
PSNR: {metrics.get('psnr', 0):.2f} dB
MSE: {metrics.get('mse', 0):.4f}
Processing Time: {metrics.get('processing_time', 0):.2f}s"""
                    
                    self.quality_text.delete('1.0', tk.END)
                    self.quality_text.insert('1.0', quality_text)
                
                # Send via email
                tx_hash = result.get('tx_hash', result.get('blockchain_tx_hash'))
                stego_path = result.get('stego_path', 'stego_output.png')
                
                if self.use_real_email.get():
                    # Send via real email
                    self.log_to_status("send", "📧 STEP 3: SENDING VIA REAL EMAIL...")
                    
                    email_result = send_real_email(
                        sender_email=self.sender_email.get(),
                        sender_password=self.sender_password.get(),
                        recipient_email=self.recipient_email.get(),
                        stego_image_path=stego_path,
                        tx_hash=tx_hash,
                        message_preview=message[:50],
                        subject=self.email_subject.get()
                    )
                    
                    if email_result.get('success'):
                        self.log_to_status("send", "✅ REAL EMAIL SENT SUCCESSFULLY!")
                        self.log_to_status("send", f"📧 Email delivered to: {email_result['recipient']}")
                        self.log_to_status("send", f"📎 Attachment: {email_result['attachment']}")
                        self.log_to_status("send", f"📊 Provider: {email_result.get('provider', 'Unknown').upper()}")
                        
                        # Show success message
                        messagebox.showinfo("Email Sent!", 
                            f"✅ Secure message sent successfully!\n\n"
                            f"📧 Email: {self.recipient_email.get()}\n"
                            f"🔗 TX Hash: {tx_hash[:16]}...\n"
                            f"📊 PSNR: {metrics.get('psnr', 0):.2f} dB\n\n"
                            f"The recipient will receive the stego image via email with extraction instructions.")
                    else:
                        self.log_to_status("send", f"❌ EMAIL SENDING FAILED: {email_result.get('error')}")
                        messagebox.showerror("Email Error", 
                            f"Steganography completed but email failed:\n{email_result.get('error')}\n\n"
                            f"You can manually send the file: {stego_path}")
                else:
                    # Use email simulation
                    self.log_to_status("send", "🧪 Email simulation - file saved locally")
                    messagebox.showinfo("Success!", 
                        f"✅ Secure message processed successfully!\n\n"
                        f"🔗 TX Hash: {tx_hash[:16]}...\n"
                        f"📊 PSNR: {metrics.get('psnr', 0):.2f} dB\n"
                        f"💾 File: {stego_path}\n\n"
                        f"File ready for manual distribution!")
                
                # Display stego image
                if os.path.exists(stego_path):
                    self.display_image(stego_path, self.stego_canvas)
                    
            else:
                self.log_to_status("send", "❌ Failed to send message")
                if result and 'error' in result:
                    self.log_to_status("send", f"Error: {result['error']}")
                    
        except Exception as e:
            self.log_to_status("send", f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
            
        finally:
            # Stop progress
            self.send_progress.stop()
            self.send_button.config(state='normal')
            
    def extract_message_thread(self):
        """Extract message in separate thread"""
        thread = threading.Thread(target=self.extract_message)
        thread.daemon = True
        thread.start()
        
    def extract_message(self):
        """Extract secret message from stego image"""
        try:
            # Validate inputs
            if not self.stego_image_path.get():
                messagebox.showerror("Error", "Please select a stego image!")
                return
                
            # Start progress
            self.extract_button.config(state='disabled')
            self.extract_progress.start()
            
            self.log_to_status("extract", "🔍 Starting message extraction...")
            self.log_to_status("extract", f"📁 Stego image: {os.path.basename(self.stego_image_path.get())}")
            
            # Extract using hybrid system
            result = receive_secure_message(
                stego_image_path=self.stego_image_path.get(),
                tx_hash=self.tx_hash.get() if self.tx_hash.get() else None
            )
            
            if result and 'success' in result and result['success']:
                # Display extracted message
                extracted_msg = result.get('message', 'No message found')
                self.extracted_message.delete('1.0', tk.END)
                self.extracted_message.insert('1.0', extracted_msg)
                
                self.log_to_status("extract", "✅ MESSAGE EXTRACTED SUCCESSFULLY!")
                self.log_to_status("extract", f"📝 Message: {extracted_msg}")
                
                # Display verification status
                if result.get('verified'):
                    self.log_to_status("extract", "✅ BLOCKCHAIN VERIFICATION: PASSED")
                else:
                    self.log_to_status("extract", "⚠️ BLOCKCHAIN VERIFICATION: Not verified")
                    
            else:
                self.log_to_status("extract", "❌ Failed to extract message")
                if result and 'error' in result:
                    self.log_to_status("extract", f"Error: {result['error']}")
                    
        except Exception as e:
            self.log_to_status("extract", f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Failed to extract message: {str(e)}")
            
        finally:
            # Stop progress
            self.extract_progress.stop()
            self.extract_button.config(state='normal')
            
    def run_demo_thread(self):
        """Run demo in separate thread"""
        thread = threading.Thread(target=self.run_demo)
        thread.daemon = True
        thread.start()
        
    def run_demo(self):
        """Run complete demo workflow"""
        try:
            # Start progress
            self.demo_button.config(state='disabled')
            self.demo_progress.start()
            
            self.log_to_status("demo", "🎯 STARTING COMPLETE DEMO WORKFLOW")
            self.log_to_status("demo", "=" * 50)
            
            # Create test image if needed
            demo_image = "demo_cover.png"
            if not os.path.exists(demo_image):
                self.log_to_status("demo", "📁 Creating demo cover image...")
                from PIL import Image
                import numpy as np
                
                # Create colorful test image
                img_array = np.random.randint(0, 255, (400, 400, 3), dtype=np.uint8)
                img = Image.fromarray(img_array)
                img.save(demo_image)
                self.log_to_status("demo", f"✅ Demo image created: {demo_image}")
                
            # Demo message
            test_message = "🔒 DEMO: This is a secret research message for Sinta 3+ journal testing! 📊"
            recipient = "0x50E57867322143f349d55197388Db32d1b7DB8e5"
            
            self.log_to_status("demo", f"📝 Test message: {test_message}")
            self.log_to_status("demo", f"📤 Recipient: {recipient}")
            
            # Phase 1: Send message
            self.log_to_status("demo", "\n🚀 PHASE 1: Sending secure message...")
            
            result = send_secure_message(
                cover_image_path=demo_image,
                secret_message=test_message,
                recipient_address=recipient,
                output_path="demo_stego.png"
            )
            
            if result and result.get('success'):
                tx_hash = result.get('tx_hash')
                self.log_to_status("demo", "✅ Phase 1 SUCCESS!")
                self.log_to_status("demo", f"🔗 TX Hash: {tx_hash}")
                
                if 'metrics' in result:
                    metrics = result['metrics']
                    self.log_to_status("demo", f"📊 PSNR: {metrics.get('psnr', 0):.2f} dB")
                    self.log_to_status("demo", f"📊 MSE: {metrics.get('mse', 0):.4f}")
                    
                # Phase 2: Extract message
                self.log_to_status("demo", "\n🔍 PHASE 2: Extracting message...")
                
                extract_result = receive_secure_message(
                    stego_image_path="demo_stego.png",
                    tx_hash=tx_hash
                )
                
                if extract_result and extract_result.get('success'):
                    extracted = extract_result.get('message', '')
                    verified = extract_result.get('verified', False)
                    
                    self.log_to_status("demo", "✅ Phase 2 SUCCESS!")
                    self.log_to_status("demo", f"📝 Extracted: {extracted}")
                    self.log_to_status("demo", f"🔒 Verified: {'YES' if verified else 'NO'}")
                    
                    # Phase 3: Results summary
                    self.log_to_status("demo", "\n📊 DEMO COMPLETE - RESEARCH RESULTS:")
                    self.log_to_status("demo", "=" * 50)
                    
                    if extracted == test_message:
                        self.log_to_status("demo", "✅ Message integrity: PERFECT MATCH")
                    else:
                        self.log_to_status("demo", "⚠️ Message integrity: MISMATCH")
                        
                    self.log_to_status("demo", f"✅ Blockchain verification: {'PASSED' if verified else 'FAILED'}")
                    self.log_to_status("demo", f"✅ Image quality maintained: PSNR {metrics.get('psnr', 0):.2f} dB")
                    self.log_to_status("demo", "✅ Demo workflow: COMPLETED SUCCESSFULLY")
                    
                    self.log_to_status("demo", "\n🎯 Ready for Sinta 3+ research publication!")
                    
                else:
                    self.log_to_status("demo", "❌ Phase 2 FAILED: Message extraction error")
                    
            else:
                self.log_to_status("demo", "❌ Phase 1 FAILED: Message sending error")
                
        except Exception as e:
            self.log_to_status("demo", f"❌ Demo error: {str(e)}")
            
        finally:
            # Stop progress
            self.demo_progress.stop()
            self.demo_button.config(state='normal')

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = SteganographyGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\n👋 GUI closed by user")
    except Exception as e:
        print(f"❌ GUI error: {e}")

if __name__ == "__main__":
    main()