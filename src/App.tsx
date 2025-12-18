import { useState } from 'react'
import './App.css'

interface Question {
  id: number;
  text: string;
  reverse: boolean; // true if higher score means lower emotion
}

const questions: Question[] = [
  { id: 1, text: "Bugün kendinizi ne kadar mutlu hissediyorsunuz?", reverse: false },
  { id: 2, text: "Stresli veya endişeli misiniz?", reverse: true },
  { id: 3, text: "Enerjik ve canlı hissediyor musunuz?", reverse: false },
  { id: 4, text: "Üzgün veya melankolik misiniz?", reverse: true },
  { id: 5, text: "Rahat ve huzurlu musunuz?", reverse: false },
  { id: 6, text: "Sinirli veya kızgın hissediyor musunuz?", reverse: true },
  { id: 7, text: "Motivasyonlu ve istekli misiniz?", reverse: false },
  { id: 8, text: "Yorgun veya bitkin misiniz?", reverse: true },
  { id: 9, text: "Neşeli ve eğlenceli hissediyor musunuz?", reverse: false },
  { id: 10, text: "Kaygılı veya gergin misiniz?", reverse: true }
];

interface Recommendation {
  title: string;
  artist: string;
  emotion: string;
  features: {
    danceability: number;
    energy: number;
    valence: number;
    tempo: number;
  };
}

interface Stats {
  total_recommendations: number;
  emotion: string;
  avg_danceability: number;
  avg_energy: number;
  model_info: {
    total_songs?: number;
    emotion_distribution?: Record<string, number>;
    features_count?: number;
    model_type?: string;
  };
}

interface EmotionAnalysis {
  detected_emotion: string;
  confidence: string;
  mood_description: string;
}

interface ApiResponse {
  recommendations: Recommendation[];
  stats: Stats;
  description: string;
  emotion_analysis: EmotionAnalysis;
}

function App() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [emotionAnalysis, setEmotionAnalysis] = useState<EmotionAnalysis | null>(null);
  const [description, setDescription] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const handleAnswer = (score: number) => {
    const newAnswers = [...answers, score];
    setAnswers(newAnswers);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      // Test tamamlandı, öneri al
      getRecommendations(newAnswers);
    }
  };

  const getRecommendations = async (answers: number[]) => {
    setLoading(true);
    try {
      // Puan hesapla (reverse sorular için 6-score)
      const totalScore = answers.reduce((sum, score, index) => {
        const question = questions[index];
        const adjustedScore = question.reverse ? 6 - score : score;
        return sum + adjustedScore;
      }, 0);

      // Duygu belirle
      let emotion = 'neutral';
      if (totalScore <= 20) emotion = 'sad';
      else if (totalScore <= 35) emotion = 'neutral';
      else emotion = 'happy';

      const response = await fetch('http://localhost:5000/api/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ emotion }),
      });

      if (response.ok) {
        const data: ApiResponse = await response.json();
        setRecommendations(data.recommendations || []);
        setStats(data.stats);
        setEmotionAnalysis(data.emotion_analysis);
        setDescription(data.description);
      } else {
        console.error('Backend error');
        // Fallback: örnek öneriler
        setRecommendations([
          {
            title: 'Happy Song',
            artist: 'Artist',
            emotion: 'happy',
            features: { danceability: 0.8, energy: 0.7, valence: 0.9, tempo: 120 }
          },
          {
            title: 'Sad Song',
            artist: 'Artist',
            emotion: 'sad',
            features: { danceability: 0.3, energy: 0.2, valence: 0.2, tempo: 80 }
          },
          {
            title: 'Neutral Song',
            artist: 'Artist',
            emotion: 'neutral',
            features: { danceability: 0.5, energy: 0.5, valence: 0.5, tempo: 100 }
          }
        ]);
        setStats({
          total_recommendations: 3,
          emotion: emotion,
          avg_danceability: 0.533,
          avg_energy: 0.467,
          model_info: { total_songs: 24, features_count: 11 }
        });
        setEmotionAnalysis({
          detected_emotion: emotion,
          confidence: 'medium',
          mood_description: 'Duygu durumunuza uygun müzik önerileri'
        });
        setDescription('Müzik önerileri');
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setRecommendations([]);
    }
    setLoading(false);
  };

  const resetTest = () => {
    setCurrentQuestion(0);
    setAnswers([]);
    setRecommendations([]);
    setStats(null);
    setEmotionAnalysis(null);
    setDescription('');
  };

  if (loading) {
    return (
      <div className="app">
        <h1>🎵 Müzik Duygu Öneri Sistemi</h1>
        <div className="loading">Öneriler yükleniyor...</div>
      </div>
    );
  }

  if (recommendations.length > 0) {
    return (
      <div className="app">
        <h1>🎵 Müzik Önerileriniz</h1>

        {emotionAnalysis && (
          <div className="emotion-summary">
            <h2>📊 Duygu Analizi</h2>
            <p><strong>Tespit Edilen Duygu:</strong> {emotionAnalysis.detected_emotion.toUpperCase()}</p>
            <p><strong>Güven Seviyesi:</strong> {emotionAnalysis.confidence}</p>
            <p><strong>Açıklama:</strong> {emotionAnalysis.mood_description}</p>
          </div>
        )}

        {stats && (
          <div className="stats-summary">
            <h2>📈 İstatistikler</h2>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Toplam Öneri:</span>
                <span className="stat-value">{stats.total_recommendations}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Ort. Dans Edilebilirlik:</span>
                <span className="stat-value">{stats.avg_danceability}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Ort. Enerji:</span>
                <span className="stat-value">{stats.avg_energy}</span>
              </div>
              {stats.model_info.total_songs && (
                <div className="stat-item">
                  <span className="stat-label">Dataset Şarkı Sayısı:</span>
                  <span className="stat-value">{stats.model_info.total_songs}</span>
                </div>
              )}
            </div>
          </div>
        )}

        <div className="recommendations">
          {recommendations.map((rec, index) => (
            <div key={index} className="recommendation-card">
              <h3>{rec.title}</h3>
              <p className="artist">{rec.artist}</p>
              <span className="emotion">{rec.emotion}</span>

              <div className="features">
                <h4>🎵 Müzik Özellikleri</h4>
                <div className="feature-grid">
                  <div className="feature-item">
                    <span className="feature-label">Dans Edilebilirlik:</span>
                    <div className="feature-bar">
                      <div
                        className="feature-fill"
                        style={{ width: `${rec.features.danceability * 100}%` }}
                      ></div>
                    </div>
                    <span className="feature-value">{rec.features.danceability}</span>
                  </div>
                  <div className="feature-item">
                    <span className="feature-label">Enerji:</span>
                    <div className="feature-bar">
                      <div
                        className="feature-fill"
                        style={{ width: `${rec.features.energy * 100}%` }}
                      ></div>
                    </div>
                    <span className="feature-value">{rec.features.energy}</span>
                  </div>
                  <div className="feature-item">
                    <span className="feature-label">Pozitiflik:</span>
                    <div className="feature-bar">
                      <div
                        className="feature-fill"
                        style={{ width: `${rec.features.valence * 100}%` }}
                      ></div>
                    </div>
                    <span className="feature-value">{rec.features.valence}</span>
                  </div>
                  <div className="feature-item">
                    <span className="feature-label">Tempo:</span>
                    <span className="feature-value">{rec.features.tempo} BPM</span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
        <button onClick={resetTest} className="reset-btn">Tekrar Test Yap</button>
      </div>
    );
  }

  return (
    <div className="app">
      <h1>🎵 Müzik Duygu Testi</h1>
      <div className="progress">
        Soru {currentQuestion + 1} / {questions.length}
      </div>
      <div className="question">
        <h2>{questions[currentQuestion].text}</h2>
        <div className="options">
          {[1, 2, 3, 4, 5].map(score => (
            <button
              key={score}
              onClick={() => handleAnswer(score)}
              className="option-btn"
            >
              {score}
            </button>
          ))}
        </div>
        <div className="scale">
          <span>Hiç</span>
          <span>Çok Az</span>
          <span>Orta</span>
          <span>Çok</span>
          <span>Çok Fazla</span>
        </div>
      </div>
    </div>
  );
}

export default App
