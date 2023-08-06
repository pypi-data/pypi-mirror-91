"""This is the magic bot by Castellani Davide :)
With this programm you can easily create a repository on GitHub with a basic template, personalized for your use.

If there was any type of problem you can contact me on my help email: help@castellanidavide.it
"""
# Some imports
from datetime import datetime as dt
from getpass import getpass
from github import Github
from re import escape, compile
from requests import get as wget
from time import sleep
from threading import Thread, active_count
from sys import argv

__author__ = "help@castellanidavide.it"
__version__ = "7.0 2021-01-11"

class create_structure:
	def __init__ (self, tocken=None, souces=['CastellaniDavide'], organization_name="", IGNORE=[], verbose=False, answers=None):
		"""Main function
		"""
		# Set main variabiles
		self.CONTINUE = True
		self.TOKEN = tocken
		self.SOURCES_OF_TEMPLATES = souces
		self.ORGANIZATION_NAME = organization_name
		self.IGNORE = IGNORE
		self.VERBOSE = verbose
		self.ANSWERS = answers

		# Initial inputs
		self.initial_inputs()

		if self.CONTINUE:
			self.login() # Login

			# Make questions
			self.asks()

			# Make repo
			Thread(target = self.create_repo()).start()

			# Get template
			self.choose_template()

			# Get changes
			self.change_map()
			
			# Make all
			self.scan_and_elaborate()

	def initial_inputs(self):
		"""Initial input read
		"""

		# Check if there were all argv
		try:
			# Go to documentation if requested
			assert (not("-h" in argv or "--help" in argv))

			# Read arguments
			for arg in argv:
				# find folders and files
				if "--ignore=" in arg or "-i=" in arg:
					self.IGNORE = [i for i in arg.replace("--ignore=", "").replace("-i=", "").replace("'", "").replace('"', "")[1:-1].split(",")]
				# find organization
				if "--organization=" in arg or "-o=" in arg:
					self.ORGANIZATION_NAME = arg.replace("--organization=", "").replace("-o=", "")
				# find souces
				if "--sources=" in arg or "-s=" in arg:
					self.SOURCES_OF_TEMPLATES = [i for i in arg.replace("--sources=", "").replace("-s=", "").replace("'", "").replace('"', "")[1:-1].split(",")]
				# find tocken
				if "--token=" in arg or "-t=" in arg:
					self.TOKEN = arg.replace("--token=", "").replace("-t=", "")
				# find verbose
				if "--vebose" in arg or "-v" in arg:
					self.VERBOSE = True
		
			# Check all data
			assert(self.TOKEN != "TODO" and self.TOKEN != None and self.TOKEN != "***")

			if self.VERBOSE : print(f"\u2139 self.CONTINUE\t\t\t{self.CONTINUE}\n\u2139 self.TOKEN\t\t\t{self.TOKEN}\n\u2139 self.SOURCES_OF_TEMPLATES\t{self.SOURCES_OF_TEMPLATES}\n\u2139 self.ORGANIZATION_NAME\t{self.ORGANIZATION_NAME}\n\u2139 self.IGNORE\t\t\t{self.IGNORE}\n\u2139 self.VERBOSE\t\t\t{self.VERBOSE}")

		except:
			self.CONTINUE = False
			documentation = ["usage create_structure",
							"\t[--ignore= | -i=]",
							"\t[--organization= | -o=]",
							"\t[--sources= | -s=]",
							"\t[--token= | -t=]",
							"\t[--verbose | -v]",
							"",
							"These are the create_structure arguments:",
							"\t--ignore= or -i=		(optional) The folders to be ignored",
							"\t--organization= or -o=		(optional) The organization name, leave empty if you want to create repos in your personal account",
							"\t--sources= or -s=		(optional) The array with your favourite sources, for eg. ['CastellaniDavide']",
							"\t--token= or -t=			The GitHub tocken with repo and organization permission",
							"\t--verbose or -v			Verbose option, you will see the main variabiles and lots more"
							"",
							"Extra situation(s):",
							"\t--help or -h			To see the documentation",
							"",
							"Made with ❤  by Castellani Davide (@DavideC03)",
							""]

			for line in documentation:
				print(line)
	
	def login(self):
		"""Made the login in GitHub
		"""
		self.g = Github(self.TOKEN)
	
	def asks(self):
		"""Manage the run variabiles
		"""
		if self.ANSWERS == None: # Make questions
			questions = [["name",		"Name of the project (es. create_structure): "],
						["extention",	"Extenction of the main programm (es. py): "],
						["descr",		"Description of the project: "],
						["prefix",		"Insert a prefix for the repository (or don't insert anything): "],
						["team",		"Do you want insert this repo into a team? [y/N]: "],
						["private",		"Is that private? [y/N]: "],
						]
			self.ANSWERS = {}
			
			# Get infos
			for question_tag, current_quest in questions:
				if question_tag == "team":
					self.ANSWERS["team"] = ""	# default value
					if self.ORGANIZATION_NAME != "":	# If there is an organization
						if create_structure.is_positive(input(f"\u2753 {current_quest}")):
							self.choose_team()						
				else:
					self.ANSWERS[question_tag] = input(f"\u2753 {current_quest}")

			print()

	def choose_team(self):
		"""Choose a team
		"""
		try:
			# Search teams
			teams = self.g.get_organization(self.ORGANIZATION_NAME).get_teams()
			
			nteams = 0
			# Give the option to the user
			for i, team in enumerate(teams):
				nteams += 1
				print(f"\t{i})\t{team.name}")

			assert (nteams != 0)

			# Save the team choosen
			try:
				self.ANSWERS["team"] = teams[int(input("\u2753 Insert your team number: "))].id
			except:
				print("This team didn't exist, try again")
				self.choose_team()
		except:	# No teams
			print("Sorry, you didn't have any team. Create a new team to use this option")

	def create_repo(self):
		"""Create the repo
		"""
		if self.ORGANIZATION_NAME == "":
			self.repo = self.g.get_user().create_repo(self.ANSWERS['name'] if(self.ANSWERS['prefix'] == "") else f"{self.ANSWERS['prefix']}-{self.ANSWERS['name']}", description=self.ANSWERS['descr'], private=create_structure.is_positive(self.ANSWERS['private']), has_issues=True, has_wiki=False, has_downloads=True, has_projects=False)
		else:
			if self.ANSWERS["team"] == "":
				self.repo = self.g.get_organization(self.ORGANIZATION_NAME).create_repo(self.ANSWERS['name'] if(self.ANSWERS['prefix'] == "") else f"{self.ANSWERS['prefix']}-{self.ANSWERS['name']}", description=self.ANSWERS['descr'], private=create_structure.is_positive(self.ANSWERS['private']), has_issues=True, has_wiki=False, has_downloads=True, has_projects=False)
			else:
				self.repo = self.g.get_organization(self.ORGANIZATION_NAME).create_repo(self.ANSWERS['name'] if(self.ANSWERS['prefix'] == "") else f"{self.ANSWERS['prefix']}-{self.ANSWERS['name']}", description=self.ANSWERS['descr'], private=create_structure.is_positive(self.ANSWERS['private']), has_issues=True, has_wiki=False, has_downloads=True, has_projects=False, team_id=self.ANSWERS["team"])
		
		print(f"\u2714 Repo built")

	def choose_template(self):
		"""This helps to find the correct template
		"""
		# If there wasn't any other template for your type of extention and no one default into SOURCES list, give my default code
		self.template_name = "CastellaniDavide/default-template" 

		# Check if there is wanted template
		for source in self.SOURCES_OF_TEMPLATES:
			if source != "TODO" and self.template_name == "CastellaniDavide/default-template":
				try:
					self.template_name = self.g.get_repo(f"{source}/{self.ANSWERS['extention']}-template").full_name
					break
				except:
					pass

		# Check if there was a default template
		if self.template_name == "CastellaniDavide/default-template":
			for source in self.SOURCES_OF_TEMPLATES:
				if source != "TODO" and self.template_name == "CastellaniDavide/default-template":
					try:
						print (f"Try: {source}/default-template")
						self.template_name = self.g.get_repo(f"{source}/default-template").full_name
						break
					except:
						pass
		
		self.template = self.g.get_repo(self.template_name)
		print(f"\u2714 Template founded ({self.template_name})")
		
	def scan_and_elaborate(self, loc=""):
		"""Scan all files in the repository and push it in the new directory (cahanging the necessary)
		"""
		contents = self.template.get_contents(f"{loc}")
		for content_file in sorted(contents, reverse=True, key=create_structure.name_of_path): # Put .folders at the end
			if not content_file.path in [".castellanidavide", ""] + self.IGNORE:
				if content_file.path == ".github/workflows": # Wait the end of others before do workflows
					while (active_count() != 2): pass

				if content_file.type == "file":
					Thread(target = self.create_file, args = (self.change(content_file.path), f"{self.change(wget(f'https://raw.githubusercontent.com/{self.template_name}/master/{content_file.path}').text)}")).start()
				else:
					Thread(target = self.scan_and_elaborate, args = (content_file.path, )).start()		

	def name_of_path(item):
		"""For sorting the folders, gives the path attributes
		"""
		if item.path == ".github/workflows":
			return "..." # move to the end
		else:
			return item.path

	def change_map(self):
		"""Returns a map of changes
		"""
		time = dt.now()
		
		# repo changes
		change_map = eval(wget(f"https://raw.githubusercontent.com/{self.template_name}/master/.castellanidavide/change.json").text)

		# answer changes
		for key, value in self.ANSWERS.items():
			change_map[f"sol{key}sol"] = value

		# special changes
		change_map["time__now"] = f"{str(time.year)}-{str(time.month)}-{str(time.day)}"
		change_map["time_now"]  = f"{str(time.year)}{str(time.month)}{str(time.day)}"

		# re dict, because I can use it faster (eg. for changes)
		self.change_map = dict((escape(k), v) for k, v in change_map.items())

	def change(self, text):
		"""Returns the changed page
		Change two times for special keys
		"""
		return compile("|".join(self.change_map.keys())).sub(lambda m: self.change_map[escape(m.group(0))], compile("|".join(self.change_map.keys())).sub(lambda m: self.change_map[escape(m.group(0))], text))

	def create_file (self, path, file):
		"""Create the file into the repo
		"""
		try:
			self.repo.create_file(path, f"Created {path}", file)
			print(f"\u2714 Created {path}")
		except:
			# If it's an error, possible with multitreading, try again
			sleep(0.5)
			self.create_file (path, file)

	def is_positive(answer):
		"""Returns true is the answer is affermative
		"""
		return answer in ["y", "Y", "yes", "Yes"]

if __name__ == "__main__":
	""" Read the argv, and sometimes writes the documentation
	"""
	create_structure() # Entry point	
	