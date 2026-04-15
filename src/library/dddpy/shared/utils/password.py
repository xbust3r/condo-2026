from password_strength import PasswordPolicy, PasswordStats

import bcrypt

class password():
    
    @staticmethod
    def check_policies(password):
        policy = PasswordPolicy.from_names(
            length=8,  # min length: 8
            uppercase=1,  # need min. 2 uppercase letters
            numbers=1,  # need min. 2 digits
            #special=1,  # need min. 2 special characters
            #nonletters=1,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        return policy.test(password)
    
    @staticmethod
    def check_stats(password):
        
        stats=PasswordStats(password)
        return stats.strength()
    
    @staticmethod
    def bcrypt_password(password: str) -> str:
        """Hash a password and return the hash as a string."""
        salt = bcrypt.gensalt(10)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def generate(password: str) -> str:
        """Hash a password using default salt and return as string."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify if the provided plain text password matches the stored hashed password.
        Normalizes hashed_password to bytes before comparison.
        """
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
