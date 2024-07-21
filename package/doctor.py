from flask_restful import Resource, Api, request
from package.model import conn
import pymongo


client = pymongo.MongoClient("mongodb+srv://Sanjo:sanjo_boo02@cluster0.vaait.mongodb.net/Database?retryWrites=true&w=majority")
db = client['Database']
col = db['doctors']

class Doctors(Resource):
    """This contain apis to carry out activity with all doctors"""

    def get(self):
        """Retrive list of all the doctor"""

        doctors = conn.execute("SELECT * FROM doctor ORDER BY doc_date DESC").fetchall()
        return doctors



    def post(self):
        """Add the new doctor"""

        doctorInput = request.get_json(force=True)
        doc_first_name=doctorInput['doc_first_name']
        doc_last_name = doctorInput['doc_last_name']
        doc_ph_no = doctorInput['doc_ph_no']
        doc_address = doctorInput['doc_address']
        doctorInput['doc_id']=conn.execute('''INSERT INTO doctor(doc_first_name,doc_last_name,doc_ph_no,doc_address)
            VALUES(?,?,?,?)''', (doc_first_name, doc_last_name,doc_ph_no,doc_address)).lastrowid
        conn.commit()
        dic = {"id":doctorInput['doc_id'],"first_name":doc_first_name,"last_name":doc_last_name,"phone":doc_ph_no,"address":doc_address}
        col.insert_one(dic)
        return doctorInput

class Doctor(Resource):
    """It include all the apis carrying out the activity with the single doctor"""


    def get(self,id):
        """get the details of the docktor by the doctor id"""

        doctor = conn.execute("SELECT * FROM doctor WHERE doc_id=?",(id,)).fetchall()
        return doctor

    def delete(self, id):
        """Delete the doctor by its id"""

        conn.execute("DELETE FROM doctor WHERE doc_id=?", (id,))
        myquery = { "id": id }
        col.delete_one(myquery)
        conn.commit()
        return {'msg': 'sucessfully deleted'}

    def put(self,id):
        """Update the doctor by its id"""

        doctorInput = request.get_json(force=True)
        doc_first_name=doctorInput['doc_first_name']
        doc_last_name = doctorInput['doc_last_name']
        doc_ph_no = doctorInput['doc_ph_no']
        doc_address = doctorInput['doc_address']
        conn.execute(
            "UPDATE doctor SET doc_first_name=?,doc_last_name=?,doc_ph_no=?,doc_address=? WHERE doc_id=?",
            (doc_first_name, doc_last_name, doc_ph_no, doc_address, id))
        myquery = { "id": id }
        newvalues = { "$set": {"id":id,"first_name":doc_first_name,"last_name":doc_last_name,"phone":doc_ph_no,"address":doc_address} }
        col.update_one(myquery, newvalues)
        conn.commit()
        return doctorInput
