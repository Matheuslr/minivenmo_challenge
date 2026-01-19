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
        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')


    def retrieve_feed(self):
        # TODO: add code here
        return []

    def add_friend(self, new_friend):
        # TODO: add code here
        pass

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
          self.pay_with_card
        else:
          target.balance -= amount   
          
        self.feed.append(f"{self.username} paid {target.username} {amount} for {note}")     

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
        # TODO: add code here
        pass

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass


class MiniVenmo:
    
    def create_user(self, username, balance, credit_card_number):
        user = User(username, balance, credit_card_number)
        return user

    def render_feed(self, feed):
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch
        # TODO: add code here
        pass

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
        venmo.render_feed(feed)

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
      
      assert joe2.balance == 5.00
    
if __name__ == '__main__':
    unittest.main()
