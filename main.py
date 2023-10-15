import cv2
import multiprocessing
import time
import logging
import coloredlogs
import os
import psutil


log_level = os.environ.get('LOG_LEVEL', 'DEBUG').upper()
log_numeric_level = getattr(logging, log_level, None)
coloredlogs.install(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S.%f', level=log_level)
# logging.basicConfig(level=logging.INFO) 
logging.basicConfig(level=log_numeric_level) 
logger = logging.getLogger(__name__)


def capture_frames_and_save(input_video, output_folder, start_frame, step, total_frames):
    logger.debug(f"reading video from {start_frame} to {total_frames} with step {step}")
    cap = cv2.VideoCapture(input_video)
    logger.debug("finished reading video")
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    logger.debug(f"Starting from frame {start_frame} to {total_frames}")

    for frame_number in range(start_frame, total_frames, step):
        logger.debug(f"Capturing frame {frame_number}")
        success, frame = cap.read()
        if not success:
            logger.error("failed to read frame")
            break
        
        if frame_number % step == 0:
            frame_filename = f"{output_folder}/frame_{frame_number}.jpg"
            logger.info(f"Saving frame {frame_filename}")
            cv2.imwrite(frame_filename, frame)

    cap.release()
    
    
def main():
    start = time.time()
    logger.info("start")
    
    input_video = "1.MOV"  # Replace with your video file
    output_folder = "_output_frames"  # Output folder to save frames
    available_cors = psutil.cpu_count()
    num_processes = available_cors  # Number of parallel processes to use

    cap = cv2.VideoCapture(input_video)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create the output folder if it doesn't exist    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    processes = []

    for i in range(num_processes):
        start_frame = i * total_frames // num_processes
        # end frame for each process
        end_frame = min((i + 1) * total_frames // num_processes, total_frames)  # Calculate the end frame

        step = 5  # Capture every 5th frame
        process = multiprocessing.Process(target=capture_frames_and_save,
                                         args=(input_video, output_folder, start_frame, step, end_frame))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    cap.release()
    end = time.time()
    print(f"Time taken: {end - start} seconds")

if __name__ == "__main__":
    main()
