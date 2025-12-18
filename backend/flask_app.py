"""
🎵 Müzik Duygusal Öneri Sistemi - Flask Backend
React Frontend ile entegre API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from pathlib import Path
import json
from music_recommender import MusicRecommender
from ml_emotion_classifier import EmotionClassifier

app = Flask(__name__)
CORS(app)  # CORS desteği

# Global değişkenler
recommender = None
classifier = None

def init_models():
    """Modelleri başlat"""
    global recommender, classifier
    try:
        recommender = MusicRecommender()
        classifier = EmotionClassifier()
        classifier.prepare_data()
        # Gelişmiş model eğitimi dene, olmazsa basit olanı kullan
        try:
            classifier.train_advanced_model()
        except Exception as e:
            print(f"Gelişmiş model eğitimi başarısız, basit model kullanılıyor: {e}")
            classifier.train_random_forest()
        print("✅ Modeller başarıyla yüklendi")
        return True
    except Exception as e:
        print(f"❌ Model yükleme hatası: {e}")
        return False

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Gelişmiş duygu durumuna göre müzik önerileri"""
    try:
        data = request.get_json()
        emotion = data.get('emotion', 'neutral')

        if not recommender:
            return jsonify({'error': 'Model not loaded'}), 500

        # Dataset'ten öneriler al
        recommendations = []

        try:
            df = pd.read_csv('../data/music_emotion.csv')
            # Duygu durumuna göre filtrele
            filtered_df = df[df['emotion'].str.lower() == emotion.lower()]

            if len(filtered_df) == 0:
                # Benzer duygular için genişlet
                emotion_mapping = {
                    'happy': ['happy', 'energetic'],
                    'sad': ['sad', 'calm'],
                    'angry': ['angry', 'energetic'],
                    'calm': ['calm', 'sad'],
                    'energetic': ['energetic', 'happy'],
                    'romantic': ['romantic', 'calm'],
                    'neutral': ['neutral', 'calm']
                }
                similar_emotions = emotion_mapping.get(emotion.lower(), [emotion])
                filtered_df = df[df['emotion'].str.lower().isin(similar_emotions)]

            if len(filtered_df) == 0:
                filtered_df = df

            # Rastgele 5 öneri seç
            sample = filtered_df.sample(min(5, len(filtered_df)))

            recommendations = []
            for _, row in sample.iterrows():
                rec = {
                    'title': row['title'],
                    'artist': row['artist'],
                    'emotion': row['emotion'],
                    'features': {
                        'danceability': round(row['danceability'], 3),
                        'energy': round(row['energy'], 3),
                        'valence': round(row['valence'], 3),
                        'tempo': round(row['tempo'], 1)
                    }
                }
                recommendations.append(rec)

        except Exception as e:
            print(f"Dataset okuma hatası: {e}")
            recommendations = [
                {
                    'title': 'Happy Song',
                    'artist': 'Unknown Artist',
                    'emotion': emotion,
                    'features': {'danceability': 0.8, 'energy': 0.7, 'valence': 0.9, 'tempo': 120}
                }
            ]

        # İstatistikler
        stats = {
            'total_recommendations': len(recommendations),
            'emotion': emotion,
            'avg_danceability': round(sum(r['features']['danceability'] for r in recommendations) / len(recommendations), 3),
            'avg_energy': round(sum(r['features']['energy'] for r in recommendations) / len(recommendations), 3),
            'model_info': classifier.get_model_info() if classifier else {}
        }

        # Duygu açıklaması
        emotion_descriptions = {
            'happy': 'Neşeli ve enerjik müzik önerileri',
            'sad': 'Hüzünlü ve duygusal müzik önerileri',
            'angry': 'Sert ve enerjik müzik önerileri',
            'calm': 'Sakin ve rahatlatıcı müzik önerileri',
            'energetic': 'Hareketli ve motive edici müzik önerileri',
            'romantic': 'Romantik ve duygusal müzik önerileri',
            'neutral': 'Dengeli ve orta tempolu müzik önerileri'
        }

        response = {
            'recommendations': recommendations,
            'stats': stats,
            'description': emotion_descriptions.get(emotion.lower(), 'Müzik önerileri'),
            'emotion_analysis': {
                'detected_emotion': emotion,
                'confidence': 'high',  # Basitleştirilmiş
                'mood_description': emotion_descriptions.get(emotion.lower(), '')
            }
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Sağlık kontrolü"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Modelleri başlat
    if init_models():
        print("🚀 Flask API sunucusu başlatılıyor...")
        print("📱 API: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ Modeller yüklenemedi, çıkış yapılıyor...")
        exit(1)