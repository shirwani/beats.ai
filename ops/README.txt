###############################
# DEV MACHINE ENVIRONMENT SETUP
###############################
which python3
python3 -m venv venv
alias python="venv/bin/python3.12"
alias pip="venv/bin/pip3.12"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt


##################
# ADDITIONAL SETUP
##################
mkdir -p dataset/downloads
# Create text file with list of artists


############################
# SET UP CASSANDRA IN DOCKER
############################
docker pull cassandra:latest
docker run --name cassandra-container -p 9042:9042 -d cassandra:latest
docker exec -it cassandra-container cqlsh

# Create new keyspace
CREATE KEYSPACE BEATS_AI
WITH REPLICATION = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};
# List tables in the keyspace
describe tables;

pip install cassandra-driver
python cassandra_db_setup.py


#####################################################
# DOWNLOAD TRACKS FOR ARTISTS LISTED IN THE TEXT FILE
#####################################################
python download_tracks


########################################
# EXTRACTING INFO FROM DOWNLOADED TRACKS
########################################
python extract_audio_features.py


##############
# RUN ANALYSIS
##############
python basic_analysis.py


####################################################################
# MAKE A LOCAL COPY OF CASSANDRA DATA IF WE HAVEN'T MOUNTED A VOLUME
####################################################################
docker exec cassandra-container cqlsh -e "COPY beats_ai.tracks TO '/tmp/tracks.csv' WITH HEADER = true;"
docker cp cassandra-container:/tmp/tracks.csv .dataset/cassandra/tracks.csv


################################
# Chordino - via chord-extractor
################################
git clone https://github.com/ohollo/chord-extractor.git
cd chord-extractor
docker build -t chord-extractor .
docker run -v /path/to/your/audio/files:/audio_files chord-extractor python3 -m chord_extractor /audio_files/your_audio_file.wav

docker run -v /Users/macmini/PycharmProjects/beats.ai/samples:/audio_files chord-extractor python3 -m chord_extractor /audio_files/amends.mp3



