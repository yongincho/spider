from imutils import paths
import face_recognition
import pickle
import datetime
import cv2
import os
import sys
import psycopg2
import traceback
import time
import settings
from s3wrapper import S3Wrapper

class AgentSpider(object):

    def __init__(self):
        self.faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.registeredFaceEncoding()

    def registeredFaceEncoding(self):
        imagePaths = list(paths.list_images('Images'))
        knownEncodings = []
        knownNames = []
        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            name = imagePath.split(os.path.sep)[-2]
            print (name)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            #Use Face_recognition to locate faces
            boxes = face_recognition.face_locations(rgb,model='hog')
            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)
            # loop over the encodings
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)
        #save emcodings along with their names in dictionary data
        data = {"encodings": knownEncodings, "names": knownNames}
        #use pickle to save data into a file for later use
        f = open("face_enc", "wb")
        f.write(pickle.dumps(data))
        f.close()

    def identifyFace(self, identify_name, imgpath):
        verify_result = False
        data = pickle.loads(open('face_enc', "rb").read())

        image = cv2.imread(imgpath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #convert image to Greyscale for haarcascade
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(60, 60),
                                            flags=cv2.CASCADE_SCALE_IMAGE)
        encodings = face_recognition.face_encodings(rgb)
        names = []

        for encoding in encodings:

            matches = face_recognition.compare_faces(data["encodings"], encoding)

            name = "Unknown"
            # check to see if we have found a match
            if True in matches:
                #Find positions at which we get True and store them
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    #Check the names at respective indexes we stored in matchedIdxs
                    name = data["names"][i]
                    #increase count for the name we got
                    counts[name] = counts.get(name, 0) + 1
                #set name which has highest count
                name = max(counts, key=counts.get)


            if name == identify_name:
                # verification success
                verify_result = True
                break
        return verify_result
    def worker(self):

        downloaded_path = "download"
        s3 = S3Wrapper(settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY)

        try:
            conn = psycopg2.connect(host="ec2-52-78-98-64.ap-northeast-2.compute.amazonaws.com", dbname="spider", user="jcho", password="whdyddls")
            cur = conn.cursor()
        except Exception:
            print('Fail to connect DB')
            traceback.print_exc()

        while 1:
            print("waiting...")
            try:
                # 0 : waiting for detection, 1 : detecting, 2 : detection complete
                query = 'SELECT * FROM face_spideridentifyrequest WHERE status = 0'
                cur.execute(query)
                result = cur.fetchall()
                for row in result:
                    idx = row[0]
                    username = row[1]
                    s3_filename = row[2]
                    parent_id = row[5]
                    ticket = row[6]

                    # update status value to 1
                    query = "UPDATE face_spideridentifyrequest SET status = 1 WHERE id = " + str(idx)
                    cur.execute(query)
                    conn.commit()


                    # detection start
                    print(s3_filename)
                    print(downloaded_path + '/' + s3_filename)
                    #s3.download("spider-face-bucket", s3_filename, downloaded_path + '/' + s3_filename)
                    s3.download("spider-face-bucket", s3_filename, s3_filename+'.png')

                    verify_result = self.identifyFace(username, s3_filename+'.png')
                    msg = "Verify : " + str(verify_result)
                    # update status value to 2
                    query = "UPDATE face_spideridentifyrequest SET status = 2 WHERE id = " + str(idx)
                    cur.execute(query)
                    conn.commit()

                    # insert result into DB
                    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    query = "INSERT INTO face_spideruserlog(log_body, log_type, log_success, log_time, user_info_id, log_ticket) " + "VALUES('%s', 2, 1, '%s', " % (msg, now_time) + str(parent_id) + ", '%s');" % (ticket)
                    cur.execute(query)
                    conn.commit() 
            except:
                traceback.print_exc()

            time.sleep(1)

if __name__ == "__main__":
    asp = AgentSpider()
    if not os.path.exists("Images"):
        print ("Not exists Images Directory")
        sys.exit()

    #asp.registeredFaceEncoding()
    #asp.identifyFace(sys.argv[1])
    asp.worker()


