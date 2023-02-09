import os
import subprocess
import pwd
import crypt
import n4d.responses

class AlumnatAccountManager:
	
	ALUMNAT_USER="alumnat"
	ALUMNAT_UID=69999
	ALUMNAT_HOME="/run/%s/home"%ALUMNAT_USER
	
	def __init__(self):
		
		self.get_alumnat_status()
		
	#def init
	
	def startup(self,options):
		
		# already manages if user is enabled
		pass
		
	#def startup
	
	
	def _run_command(self,command):
		
		ret={}
		command="LC_ALL=C %s"%command
		p=subprocess.Popen([command],shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		ret["stdout"],ret["stderr"]=p.communicate()
		ret["returncode"]=p.returncode
		
		return ret
		
	#def _run_command
	
	def _build_response(self):
		
		ret={}
		ret["status"]=False
		ret["msg"]=None
	
		return ret
		
	#def _build_response
	
	def _disable_password_change(self,password):
		
		command="passwd -n 1000000 '%s'"%password
		ret=self._run_command(command)
		
		if ret["returncode"]==0:
			return True
		else:
			return False
		
	#def _disable_password_change
			
	def _set_pam_config(self,status=True):
		
		mode="--enable"		
		if not status:
			mode="--remove"
		command="pam-auth-update %s alumnatuser"%mode
		
		ret=self._run_command(command)
		
		if ret["returncode"]==0:
			return True
		else:
			return False
		
	#def _set_pam_config
	
	def _encrypt_passwd(self,password):

		encryptPasswd=crypt.crypt(password)
		return encryptPasswd

	#def _encrypt_passwd
	
	# ############## #
	# PUBLIC FUNCTIONS   #
	# ############## #
	
	def get_alumnat_status(self):
		
		ret=self._build_response()
		ret["status"]=False
		
		try:
			alumnat_user=pwd.getpwnam(AlumnatAccountManager.ALUMNAT_USER)
			ret["status"]=True
			ret["msg"]="%s is enabled"%(AlumnatAccountManager.ALUMNAT_USER)
			
		except Exception as e:
			ret["msg"]=str(e)
		
		self.enabled=ret["status"]
			
		#return ret
		return n4d.responses.build_successful_call_response(ret)
		
	#def get_alumnat_status
	
	def fix_alumnat_password(self,password):
		
		ret=self._build_response()
		tmpPassword=self._encrypt_passwd(password)

		if self.enabled:
			command="usermod -p '%s' %s"%(tmpPassword,AlumnatAccountManager.ALUMNAT_USER)
			p_return=self._run_command(command)
			
			if p_return["returncode"]==0:
				ret["status"]=True
				ret["msg"]="Password changed"
			else:
				ret["status"]=False
				ret["msg"]=p_return["stderr"]
				
			self._disable_password_change(tmpPassword)
			
		else:

			ret["status"]=False
			ret["msg"]="User does not exist"
			
		#return ret
		return n4d.responses.build_successful_call_response(ret)
		
		
	#def fix_alumnat_password
	
	def enable_alumnat_user(self,password):
		
		ret=self._build_response()
		
		if not self.enabled:
			tmpPassword=self._encrypt_passwd(password)
			command="useradd -p '%s' -M -N -u %s -r -s /bin/bash -G cdrom,dip,plugdev,sambashare -d %s %s"%(tmpPassword,AlumnatAccountManager.ALUMNAT_UID,AlumnatAccountManager.ALUMNAT_HOME,AlumnatAccountManager.ALUMNAT_USER)
			p_return=self._run_command(command)
			
			if p_return["returncode"]==0:
				ret["status"]=True
				ret["msg"]="Alumnat user created"
				
				self._disable_password_change(tmpPassword)
				self._set_pam_config(True)
				self.enabled=True
			else:
				ret["status"]=False
				ret["msg"]=p_return["stderr"]
				
			return n4d.responses.build_successful_call_response(ret)
			
		ret["status"]=False
		ret["msg"]="%s already enabled"%AlumnatAccountManager.ALUMNAT_USER
		
		#return ret
		return n4d.responses.build_successful_call_response(ret)
			
	#def add_alumnat_user
	
	def disable_alumnat_user(self):
		
		ret=self._build_response()
		
		if self.enabled:
			command="userdel %s"%AlumnatAccountManager.ALUMNAT_USER
			p_return=self._run_command(command)
			
			if p_return["returncode"]==0:
				ret["status"]=True
				ret["msg"]="%s disabled"%AlumnatAccountManager.ALUMNAT_USER
				self._set_pam_config(False)
				self.enabled=False
			else:
				ret["status"]=False
				ret["msg"]=p_return["stderr"]
				
			return n4d.responses.build_successful_call_response(ret)
			
		ret["status"]=False
		ret["msg"]="%s is not enabled"%AlumnatAccountManager.ALUMNAT_USER
		
		#return ret
		return n4d.responses.build_successful_call_response(ret)

		
	#def remove_alumnat_user
	
#class AlumnatAccountManager


if __name__=="__main__":
	
	gam=AlumnatAccountManager()
	print(gam.get_alumnat_status())
	print(gam.enable_alumnat_user())
	print(gam.disable_alumnat_user())
