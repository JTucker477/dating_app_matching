import random
from statistics import mean

random.seed(10)
# Has to be even

# prob1 determines if they get reported
# prob1 = report_probability * lying_m + baseline_report
# prob2 = report_probability * lying_f + baseline_report

# m_reputation determines if they get kicked out in the next round... 
# m_reputation = float(self.reputation[self.m_agent_list[i][0].id][1]) / amt_rounds
# f_reputation = float(self.reputation[self.m_agent_list[i][0].id][1]) / amt_rounds
# rep_score_f = f_reputation  * harshness
# rep_score_m = m_reputation * harshness

amt_agents = 26
amt_rounds = 100
amt_tests = 100
log =False

opportunity_scale = 1
utility_scale = 1


report_probability = 1
forgive_difficulty = 1
baseline_report = .1
# For each percentage of catfishing, .01 * harshness
harshness =5

agent_save = .05
agent_evil = .1
# Whether to print all the info for each round

class Agent():
    def __init__(self):

        self.id = 0 
        self.participating = 1  

        self.score = 0
        self.report = 0
        self.utility = 0
        self.total_lying = 0
        

    def set_report(self):
        # prob = random.random()
        # if prob > .5:
        # self.report = self.score
        if self.participating == 1:
            # print("hi")
            self.report = min(self.report + agent_evil, 1)
        else:
            # print('hey')
            self.report = max((self.report - agent_save), self.score)

class Simulator():
    def __init__(self):
        self.overall_summary = []
    def generate(self):

        self.reputation = {}
        self.m_agent_list = []
        self.f_agent_list = []

        self.valid_m = []
        self.valid_m = []

        self.summary = []
       
        

        for i in range(amt_rounds):
            self.summary.append({})
        

        # Initialize the agents
        for i in range(int(amt_agents / 2)):
            temp = Agent()
            temp.score  = random.random()
            temp.id = i
            # Reputation of 0 is the best
            self.reputation[temp.id] = [[], 0 ] 
            # the second value in the tuple means whether they're included in the roudnd
            temp.participating = 1
            self.m_agent_list.append(temp)
   
        for i in range(int(amt_agents / 2)):
            temp = Agent()
            temp.score  = random.random()
            temp.id = i + len(self.m_agent_list)
            # Reputation of 0 is the best
            self.reputation[temp.id] = [[], 0 ]
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
            
            
            # 
            prob1 = report_probability * lying_m + baseline_report
            prob2 = report_probability * lying_f + baseline_report
            # print(prob1)
            # print("prob",prob1,prob2)
            rand1 = random.random()
            rand2 = random.random()
            # print(rand1, rand2)
            # print(prob1, prob2)
            
            # print(prob1 > rand1, prob2 > rand2)

            m_reputation = self.reputation[self.valid_m[i].id]
            f_reputation = self.reputation[self.valid_f[i].id]

            # Player chose to report (either intentionally or mistakeningly)
            if prob1 > rand1:
                # print("hey")
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
            # Percentage of total rounds they cheated... 
            m_reputation = float(self.reputation[self.m_agent_list[i].id][1]) / amt_rounds
            f_reputation = float(self.reputation[self.m_agent_list[i].id][1]) / amt_rounds


            # Decide whether they should be kicked out in the next round
            # Rep_score will be between 0 and 1
            rep_score_f = f_reputation  * harshness
            rep_score_m = m_reputation * harshness
            # print("rep_score", rep_score_m, rep_score_f)
            if rep_score_m > random.random():
                # print("hey2")
                self.m_agent_list[i].participating = 0
            else:
                self.m_agent_list[i].participating = 1

            if rep_score_f > random.random():
                # print("hey2")
                self.f_agent_list[i].participating = 0
            else:
                self.f_agent_list[i].participating = 1


    # def summary(self):
        # overall_utility = sum([agent[0].utility for agent in self.m_agent_list]) + sum([agent[0].utility for agent in self.f_agent_list])
        # print("overall utility: ", overall_utility)
        # for i in range()
    def calculate_summary(self, round):
        # print("amt2",len(self.valid_m))
       
        for i in range(len(self.m_agent_list)):
            m_agent = self.m_agent_list[i]
            f_agent = self.f_agent_list[i]
            self.summary[round][m_agent.id] = {"participation": "no", "utility": "x", "lied": "x", "reported": "x"}
            self.summary[round][f_agent.id] = {"participation": "no", "utility": "x", "lied": "x", "reported": "x"}
        i = 0
        for agent_m, agent_f in zip(self.valid_m, self.valid_f):
            # print(i)
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
        
        # self.overall_summary[round] = {"kicked out": }
        # print(self.summary[round])
    def print_summary(self):

        for i in range(amt_rounds):

            print("round ", i)
            print("----" * 10)
            for j in range(len(self.m_agent_list)):
                m_agent = self.m_agent_list[j]
                f_agent = self.f_agent_list[j]
                m_summ = self.summary[i][m_agent.id]
                f_summ = self.summary[i][f_agent.id]
                print("agent ", m_agent.id, "with score" , m_agent.score, ": participation ", m_summ["participation"], ", utility ", m_summ["utility"],
                    ", lied ", m_summ["lied"], ", reported? ", m_summ["reported"])
                print("agent ", f_agent.id, "with score" , f_agent.score, ": participation ", f_summ["participation"], ", utility ", f_summ["utility"],
                    ", lied ", f_summ["lied"], ", reported? ", f_summ["reported"])
            print("----" * 40)
        total_utility = sum([agent.utility for agent in self.m_agent_list]) + sum([agent.utility for agent in self.f_agent_list])

        print("overall utility: " , total_utility)
        
    def run_simulation(self):
        self.generate()
        # Let's run the rounds!
        for i in range(amt_rounds):
            
            self.valid_m = [agent for agent in self.m_agent_list if agent.participating == 1]
            self.valid_f = [agent for agent in self.f_agent_list if agent.participating == 1]

            # print(len(self.valid_m))
       
            for agent in self.m_agent_list:
                agent.set_report()
            for agent in self.f_agent_list:
                agent.set_report()
            # Match people together
            self.valid_m.sort( key = lambda x: x.report, reverse=True)
            self.valid_f.sort( key = lambda x: x.report,reverse = True )
            # if i ==0:
            #     print([agent[0].report for agent in self.valid_m])
            amt_of_participants = min(len(self.valid_m),len(self.valid_f) )
            

            self.valid_m = self.valid_m[0:amt_of_participants]
            self.valid_f = self.valid_f[0:amt_of_participants]

            # Update the utility
            for agent_m, agent_f in zip(self.valid_m, self.valid_f):
                agent_m.utility += (utility_scale *  agent_f.score) - (opportunity_scale * (agent_m.report - agent_f.score))
                agent_f.utility +=  (utility_scale *  agent_m.score) - (opportunity_scale * (agent_f.report - agent_m.score))
            # if i == 0:
            #     print("first")
            #     print([agent[0].id for agent in self.valid_f])
            #     print([agent[0].id for agent in self.valid_m])
            #     
            #     print("second")
            #     print([agent[0].id for agent in self.valid_f])
            #     print([agent[0].id for agent in self.valid_m])
            self.reporting()
            self.calculate_summary(i)
            self.reputation_system()
            # print(i, "chicken")
            # for round in range(10):
            #     print("go",self.summary[round])
        if log:
            self.print_summary()
        total_utility = sum([agent.utility for agent in self.m_agent_list]) + sum([agent.utility for agent in self.f_agent_list])
        self.overall_summary.append(total_utility)
    def run_tests(self):
        for i in range(amt_tests):
            self.run_simulation()
        print(mean(self.overall_summary))

sim = Simulator()
sim.run_tests()







# in this linear case, most attractives get with each other. in the non linear case, they aren't

# Let's say each person has a random assignment of who they want. Then, the bump increases their score, but it's decreased with reputation

# Maybe the report goes into their rating any increases it for them. Then what? 





# Maybe just bumps them up a rank ? 



