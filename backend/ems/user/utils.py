from .models import User
from core.utils import hash_password, JWT_generator, verify_password
from core.responses import Responses as r


def login_utility(data: dict) -> str:
    try:
        user = User.objects.get(email=data["email"])
        print(user.email)
        if verify_password(data["password"], user.password):
            payload = {"name": user.name, "role": user.role}
            token = JWT_generator(payload)
            return r.set_data({"token": token}).ok
        else:
            return r.unauthorized

    except User.DoesNotExist:
        return r.not_found

    except Exception as e:
        print(f"Error: {str(e)}")
        return r.server_error
