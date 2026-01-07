import sqlite3
import json

class AdvancedCoralDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('advanced_coral.db')
        self.create_tables()
        self.populate_coral_species()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Coral species with full taxonomy
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS coral_species (
                id INTEGER PRIMARY KEY,
                common_name TEXT,
                scientific_name TEXT,
                family TEXT,
                genus TEXT,
                morphology TEXT,
                bleaching_resistance TEXT,
                conservation_status TEXT,
                color_patterns TEXT,
                typical_size_cm INTEGER,
                image_features TEXT
            )
        ''')
        
        # Analysis results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                timestamp TEXT,
                predicted_species TEXT,
                confidence REAL,
                health_status TEXT,
                health_confidence REAL,
                bleaching_percentage REAL,
                family TEXT,
                genus TEXT,
                insights_json TEXT
            )
        ''')
        
        self.conn.commit()
    
    def populate_coral_species(self):
        """Real coral species data"""
        corals = [
            # Acroporidae family (branching)
            ("Staghorn Coral", "Acropora cervicornis", "Acroporidae", "Acropora", 
             "Branching", "Low", "Critically Endangered", "Brown/Yellow", 300,
             "Thick branches, antler-like"),
            
            ("Elkhorn Coral", "Acropora palmata", "Acroporidae", "Acropora",
             "Branching", "Low", "Critically Endangered", "Golden brown", 350,
             "Flat branches, elk antler shape"),
            
            ("Table Coral", "Acropora hyacinthus", "Acroporidae", "Acropora",
             "Plate/Table", "Medium", "Vulnerable", "Blue/Purple", 200,
             "Horizontal plates, tiered"),
            
            # Poritidae family (boulder)
            ("Great Star Coral", "Montastraea cavernosa", "Merulinidae", "Montastraea",
             "Boulder", "Medium", "Vulnerable", "Green/Brown", 150,
             "Massive, star-shaped polyps"),
            
            ("Mustard Hill Coral", "Porites astreoides", "Poritidae", "Porites",
             "Boulder", "High", "Least Concern", "Yellow/Green", 100,
             "Small mounds, mustard color"),
            
            ("Brain Coral", "Diploria labyrinthiformis", "Merulinidae", "Diploria",
             "Boulder", "High", "Near Threatened", "Brown/Green", 180,
             "Grooved like brain"),
            
            # Other families
            ("Leaf Coral", "Pavona decussata", "Agariciidae", "Pavona",
             "Plate", "Medium", "Least Concern", "Cream/Brown", 120,
             "Leaf-like plates"),
            
            ("Flower Coral", "Mussa angulosa", "Faviidae", "Mussa",
             "Boulder", "Low", "Vulnerable", "Red/Orange", 80,
             "Large fleshy polyps"),
            
            ("Soft Coral", "Sinularia flexibilis", "Alcyoniidae", "Sinularia",
             "Soft", "Medium", "Data Deficient", "Various", 150,
             "Flexible, tree-like")
        ]
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM coral_species")
        if cursor.fetchone()[0] == 0:
            cursor.executemany('''
                INSERT INTO coral_species 
                (common_name, scientific_name, family, genus, morphology, 
                 bleaching_resistance, conservation_status, color_patterns, 
                 typical_size_cm, image_features)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', corals)
            self.conn.commit()
    
    def identify_coral(self, image_features):
        """
        Identify coral based on features
        Returns: species_info, confidence
        """
        cursor = self.conn.cursor()
        
        # For demo: match based on features
        if "branch" in image_features.lower():
            cursor.execute("SELECT * FROM coral_species WHERE morphology='Branching' LIMIT 1")
        elif "boulder" in image_features.lower() or "massive" in image_features.lower():
            cursor.execute("SELECT * FROM coral_species WHERE morphology='Boulder' LIMIT 1")
        elif "plate" in image_features.lower() or "table" in image_features.lower():
            cursor.execute("SELECT * FROM coral_species WHERE morphology='Plate/Table' LIMIT 1")
        else:
            cursor.execute("SELECT * FROM coral_species LIMIT 1")
        
        result = cursor.fetchone()
        if result:
            # Convert to dictionary
            keys = ['id', 'common_name', 'scientific_name', 'family', 'genus', 
                   'morphology', 'bleaching_resistance', 'conservation_status',
                   'color_patterns', 'typical_size_cm', 'image_features']
            species_info = dict(zip(keys, result))
            
            # Simulate confidence based on features match
            confidence = 85.5  # Base confidence
            
            return species_info, confidence
        
        return None, 0
    
    def save_analysis(self, analysis_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO analyses 
            (filename, timestamp, predicted_species, confidence, health_status,
             health_confidence, bleaching_percentage, family, genus, insights_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            analysis_data['filename'],
            analysis_data['timestamp'],
            analysis_data['predicted_species'],
            analysis_data['confidence'],
            analysis_data['health_status'],
            analysis_data['health_confidence'],
            analysis_data['bleaching_percentage'],
            analysis_data['family'],
            analysis_data['genus'],
            json.dumps(analysis_data['insights'])
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_species(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM coral_species")
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = AdvancedCoralDatabase()
    print("✅ Advanced coral database created!")
    print("📊 Species in database:")
    
    species = db.get_all_species()
    for s in species:
        print(f"  - {s[1]} ({s[3]}) - {s[5]}")
    
    db.close()