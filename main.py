import re
import unittest
import uuid


class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass


class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note
 

class User:

    def __init__(self, username, balance, credit_card_number,):
        self.credit_card_number = credit_card_number
        self.balance = balance
        self.feed = []
        self.friends = []
        
        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')


    def retrieve_feed(self):
        return self.feed

    def retrieve_friends(self):
        return self.friends
      
    def add_friend(self, new_friend):
        self.friends.append(new_friend)
        self._add_friend_on_feed(new_friend)

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        if target.balance < amount:
          self.pay_with_card(target, amount, note)
        else:
          self.pay_with_balance(target, amount, note)
                    
        self._add_payment_on_feed(target, amount, note)
    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        elif self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment

    def pay_with_balance(self, target, amount, note):
        self.balance -= amount
        
        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        elif self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')
          
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)
        
        return payment

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass
    
    def _add_payment_on_feed(self, target, amount, note):
        self.feed.append(f"{self.username} paid {target.username} {amount:.2f} for {note}")           
    def _add_friend_on_feed(self, new_friend):
        self.feed.append(f"{self.username} added {new_friend.username} as friends")      

class MiniVenmo:
    
    def create_user(self, username, balance, credit_card_number):
        user = User(username, balance, credit_card_number)
        return user

    def render_info(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        for item in feed:
          print(item)

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")

        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_info(feed)

        bobby.add_friend(carol)


class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()

    def test_user_creation(self):
      venmo = MiniVenmo()
      user = venmo.create_user("joedoe", 500.00, "4111111111111111")
      assert user.username == "joedoe"
      assert user.credit_card_number == "4111111111111111"
      assert user.balance == 500.00
      
    def test_venmo_payment(self):
      venmo = MiniVenmo()
      joe1 = venmo.create_user("joe1", 5.00, "4111111111111111")
      joe2 = venmo.create_user("joe2", 10.00, "4242424242424242")
      
      joe1.pay(joe2, 5.00, "Coffee")
      
      assert joe1.balance == 0.00
      
    def test_venmo_payment_without_sufficient_credit(self):
      venmo = MiniVenmo()
      joe1 = venmo.create_user("joe1", 5.00, "4111111111111111")
      joe2 = venmo.create_user("joe2", 10.00, "4242424242424242")
      
      joe1.pay(joe2, 15.00, "Coffee")
      
      assert joe1.balance == 5.00
      
    def test_feed(self):
      venmo = MiniVenmo()
      joe1 = venmo.create_user("joe1", 5.00, "4111111111111111")
      joe2 = venmo.create_user("joe2", 10.00, "4242424242424242")
      
      joe1.pay(joe2, 5.00, "Coffee")
      feed = joe1.retrieve_feed()
      
      assert feed == ['joe1 paid joe2 5.00 for Coffee']

    def test_add_friend(self):
      venmo = MiniVenmo()
      joe1 = venmo.create_user("joe1", 5.00, "4111111111111111")
      joe2 = venmo.create_user("joe2", 10.00, "4242424242424242")
      
      joe1.add_friend(joe2)
      
      assert joe2 in joe1.retrieve_friends()
      

if __name__ == '__main__':
    unittest.main()
