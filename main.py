# import cv2
# import face_recognition
# import math
# import numpy
# import time
# from multiprocessing import Manager, Process, cpu_count
# from datetime import datetime
#
#
# def capture(read_frame_list, Global, worker_num, is_capture_finished):
#     video_capture = cv2.VideoCapture("video.mp4")
#     Global.frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     capture_frame = cv2.VideoWriter('capture.avi', fourcc, 24, (1920, 1080))
#
#     for i in range(int(Global.frame_count)):
#         ret, frame = video_capture.read()
#         print(f"{(i / Global.frame_count) * 100} %")
#         if not ret:
#             break
#         try:
#             read_frame_list[i] = frame
#         except EOFError as e:
#             print(e)
#     # testing to see if capture works properly
#     # for i in range(len(read_frame_list)):
#     #     capture_frame.write(read_frame_list[i])
#     print("Finished the capture function")
#     video_capture.release()
#     cv2.destroyAllWindows()
#     is_capture_finished.value = True
#
#
# def process(worker_id, read_frame_list, write_frame_list, Global, worker_num, is_capture_finished):
#     print(f"{worker_id} is executing")
#     # while not is_capture_finished.value:
#     #     time.sleep(0.01)
#
#     # pass frames_per_worker as parameter
#     frames_per_worker = math.floor(len(read_frame_list) / worker_num)
#     known_face_encodings = Global.known_face_encodings
#     known_face_names = Global.known_face_names
#     count = 0
#
#     for i in range((worker_id - 1) * frames_per_worker + 1, worker_id * frames_per_worker):
#
#         # time.sleep(0.01)
#         frame_process = read_frame_list[i]
#         rgb_frame = numpy.ascontiguousarray(frame_process[:, :, ::-1])
#
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             name = "Unknown"
#             # global count
#             print(f"{(count / len(read_frame_list)) * 100}%")
#             count += 1
#
#             if True in matches:
#                 first_match_index = matches.index(True)
#                 name = known_face_names[first_match_index]
#                 cv2.rectangle(frame_process, (left, top), (right, bottom), (0, 0, 255), 2)
#                 cv2.rectangle(frame_process, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#                 font = cv2.FONT_HERSHEY_DUPLEX
#                 cv2.putText(frame_process, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#
#                 write_frame_list[i] = frame_process.astype(numpy.uint8)
#             time.sleep(0.01)
#
#     print("Process finished")
#
#
# if __name__ == '__main__':
#     start_dateTime = datetime.now()
#     print(start_dateTime)
#
#     Global = Manager().Namespace()
#     Global.frame_count = 0
#
#     read_frame_list = Manager().dict()
#     write_frame_list = Manager().dict()
#
#     if cpu_count() > 2:
#         worker_num = cpu_count()
#     else:
#         worker_num = 2
#
#     is_capture_finished = Manager().Value('i', False)
#
#     capture_process = Process(target=capture, args=(read_frame_list, Global, worker_num, is_capture_finished))
#     capture_process.start()
#
#     capture_process.join()
#     print("Capture process finished")
#
#
#     deepika_image = face_recognition.load_image_file("deepika.webp")
#     deepika_face_encoding = face_recognition.face_encodings(deepika_image)[0]
#
#     shahrukh_image = face_recognition.load_image_file("shahrukh.jpeg")
#     shahrukh_face_encoding = face_recognition.face_encodings(shahrukh_image)[0]
#
#     # arrays of known face encodings and their names
#     Global.known_face_encodings = [
#         deepika_face_encoding,
#         shahrukh_face_encoding
#     ]
#     Global.known_face_names = [
#         "Deepika",
#         "Shahrukh"
#     ]
#
#     processes = []
#     print('process start')
#     for worker_id in range(1, worker_num + 1):
#         p = Process(target=process, args=(worker_id, read_frame_list, write_frame_list, Global, worker_num, is_capture_finished))
#         processes.append(p)
#         p.start()
#
#     for p in processes:
#         p.join()
#
#     # write_frame_list.sort(key=lambda tup: tup[0])
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     out = cv2.VideoWriter('output_final.avi', fourcc, 24, (1920, 1080))
#
#     for frame_key in sorted(write_frame_list.keys()):
#         if write_frame_list[frame_key] is not None:
#             frame = write_frame_list[frame_key]
#             out.write(frame.astype(numpy.uint8))
#
#     out.release()
#     end_dateTime = datetime.now()
#     print(end_dateTime)
#     total = end_dateTime - start_dateTime
#     print(total.total_seconds() / 60)
#     cv2.destroyAllWindows()
import os
import cv2
import face_recognition
import math
import numpy
import time
from multiprocessing import Manager, Process, cpu_count
from datetime import datetime


def capture(read_frame_list, Global,is_capture_finished):
    video_capture = cv2.VideoCapture("video_small.mp4")
    Global.frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # capture_frame = cv2.VideoWriter('capture.avi', fourcc, 24, (1920, 1080))

    for i in range(int(Global.frame_count)):
        ret, frame = video_capture.read()
        # print(f"{(math.floor(i / Global.frame_count) * 100)} %")
        if not ret:
            break
        try:
            read_frame_list[i] = frame
        except EOFError as e:
            print(e)
    # testing to see if capture works properly
    # for i in range(len(read_frame_list)):
    #     capture_frame.write(read_frame_list[i])
    print("Finished the capture function")
    video_capture.release()
    cv2.destroyAllWindows()
    is_capture_finished.value = True

def process(worker_id, read_frame_list, write_frame_list, Global, frames_per_worker, is_capture_finished):
    print(f"{worker_id} is executing")
    # while not is_capture_finished.value:
    #     time.sleep(0.01)

    # pass frames_per_worker as parameter
    # frames_per_worker = math.floor(len(read_frame_list) / worker_num)
    known_face_encodings = Global.known_face_encodings
    known_face_names = Global.known_face_names

    for i in range((worker_id - 1) * frames_per_worker + 1, worker_id * frames_per_worker):

        # time.sleep(0.01)
        frame_process = read_frame_list[i]
        frame_process = cv2.resize(frame_process, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = numpy.ascontiguousarray(frame_process[:, :, ::-1])
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            # global count
            # print(f"{(Global.count / len(read_frame_list)) * 100}%")
            # Global.count += 1

            if True in matches:
                # first_match_index = matches.index(True)
                # name = known_face_names[first_match_index]
                # cv2.rectangle(frame_process, (left, top), (right, bottom), (0, 0, 255), 2)
                # cv2.rectangle(frame_process, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                # font = cv2.FONT_HERSHEY_DUPLEX
                # cv2.putText(frame_process, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                # top *= 4
                # right *= 4
                # bottom *= 4
                # left *= 4
                frame_process = cv2.resize(frame_process.astype(numpy.uint8), (1920, 1080))
                write_frame_list[i] = frame_process
                # write_frame_list[i] = cv2.resize(write_frame_list[i], (1920, 1080))

            time.sleep(0.01)

    print(f"Process finished {worker_id}")


if __name__ == '__main__':
    start_dateTime = datetime.now()
    print(start_dateTime)
    # debug = input("Debugging?")

    Global = Manager().Namespace()
    Global.frame_count = 0

    read_frame_list = Manager().dict()
    write_frame_list = Manager().dict()

    worker_num = cpu_count()

    is_capture_finished = Manager().Value('i', False)

    capture_process = Process(target=capture, args=(read_frame_list, Global, is_capture_finished))
    capture_process.start()

    capture_process.join()
    print("Capture process finished")

    path = "/Users/sharayujanga/Desktop/faceRecMultiprocess"
    image_files = []
    known_face_encodings = []
    known_face_names = []
    for root, directories, files in os.walk(path):
        for file in files:
            if file.endswith((".jpg", ".jpeg", ".png", "webp")):
                image_files.append(os.path.join(root, file))

    # print(image_files)

    for image_file in image_files:
        image = face_recognition.load_image_file(image_file)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        folder_name = os.path.basename(os.path.dirname(image_file))
        known_face_names.append(folder_name)

    Global.known_face_encodings = known_face_encodings
    Global.known_face_names = known_face_names
    # print(Global.known_face_names)

    processes = []
    print('process start')
    frames_per_worker = math.floor(len(read_frame_list) / worker_num)
    for worker_id in range(1, worker_num + 1):
        p = Process(target=process, args=(worker_id, read_frame_list, write_frame_list, Global, frames_per_worker, is_capture_finished))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # write_frame_list.sort(key=lambda tup: tup[0])
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_resized.avi', fourcc, 24, (1920, 1080))  # Change the output size as needed

    for frame_key in sorted(write_frame_list.keys()):
        if write_frame_list[frame_key] is not None:
            frame = write_frame_list[frame_key]
            print("writing frame")
            out.write(frame.astype(numpy.uint8))

    out.release()
    end_dateTime = datetime.now()
    print(end_dateTime)
    total = end_dateTime - start_dateTime
    print(f"{total.total_seconds() / 60} minutes")
    cv2.destroyAllWindows()