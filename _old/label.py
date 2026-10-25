class GmailLabelManager:

    def __init__(self, service):
        self.service = service


    def create_label(self, label_name):

        labels = self.service.users().labels().list(
            userId="me"
        ).execute()

        for label in labels["labels"]:
            if label["name"] == label_name:
                return label["id"]


        result = self.service.users().labels().create(
            userId="me",
            body={
                "name": label_name
            }
        ).execute()

        return result["id"]

    def add_label(self, message_id, label_id):
        self.service.users().messages().modify(
            userId="me",
            id=message_id,
            body={
                "addLabelIds":[label_id]
            }
        ).execute()