import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base, engine
import models  # ensure all models are imported

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    print("Reset completed successfully!")