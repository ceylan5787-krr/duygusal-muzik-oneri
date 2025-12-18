import { useState } from 'react';
import './App.css';

interface Question {
  id: number;
  text: string;
  reverse: boolean;
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

const calculateEmotion = (answers: number[]): string => {
  const emotionScores = {
    happy: (answers[0] + answers[8]) / 2,
    sad: (6 - answers[3]) / 1,
    angry: (6 - answers[5]) / 1,
    calm: (answers[4] + (6 - answers[9])) / 2,
    energetic: (answers[2] + answers[6]) / 2,
    romantic: 0,
    neutral: 0
  };

  const stressFactor = (6 - answers[1] + 6 - answers[9]) / 2;
  const fatigueFactor = (6 - answers[7]) / 1;

  emotionScores.sad += stressFactor * 0.3;
  emotionScores.angry += stressFactor * 0.4;
  emotionScores.calm += fatigueFactor * 0.5;
  emotionScores.energetic -= fatigueFactor * 0.3;

  let maxEmotion = 'neutral';
  let maxScore = 0;

  Object.entries(emotionScores).forEach(([emotion, score]) => {
    if (score > maxScore) {
      maxScore = score;
      maxEmotion = emotion;
    }
  });

  return maxEmotion;
};

function App() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState<number[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [emotionAnalysis, setEmotionAnalysis] = useState<EmotionAnalysis | null>(null);
  const [loading, setLoading] = useState(false);

  const handleAnswer = (score: number) => {
    const newAnswers = [...answers, score];
    setAnswers(newAnswers);

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      getRecommendations(newAnswers);
    }
  };

  const getRecommendations = async (answers: number[]) => {
    setLoading(true);
    try {
      const emotion = calculateEmotion(answers);
      // API çağrısı
      const response = await fetch('http://localhost:5000/api/recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ emotion }),
      });

      if (response.ok) {
        const data: ApiResponse = await response.json();
        setRecommendations(data.recommendations || []);
        setStats(data.stats);
        setEmotionAnalysis(data.emotion_analysis);
      } else {
        throw new Error("API hatası");
      }
    } catch (error) {
      console.error('Error:', error);
      // Fallback: API çalışmazsa örnek veri göster
      const fallbackEmotion = calculateEmotion(answers);
      setRecommendations([
        { title: 'Demo Song 1', artist: 'Artist A', emotion: fallbackEmotion, features: { danceability: 0.8, energy: 0.7, valence: 0.9, tempo: 120 } },
        { title: 'Demo Song 2', artist: 'Artist B', emotion: 'neutral', features: { danceability: 0.5, energy: 0.5, valence: 0.5, tempo: 100 } }
      ]);
      setStats({
        total_recommendations: 2,
        emotion: fallbackEmotion,
        avg_danceability: 0.65,
        avg_energy: 0.60,
        model_info: {
          total_songs: 1000,
          features_count: 11,
          model_type: 'RandomForest (Demo)',
          emotion_distribution: {
            happy: 190, sad: 173, neutral: 139, angry: 139,
            energetic: 124, romantic: 122, calm: 113
          }
        }
      });
      setEmotionAnalysis({
        detected_emotion: fallbackEmotion,
        confidence: 'medium',
        mood_description: 'API bağlantısı kurulamadı, demo modu aktif.'
      });
    }
    setLoading(false);
  };

  const resetTest = () => {
    setCurrentQuestion(0);
    setAnswers([]);
    setRecommendations([]);
    setStats(null);
    setEmotionAnalysis(null);
  };

  // Dataset dağılımını sıralamak için yardımcı fonksiyon
  const getSortedDistribution = () => {
    if (!stats?.model_info?.emotion_distribution) return [];
    return Object.entries(stats.model_info.emotion_distribution)
      .sort(([, a], [, b]) => b - a); // Sayıya göre azalan sıralama
  };

  if (loading) {
    return (
      <div className="main-container">
        <div className="app-card loading-container">
          <div className="spinner"></div>
          <h2>Analiz Yapılıyor...</h2>
          <p>Sizin için en uygun şarkıları seçiyoruz.</p>
        </div>
      </div>
    );
  }

  if (recommendations.length > 0) {
    return (
      <div className="main-container">
        <div className="results-wrapper">
          <h1 className="main-title">🎵 Müzik Önerileriniz</h1>
          
          {emotionAnalysis && (
            <div className="result-card analysis-card">
              <h3>Duygu Durumu</h3>
              <div className="emotion-badge-large">{emotionAnalysis.detected_emotion.toUpperCase()}</div>
              <p className="mood-desc">{emotionAnalysis.mood_description}</p>
            </div>
          )}

          <div className="result-card recommendations-card">
            <h3>Önerilen Şarkılar</h3>
            <div className="song-list">
              {recommendations.slice(0, 5).map((rec, index) => (
                <div key={index} className="song-item">
                  <div className="song-content">
                    <div className="song-title">{rec.title}</div>
                    <div className="song-artist">{rec.artist}</div>
                  </div>
                  <div className="song-tags">
                    <span className="tag bpm">{rec.features.tempo} BPM</span>
                    <span className="tag mood">Mod: %{(rec.features.valence * 100).toFixed(0)}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {stats && (
            <div className="result-card stats-card-detailed">
              <h3>📊 İstatistikler & Veri Analizi</h3>
              
              {/* Bölüm 1: Öneri Özeti */}
              <div className="stats-section">
                <h4>Öneri Özeti</h4>
                <div className="stats-grid-mini">
                  <div className="stat-box-mini">
                    <span className="stat-label">Ort. Enerji</span>
                    <span className="stat-val">%{(stats.avg_energy * 100).toFixed(0)}</span>
                  </div>
                  <div className="stat-box-mini">
                    <span className="stat-label">Ort. Dans</span>
                    <span className="stat-val">%{(stats.avg_danceability * 100).toFixed(0)}</span>
                  </div>
                  <div className="stat-box-mini">
                    <span className="stat-label">Model</span>
                    <span className="stat-val" style={{fontSize: '0.8rem'}}>{stats.model_info.model_type || 'N/A'}</span>
                  </div>
                </div>
              </div>

              {/* Bölüm 2: Dataset Bilgileri */}
              {stats.model_info.emotion_distribution && (
                <div className="stats-section dataset-section">
                  <h4>Dataset Analizi ({stats.model_info.total_songs} Şarkı)</h4>
                  <p className="dataset-subtitle">Modelin eğitildiği veri setindeki duygu dağılımı:</p>
                  
                  <div className="distribution-chart">
                    {getSortedDistribution().map(([emotion, count]) => {
                      // Yüzdelik hesaplama (Toplam şarkı sayısına göre)
                      const total = stats.model_info.total_songs || 1;
                      const percent = ((count / total) * 100).toFixed(1);
                      
                      return (
                        <div key={emotion} className="dist-row">
                          <div className="dist-label">
                            <span className="d-name">{emotion.charAt(0).toUpperCase() + emotion.slice(1)}</span>
                            <span className="d-count">{count} şarkı</span>
                          </div>
                          <div className="dist-bar-bg">
                            <div 
                              className="dist-bar-fill" 
                              style={{ 
                                width: `${percent}%`,
                                backgroundColor: emotion === stats.emotion ? '#667eea' : '#a3bffa'
                              }}
                            ></div>
                          </div>
                          <span className="dist-percent">%{percent}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
            </div>
          )}

          <button onClick={resetTest} className="primary-btn reset-btn">Yeniden Test Yap</button>
        </div>
      </div>
    );
  }

  return (
    <div className="main-container">
      <div className="app-card question-card">
        <div className="progress-container">
          <div className="progress-bar-bg">
            <div 
              className="progress-bar-fill" 
              style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
            ></div>
          </div>
          <span className="progress-text">{currentQuestion + 1} / {questions.length}</span>
        </div>

        <h2 className="question-text">{questions[currentQuestion].text}</h2>
        
        <div className="options-container">
          {[1, 2, 3, 4, 5].map(score => (
            <button
              key={score}
              onClick={() => handleAnswer(score)}
              className="option-circle"
            >
              {score}
            </button>
          ))}
        </div>
        
        <div className="scale-legend">
          <span>Hiç</span>
          <span>Çok Fazla</span>
        </div>
      </div>
    </div>
  );
}

export default App;