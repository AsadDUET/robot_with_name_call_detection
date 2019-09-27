import sqlite3
from gtts import gTTS

connection = sqlite3.connect('agricultureData.db')
cursor = connection.cursor()

def create_table():
    cursor.execute (" CREATE TABLE IF NOT EXISTS treatment_for_disease (plant TEXT, disease TEXT, treatment TEXT, audio_file TEXT)")
    
def data_entry(plant, disease, treatment, audio_file):
    cursor.execute ("INSERT INTO treatment_for_disease (plant, disease, treatment, audio_file) VALUES (?, ?, ?, ?)",(plant, disease, treatment, audio_file))
    connection.commit()
def read_from_db(plant,disease):
    cursor.execute(" SELECT audio_file, treatment FROM treatment_for_disease WHERE plant='"+plant+"' AND disease='"+disease+"'")
    return cursor.fetchall()[0]
if __name__=='__main__':
    #create_table() treatment
    plant="টমেটো"
    disease="নাবী ধ্বসা"
    treatment="প্রতি লিটার পানিতে ২ গ্রাম সিকিউর মিশিয়ে, স্প্রে করলে ভাল ফল পাওয়া যায় ,"
    audio_file="treatment_tomato_late_blight"
    tts = gTTS(text= treatment , lang='bn')
    tts.save("sound/"+ audio_file+".mp3")
#    data_entry(plant, disease, treatment, audio_file)
#    print(read_from_db("a","b")[1])
    cursor.close()
    connection.close()
#    