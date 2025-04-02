import time
import numpy as np
import ndirust_py
import psutil
import os
from datetime import datetime

# Initialize NDI
ndirust_py.initialize_ndi()

# Create an NDI sender
sender_name = "Performance Test"
sender = ndirust_py.sender.NdiSender(sender_name)

# Create a solid black frame
width, height = 1920, 1080
fps_n, fps_d = 60, 1  # 60 frames per second

print(f"Sending NDI stream: {width}x{height} @ {fps_n}/{fps_d} fps")
print(f"Press Ctrl+C to stop")

# Initialize frame counter and performance metrics
frame_count = 0
start_time = time.time()
last_stats_time = start_time
process = psutil.Process(os.getpid())
initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
frame_times = []
stats_interval = 5.0  # Print stats every 5 seconds

# Try using different NDI formats to see if they improve performance
# The current implementation in our module uses BGRA format by default
# Let's try to create a frame in NV12 format which is more efficient for compression

# For testing different formats
test_format = "UYVY"  # Change between tests: BGRA (default), I420, NV12, UYVY

if test_format == "BGRA":
    # BGRA format (used in current implementation) - 4 bytes per pixel
    # Pre-create black background
    frame_data = np.zeros((height, width, 4), dtype=np.uint8)
    frame_data[:, :, 3] = 255  # Alpha channel
    frame_buffer = frame_data.tobytes()
    print("Using BGRA format (4 bytes per pixel)")
    
elif test_format == "NV12":
    # NV12 format (more efficient for compression) - 1.5 bytes per pixel
    # In NV12: Y plane followed by interleaved UV plane at half resolution
    y_plane_size = width * height
    uv_plane_size = width * height // 2
    total_size = y_plane_size + uv_plane_size
    
    # Create buffer
    frame_data = np.zeros(total_size, dtype=np.uint8)
    
    # Fill Y plane with black (0)
    y_plane = frame_data[:y_plane_size]
    y_plane.fill(0)  # Black in Y plane is 0
    
    # Fill UV plane with neutral color (128)
    uv_plane = frame_data[y_plane_size:]
    uv_plane.fill(128)  # Neutral UV is 128,128
    
    frame_buffer = frame_data.tobytes()
    print("Using NV12 format (1.5 bytes per pixel)")

elif test_format == "I420":
    # I420/YUV420P format - 1.5 bytes per pixel
    # In I420: Y plane, U plane, V plane (with U and V at quarter size)
    y_plane_size = width * height
    u_plane_size = width * height // 4
    v_plane_size = width * height // 4
    total_size = y_plane_size + u_plane_size + v_plane_size
    
    # Create buffer
    frame_data = np.zeros(total_size, dtype=np.uint8)
    
    # Fill Y plane with black (0)
    y_plane = frame_data[:y_plane_size]
    y_plane.fill(0)  # Black in Y plane is 0
    
    # Fill U and V planes with neutral color (128)
    u_plane = frame_data[y_plane_size:y_plane_size+u_plane_size]
    v_plane = frame_data[y_plane_size+u_plane_size:]
    u_plane.fill(128)  # Neutral U is 128
    v_plane.fill(128)  # Neutral V is 128
    
    frame_buffer = frame_data.tobytes()
    print("Using I420 format (1.5 bytes per pixel)")

else:  # UYVY
    # UYVY format (format used in send_test_pattern) - 2 bytes per pixel
    # Interleaved: U Y V Y U Y V Y ...
    frame_data = np.zeros(width * height * 2, dtype=np.uint8)
    
    # For black in UYVY:
    # Y component is 0 (black)
    # U and V components are 128 (neutral)
    
    # Set UV components to neutral
    frame_data[0::4] = 128  # U
    frame_data[2::4] = 128  # V
    
    # Y components already 0 for black
    
    frame_buffer = frame_data.tobytes()
    print("Using UYVY format (2 bytes per pixel)")

print(f"Buffer size: {len(frame_buffer)/1024/1024:.2f} MB")

try:
    while True:
        frame_start_time = time.time()
        
        # Measure time before sending
        before_send = time.time()
        
        # Send the frame
        sender.send_video_frame(frame_buffer, width, height, fps_n, fps_d)
        
        # Measure time after sending (NDI send overhead)
        send_time = time.time() - before_send
        
        # Increment frame counter
        frame_count += 1
        
        # Calculate total frame processing time
        frame_end_time = time.time()
        frame_time = frame_end_time - frame_start_time
        frame_times.append(frame_time)
        
        # Print stats periodically
        current_time = time.time()
        if current_time - last_stats_time >= stats_interval:
            # Calculate metrics
            elapsed = current_time - start_time
            actual_fps = frame_count / elapsed
            current_memory = process.memory_info().rss / (1024 * 1024)  # MB
            memory_diff = current_memory - initial_memory
            cpu_percent = process.cpu_percent()
            
            # Keep only the last 100 frame times for average calculation
            if len(frame_times) > 100:
                frame_times = frame_times[-100:]
            
            avg_frame_time = sum(frame_times) / len(frame_times) * 1000  # ms
            
            # Print stats
            print(f"\n--- Performance Stats at {datetime.now().strftime('%H:%M:%S')} ---")
            print(f"Total frames: {frame_count}, Running time: {elapsed:.2f}s")
            print(f"Target FPS: {fps_n}/{fps_d} = {fps_n/fps_d:.2f}, Actual FPS: {actual_fps:.2f}")
            print(f"Average frame processing time: {avg_frame_time:.2f}ms")
            print(f"Last NDI send overhead: {send_time*1000:.2f}ms")
            print(f"CPU usage: {cpu_percent:.1f}%")
            print(f"Memory usage: {current_memory:.1f}MB (Δ: {memory_diff:+.1f}MB)")
            print(f"Format: {test_format}")
            print("--------------------------------------")
            
            # Reset for next interval
            last_stats_time = current_time
            
            # If we're constantly missing frames, print a warning
            if actual_fps < fps_n / fps_d * 0.9:  # If we're below 90% of target
                print("WARNING: Not meeting target FPS, CPU may be overloaded")
        
        # Only sleep if we have time to spare
        elapsed = time.time() - frame_start_time
        sleep_time = max(0, (1.0/fps_n) - elapsed)
        if sleep_time > 0:
            time.sleep(sleep_time)
        
except KeyboardInterrupt:
    print("\nStream stopped by user")
finally:
    # Final stats
    end_time = time.time()
    total_time = end_time - start_time
    avg_fps = frame_count / total_time if total_time > 0 else 0
    
    # Clean up
    sender.close()
    
    print("\n=== Final Performance Summary ===")
    print(f"Total frames sent: {frame_count}")
    print(f"Total runtime: {total_time:.2f} seconds")
    print(f"Average FPS: {avg_fps:.2f} (target: {fps_n/fps_d:.2f})")
    if frame_times:
        print(f"Average frame processing time: {(sum(frame_times) / len(frame_times) * 1000):.2f}ms")
    print(f"Memory usage: {process.memory_info().rss / (1024 * 1024):.1f}MB")
    print(f"Format used: {test_format}")
    print("==================================") 