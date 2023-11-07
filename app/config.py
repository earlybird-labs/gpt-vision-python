from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass
class Config:
    OPENAI_KEY: str = os.getenv("OPENAI_KEY")