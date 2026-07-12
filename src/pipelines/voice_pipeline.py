import streamlit as st
import numpy as np
import librosa
# from speechbrain.inference.speaker import EncoderClassifier
from resemblyzer import VoiceEncoder,preprocess_wav
import io

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()
    
    
def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_bytes),sr=16000,mono=True) 
        wav= preprocess_wav(audio)
        embeddings = encoder.embed_utterance(wav)
        print("Embedding length:", len(embeddings.squeeze()))
        print("First 5:", embeddings.squeeze()[:5])
        return embeddings.tolist()
    
    except Exception as e:
        st.error(f"Error processing audio: {e}")
        return None


def identify_speaker(new_embedding,candidate_dict,threshold=0.65):
    if not candidate_dict:
        return None, 0.0
    
    best_sid = None
    best_score = -1
    
    for sid, stored_embedding in candidate_dict.items():
        if stored_embedding:
            similarity = np.dot(new_embedding, stored_embedding)
            if similarity > best_score:
                best_score = similarity
                best_sid = sid
                
    if best_score >= threshold:
        return best_sid, best_score
    else:
        return None, best_score
    
    
def process_bluk_audio(audio_bytes,candidate_dict,threshold=0.65):
    try:
        encoder = load_voice_encoder()
        wav, sr= librosa.load(io.BytesIO(audio_bytes),sr=16000,mono=True) 
        segments = librosa.effects.split(wav, top_db=30)
        
        identified_sid = {}
        for start, end in segments:
            if end - start < sr * 0.5:  # Skip segments shorter than 1 second
                continue
            segment_audio = wav[start:end]
            wav = preprocess_wav(segment_audio)
            embeddings = encoder.embed_utterance(wav)
            
            sid, score = identify_speaker(embeddings, candidate_dict, threshold)
            if sid not in identified_sid or score > identified_sid[sid]:
                identified_sid[sid] = score
                
        return identified_sid
    
    except Exception as e:
        st.error(f"Error Bluk processing audio: {e}")
        return {}
            

    