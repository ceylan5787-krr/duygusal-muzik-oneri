"""
Müzik Duygu Dataseti Simülasyonu - Genişletilmiş (1000 şarkı)
"""

import pandas as pd
import numpy as np
from pathlib import Path

def create_large_music_emotion_dataset():
    """1000 şarkılık müzik-duygu dataseti oluştur"""

    # Gerçekçi şarkı isimleri ve sanatçılar
    song_titles = [
        # Happy songs
        "Happy", "Walking on Sunshine", "Uptown Funk", "Can't Stop the Feeling!",
        "Happy Song", "Joyful Melody", "Sunshine Days", "Cheerful Tune",
        "Good Vibrations", "Don't Worry Be Happy", "Three Little Birds", "Here Comes the Sun",
        "Yellow", "Shake It Off", "Happy Together", "Sugar", "Valerie", "September",
        "Dancing Queen", "I Wanna Dance with Somebody", "Footloose", "Celebration",
        "Wake Me Up", "Shut Up and Dance", "Best Day Ever", "Lucky", "Smile", "Life is a Highway",
        "Walking on Sunshine", "I'm Happy Just to Dance with You", "Good Day Sunshine", "Ob-La-Di, Ob-La-Da",
        "Hey Jude", "Let It Be", "Twist and Shout", "I Saw Her Standing There",
        "All You Need is Love", "Here Comes the Sun", "Blackbird", "Yesterday",
        "Strawberry Fields Forever", "Penny Lane", "Eleanor Rigby", "Norwegian Wood",
        "Michelle", "And I Love Her", "If I Fell", "I'll Follow the Sun",
        "Nowhere Man", "Ticket to Ride", "Paperback Writer", "Day Tripper",

        # Sad songs
        "Someone Like You", "Hurt", "Yesterday", "Tears in Heaven",
        "Nothing Compares 2 U", "My Heart Will Go On", "Hallelujah", "The Greatest",
        "Skinny Love", "Hurt", "Mad World", "Everybody Hurts",
        "Creep", "Black Hole Sun", "Lithium", "Smells Like Teen Spirit",
        "Come as You Are", "Heart-Shaped Box", "In Bloom", "About a Girl",
        "Lake of Fire", "Territorial Pissings", "Serve the Servants", "Scentless Apprentice",
        "Stay Away", "Something in the Way", "Endless, Nameless", "Even in His Youth",
        "Aneurysm", "Blew", "School", "Love Buzz",
        "Negative Creep", "Dive", "Lounge Act", "Breed",
        "Polly", "Swap Meet", "Mr. Moustache", "Big Cheese",
        "Sappy", "Opinion", "Sliver", "Been a Son",

        # Angry songs
        "Break Stuff", "Killing in the Name", "Bulls on Parade", "Fight the Power",
        "Fury Unleashed", "Rage Against", "Thunderstruck", "Back in Black",
        "Welcome to the Jungle", "You Give Love a Bad Name", "Livin' on a Prayer", "Born to Be Wild",
        "Highway to Hell", "Kickstart My Heart", "Dr. Feelgood", "Girls, Girls, Girls",
        "The Final Countdown", "Jump", "Panama", "Hot for Teacher",
        "Pour Some Sugar on Me", "Photograph", "Rock of Ages", "Foolin'",
        "Double or Nothing", "Nobody's Fool", "Looks That Kill", "Home Sweet Home",
        "Smokin' in the Boys Room", "Cum on Feel the Noize", "I Love Rock 'n' Roll", "Barracuda",
        "Breaking the Law", "You've Got Another Thing Comin'", "Painkiller", "The Trooper",
        "Run to the Hills", "Hallowed Be Thy Name", "Fear of the Dark", "Iron Maiden",

        # Calm songs
        "Weightless", "River Flows in You", "Comptine d'un autre été", "Peaceful Piano",
        "Tranquil Waters", "Zen Garden", "Meditation Music", "Moonlight Sonata",
        "Nocturne Op. 9 No. 2", "Clair de Lune", "Gymnopédie No. 1", "The Swan",
        "Ave Maria", "Panis Angelicus", "Pie Jesu", "O Mio Babbino Caro",
        "Nessun Dorma", "La Bohème", "Turandot", "Madame Butterfly",
        "Rigoletto", "La Traviata", "Aida", "Otello",
        "Falstaff", "Don Carlo", "Simon Boccanegra", "Un Ballo in Maschera",
        "La Forza del Destino", "Il Trovatore", "Macbeth", "Nabucco",
        "I Lombardi", "Ernani", "I Due Foscari", "Attila",

        # Energetic songs
        "Thunderstruck", "We Will Rock You", "Eye of the Tiger", "Livin' on a Prayer",
        "High Energy", "Pump Up the Jam", "Jump", "Thunderstruck",
        "Back in Black", "Highway to Hell", "Thunderstruck", "You Shook Me All Night Long",
        "T.N.T.", "Dirty Deeds Done Dirt Cheap", "Let There Be Rock", "Whole Lotta Rosie",
        "Highway to Hell", "Girls Got Rhythm", "Walk All Over You", "Touch Too Much",
        "If You Want Blood (You've Got It)", "Let There Be Rock", "Hell Ain't a Bad Place to Be", "Problem Child",
        "Sin City", "Walk All Over You", "Bad Boy Boogie", "Overdose",
        "Hell's Bells", "Shoot to Thrill", "What Do You Do for Money Honey", "Givin' the Dog a Bone",
        "Let Me Put My Love Into You", "Rock and Roll Ain't Noise Pollution", "Jailbreak", "The Jack",
        "You Ain't Got a Hold on Me", "Show Business", "Soul Stripper", "Baby Please Don't Go",

        # Romantic songs
        "Unchained Melody", "At Last", "Fly Me to the Moon", "Love Story",
        "Perfect", "All of Me", "Thinking Out Loud", "Make You Feel My Love",
        "Wonderful Tonight", "More Than Words", "I Will Always Love You", "My Heart Will Go On",
        "Un-break My Heart", "It Must Have Been Love", "Lady in Red", "Careless Whisper",
        "Against All Odds", "Every Breath You Take", "With or Without You", "Nothing Else Matters",
        "November Rain", "Sweet Child o' Mine", "Patience", "Welcome to the Jungle",
        "Paradise City", "Don't Cry", "Civil War", "Yesterdays",
        "The Garden", "Garden of Eden", "Don't Damn Me", "Bad Apples",
        "Dead Horse", "Coma", "Breakdown", "Pretty Tied Up",

        # Neutral songs
        "Ordinary Day", "Middle Ground", "Balanced Life", "Everyday Song",
        "Normal Tune", "Standard Melody", "Regular Beat", "Common Song",
        "Average Day", "Plain Jane", "Simple Life", "Basic Beat",
        "Routine", "Normalcy", "Standard Issue", "Regular Guy",
        "Plain Song", "Basic Melody", "Simple Tune", "Common Beat",
        "Everyday Melody", "Standard Song", "Normal Tune", "Basic Rhythm",
        "Regular Song", "Plain Melody", "Simple Beat", "Common Tune",
        "Average Song", "Middle Tune", "Balanced Beat", "Everyday Rhythm",
        "Standard Tune", "Normal Song", "Basic Beat", "Regular Melody",
        "Plain Beat", "Simple Song", "Common Rhythm", "Average Tune"
    ]

    artists = [
        # Happy artists
        "Pharrell Williams", "Katrina and the Waves", "Mark Ronson ft. Bruno Mars", "Justin Timberlake",
        "Various Artists", "Unknown", "Sunshine Band", "Cheerful Artists",
        "The Beach Boys", "Bobby McFerrin", "Bob Marley", "The Beatles",
        "Coldplay", "Taylor Swift", "The Turtles", "Maroon 5", "Amy Winehouse", "Earth, Wind & Fire",
        "ABBA", "Whitney Houston", "Kenny Loggins", "Kool & The Gang",
        "Avicii", "Walk the Moon", "SpongeBob SquarePants", "Britney Spears", "Charlie Chaplin", "Rascal Flatts",
        "The Beatles", "The Beatles", "The Beatles", "The Beatles",
        "The Beatles", "The Beatles", "The Beatles", "The Beatles",
        "The Beatles", "The Beatles", "The Beatles", "The Beatles",
        "The Beatles", "The Beatles", "The Beatles", "The Beatles",
        "The Beatles", "The Beatles", "The Beatles", "The Beatles",
        "The Beatles", "The Beatles", "The Beatles", "The Beatles",

        # Sad artists
        "Adele", "Nine Inch Nails", "The Beatles", "Eric Clapton",
        "Sinead O'Connor", "Celine Dion", "Leonard Cohen", "Sia",
        "Bon Iver", "Johnny Cash", "Tears for Fears", "R.E.M.",
        "Radiohead", "Soundgarden", "Nirvana", "Nirvana",
        "Nirvana", "Nirvana", "Nirvana", "Nirvana",
        "Nirvana", "Nirvana", "Nirvana", "Nirvana",
        "Nirvana", "Nirvana", "Nirvana", "Nirvana",
        "Nirvana", "Nirvana", "Nirvana", "Nirvana",
        "Nirvana", "Nirvana", "Nirvana", "Nirvana",
        "Nirvana", "Nirvana", "Nirvana", "Nirvana",
        "Nirvana", "Nirvana", "Nirvana", "Nirvana",

        # Angry artists
        "Limp Bizkit", "Rage Against the Machine", "Rage Against the Machine", "Public Enemy",
        "Metal Band", "Rage Against", "AC/DC", "AC/DC",
        "Guns N' Roses", "Bon Jovi", "Bon Jovi", "Steppenwolf",
        "AC/DC", "Mötley Crüe", "Mötley Crüe", "Mötley Crüe",
        "Europe", "Van Halen", "Van Halen", "Van Halen",
        "Def Leppard", "Def Leppard", "Def Leppard", "Def Leppard",
        "Def Leppard", "Def Leppard", "Mötley Crüe", "Mötley Crüe",
        "Mötley Crüe", "Quiet Riot", "Joan Jett", "Heart",
        "Judas Priest", "Judas Priest", "Judas Priest", "Iron Maiden",
        "Iron Maiden", "Iron Maiden", "Iron Maiden", "Iron Maiden",

        # Calm songs
        "Marconi Union", "Yiruma", "Yann Tiersen", "Piano Artist",
        "Nature Sounds", "Zen Master", "Meditation Guru", "Ludwig van Beethoven",
        "Frédéric Chopin", "Claude Debussy", "Erik Satie", "Camille Saint-Saëns",
        "Franz Schubert", "César Franck", "Andrew Lloyd Webber", "Giacomo Puccini",
        "Giacomo Puccini", "Giacomo Puccini", "Giacomo Puccini", "Giacomo Puccini",
        "Giuseppe Verdi", "Giuseppe Verdi", "Giuseppe Verdi", "Giuseppe Verdi",
        "Giuseppe Verdi", "Giuseppe Verdi", "Giuseppe Verdi", "Giuseppe Verdi",
        "Giuseppe Verdi", "Giuseppe Verdi", "Giuseppe Verdi", "Giuseppe Verdi",
        "Giuseppe Verdi", "Giuseppe Verdi", "Giuseppe Verdi", "Giuseppe Verdi",

        # Energetic songs
        "AC/DC", "Queen", "Survivor", "Bon Jovi",
        "Technotronic", "Van Halen", "AC/DC", "AC/DC",
        "AC/DC", "AC/DC", "AC/DC", "AC/DC",
        "AC/DC", "AC/DC", "AC/DC", "AC/DC",
        "AC/DC", "AC/DC", "AC/DC", "AC/DC",
        "AC/DC", "AC/DC", "AC/DC", "AC/DC",
        "AC/DC", "AC/DC", "AC/DC", "AC/DC",
        "AC/DC", "AC/DC", "AC/DC", "AC/DC",
        "AC/DC", "AC/DC", "AC/DC", "AC/DC",
        "AC/DC", "AC/DC", "AC/DC", "AC/DC",

        # Romantic songs
        "The Righteous Brothers", "Etta James", "Frank Sinatra", "Taylor Swift",
        "Ed Sheeran", "John Legend", "Ed Sheeran", "Bob Dylan",
        "Eric Clapton", "Extreme", "Whitney Houston", "Celine Dion",
        "Toni Braxton", "Roxette", "Chris de Burgh", "Wham!",
        "Phil Collins", "The Police", "U2", "Metallica",
        "Guns N' Roses", "Guns N' Roses", "Guns N' Roses", "Guns N' Roses",
        "Guns N' Roses", "Guns N' Roses", "Guns N' Roses", "Guns N' Roses",
        "Guns N' Roses", "Guns N' Roses", "Guns N' Roses", "Guns N' Roses",
        "Guns N' Roses", "Guns N' Roses", "Guns N' Roses", "Guns N' Roses",

        # Neutral songs
        "Everyday Artist", "Normal Band", "Balance Music", "Standard Group",
        "Regular Singer", "Common Band", "Typical Artist", "Average Group",
        "Mid-level Artist", "Standard Band", "Normal Music", "Basic Group",
        "Routine Singer", "Common Band", "Standard Artist", "Regular Group",
        "Plain Singer", "Basic Band", "Simple Music", "Common Group",
        "Everyday Singer", "Standard Band", "Normal Music", "Basic Group",
        "Regular Singer", "Plain Band", "Simple Music", "Common Group",
        "Average Singer", "Middle Band", "Balanced Music", "Everyday Group",
        "Standard Singer", "Normal Band", "Basic Music", "Regular Group",
        "Plain Singer", "Simple Band", "Common Music", "Average Group"
    ]

    emotions = [
        # Happy
        *["happy"] * 56,
        # Sad
        *["sad"] * 44,
        # Angry
        *["angry"] * 40,
        # Calm
        *["calm"] * 36,
        # Energetic
        *["energetic"] * 40,
        # Romantic
        *["romantic"] * 36,
        # Neutral
        *["neutral"] * 40
    ]

    # 1000 şarkı için verileri genişlet
    n_songs = 1000
    titles = np.random.choice(song_titles, n_songs, replace=True)
    artists_list = np.random.choice(artists, n_songs, replace=True)
    emotions_list = np.random.choice(emotions, n_songs, replace=True)

    # Müzik özellikleri - duygu durumuna göre dağılım
    data = []
    for i in range(n_songs):
        emotion = emotions_list[i]

        # Duygu durumuna göre ortalama değerler
        emotion_params = {
            'happy': {'dance': (0.6, 0.9), 'energy': (0.7, 0.95), 'valence': (0.7, 0.95), 'tempo': (120, 160)},
            'sad': {'dance': (0.2, 0.5), 'energy': (0.1, 0.4), 'valence': (0.1, 0.4), 'tempo': (60, 100)},
            'angry': {'dance': (0.4, 0.7), 'energy': (0.8, 0.98), 'valence': (0.2, 0.5), 'tempo': (140, 180)},
            'calm': {'dance': (0.1, 0.4), 'energy': (0.05, 0.3), 'valence': (0.3, 0.6), 'tempo': (50, 90)},
            'energetic': {'dance': (0.5, 0.8), 'energy': (0.8, 0.98), 'valence': (0.6, 0.9), 'tempo': (150, 190)},
            'romantic': {'dance': (0.2, 0.5), 'energy': (0.2, 0.5), 'valence': (0.4, 0.7), 'tempo': (70, 110)},
            'neutral': {'dance': (0.3, 0.6), 'energy': (0.3, 0.6), 'valence': (0.3, 0.6), 'tempo': (90, 130)}
        }

        params = emotion_params.get(emotion, emotion_params['neutral'])

        song_data = {
            'title': titles[i],
            'artist': artists_list[i],
            'emotion': emotion,
            'danceability': np.clip(np.random.normal(np.mean(params['dance']), 0.1), 0, 1),
            'energy': np.clip(np.random.normal(np.mean(params['energy']), 0.1), 0, 1),
            'valence': np.clip(np.random.normal(np.mean(params['valence']), 0.1), 0, 1),
            'tempo': np.clip(np.random.normal(np.mean(params['tempo']), 10), 40, 200),
            'acousticness': np.random.uniform(0, 0.8),
            'instrumentalness': np.random.uniform(0, 0.9),
            'liveness': np.random.uniform(0, 0.8),
            'speechiness': np.random.uniform(0, 0.6)
        }
        data.append(song_data)

    df = pd.DataFrame(data)

    # Klasör oluştur
    Path('../data').mkdir(exist_ok=True)

    # CSV kaydet
    df.to_csv('../data/music_emotion.csv', index=False)
    print(f"✅ Büyük ölçekli dataset oluşturuldu: {len(df)} şarkı")
    print("Duygu dağılımı:")
    print(df['emotion'].value_counts())
    print(f"\nÖrnek veriler:\n{df.head()}")

if __name__ == '__main__':
    create_large_music_emotion_dataset()

    # Daha fazla örnek veriler
    data = {
        'title': [
            'Happy', 'Walking on Sunshine', 'Uptown Funk', 'Can\'t Stop the Feeling!',
            'Happy Song 2', 'Joyful Melody', 'Sunshine Days', 'Cheerful Tune',
            'Sad Song', 'Someone Like You', 'Hurt', 'Yesterday',
            'Tears in Heaven', 'My Heart Will Go On', 'Nothing Compares 2 U', 'Hallelujah',
            'Angry', 'Break Stuff', 'Killing in the Name', 'Bulls on Parade',
            'Fury Unleashed', 'Rage Against', 'Thunderstruck', 'Back in Black',
            'Calm', 'Weightless', 'River Flows in You', 'Comptine d\'un autre été',
            'Peaceful Piano', 'Tranquil Waters', 'Zen Garden', 'Meditation Music',
            'Energetic', 'Thunderstruck', 'We Will Rock You', 'Eye of the Tiger',
            'High Energy', 'Pump Up the Jam', 'Livin\' on a Prayer', 'Jump',
            'Romantic', 'Unchained Melody', 'At Last', 'Fly Me to the Moon',
            'Love Story', 'Perfect', 'All of Me', 'Thinking Out Loud',
            'Neutral', 'Ordinary Day', 'Middle Ground', 'Balanced Life',
            'Everyday Song', 'Normal Tune', 'Standard Melody', 'Regular Beat'
        ],
        'artist': [
            'Pharrell Williams', 'Katrina and the Waves', 'Mark Ronson ft. Bruno Mars', 'Justin Timberlake',
            'Various Artists', 'Unknown', 'Sunshine Band', 'Cheerful Artists',
            'Unknown', 'Adele', 'Nine Inch Nails', 'The Beatles',
            'Eric Clapton', 'Celine Dion', 'Sinead O\'Connor', 'Leonard Cohen',
            'Limp Bizkit', 'Rage Against the Machine', 'Rage Against the Machine', 'Rage Against the Machine',
            'Metal Band', 'Rage Against', 'AC/DC', 'AC/DC',
            'Marconi Union', 'Yiruma', 'Yann Tiersen', 'Yann Tiersen',
            'Piano Artist', 'Nature Sounds', 'Zen Master', 'Meditation Guru',
            'AC/DC', 'Queen', 'Survivor', 'Survivor',
            'Technotronic', 'Bon Jovi', 'Van Halen', 'Van Halen',
            'The Righteous Brothers', 'Etta James', 'Frank Sinatra', 'Frank Sinatra',
            'Taylor Swift', 'Ed Sheeran', 'John Legend', 'Ed Sheeran',
            'Everyday Artist', 'Normal Band', 'Balance Music', 'Standard Group',
            'Regular Singer', 'Common Band', 'Typical Artist', 'Average Group'
        ],
        'emotion': [
            'happy', 'happy', 'happy', 'happy',
            'happy', 'happy', 'happy', 'happy',
            'sad', 'sad', 'sad', 'sad',
            'sad', 'sad', 'sad', 'sad',
            'angry', 'angry', 'angry', 'angry',
            'angry', 'angry', 'energetic', 'energetic',
            'calm', 'calm', 'calm', 'calm',
            'calm', 'calm', 'calm', 'calm',
            'energetic', 'energetic', 'energetic', 'energetic',
            'energetic', 'energetic', 'energetic', 'energetic',
            'romantic', 'romantic', 'romantic', 'romantic',
            'romantic', 'romantic', 'romantic', 'romantic',
            'neutral', 'neutral', 'neutral', 'neutral',
            'neutral', 'neutral', 'neutral', 'neutral'
        ],
        'danceability': np.random.uniform(0.3, 0.9, 56),
        'energy': np.random.uniform(0.2, 0.95, 56),
        'valence': np.random.uniform(0.1, 0.9, 56),
        'tempo': np.random.uniform(60, 180, 56),
        'acousticness': np.random.uniform(0, 0.8, 56),
        'instrumentalness': np.random.uniform(0, 0.9, 56),
        'liveness': np.random.uniform(0, 0.8, 56),
        'speechiness': np.random.uniform(0, 0.6, 56)
    }

    df = pd.DataFrame(data)

    # Klasör oluştur
    Path('../data').mkdir(exist_ok=True)

    # CSV kaydet
    df.to_csv('../data/music_emotion.csv', index=False)
    print(f"✅ Büyük ölçekli dataset oluşturuldu: {len(df)} şarkı")
    print("Duygu dağılımı:")
    print(df['emotion'].value_counts())
    print(f"\nÖrnek veriler:\n{df.head()}")

if __name__ == '__main__':
    create_large_music_emotion_dataset()