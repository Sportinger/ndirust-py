#!/usr/bin/env python
"""
GUI example showing NDI video preview using Tkinter.

This example demonstrates how to:
1. Find NDI sources on the network
2. Connect to a source and receive frames
3. Display the video frames in a GUI window using Tkinter
4. Allow switching between different sources

Requirements:
- tkinter (included with most Python installations)
- pillow (pip install pillow)
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk

# Ensure the NDI SDK is in the PATH
ndi_sdk_path = r"C:\Program Files\NDI\NDI 6 SDK\Bin\x64"
if os.path.exists(ndi_sdk_path):
    os.environ["PATH"] = ndi_sdk_path + os.pathsep + os.environ["PATH"]

try:
    import ndirust_py
except ImportError as e:
    print(f"Error importing ndirust_py module: {e}")
    print("Make sure you have installed the ndirust-py package.")
    sys.exit(1)

class NdiPreviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NDI Video Preview")
        self.root.geometry("1280x800")  # Default window size
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Initialize NDI
        if not ndirust_py.initialize_ndi():
            print("Failed to initialize NDI")
            self.root.destroy()
            return
        
        # Create NDI objects
        self.finder = ndirust_py.discovery.NdiFinder()
        self.receiver = None
        self.sources = []
        self.current_source_index = -1
        self.running = True
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0
        
        # Set up the GUI
        self.setup_ui()
        
        # Start the source discovery thread
        self.discovery_thread = threading.Thread(target=self.discover_sources, daemon=True)
        self.discovery_thread.start()
        
        # Start the receiver thread
        self.receiver_thread = threading.Thread(target=self.receive_frames, daemon=True)
        self.receiver_thread.start()
        
        # Start the stats update timer
        self.root.after(1000, self.update_stats)
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Sources dropdown
        ttk.Label(control_frame, text="NDI Sources:").pack(side=tk.LEFT, padx=(0, 5))
        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(control_frame, textvariable=self.source_var, state="readonly", width=40)
        self.source_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.source_combo.bind("<<ComboboxSelected>>", self.on_source_selected)
        
        # Refresh button
        self.refresh_btn = ttk.Button(control_frame, text="Refresh Sources", command=self.refresh_sources)
        self.refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status and stats
        self.status_var = tk.StringVar(value="Status: Initializing...")
        self.stats_var = tk.StringVar(value="Stats: No data")
        
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        ttk.Label(status_frame, textvariable=self.status_var).pack(side=tk.TOP, anchor=tk.E)
        ttk.Label(status_frame, textvariable=self.stats_var).pack(side=tk.TOP, anchor=tk.E)
        
        # Video frame
        self.video_frame = ttk.Frame(main_frame, borderwidth=2, relief=tk.GROOVE)
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for displaying the video
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        self.canvas.create_text(640, 400, text="Waiting for NDI source...", fill="white", font=("Arial", 20))
    
    def discover_sources(self):
        """Thread function to periodically discover NDI sources."""
        while self.running:
            try:
                self.sources = self.finder.find_sources(timeout_ms=1000)
                
                if not self.sources:
                    self.root.after(0, lambda: self.status_var.set("Status: No NDI sources found"))
                else:
                    source_names = [str(source).replace("NdiSource(name='", "").replace("')", "") for source in self.sources]
                    
                    # Update the combobox on the main thread
                    self.root.after(0, lambda names=source_names: self.update_source_list(names))
                
                # Don't poll too frequently
                time.sleep(2)
            except Exception as e:
                print(f"Error in discovery thread: {e}")
                time.sleep(1)
    
    def update_source_list(self, source_names):
        """Update the sources dropdown with found sources."""
        current_selection = self.source_var.get()
        self.source_combo['values'] = source_names
        
        # If we have sources but none selected, select the first one
        if source_names and not current_selection and self.current_source_index < 0:
            self.source_combo.current(0)
            self.on_source_selected(None)
        # Otherwise try to maintain the previous selection
        elif current_selection in source_names:
            self.source_var.set(current_selection)
    
    def on_source_selected(self, event):
        """Handle source selection from the dropdown."""
        selected = self.source_var.get()
        if selected:
            # Find the index of the selected source
            for i, source in enumerate(self.sources):
                source_name = str(source).replace("NdiSource(name='", "").replace("')", "")
                if source_name == selected:
                    if i != self.current_source_index:
                        self.current_source_index = i
                        # Reset stats
                        self.frame_count = 0
                        self.start_time = time.time()
                        self.status_var.set(f"Status: Connected to {selected}")
                    break
    
    def refresh_sources(self):
        """Manually refresh the NDI sources."""
        self.status_var.set("Status: Refreshing sources...")
        self.sources = self.finder.find_sources(timeout_ms=3000)
        
        if not self.sources:
            self.status_var.set("Status: No NDI sources found")
            self.source_combo['values'] = []
            return
        
        source_names = [str(source).replace("NdiSource(name='", "").replace("')", "") for source in self.sources]
        self.source_combo['values'] = source_names
        self.status_var.set(f"Status: Found {len(source_names)} sources")
    
    def receive_frames(self):
        """Thread function to receive NDI frames from the selected source."""
        receiver_initialized = False
        connected_source_name = None
        
        while self.running:
            try:
                # If we have a valid source selected
                if self.current_source_index >= 0 and self.current_source_index < len(self.sources):
                    source = self.sources[self.current_source_index]
                    source_name = str(source).replace("NdiSource(name='", "").replace("')", "")
                    
                    # If source changed, reconnect
                    if source_name != connected_source_name:
                        # Close previous receiver if it exists
                        if self.receiver:
                            self.receiver.close()
                            self.receiver = None
                            receiver_initialized = False
                        
                        # Create a new receiver
                        self.receiver = ndirust_py.receiver.NdiReceiver()
                        
                        # Connect to the source
                        self.receiver.connect_to_source(source_name)
                        connected_source_name = source_name
                        receiver_initialized = True
                    
                    # Receive a frame if connected
                    if receiver_initialized:
                        frame_type, frame = self.receiver.receive_frame(timeout_ms=100)
                        
                        # If we got a video frame, display it
                        if int(frame_type) == 1 and frame is not None:  # Video frame
                            self.frame_count += 1
                            self.update_video_frame(frame)
                else:
                    time.sleep(0.1)  # No source selected, wait a bit
            
            except Exception as e:
                print(f"Error in receiver thread: {e}")
                time.sleep(1)
                
                # Try to reinitialize the receiver
                if self.receiver:
                    self.receiver.close()
                    self.receiver = None
                    receiver_initialized = False
    
    def update_video_frame(self, frame):
        """Convert NDI frame to an image and display it on the canvas."""
        try:
            # Get the frame data as bytes
            frame_bytes = frame.get_data()
            if not frame_bytes:
                return
            
            # Process based on the pixel format
            format_name = frame.get_four_cc_name()
            
            if format_name in ["BGRA", "RGBA"]:
                # Get frame dimensions
                width = frame.width
                height = frame.height
                
                # Convert bytes to numpy array
                buffer = np.frombuffer(frame_bytes, dtype=np.uint8)
                
                # Reshape to an image array
                if format_name == "BGRA":
                    # BGRA to RGBA conversion
                    img_array = buffer.reshape((height, width, 4))[:, :, [2, 1, 0, 3]]
                else:
                    img_array = buffer.reshape((height, width, 4))
                
                # Create PIL Image from array
                img = Image.fromarray(img_array, 'RGBA')
                
                # Scale image to fit canvas (if needed)
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
                
                if canvas_width > 10 and canvas_height > 10:  # Ensure canvas has been drawn
                    # Calculate scaling to fit the canvas while preserving aspect ratio
                    scale_w = canvas_width / width
                    scale_h = canvas_height / height
                    scale = min(scale_w, scale_h)
                    
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    
                    if new_width != width or new_height != height:
                        img = img.resize((new_width, new_height), Image.LANCZOS)
                
                # Convert to Tkinter PhotoImage
                photo = ImageTk.PhotoImage(img)
                
                # Update canvas on main thread
                self.root.after(0, lambda p=photo: self._update_canvas_image(p))
        except Exception as e:
            print(f"Error updating video frame: {e}")
    
    def _update_canvas_image(self, photo):
        """Update the canvas with the new image (must be called from main thread)."""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Center the image
        x = (canvas_width - photo.width()) // 2
        y = (canvas_height - photo.height()) // 2
        
        # Create new image on canvas
        self.canvas.create_image(x, y, anchor=tk.NW, image=photo)
        
        # Keep a reference to prevent garbage collection
        self.canvas.image = photo
    
    def update_stats(self):
        """Update performance statistics."""
        if self.running:
            # Calculate FPS
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                self.fps = self.frame_count / elapsed
            
            # Update stats label
            self.stats_var.set(f"Stats: {self.frame_count} frames, {self.fps:.2f} FPS")
            
            # Schedule next update
            self.root.after(1000, self.update_stats)
    
    def on_closing(self):
        """Handle window close event."""
        self.running = False
        
        # Wait for threads to finish
        if self.discovery_thread.is_alive():
            self.discovery_thread.join(timeout=1.0)
        
        if self.receiver_thread.is_alive():
            self.receiver_thread.join(timeout=1.0)
        
        # Clean up NDI resources
        if self.receiver:
            self.receiver.close()
        
        if self.finder:
            self.finder.close()
        
        self.root.destroy()

def main():
    # Create the main window
    root = tk.Tk()
    app = NdiPreviewApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main() 