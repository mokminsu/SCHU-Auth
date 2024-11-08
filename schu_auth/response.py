from dataclasses import dataclass

@dataclass
class AuthResponse:
    user_id: str
    name: str
    gender: str
    major: str
    grade: str
    professor: str

    def __str__(self):
        return (f'AuthResponse(user_id={self.user_id}, name={self.name}, major={self.major}, grade={self.grade}, professor={self.professor})')
