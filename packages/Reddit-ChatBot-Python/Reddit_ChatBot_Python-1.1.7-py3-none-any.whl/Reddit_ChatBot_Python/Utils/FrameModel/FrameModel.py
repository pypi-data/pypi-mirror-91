import json
from types import SimpleNamespace


class FrameModel:
    """
    mostly important fields of MESG:
    msg_id
    is_op_msg
    is_guest_msg
    message
    ts
    channel_url
    user -> name, guest_id, is_blocked_by_me
    mentioned_users
    """

    @staticmethod
    def get_frame_data(data):
        data_r = data[4:]
        data_j = json.loads(data_r, object_hook=lambda d: SimpleNamespace(**d))
        type_f = data[:4]

        # some presets
        if type_f == "MESG" and data_j.message == "":
            data_j.message = "[snoomoji]"
        data_j.type_f = type_f

        return data_j
