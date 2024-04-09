import os
import json

class DataIngestor:
    def __init__(self, csv_path: str):
        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]

        self.data = {}
        self.index_dict = {}

        with open (csv_path, 'r') as f:
            first_line = True
            for line in f.readlines():
                if first_line:
                    self.columns = line.strip().split(',')
                    for col in range(len(self.columns)):
                        self.index_dict[self.columns[col]] = col
                    first_line = False
                else:
                    curr_line = line.strip().split(',')

                    question = curr_line[8]
                    if question not in self.data:
                        self.data[question] = {}
                    
                    location = curr_line[4]
                    if location not in self.data[question]:
                        self.data[question][location] = []
                    
                    self.data[question][location].append(curr_line)
    
        # q = "Percent of adults aged 18 years and older who have an overweight classification"
        # for value in self.data[q]["District of Columbia"]:
        #     print(value[11])

        
        
