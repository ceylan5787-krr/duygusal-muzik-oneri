"""
Gelişmiş Duygu Sınıflandırma Modeli
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
import joblib
import os

class EmotionClassifier:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.df = None
        self.model_path = 'models/emotion_classifier.pkl'
        self.scaler_path = 'models/scaler.pkl'

    def prepare_data(self):
        """Veriyi hazırla ve ön işleme yap"""
        try:
            self.df = pd.read_csv('../data/music_emotion.csv')

            # Ek özellikler hesapla
            self.df['energy_valence_ratio'] = self.df['energy'] / (self.df['valence'] + 0.001)
            self.df['tempo_energy'] = self.df['tempo'] * self.df['energy']
            self.df['acoustic_dance'] = self.df['acousticness'] * self.df['danceability']

            # Duygu mapping'i genişlet
            emotion_mapping = {
                'happy': 0,
                'sad': 1,
                'angry': 2,
                'calm': 3,
                'energetic': 4,
                'romantic': 5,
                'neutral': 6
            }
            self.df['emotion_encoded'] = self.df['emotion'].map(emotion_mapping)

            print(f"✅ Veri hazırlandı: {len(self.df)} şarkı, {len(self.df.columns)} özellik")
            print(f"   Duygu dağılımı: {self.df['emotion'].value_counts().to_dict()}")

        except Exception as e:
            print(f"❌ Veri hazırlama hatası: {e}")
            self.df = pd.DataFrame()

    def train_advanced_model(self):
        """Gelişmiş model eğitimi"""
        if self.df is None or len(self.df) == 0:
            print("❌ Veri yok, model eğitilemiyor")
            return

        # Özellikler
        features = [
            'danceability', 'energy', 'valence', 'tempo', 'acousticness',
            'instrumentalness', 'liveness', 'speechiness',
            'energy_valence_ratio', 'tempo_energy', 'acoustic_dance'
        ]

        X = self.df[features]
        y = self.df['emotion_encoded']

        # Eğitim/test böl
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Pipeline oluştur
        self.model = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            ))
        ])

        # Model eğitimi
        self.model.fit(X_train, y_train)

        # Tahmin ve değerlendirme
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5)

        print(f"✅ Gelişmiş model eğitildi!")
        print(f"   Test Doğruluğu: {accuracy:.3f}")
        print(f"   CV Ortalama: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        print(f"\nSınıflandırma Raporu:\n{classification_report(y_test, y_pred)}")

        # Modeli kaydet
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, self.model_path)
        print(f"✅ Model kaydedildi: {self.model_path}")

    def train_random_forest(self):
        """Basit Random Forest modeli (fallback)"""
        if self.df is None or len(self.df) == 0:
            print("❌ Veri yok, model eğitilemiyor")
            return

        # Özellikler
        features = ['danceability', 'energy', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'liveness', 'speechiness']
        X = self.df[features]
        y = self.df['emotion_encoded']

        # Eğitim/test böl
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model oluştur
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Tahmin
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"✅ Temel model eğitildi. Doğruluk: {accuracy:.3f}")

    def load_model(self):
        """Kaydedilmiş modeli yükle"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print("✅ Model yüklendi")
                return True
        except Exception as e:
            print(f"❌ Model yükleme hatası: {e}")
        return False

    def predict_emotion(self, features):
        """Gelişmiş duygu tahmin et"""
        if self.model is None:
            if not self.load_model():
                return 'neutral'

        try:
            # Özellikleri genişlet
            features_extended = features.copy()
            features_extended.extend([
                features[1] / (features[2] + 0.001),  # energy_valence_ratio
                features[3] * features[1],  # tempo_energy
                features[4] * features[0]   # acoustic_dance
            ])

            prediction = self.model.predict([features_extended])

            # Ters mapping
            emotion_mapping_reverse = {
                0: 'happy',
                1: 'sad',
                2: 'angry',
                3: 'calm',
                4: 'energetic',
                5: 'romantic',
                6: 'neutral'
            }

            return emotion_mapping_reverse.get(prediction[0], 'neutral')

        except Exception as e:
            print(f"❌ Tahmin hatası: {e}")
            return 'neutral'

    def get_model_info(self):
        """Model bilgilerini döndür"""
        if self.df is None:
            return {}

        emotion_counts = self.df['emotion'].value_counts().to_dict()
        total_songs = len(self.df)

        return {
            'total_songs': total_songs,
            'emotion_distribution': emotion_counts,
            'features_count': len(self.df.columns) - 2,  # emotion ve encoded hariç
            'model_type': 'GradientBoosting' if hasattr(self.model, 'named_steps') else 'RandomForest'
        }