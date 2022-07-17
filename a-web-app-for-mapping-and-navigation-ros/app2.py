from flask import Flask, render_template, url_for,g,jsonify,request,send_from_directory
from sqlite3 import Error
import subprocess
import signal
import os
import time
import sqlite3


app = Flask(__name__)		
class roslaunch_process():
    @classmethod
    def start_navigation(self,mapname):

        self.process_navigation = subprocess.Popen(["roslaunch","--wait", "ur_robot_driver", "ur5_bringup.launch"])
    #subprocess.Popen使用指令termimal [roslaunch +"wait(timeout): 等待子进程终止"+ "pkg" + ".launch"]
    @classmethod
    def stop_navigation(self):
        self.process_navigation.send_signal(signal.SIGINT)	
    #send_signal(signal.SIGINT)發送SIGINT和 SIGQUIT以中斷並終止另一個進程的計算
    @classmethod
    def start_mapping(self):

        self.process_mapping = subprocess.Popen(["roslaunch", "--wait", "ur5_moveit_config", "ur5_moveit_planning_execution.launch"])
    @classmethod
    def rviz(self):

        self.process_rviz = subprocess.Popen(["roslaunch", "--wait", "ur5_moveit_config", "moveit_rviz.launch"])

    @classmethod
    def ctrl(self):

        self.process_ctrl = subprocess.Popen(["roslaunch", "--wait", "ur_robot_driver", "ctrl.launch"])

    @classmethod
    def stop_mapping(self):

        self.process_mapping.send_signal(signal.SIGINT)    
@app.route('/', methods=['GET','POST'])
def ocr(): 
  return render_template('ocr.html')
@app.before_first_request
def create_table():
   
    subprocess.Popen(["roslaunch", "ur_robot_driver", "ur5_bringup.launch"])
    #subprocess.Popen=(使用指令termimal) [roslaunch + "pkg" + ".launch"]

  
@app.route('/ur5',methods=['GET','POST'])

def navigation():
   subprocess.Popen(["rosrun", "ur_robot_driver", "move.py"])
   return "success"
@app.route('/check', methods=['GET','POST'])
def check(): 
  return render_template('urdf_3d.html')
@app.route("/ur5/<variable>" , methods=['GET','POST'])
def gotomapping(variable):
  if variable == "index":
        roslaunch_process.start_mapping()
        roslaunch_process.rviz()
        roslaunch_process.ctrl()

  elif variable == "gotomapping":		
        roslaunch_process.stop_navigation()
        time.sleep(2)
        roslaunch_process.start_mapping()
  return render_template('ocr.html')



@app.route("/navigation/loadmap" , methods=['POST'])
def navigation_properties():

	mapname = request.get_data().decode('utf-8')
	
	roslaunch_process.stop_navigation()
	time.sleep(5)
	roslaunch_process.start_navigation(mapname)
	return("success")


@app.route("/shutdown" , methods=['POST'])
def shutdown():
	os.system("shutdown now") 
	return("shutting down the robot")	




@app.route("/restart" , methods=['POST'])
def restart():
	os.system("restart now") 
	return("restarting the robot")


@app.route('/static/model/<path:filename>')
def serveArmModel(filename):
    """Lets ros3djs access the meshes used to render the arm model"""
    return flask.send_from_directory('../ur5/ur5_description/urdf', filename)


if __name__ == '__main__':
	app.run(debug=False)    
