# Load packages --------------------------------------------------------------------------------
library(tidyjson)
library(RSQLite)
library(stringr)
library(tidyverse)

# Read in and structure data ------------------------------------------------------------------

con = dbConnect(SQLite(),dbname = "../js/experiment_1/participants.db");
df.data = dbReadTable(con,"explanations")
dbDisconnect(con)

#filter out incompletes 
df.data = df.data %>% 
  filter(status %in% 3:5) %>% 
  # filter(!str_detect(uniqueid,'debug')) %>% 
  filter(codeversion == 'experiment_1')

# demographic data 
df.demographics = df.data$datastring %>% 
  spread_values(condition = jnumber('condition'),
                age = jnumber('questiondata','age'),
                gender = jstring('questiondata','sex'),
                feedback = jstring('questiondata','feedback')
  ) %>% 
  rename(participant = document.id) %>% 
  mutate(time = difftime(df.data$endhit,df.data$beginhit,units = 'mins'))

# trial data 
df.long = df.data$datastring %>% 
  as.tbl_json() %>% 
  spread_values(participant = jstring('workerId')) %>%
  enter_object('data') %>%
  gather_array('order') %>% 
  enter_object('trialdata') %>% 
  spread_values(clip = jstring('clip'),
                outcome = jstring('outcome')) %>% 
  enter_object('questions') %>% 
  gather_array('index') %>% 
  append_values_string('question') %>% 
  left_join(
    df.data$datastring %>% 
      as.tbl_json() %>% 
      enter_object('data') %>%
      gather_array('order') %>% 
      enter_object('trialdata') %>% 
      enter_object('response') %>% 
      gather_array('index') %>% 
      append_values_number('response')
  ) %>% 
  mutate(clip = str_replace_all(clip,"clip_",""),
         clip = as.numeric(clip)) %>% 
  select(-document.id,participant,clip,order,outcome,index,question,response) %>% 
  arrange(participant,clip,index)
  

  
  