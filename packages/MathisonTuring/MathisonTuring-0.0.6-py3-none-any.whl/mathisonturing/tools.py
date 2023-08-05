import pyrebase
import json
from validict import validate

class auth:

    def __init__(self, institution, project, token):

        for i in [institution, project, token]: 
            if not isinstance(i, str): 
                raise TypeError("The unsupported operand " + str(inputs[i]) + " should be a string. Right now it is a ", type(institution))

        self.institution = institution.lower() 
        self.project = project.lower() 
        self.token = token
        self.group = "groups"
        self.apiKey = "AIzaSyCtdHz-CZ0oXkMcuqL6ke2zcBkbhwmalzk"
        self.datetime = {".sv": "timestamp"}

        config = {
        "apiKey": self.apiKey,
        "authDomain": "startup-mvp-85dc4.firebaseapp.com",
        "projectId":"startup-mvp-85dc4",
        "databaseURL": "https://startup-mvp-85dc4.firebaseio.com",
        "storageBucket": "startup-mvp-85dc4.appspot.com",
        }

        self.config = pyrebase.initialize_app(config)
        self.database = self.config.database()

    def publish(self):
        self.database.child(self.group).child(self.institution).child(self.project).child(self.token).push(self.data)

    def cancel_task(self,id):
        self.database.child(self.group).child(self.institution).child(self.project).child(self.token).child(id).update({"status":False})

    def update(self,id):
        self.database.child(self.group).child(self.institution).child(self.project).child(self.token).child(id).update(self.data)

    def remove(self,id):
        self.database.child(self.group).child(self.institution).child(self.project).child(self.token).child(id).remove()

    def bounding_box(self, data):

        """ 
        
        Output Example: Draw a box around each rooftop and pool.

        Input Example = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "min_width":int,
        "min_height": int,
        "if_not_conclusive": str}

        """

        template = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "min_width":int,
        "min_height": int,
        "if_not_conclusive": str}

        validate(template, data)

        data.update({"operation":"bounding_box", "status": "submitted", "datetime": self.datetime})

        self.data = data
        
    def classification(self, data):

        """
        
        Output Example: Select the most appropriate categories for the tee shown.

        Input Example = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "choices":bool,
        "if_not_conclusive": str}

        """

        template = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "choices":bool,
        "if_not_conclusive": str}

        data.update({"operation":"classification", "status": "submitted", "datetime": self.datetime})

        self.data = data

    def cuboid(self, data):

        """
        Output Example: Draw a cuboid around each building or tower.

        Input Example = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "if_not_conclusive": str}

        """

        template = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "if_not_conclusive": str}

        data.update({"operation":"cuboid", "status": "submitted", "datetime": self.datetime})

        self.data = data

    def splines(self, data):

        """
        Output Example: Annotate all the lines and circles of the field.

        Input Example = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "splines":bool,
        "with_labels":bool,
        "if_not_conclusive": str}

        """

        template = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "splines":bool,
        "with_labels":bool,
        "if_not_conclusive": str}

        data.update({"operation":"splines", "status": "submitted", "datetime": self.datetime})

        self.data = data

    def point(self, data):

        """
        
        Output Example: Draw a point in each facial point and limb joint.

        Input Example = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "splines":bool,
        "with_labels":bool,
        "if_not_conclusive": str}

        """
        template = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "splines":bool,
        "with_labels":bool,
        "if_not_conclusive": str}

        data.update({"operation":"point", "status": "submitted", "datetime": self.datetime})

        self.data = data

    def polygon(self, data):

        """
        
        Output Example: Draw a tight polygon around every pool in the image.

        Input Example = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "if_not_conclusive": str}

        """

        template = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "if_not_conclusive": str}

        data.update({"operation":"polygon", "status": "submitted", "datetime": self.datetime})

        self.data = data

    def segmentation(self, data):

        """
        Output Example: Segment by vehicles, pedestrians, bikes, roads, road markings, background and obstacles in each image.

        Input Example = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "if_not_conclusive": str}

        """

        template = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "with_labels":bool,
        "if_not_conclusive": str}

        data.update({"operation":"segmentation", "status": "submitted", "datetime": self.datetime})

        self.data = data

    def transcription(self, data):

        """ 
        Output Example:"Transcribe the menu."
        
        Input Example = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "if_not_conclusive": str}

        """

        template = {"instruction":str,
        "attachement": str,
        "attachement_type": str,
        "objects_to_annotate": list,
        "if_not_conclusive": str}

        data.update({"operation":"transcription", "status": "submitted", "datetime": self.datetime})

        self.data = data
