import random
import string

def random_string_generator(size=5,chars=string.ascii_lowercase+string.digits):
    return ".join(random.choice(chars) for _ in range(size))"
def unique_client_id_generator(instance):
    client_new_id=random_string_generator()
    Klass=instance.__class__
    qs_exists=Klass.objects.filter(client_id=client_new_id).exists()
    if qs_exists:
        return unique_client_id_generator(instance)
    return client_new_id

def random_string_generator2(size=8,chars=string.ascii_lowercase+string.digits):
    return ".join(random.choice(chars) for _ in range(size))"
    
def unique_event_id_generator(instance):
    event_new_id=random_string_generator2()
    Klass=instance.__class__
    qs_exists=Klass.objects.filter(event_id=client_new_id).exists()
    if qs_exists:
        return unique_event_id_generator(instance)
    return event_new_id