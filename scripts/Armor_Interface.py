#!/usr/bin/env python

from armor_msgs.srv import ArmorDirective
import rospy

def add_ontology(command,primary_command_spec,secondary_command_spec,arg):
	 global client
	 rospy.wait_for_service('armor_interface_srv')
	 client = rospy.ServiceProxy('armor_interface_srv', ArmorDirective)
	 msg = ArmorDirective()
	 msg.client_name = 'tutorial'
	 msg.reference_name = 'ontoTest'
	 msg.command = command
	 msg.primary_command_spec = primary_command_spec
	 msg.secondary_command_spec = secondary_command_spec
	 msg.args=arg
	 resp=client(msg)
	 return resp
	 
        
def main():
    # init node
    rospy.init_node('armor')
    # init service
    #rospy.wait_for_service('armor_interface_srv')
    #client = rospy.ServiceProxy('armor_interface_srv', ArmorDirective)
    resp1=add_ontology('LOAD','FILE','',['/root/ros_ws/src/exprob_ass1/cluedo_ontology.owl', 'http://www.emarolab.it/cluedo-ontology', 'true', 'PELLET', 'true'])    
    resp2=add_ontology('ADD','CLASS','CLASS',['INCORRECT','HIPOTESIS'])   
    resp2=add_ontology('DISJOINT','CLASS','',['PERSON','PLACE'])
    resp2=add_ontology('DISJOINT','CLASS','',['PLACE','WEAPON'])
    resp2=add_ontology('DISJOINT','CLASS','',['WEAPON','PERSON'])
    resp2=add_ontology('DISJOINT','CLASS','',['INCORRECT','PERSON'])
    resp2=add_ontology('DISJOINT','CLASS','',['WEAPON','INCORRECT'])
    resp2=add_ontology('DISJOINT','CLASS','',['INCORRECT','PLACE'])

    resp2=add_ontology('ADD','OBJECTPROP','IND',['who','HP1','Jim'])
    resp2=add_ontology('ADD','IND','CLASS',['Jim','PERSON'])
    resp4=add_ontology('REASON','','',[])
    resp3=add_ontology('ADD','OBJECTPROP','IND',['what','HP1','Rope'])
    resp2=add_ontology('ADD','IND','CLASS',['Rope','WEAPON'])
    resp4=add_ontology('REASON','','',[])
    resp4=add_ontology('ADD','OBJECTPROP','IND',['where','HP1','Library'])
    resp2=add_ontology('ADD','IND','CLASS',['Library','PLACE'])
    resp4=add_ontology('REASON','','',[])
    resp4=add_ontology('ADD','OBJECTPROP','IND',['who','HP2','Luca'])   
    resp2=add_ontology('ADD','IND','CLASS',['Luca','PERSON'])
    resp4=add_ontology('ADD','OBJECTPROP','IND',['who','HP2','Alice'])
    resp2=add_ontology('ADD','IND','CLASS',['Alice','PERSON'])
    resp2=add_ontology('ADD','IND','CLASS',['HP1','INCORRECT'])
    resp2=add_ontology('ADD','IND','CLASS',['HP2','INCORRECT'])
    resp2=add_ontology('ADD','IND','CLASS',['HP3','INCORRECT'])

    #resp2=add_ontology('DISJOINT','IND','',['Alice','Luca']) 
    resp4=add_ontology('REASON','','',[])
    #resp4=add_ontology('ADD','OBJECTPROP','IND',['where','HP2','Library'])
    #resp2=add_ontology('ADD','IND','CLASS',['Library','PLACE'])
    resp4=add_ontology('REASON','','',[])

    resp4=add_ontology('ADD','OBJECTPROP','IND',['what','HP2','Gun'])
    resp2=add_ontology('ADD','IND','CLASS',['Gun','WEAPON'])
    resp2=add_ontology('DISJOINT','IND','CLASS',['PERSON'])
    resp2=add_ontology('DISJOINT','IND','CLASS',['PLACE'])
    resp2=add_ontology('DISJOINT','IND','CLASS',['WEAPON'])
    resp4=add_ontology('REASON','','',[])
    resp5=add_ontology('QUERY','IND','CLASS',['COMPLETED'])
    print(resp5)
    resp6=add_ontology('QUERY','IND','CLASS',['INCONSISTENT'])
    resp7=add_ontology('QUERY','IND','CLASS',['INCORRECT'])

    print(resp7)

    #resp5=add_ontology('REMOVE','IND','',['HP3'])
    #resp4=add_ontology('REASON','','',[])

    



if __name__ == '__main__':
    main()
    


