import dlib
import face_recognition_models
import numpy as np
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    dector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    facerec = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return dector, sp, facerec


def get_face_embedding(image_np):
    dector, sp, facerec = load_dlib_models()
    faces = dector(image_np, 2)
    encodings = []
    
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape,2) #128D embedding
        encodings.append(np.array(face_descriptor))
        
    return encodings

@st.cache_resource
def get_trained_model():
    x = []
    y =[]
    student_db = get_all_students()
    if not student_db:
        return None
    
    for student in student_db:
        embeddings = student.get("face_embeddings")
        if embeddings:
            x.append(np.array(embeddings))
            y.append(student.get("student_id"))
            
    if len(x) == 0:
        return 0
    
    classifier = SVC(kernel='linear', probability=True)
    try:
        classifier.fit(x, y)
    except Exception as e:
        st.error(f"Error training the model: {e}")
        pass
    
    return {'classifier': classifier, 'x': x, 'y': y}

def train_model():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return model_data




def predict_attendance(class_image_np):
    encodings = get_face_embedding(class_image_np)
    detected_students = {}
    model_data = get_trained_model()
    
    if not model_data:
        return detected_students,[],len(encodings)
    
    
    classifier = model_data['classifier']
    x_train = model_data['x']
    y_train = model_data['y']
    
    all_students = sorted(list(set(y_train)))
    
    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(classifier.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        student_embeddings = x_train[y_train.index(predicted_id)]
        
        # check once:- 
        
        best_match_score = np.linalg.norm(student_embeddings - encoding)
        resemblance_threshold = 0.5  

        if best_match_score <= resemblance_threshold:
            detected_students[predicted_id] = True
        
        return detected_students, all_students, len(encodings)
    
    