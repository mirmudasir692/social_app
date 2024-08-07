from django.db import models
from moments.models import Moment
from blog.models import Blog
from accounts.models import User
from django.db.models import Q, F, BooleanField, Case, When, Value
from utils.chatsystem import decrypt_message, encrypt_message


class MessageGroupManager(models.Manager):
    def get_group(self, user1_id, user2_id):
        users = sorted([user1_id, user2_id])
        name = f"msgxid${users[0]}&{users[1]}"
        group = None
        try:
            group = self.get(name=name)
        except self.model.DoesNotExist:
            self.create(name=name, user1_id=user1_id, user2_id=user2_id)
        return group


    def get_groups(self, user_id):
        groups = self.filter(Q(user1_id=user_id) | Q(user2_id=user_id))
        print("groups", groups)
        return groups

    def allocate_user(self, user_id, group):
        print("sender", group.user1.id)
        print("receiver", group.user2.id)
        print("user_id", user_id)

        if group.user1.id == user_id:
            print("allocated")
            return group.user2.id
        elif group.user2.id == user_id:
            return group.user1.id
        return False


class MessageGroup(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_groups")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends_group")

    objects = MessageGroupManager()

    def __str__(self):
        return str(self.name)


class MessageManager(models.Manager):
    def save_message(self, data, group, sender_id, receiver_id):
        print("data", data)
        print("group_id", group)
        print("sender_id", sender_id)
        print("receiver_id", receiver_id)
        message = data.get("message", None)
        encrypted_msg = encrypt_message(message) if message else " "
        blog_id = data.get("blog_id", None)
        moment_id = data.get("moment_id", None)
        file = data.get("file", None)
        message_instance = self.create(group_id=group, message=encrypted_msg, moment_id=moment_id,
                    blog_id=blog_id, file=file, sender_id=sender_id, receiver_id=receiver_id)
        message_instance.message = self.show_message(sender_id, message_instance)
        return message_instance

    def show_message(self, sender_id, message):
        try:
            if message and (message.sender.id == sender_id or message.receiver.id == sender_id):
                print("show_message", type(message))
                decrypted_message = decrypt_message(message.message)
                print("decrypted_message1", decrypted_message)
                return decrypted_message
            return " "
        except Exception as e:
            print("Error decrypting message", str(e))
            return " "

    def get_last_message(self, group, user_id):
        last_message = group.group_messages.last()
        print("model1", last_message.sender.id)
        # return last_message
        if last_message:
            decrypted_msg = self.show_message(user_id, last_message)
            print("decrypted_msg", decrypted_msg)
            # last_message = 0
            return decrypted_msg
        else:
            return None

    def get_all_messages(self, group_id, login_user_id):
        print("group_id", group_id)
        messages = self.filter(group__name=group_id).order_by("timestamp")
        print("filtered messages", messages)
        for message in messages:
            message.message = self.show_message(sender_id=login_user_id, message=message)
        return messages

    def separate_group_users(self, group_name):
        _, first_part = group_name.split("$")
        user1_id, user2_id = first_part.split("&")
        return user1_id, user2_id


    def share_moment(self, sender_id,  data):
        moment_id = data.get("moment_id", None)
        group_name_list = data.get("group_name_list")
        for group_name in group_name_list:
            try:
                user1, user2 = self.separate_group_users(group_name)
                receiver_id = user2 if sender_id == user1 else user2
                self.create(group=MessageGroup.objects.get(name=group_name), moment_id=moment_id, sender_id=sender_id, receiver_id=receiver_id)

            except ValueError:
                print(f"Error processing group name: {group_name}")
            except Exception as e:
                print(f"An error occurred: {e}")

    def share_blog(self, sender_id,  data):
        blog_id = data.get("blog_id", None)
        group_name_list = data.get("group_name_list")
        for group_name in group_name_list:
            try:
                user1, user2 = self.separate_group_users(group_name)
                receiver_id = user2 if sender_id == user1 else user1
                self.create(group=MessageGroup.objects.get(name=group_name), blog_id=blog_id, sender_id=sender_id, receiver_id=receiver_id)

            except ValueError:
                print(f"Error processing group name: {group_name}")
            except Exception as e:
                print(f"An error occurred: {e}")

    def separate_share_task(self, sender_id, data):
        blog_id = data.get("blog_id", None)
        moment_id = data.get("moment_id", None)
        if blog_id is not None:
            return self.share_blog(sender_id, data)
        elif moment_id is not None:
            return self.share_moment(sender_id, data)
        else:
            return


class Message(models.Model):
    group = models.ForeignKey(MessageGroup, on_delete=models.CASCADE, related_name="group_messages")
    message = models.TextField(max_length=500, blank=True)
    moment = models.ForeignKey(Moment, null=True, on_delete=models.CASCADE, related_name="moments_send")
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, related_name="blogs_send")
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="message_files", null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_sent")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages_received")

    objects = MessageManager()

    def __str__(self):
        return self.group.name
