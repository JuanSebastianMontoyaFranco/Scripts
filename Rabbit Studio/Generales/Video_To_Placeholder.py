import cv2
import os

def extract_frame_from_videos(folder_path, output_folder, frame_time=4):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    video_files = [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    reference_size = None
    
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            print(f"No se pudo abrir el video: {video_file}")
            continue
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(fps * frame_time)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            print(f"No se pudo extraer el frame del video: {video_file}")
            continue
        
        if reference_size is None:
            reference_size = (frame.shape[1], frame.shape[0])  # (width, height)
        else:
            frame = cv2.resize(frame, reference_size)
        
        output_path = os.path.join(output_folder, f"{os.path.splitext(video_file)[0]}.jpg")
        cv2.imwrite(output_path, frame)
        print(f"Frame guardado: {output_path}")
    
folder_videos = "C:\\Users\\jsm21\\Downloads\\videos"
output_images = "C:\\Users\\jsm21\\Downloads\\Imagenes"
extract_frame_from_videos(folder_videos, output_images)
