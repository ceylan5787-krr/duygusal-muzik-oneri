"""
Müzik Öneri Sistemi
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class MusicRecommender:
    def __init__(self):
        self.df = None
        self.load_data()

    def load_data(self):
        """Veriyi yükle"""
        try:
            self.df = pd.read_csv('../data/music_emotion.csv')
            print(f"✅ Veri yüklendi: {len(self.df)} şarkı")
        except Exception as e:
            print(f"❌ Veri yükleme hatası: {e}")
            self.df = pd.DataFrame()

    def recommend_by_emotion(self, emotion, n=5):
        """Duygu durumuna göre öneri"""
        if self.df is None or len(self.df) == 0:
            return []

        # Duygu durumuna göre filtrele
        filtered = self.df[self.df['emotion'].str.lower() == emotion.lower()]

        if len(filtered) == 0:
            # Eğer yoksa rastgele öner
            filtered = self.df

        # Rastgele n şarkı seç
        recommendations = filtered.sample(min(n, len(filtered)))

        return recommendations[['title', 'artist', 'emotion']].to_dict('records')