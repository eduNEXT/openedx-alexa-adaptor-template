SKILL_FOLDER := skills
SAMPLE_SKILL_FOLDER := sample-skill

configure:

	@echo "First, you need to configure your ASK CLI...\n"
	@echo "1. Create a new profile"
	@echo "2. Enter the name of your profile"
	@echo "3. Login with your Amazon Developer account in the browser"
	@echo "4. Confirm the login in the terminal pressing the 'y' key"
	@echo "5. It is not necessary to link an AWS account, so press the 'n' key\n"
	@echo "Press enter to start with the configuration..." && read _
	@ask configure
	@echo "\n"

setup:

	@echo "Now, you need to create a new skill...\n"
	@echo "The parameters that you must enter are:"
	@echo "1. Modeling stack for your skill: Interaction Model"
	@echo "2. Programming language for your skill: Python"
	@echo "3. Method to host your skill: Alexa-hosted"
	@echo "4. Default region for your skill: us-east-1"
	@echo "5. Name of your skill: <your-skill-name>"
	@echo "6. Folder name for your skill: <your-skill-folder-name>\n"
	@echo "Press enter to start with the creation of your skill..." && read _
	@[ -d $(SKILL_FOLDER) ] || mkdir $(SKILL_FOLDER)
	@cd $(SKILL_FOLDER) && ask new
	@read -p "Please enter the name of your skill folder created above. This name is necessary \
	to copy all the files from our sample-skill to your skill folder: " skill_folder; \
	echo "Copying files..." && sleep 2 \
	&& cp -r $(SAMPLE_SKILL_FOLDER)/lambda $(SKILL_FOLDER)/$$skill_folder \
	&& cp -r $(SAMPLE_SKILL_FOLDER)/skill-package/interactionModels $(SKILL_FOLDER)/$$skill_folder/skill-package \
	&& python script.py $$skill_folder \
	&& cd $(SKILL_FOLDER)/$$skill_folder \
	&& echo "Saving changes and pushing..." && sleep 2 \
	&& git add . && git commit -m "feat: add sample skill" && git push origin master
	@echo "\nPlease, wait a few minutes until the deployment is complete. You can check the status \
	of your deployment in the Alexa Developer Console."

bootstrap: configure setup


.PHONY: bootstrap configure setup
