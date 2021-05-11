from datetime import datetime, timedelta


def congratulate(users):
   congrat_dict = {} 
   current_date = datetime.now().date()
   days ={ 0:'Monday',
           1:'Tuesday',
           2:'Wednesday',
           3:'Thursday',
           4:'Friday',
           5:'Saturday',
           6:'Sunday'}     
   start_next_week =  current_date - timedelta(days = current_date.weekday())+timedelta(days=7)
   for collegue in users:
       date_=datetime.strptime(collegue['birthday'].replace(collegue['birthday'].split('.')[0], str(current_date.year) ), '%Y.%m.%d')
       if date_.date() >= start_next_week - timedelta(days=1) and date_.date() < start_next_week + timedelta(days=6):
          if date_.weekday()== 6:
              if days[0] not in congrat_dict.keys():
                  congrat_dict[days[0]] = [collegue['name']]
              else:
                  congrat_dict[days[0]].extend([collegue['name']])
          else:
              if days[date_.weekday()] not in congrat_dict.keys():
                  congrat_dict[days[date_.weekday()]] = [collegue['name']]
              else:
                  congrat_dict[days[date_.weekday()]].extend([collegue['name']])    
   for day_ in congrat_dict.keys():
       print( 'At ',day_, ' send congratulations to:')
       for name_ in congrat_dict[day_]:
           print(name_) 
   return None

     
colegues_dict = [{'name': 'Ivan0', 'birthday':'1990.5.15'}, 
                 {'name': 'Ivan7', 'birthday':'1990.5.16'},
                 {'name': 'Ivan1', 'birthday':'1990.5.17'}, 
                 {'name': 'Ivan2', 'birthday':'1990.5.18'},
                 {'name': 'Ivan3', 'birthday':'1990.5.19'},
                 {'name': 'Ivan4', 'birthday':'1990.5.20'},
                 {'name': 'Ivan5', 'birthday':'1990.5.21'},
                 {'name': 'Ivan6', 'birthday':'1990.5.22'},
                 {'name': 'Ivan8', 'birthday':'1990.5.23'}]
congratulate(colegues_dict)
