from TelegramAdmin.models import User
from django.utils import timezone
from Log.Log import Log


class UserController:
    def __init__(self):
        self.logger = Log("AdminController")
        self.STATES = dict()
        self.NEXT_STATES = dict()

    def update_create_user(self, chat):
        try:
            user = User.objects.filter(chat_id=chat.id).first()
            if user:
                user.last_checked_bot = timezone.now()
                user.state = self.NEXT_STATES[user.state]
                user.save(force_update=True)
                return user
            else:
                self.logger.info("New User start subX : \n{}".format(chat))
                username = chat.username
                last_name = chat.last_name
                first_name = chat.first_name
                new_user = User(chat_id=chat.id,
                                username=username,
                                first_name=first_name,
                                last_name=last_name,
                                chat_type=chat.type)
                new_user.save(force_insert=True)
                return user
        except Exception as e:
            self.logger.error("update_create_user : {}".format(e))

    def update_user_state(self, chat_id, user=None):
        if user is None:
            user = User.objects.filter(chat_id=chat_id).first()
            if not user:
                raise NotImplementedError("user {} not implemented".format(chat_id))
        user.state = self.NEXT_STATES[user.state]
        user.save(force_update=True)
        return user.state

    @staticmethod
    def get_user_state(chat_id):
        return User.filter.objects(chat_id=chat_id).first().state

    def set_states(self, states):
        self.STATES = states

    def set_next_states_dict(self, next_states):
        self.NEXT_STATES = next_states
