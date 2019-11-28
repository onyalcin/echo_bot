class Empathy:
    def __init__(self):
        self.emotion_queue = None

    def affect_match(self, emotion_data, limit=0):  # TODO: add another with more limit
        if emotion_data != {}:
            e = emotion_data["emotions"]
            recognition = max(e, key=e.get)
            amount = e[recognition]
            if amount > limit:
                if recognition != 'neutral':
                    return recognition, amount
                else:
                    return None, None
            else:
                return None, None
        else:
            return None, None