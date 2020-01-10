#Traffic Speed Calculator
#PF 2020 C1 V2

#Created by Charlie Murphy
#9 January 2019
#Version 2.3.1

import math

#Road Attributions Dictionary
class Road:

    #Road Attributions
    def __init__(self):
        self.speed_limit = 120 #kph
        self.lane_width = 3.6 #m
        self.shoulder_width = 1.8 #m
        self.divided_median = True #True or False
        self.access_point_density = .5 #intersections/km
        self.lanes = 2 #number of lanes in 1 direction
        self.population_density = 'rural' #'rural' or 'urban'
        self.terrain = 'mountainous' #'level', 'rolling', 'mountainous'
        self.percent_heavy_vehichles = .4 #decimal percentage
        self.segment_distance = 1 #km

    #Free Flow Speed Calculator
    def free_flow_speed(self):
        
        #Base Free Flow Speed (BFFS)
        if self.speed_limit<65:
            BFFS = self.speed_limit
        elif self.speed_limit<80:
            BFFS = self.speed_limit + 11
        else:
            BFFS = self.speed_limit + 8

        #Adjustment Factor for Lane Width (f_LW)
        if self.lane_width>=3.7:
            f_LW = 0
        elif self.lane_width>3.4:
            f_LW = 1.9
        else:
            f_LW = 6.6

        #Adjustment Factor for Lateral Clearance (f_LC)
        if self.lanes<5:
            f_LC = (6 - (self.shoulder_width/.3))*(5 - self.lanes)*.2
        else:
            f_LC = (6 - (self.shoulder_width/.3))*.1

        #Adjustment Factor for Median Type (f_M)
        if self.divided_median==True:
            f_M = 0
            driveway_density = 2
        else:
            f_M = 1.6
            driveway_density = 3

        #Adjustment Factor for Access Points (f_A)
        f_A = min((0.25*(self.access_point_density + driveway_density)), 10)

        #Adjustment Factor for Number of Lanes (f_N)
        if self.population_density=='rural' or self.lanes>=5:
            f_N = 0
        else:
            f_N = (5 - lanes)*1.5  

        #Calculation for Free Flow Speed (FFS)
        self.FFS = BFFS - f_LW - f_LC - f_M - f_A - f_N

    #Critical Denisty Calculator
    def critical_density(self):

        #Adjustment Factor for Heavy Vehicles (f_HV)
        if self.population_density=='urban' or self.terrain=='level':
            car_equivalents = 1.5
        elif self.terrain=='rolling':
            car_equivalents = 2.5
        else:
            car_equivalents = 4.5
        f_HV = 1/(1 + self.percent_heavy_vehichles*(car_equivalents - 1))

        #Adjustment Factor for Driver Population (f_P)
        if self.population_density=='rural':
            f_P = 0.975
        else:
            f_P = 1

        #Calculation for Capacity (BaseCap)
        if self.FFS<=100:
            BaseCap = (1000 + 12*self.FFS)*f_HV*f_P*self.lanes
        else:
            BaseCap = 2200*f_HV*f_P*self.lanes

        #Calculation for Critical Density (k_C)
        self.k_C = BaseCap/self.FFS

    #Jam Density Calculator
    def jam_density(self):

        #Calculation for Jam Density (k_J)
        self.k_J = 7*self.k_C

    #Individual Speed Decrease Calculator
    def individual_speed_decrease(self):

        #Calculation for Individual Speed Decrease (ISD)
        self.ISD = (self.FFS/(self.k_C - self.k_J)) 

    #Volume-Adjusted Speed Calculator using Greensfield's Model
    def speed(self,vehichles):

        #Calculation for segment density
        density = vehichles/self.segment_distance
        
        #Calculation for Volume-Adjusted Speed (u)
        if density>=self.k_J:
            u = 0
        elif density<=self.k_C:
            u = self.FFS
        else:
            u = self.ISD*(density - self.k_J)
        return u

    #Individual Travel Time Increase Calculator
    def h_factor(self,current_load):

        #Calculate travel times before and after a given
        min_time = self.segment_distance/self.speed(current_load-1)
        max_time = self.segment_distance/self.speed(current_load)

        #Calculate difference in travel times in seconds
        return ((max_time - min_time)*3600)

    #Individual Impact on Traffic System Calculator
    def i_factor(self):

        #Calculate the decrease in speed adjusted for segment distance
        return abs(self.ISD)*self.segment_distance
        
AB = Road()
AB.free_flow_speed()
AB.critical_density()
AB.jam_density()
AB.individual_speed_decrease()
print("Individual Impact on Traffic System =",round(AB.i_factor(),3),"km^3/vehichle-hours")
print("Individual Travel Time Increase =",round(AB.h_factor(10),3),"s")



