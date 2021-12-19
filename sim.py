import random
from statistics import mean
import csv
random.seed(10)

amt_agents = 60
amt_rounds = 200
amt_tests = 10
log = False
 
amt_agents = 60
amt_rounds = 200
amt_tests = 1
log = False
 
# Save with .2
opportunity_scale = .2
utility_scale = 1
 
 
report_probability = .9
forgive_difficulty = 2
baseline_report = .1
# For each percentage of catfishing, .01 * harshness
harshness = 0
 
agent_save = .1
agent_evil = .01
 
prop_truthful = .00001
 

class Agent():
    def __init__(self):

        self.id = 0 
        self.participating = 1  

        self.score = 0
        self.report = 0
        self.utility = 0
        self.total_lying = 0

        self.truthful = True
       

    def set_report(self):
        
        if self.truthful:
            self.report = self.score
        else:
            if self.participating == 1:
           
                self.report = min(self.report + agent_evil, 1)
            else:
    
                self.report = max((self.report - agent_save), self.score)

class Simulator():
    def __init__(self):
        self.overall_summary = []
        self.truth_summary = []
        self.lie_summary = []

        self.report_summary = []
    def generate(self, prop_truthful):

        self.reputation = {}
        self.m_agent_list = []
        self.f_agent_list = []

        self.valid_m = []
        self.valid_m = []

        self.summary = []
       
        for i in range(amt_rounds):
            self.summary.append({})
        
        amt_truthful = round((amt_agents /2)* prop_truthful)
     

  
        # Initialize the agents
        for i in range(amt_truthful):
            temp = Agent()
            temp.score  = random.random()
            temp.report = temp.score
            temp.id = i
        
            # Reputation of 0 is the best
            self.reputation[temp.id] = [[], 0 ] 
            # the second value in the tuple means whether they're included in the round
            temp.participating = 1
            self.m_agent_list.append(temp)
        for i in range(amt_truthful,round(amt_agents / 2) ):
            temp = Agent()
            temp.score  = random.random()
            temp.id = i
            temp.report = temp.score
            temp.truthful = False
            # Reputation of 0 is the best
            self.reputation[temp.id] = [[], 0 ] 
            # the second value in the tuple means whether they're included in the roudnd
            temp.participating = 1
            self.m_agent_list.append(temp)
   
        for i in range(round(amt_agents / 2), round(amt_agents / 2) + amt_truthful):
            temp = Agent()
            temp.score  = random.random()
            temp.id = i
            temp.report = temp.score
        
            # Reputation of 0 is the best
            self.reputation[temp.id] = [[], 0 ] 
            # the second value in the tuple means whether they're included in the roudnd
            temp.participating = 1
            self.f_agent_list.append(temp)
        for i in range(round(amt_agents / 2) + amt_truthful, amt_agents):
            temp = Agent()
            temp.score  = random.random()
            temp.id = i
            temp.truthful = False
            temp.report = temp.score
            # Reputation of 0 is the best
            self.reputation[temp.id] = [[], 0 ] 
            # the second value in the tuple means whether they're included in the roudnd
            temp.participating = 1
            self.f_agent_list.append(temp)
   
    def reporting(self):
        
        # First, set catfishing reporting to "no" for everyone (including those who didn't particpate last round)
        for i in range(len(self.m_agent_list)):
            m_reputation = self.reputation[self.m_agent_list[i].id][0]
            f_reputation = self.reputation[self.f_agent_list[i].id][0]

            # If they were not part of the last round, we'll count that as "not catfishing"
            m_reputation.append(0)
            f_reputation.append(0)
        for i in range(len(self.valid_m)):
            
            # How much player lied this round
            lying_m = (self.valid_m[i].report - self.valid_m[i].score)
            lying_f = (self.valid_f[i].report - self.valid_f[i].score)
            
            prob1 = report_probability * lying_m + baseline_report
            prob2 = report_probability * lying_f + baseline_report
            
            rand1 = random.random()
            rand2 = random.random()
          

            m_reputation = self.reputation[self.valid_m[i].id]
            f_reputation = self.reputation[self.valid_f[i].id]

            # Player chose to report (either intentionally or mistakeningly)
            if prob1 > rand1:
         
                m_reputation[0][-1] = 1
                m_reputation[1] +=1
            
           
            if prob2 > rand2:
                f_reputation[0][-1] = 1
                f_reputation[1] +=1
         

        
    def reputation_system(self):

        # Now Calculate whether reputation score should be improved! 
        for i in range(len(self.m_agent_list)):

            m_reputation = self.reputation[self.m_agent_list[i].id]
            f_reputation = self.reputation[self.m_agent_list[i].id]


            # Count how many consecutive 0's it's been 
            m_count = 0
            for j in range(len(m_reputation[0]) - 1, -1, -1):
                if m_reputation[0][j] == 0:
                    m_count +=1
                else:
                    break
            f_count = 0
            for j in range(len(f_reputation[0]) - 1, -1, -1):
                if f_reputation[0][j] == 0:
                    f_count +=1
                else:
                    break  
            # If they haven't been reported in forgive_difficulty rounds, then improve their reputation! 
            if m_count % forgive_difficulty == 0 and m_count > 0:
                m_reputation[1] = max(m_reputation[1] - 1, 0)

            if f_count % forgive_difficulty == 0 and f_count > 0:
                f_reputation[1] = max(f_reputation[1] - 1, 0)

        # set whether they should participate in the next round !
        for i in range(len(self.m_agent_list)):
   
            m_reputation = float(self.reputation[self.m_agent_list[i].id][1]) / amt_rounds
            f_reputation = float(self.reputation[self.m_agent_list[i].id][1]) / amt_rounds


          
            rep_score_f = f_reputation  * harshness
            rep_score_m = m_reputation * harshness

            if rep_score_m > random.random():
                self.m_agent_list[i].participating = 0
            else:
                self.m_agent_list[i].participating = 1

            if rep_score_f > random.random():
                # print("hey2")
                self.f_agent_list[i].participating = 0
            else:
                self.f_agent_list[i].participating = 1



    def calculate_summary(self, round):

       
        for i in range(len(self.m_agent_list)):
            m_agent = self.m_agent_list[i]
            f_agent = self.f_agent_list[i]
            self.summary[round][m_agent.id] = {"participation": "no", "utility": "x", "lied": "x", "reported": "x"}
            self.summary[round][f_agent.id] = {"participation": "no", "utility": "x", "lied": "x", "reported": "x"}
        i = 0
        for agent_m, agent_f in zip(self.valid_m, self.valid_f):

            i+=1
         
            m_utility = (utility_scale *  agent_f.score) - (opportunity_scale * (agent_m.report - agent_f.score) )
            f_utility = (utility_scale * agent_m.score) - (opportunity_scale * (agent_f.report - agent_m.score))

            m_lying = (agent_m.report - agent_m.score)
            f_lying = (agent_f.report - agent_f.score)
            
            m_reputation = self.reputation[agent_m.id]
            f_reputation = self.reputation[agent_f.id]

            m_report = m_reputation[0][-1]
            f_report = f_reputation[0][-1]

            self.summary[round][agent_m.id] = {"participation": "yes","utility": m_utility, "lied": m_lying , "reported": m_report, "score": agent_m.score}
            self.summary[round][agent_f.id] = {"participation": "yes","utility": f_utility, "lied": f_lying , "reported": f_report, "score": agent_f.score}
        
    def print_summary(self):
      
        for i in range(amt_rounds):

            print("round ", i)
            print("----" * 10)
            for j in range(len(self.m_agent_list)):
                m_agent = self.m_agent_list[j]
                f_agent = self.f_agent_list[j]
                m_summ = self.summary[i][m_agent.id]
                f_summ = self.summary[i][f_agent.id]

             
                print("agent ", m_agent.id, "with score" , m_agent.score, "truthful?", m_agent.truthful, ": participation ", m_summ["participation"], ", utility ", m_summ["utility"],
                    ", lied ", m_summ["lied"], ", reported? ", m_summ["reported"])
                print("agent ", f_agent.id, "with score" , f_agent.score,"truthful?", f_agent.truthful, ": participation ", f_summ["participation"], ", utility ", f_summ["utility"],
                    ", lied ", f_summ["lied"], ", reported? ", f_summ["reported"])
            print("----" * 40)
        
        total_utility = sum([agent.utility for agent in self.m_agent_list]) + sum([agent.utility for agent in self.f_agent_list])

        print("overall utility: " , total_utility)
        print("overall utility: " , total_utility)
        
    def run_simulation(self,  prop_truthful):

        self.generate(prop_truthful)

        self.lying_count = {}
        for agent_m, agent_f in zip(self.m_agent_list, self.f_agent_list):
            self.lying_count[agent_m.id] = [0, agent_m.score]
            self.lying_count[agent_f.id] = [0, agent_f.score]
        # Let's run the rounds!
        for i in range(amt_rounds):
            
            self.valid_m = [agent for agent in self.m_agent_list if agent.participating == 1]
            self.valid_f = [agent for agent in self.f_agent_list if agent.participating == 1]


       
            for agent in self.m_agent_list:
                agent.set_report()
            for agent in self.f_agent_list:
                agent.set_report()
            # Match people together
            self.valid_m.sort( key = lambda x: x.report, reverse=True)
            self.valid_f.sort( key = lambda x: x.report,reverse = True )

       
            amt_of_participants = min(len(self.valid_m),len(self.valid_f) )
            

            self.valid_m = self.valid_m[0:amt_of_participants]
            self.valid_f = self.valid_f[0:amt_of_participants]

            # Update the utility
            total_report = 0
            for agent_m, agent_f in zip(self.valid_m, self.valid_f):
                
              
                self.lying_count[agent_m.id][0] += (agent_m.report - agent_m.score)
                self.lying_count[agent_f.id][0] += (agent_f.report - agent_f.score)
                total_report += agent_m.report
                total_report += agent_f.report
            
                agent_m.utility += (utility_scale *  agent_f.score) - (opportunity_scale * (agent_m.report - agent_f.score))
                agent_f.utility +=  (utility_scale *  agent_m.score) - (opportunity_scale * (agent_f.report - agent_m.score))
            
            self.report_summary.append((i,total_report / amt_agents))
            self.reporting()
            self.calculate_summary(i)
            self.reputation_system()
  
        if log:
            self.print_summary()

        truth_count=  0 
        lie_count = 0
        
        for i in range(len(self.m_agent_list)):
            m_agent = self.m_agent_list[i]
            f_agent = self.f_agent_list[i]

            if m_agent.truthful == True:
                truth_count += m_agent.utility
            else:
                lie_count += m_agent.utility
            if f_agent.truthful == True:
                truth_count += f_agent.utility
            else:
                lie_count += f_agent.utility
        self.truth_summary.append(truth_count)
        self.lie_summary.append(lie_count)
        
        total_utility = sum([agent.utility for agent in self.m_agent_list]) + sum([agent.utility for agent in self.f_agent_list])
        self.overall_summary.append(total_utility)
    def run_tests(self):



        
        for i in range(amt_tests):
                self.run_simulation(.0000001)
        print("mean overall utility: ", mean(self.overall_summary))

        if prop_truthful >= 1 - prop_truthful:
            print("mean truthful utility: ", mean(self.truth_summary))
            print("mean lie utility: ", mean(self.lie_summary) * (prop_truthful/(1 - prop_truthful)))
        else:
            print("mean truthful utility: ", mean(self.truth_summary) * ((1 - prop_truthful)/(prop_truthful)))
            print("mean lie utility: ", mean(self.lie_summary) )

sim = Simulator()
sim.run_tests()

