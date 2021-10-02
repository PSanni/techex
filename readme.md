To chat with bot on dummy website, run followings in two different terminals:  
1. run rasa server in root directory ie, (../TechExcelChatBot),  
 `rasa run -m models --endpoints endpoints.yml --enable-api --cors "*"`
2. run rasa action server by navigating to actions directory (../TechExcelChatBot/actions) and run,   
`rasa run actions --cors "*"` 