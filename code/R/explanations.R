# Load packages --------------------------------------------------------------------------------
library(tidyjson)
library(RSQLite)
library(stringr)
library(Hmisc)
library(tidyverse)

# Read in and structure data ------------------------------------------------------------------

con = dbConnect(SQLite(),dbname = "../js/experiment_1/participants.db");
df.data = dbReadTable(con,"explanations")
dbDisconnect(con)

#trialinfo
df.info = read.csv("../../data/trial_info.csv",stringsAsFactors = F)

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
df.long = df.data %>% 
  rename(participant = workerid) %>% 
  select(participant,datastring) %>% 
  as.tbl_json(.,'datastring') %>%
  enter_object('data') %>%
  gather_array('clip.order') %>%
  enter_object('trialdata') %>% 
  spread_values(clip = jstring('clip'),
                outcome = jstring('outcome')) %>% 
  enter_object('questions') %>% 
  gather_array('question.order') %>% 
  append_values_string('question') %>% 
  left_join(
    df.data %>% 
      rename(participant = workerid) %>% 
      select(participant,datastring) %>% 
      as.tbl_json(.,'datastring') %>%
      enter_object('data') %>%
      gather_array('clip.order') %>% 
      enter_object('trialdata') %>% 
      enter_object('response') %>% 
      gather_array('question.order') %>% 
      append_values_number('response')
  ) %>% 
  mutate(clip = str_replace_all(clip,"clip_",""),
         clip = as.numeric(clip)) %>% 
  select(participant,clip,clip.order,outcome,question.order,question,response) %>% 
  left_join(df.info)  %>% 
  filter(!(clip==13 & question.index == 3)) %>% 
  arrange(participant,clip,question.index) %>% 
  select(participant,clip,clip.order,outcome,question.order,question.index,question.quality,response,model.prediction,
         question.text)
  
write.csv(df.long,file = "../../data/data.csv",row.names = F)
  

# Fit model  ----------------------------------------------------------------------------------

df.regression = df.long %>% 
  # group_by(participant) %>% 
  # mutate(response = scale(response)) %>% 
  # filter(!(clip==13 & question.index == 3)) %>% 
  group_by(clip,question.index,question.text) %>% 
  summarise(data = mean(response),
            model = mean(model.prediction)) %>% 
  ungroup() %>% 
  mutate(model = lm(data~model)$fitted.values)


# Plot results (Scatter plot) -------------------------------------------------------------------------------

df.plot = df.regression

ggplot(df.plot,aes(x = model, y = data))+
  geom_smooth(method='lm',color = 'black', alpha = 0.5)+
  geom_point()+
  theme_bw()+
  theme(text = element_text(size=20),
        panel.grid = element_blank())
  
cor(df.regression$data,df.regression$model)


# Plot results (bars per question and clip)  --------------------------------------------------

df.plot = df.long %>% 
  left_join(df.regression %>% select(clip,question.index,model)) %>% 
  mutate(question.index = factor(question.index,labels= c('good','medium','bad')),
         clip = factor(clip,levels = c(5, 7, 9, 13, 16, 23), labels = paste0("clip ", c(5, 7, 9, 13, 16, 23))))

ggplot(df.plot,aes(x=question.index,y=response))+
  stat_summary(fun.y = 'mean',geom='bar',color = 'black', aes(fill = question.index),show.legend = F)+
  stat_summary(fun.data = mean_cl_boot,geom='errorbar',width=0.3)+
  stat_summary(aes(y = model), fun.y = 'mean',geom='point', color = 'red', size = 3)+
  facet_wrap(~clip)+
  labs(x = "", y ="mean agreement rating")+
  theme_bw()+
  theme(text = element_text(size=20),
        panel.grid = element_blank(),
        legend.position = 'bottom')


  


# Table with question  ------------------------------------------------------------------------

df.info %>% 
  select(clip,question.index,question.text)
  
  
