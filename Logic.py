##### importing Section 
import cv2
import mediapipe as mp
import numpy as np
from PIL import Image
import os
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

# Media pipe initiation variables
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Emotion Recognition model
model = tf.keras.models.load_model('Emotion_model.h5')

# Final classification model
final_model = tf.keras.models.load_model('Final_model.h5')




def get_face(nose_x,nose_y,nose_z):
    """
    This Function returns the bounding box of the the face 

    Parameters:
    nose_x - value of the nose-point coordinate on the x-axis
    nose_y - value of the nose-point coordinate on the y-axis
    nose_z - value of the nose-point coordinate on the z-axis
    
    Return:
    bounding_box - the boundung box that surround the face of the student from the original image, top-left and bottom-right corners
    
    """
    if (nose_z >= -30):
        x1, y1 = nose_x-65, nose_y-75
        x2, y2 = nose_x+65, nose_y+75
    if(nose_z < -50):
            x1, y1 = nose_x-155, nose_y-140
            x2, y2 = nose_x+155, nose_y+140
    else:
        x1, y1 = nose_x-95, nose_y-110
        x2, y2 = nose_x+95, nose_y+110
        
    bounding_box = [x1,y1,x2,y2]
    return bounding_box


def head_body(image):
    """
    This Function is constructed to extract the Nose Key-Point and the Angles of the Nose-Norm with the main image's frame

    Parameters:
    image - numpy array 

    Return:
    Angle_x - float, the angle of the norm with the x-axis 
    Angle_y - float, the angle of the norm with the y-axis
    Nose_z - float, value of the nose-point coordinate on the z-axis
    bounding_box - list, the boundung box that surround the face of the student from the original image

    """
    results = face_mesh.process(image)
    angle_x,angle_y,angle_z,nose_x,nose_y,nose_z = 0.0,0.0,0.0,0.0,0.0,0.0
    bounding_box = [0,0,0,0]
    # To improve performance (media pipe recommendations)
    image.flags.writeable = True

    # Convert the color space from RGB to BGR (media pipe recommendations)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []
    x1,x2,y1,y2 = 0,0,0,0
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (int(lm.x * img_w), int(lm.y * img_h))


                        nose_3d = (int(lm.x * img_w),int( lm.y * img_h), lm.z * 3000)
                        nose_x, nose_y, nose_z = int(lm.x * img_w),int( lm.y * img_h), int(lm.z * img_w)

                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    # Get the 2D Coordinates
                    face_2d.append([x, y])

                    # Get the 3D Coordinates
                    face_3d.append([x, y, lm.z])       

            # Convert it to the NumPy array
            face_2d = np.array(face_2d, dtype=np.float64)

            # Convert it to the NumPy array
            face_3d = np.array(face_3d, dtype=np.float64)

            # The camera matrix
            focal_length = 1 * img_w

            cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                    [0, focal_length, img_w / 2],
                                    [0, 0, 1]])

            # The distortion parameters
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            # Solve PnP
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            # Get rotational matrix
            rmat, jac = cv2.Rodrigues(rot_vec)

            # Get angles
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            # Get the rotation degree
            angle_x = angles[0] * 360
            angle_y = angles[1] * 360
            angle_z = angles[2] * 360

            bounding_box = get_face(nose_x,nose_y,nose_z)
    
    return (angle_x,angle_y,nose_z,bounding_box)


def prepare_data(ui,dir_path,increase):
    """
    This Function prepares the sub-video by extracting all the features and store it in data frame

    Parameters:
    dir_path - The path of the sub-video

    Return:
    Final_data - data frame, contains all the the features of all frames in the sub-video
    
    """
    
    body_features = ['Angle_x','Angle_y','Nose_z']
    facial_expressions = ['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise']
    data_set = []
    sf = 0
    
    frame_num = 0
    df = pd.DataFrame(columns=body_features+facial_expressions)

    cap = cv2.VideoCapture(dir_path)
    while cap.isOpened():

        success, image = cap.read()
        
        if not success:
            #   print("Ignoring empty camera frame.")
              break
            
        image = cv2.flip(image, 1)
        if(frame_num==0):
            frame_num+=1
            continue
        frame_num+=1
        image.flags.writeable = False
        sf += frame_num
        angle_x,angle_y,nose_z,detected_face = head_body(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if(detected_face[0] != 0):
            detect_face = (detected_face[0], detected_face[1], detected_face[2], detected_face[3])
            face = Image.fromarray(image).crop(detect_face).resize((48,48),Image.ANTIALIAS)
            cropped = np.asarray(face)
        else:
            cropped = np.asarray(Image.fromarray(image).resize((48,48),Image.ANTIALIAS))

        preds = model.predict(np.expand_dims(cropped,axis=(0,3)))
        FE = [0,0,0,0,0,0,0,0]
        idx = np.argmax(preds)
        FE[idx] = 1
        res = dict(zip(facial_expressions+body_features, FE+[round(angle_x,2),round(angle_y,2),nose_z]))
        df.loc[frame_num] = pd.Series(res)


        if cv2.waitKey(5) & 0xFF == 27:
            break
    data_set.append(df)
    cap.release()

    Final_data = pd.DataFrame(columns=body_features+facial_expressions)    
    ui.progressBar.setValue(ui.progressBar.value() + increase)  
    for d in data_set:
        Final_data = pd.concat([Final_data,d])
    return Final_data



def majority_vote(data):

    """
    This Function do majority-vote on the result of the prediction process that performed with the data extracted from the sub-video

    Parameters:
    data - data frame, from 'prepare_data' function

    Return:
    Tuple - contains the attentiveness level (average attentiveness level,average not-attentiveness level, list->attintiveness level for each sub-video)
    """
    alevel, nlevel = 0,0
    level = []
    for t in data:
        if(t.shape[0] < 1):
            continue
        preds = final_model.predict(t)
        s = np.sum(preds)
        attentive = np.count_nonzero(preds>=0.5)/preds.shape[0]
        level.append(round(attentive*100,1))
        alevel+= attentive
        nlevel+= np.count_nonzero(preds<0.5)/preds.shape[0]
        if(s >= t.shape[0] * 0.5):
            print(f'Attentive: {round(np.count_nonzero(preds>=0.5)/preds.shape[0]*100,2)}%')
        else:
            print(f'Not_attentive: {round(np.count_nonzero(preds<0.5)/preds.shape[0]*100,2)}%')
        
    return (round(alevel/len(data)*100,1),round(nlevel/len(data)*100,1),level)



def save_plot(data, interval, st_name):
    plt.figure(figsize=(7.56,3.8))
    m = list(np.arange(start=1,stop=len(data[-1])+1))
    plt.plot(m,data[-1],color='blue', marker='o')
    plt.xlabel(f'Intervals ({interval} sec)')
    plt.ylabel('Attentivness Level (%)')
    ax1 = plt.subplot()
    ax1.set_xticks(m)
    # the path that the generated graph will save to
    path = f"E:\Graduation Project\Full Project\{st_name}.jpg"
    plt.savefig(path)
    return path

def analyse(ui,videos_num,interval,st_name):
    data = []
    for i in range(1,videos_num+1):
        # extract features from sub-videos are existing in the path '/Video_temp'
        data.append(prepare_data(ui,f'Video_temp/{i}.mp4',100//videos_num))
        
    res = majority_vote(data)
    image_path = save_plot(res,interval,st_name)
    return round(np.mean(res[-1]),2),image_path


    