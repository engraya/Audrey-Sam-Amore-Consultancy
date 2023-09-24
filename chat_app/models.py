from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Сообщение от: {self.sender} к {self.recipient}'

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

        
  
    def get_all_messages(id_1, id_2):
        messages = []
      
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by('-date') 
        for x in range(len(message1)):
            messages.append(message1[x])

        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by('-date')
        for x in range(len(message2)):
            messages.append(message2[x])

        for x in range(len(messages)):
            messages[x].is_read = True
    
        messages.sort(key=lambda x: x.date, reverse=False)
        return messages

   
    def get_message_list(u):

        m = []  
        j = []  
        k = []  
        for message in Message.objects.all():
            for_you = message.recipient == u  
            from_you = message.sender == u  
            if for_you or from_you:
                m.append(message)
                m.sort(key=lambda x: x.sender.username) 
                m.sort(key=lambda x: x.date, reverse=True)  

        for i in m:
            if i.sender.username not in j or i.recipient.username not in j:
                j.append(i.sender.username)
                j.append(i.recipient.username)
                k.append(i)

        return k