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
    def bcrypt_password(password):
        salt=bcrypt.gensalt(10)
        new_password=bcrypt.hash(password,salt)
        return new_password
    
    @staticmethod
    def generate(password):
        
        salt=bcrypt.gensalt()
        #print(salt)
        hashed=bcrypt.hashpw(password.encode(),salt)
        print(hashed)
        return hashed
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify if the provided plain text password matches the stored hashed password.
        
        :param plain_password: The plain text password to verify
        :param hashed_password: The stored hashed password
        :return: True if the passwords match, False otherwise
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
