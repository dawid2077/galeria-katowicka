table simple
user:
user_id =uuid7
email
google_token


table session (it automatically joins every session who shares user id)
session_id
chat history = a dict with chat history
last_action=here in unix time we have last interaction so like writing a message or looking at the chat . so we can sort chats by last looked/interacted with

configs/ is the source of thruth  but after deployment the db will be the source of truth


place:
place_id = also here uuid7
place_name=read from configs/config.conf
place_info=read from configs/place_name (in future rag)
location_string=a string with the street and kod pocztowy in future will use google maps widget (in future try postgis)


